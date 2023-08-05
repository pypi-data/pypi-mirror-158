# -*- coding: utf-8 -*-
# Copyright IRT Antoine de Saint Exupéry et Université Paul Sabatier Toulouse III - All
# rights reserved. DEEL is a research program operated by IVADO, IRT Saint Exupéry,
# CRIAQ and ANITI - https://www.deel.ai/
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
import pathlib
import typing
from abc import abstractmethod

from .providers.provider import Provider
from .settings import get_default_settings
from .settings import Settings


class InvalidModeError(Exception):

    """
    Exception raised when a mode is not available for a
    given dataset.
    """

    def __init__(self, dataset: "BaseDataset", mode: str):
        """
        Args:
            dataset: Dataset for which the mode is not available.
            mode: Mode not available.
        """
        super().__init__(
            "Mode {} not available for dataset {}.".format(mode, dataset.name)
        )


class BaseDataset(object):

    """
    Base dataset for all dataset types.
    """

    # Name and version of the dataset:
    _name: str
    _version: str

    # The settings to use:
    _settings: Settings

    # The default mode (must be specified by inheriting classes):
    _default_mode: str

    def __init__(
        self,
        name: str,
        version: str = "latest",
        settings: typing.Optional[Settings] = None,
    ):
        """
        Creates a new dataset of the given name and version.

        Args:
            name: Name of the dataset.
            version: Version of the dataset.
            settings: The settings to use for this dataset, or `None` to use the
            default settings.
        """
        self._name = name
        self._version = version

        if settings is None:
            self._settings = get_default_settings()
        else:
            self._settings = settings

    def _make_class_info(
        self, idx_to_class: typing.Dict[int, str]
    ) -> typing.Dict[str, typing.Any]:
        """
        Utility function that can be used to convert a mapping
        from class labels to class names into a valid information
        dictionary that can be returned by a `load_` method.

        Args:
            idx_to_class: Mapping from class labels to class names.

        Returns:
            A dictionary containing information about the class in the
            given mapping.
        """

        classes = [idx_to_class[k] for k in sorted(idx_to_class.keys())]
        class_to_idx = {v: k for k, v in idx_to_class.items()}

        return {"classes": classes, "class_to_idx": class_to_idx}

    @property
    def name(self) -> str:
        """Returns: The name of the dataset."""
        return self._name

    @property
    def version(self) -> str:
        """Returns: The requested version of the dataset."""
        return self._version

    @property
    def available_modes(self) -> typing.List[str]:
        """
        Retrieve the list of available modes for this dataset.

        Returns:
            The list of available modes for this dataset.
        """
        # We lookup all attributes of the class starting with load_,
        # and we discard the ones that are not callable (even if there
        # should not be any most of the time):
        return [
            fn[5:]
            for fn in dir(self)
            if fn.startswith("load_") and callable(getattr(self, fn))
        ]

    @property
    def default_mode(self) -> str:
        """
        Retrieve the default mode for this dataset.

        Returns:
            The default mode for this dataset.
        """
        return self._default_mode

    @abstractmethod
    def load(
        self, mode: typing.Optional[str] = None, with_info: bool = False, **kwargs
    ) -> typing.Any:
        """
        Load this dataset as specified by `mode`.

        Args:
            mode: Mode to load the dataset, or `None` to use the default mode.
            with_info: Returns information about the dataset alongside the actual
                dataset(s).
            **kwargs: Extra arguments for the specific mode.

        Returns:
            The dataset as specified by `mode` and the given extra arguments.

        Raises:
            InvalidModeError: If the given mode is not available for this dataset.
        """
        pass


class Dataset(BaseDataset):

    """
    Dataset is the base class for all DEEL dataset and can be used as
    a non-specific dataset handler.

    A `Dataset` object can be extended to easily interface with the local
    file system to access datasets files using the `load` method.

    A dataset can be loaded using different modes (see `available_modes`
    and `default_mode`). Inheriting classes can add extra modes by providing
    `load_MODE` method and overriding `_default_mode`.

    Example:
        Basic usage of the `Dataset` class is via the `load` method.

        >>> dataset = Dataset("blink")
        >>> dataset.load()
        PosixPath('/home/username/.deel/datasets/blink/3.0.1')
    """

    # Information about this dataset:
    _info: typing.Dict[str, typing.Any] = {}

    # The default mode:
    _default_mode: str = "path"

    # Indicates if this dataset consists of a single file:
    _single_file: bool = False

    def __init__(
        self,
        name: str,
        version: str = "latest",
        settings: typing.Optional[Settings] = None,
    ):
        """
        Creates a new dataset of the given name and version.

        Args:
            name: Name of the dataset.
            version: Version of the dataset.
            settings: The settings to use for this dataset, or `None` to use the
            default settings.
        """
        super().__init__(name, version, settings)

        self._info[name] = name

    def _get_provider(self) -> Provider:
        """
        Create and returns a provider for this dataset.

        By default, this uses creates the provider using `self._settings`.
        This method should only be overridden if the dataset requires a
        custom provider, e.g., because the dataset is not hosted on the
        standard dataset repository.

        Returns:
            A provider suitable to retrieve this dataset.
        """
        return self._settings.make_provider(self._name)

    def load_path(self, path: pathlib.Path) -> pathlib.Path:
        """
        Load method for path mode.

        Args:
            path: Path of the dataset.

        Returns:
            The actual path to the dataset.
        """
        return path

    def load(
        self,
        mode: typing.Optional[str] = None,
        with_info: bool = False,
        force_update: bool = False,
        **kwargs
    ) -> typing.Any:
        """
        Load this dataset as specified by `mode`.

        This method checks that the given `mode` is valid, retrieve the dataset
        files using a `Provider` and then dispatches the actual loading of the
        data to a `load_MODE` method.

        If this dataset consists of a single file as specified by `_single_file`,
        the path used will be the one of this file, otherwise, the folder will
        be used.

        Args:
            mode: Mode to load the dataset, or `None` to use the default mode.
            force_update: Force update of the dataset if possible.
            with_info: Returns information about the dataset alongside the actual
                dataset(s).
            **kwargs: Extra arguments for the specific mode.

        Returns:
            The dataset as specified by `mode` and the given extra arguments.

        Raises:
            InvalidModeError: If the given mode is not available for this dataset.
        """

        if mode is None:
            mode = self.default_mode

        # Replace characters:
        mode = mode.replace(".", "_").replace("-", "_")

        if mode not in self.available_modes:
            raise InvalidModeError(self, mode)

        with self._get_provider() as provider:
            path, version = provider.get_folder(
                self._name,
                self._version,
                force_update=force_update,
                returns_version=True,
            )

        # Update version:
        self._info["version"] = version

        # If single file, retrieve the path to the first file:
        if self._single_file:
            path = next(path.iterdir())

        # Retrieve the method:
        load_fn = getattr(self, "load_" + mode)

        retvalue = load_fn(path, **kwargs)

        # Extract information from the returned value:
        try:
            assert len(retvalue) == 2
            assert isinstance(retvalue[1], dict)
            retvalue, info = retvalue
        except (TypeError, AssertionError):
            info = {}

        # If information are requested, returns it:
        if with_info:
            info.update(self._info)
            return retvalue, info

        return retvalue


class VolatileDataset(BaseDataset):

    """
    Dataset that are generated on-the-fly.
    """

    # Information about this dataset:
    _info: typing.Dict[str, typing.Any] = {}

    # The default mode:
    _default_mode: str = "basic"

    def __init__(
        self,
        name: str,
        version: str = "latest",
        settings: typing.Optional[Settings] = None,
    ):
        """
        Creates a new dataset of the given name and version.

        Args:
            name: Name of the dataset.
            version: Version of the dataset.
            settings: The settings to use for this dataset, or `None` to use the
            default settings.
        """
        super().__init__(name, version, settings)

        self._info[name] = name

    @abstractmethod
    def load_basic(self):
        """
        Load method for path mode.

        Args:
            path: Path of the dataset.

        Returns:
            The actual path to the dataset.
        """
        pass

    def load(
        self, mode: typing.Optional[str] = None, with_info: bool = False, **kwargs
    ) -> typing.Any:
        """
        Load this dataset as specified by `mode`.

        This method checks that the given `mode` is valid and generates the dataset
        using the given `load_MODE` method.

        Args:
            mode: Mode to load the dataset, or `None` to use the default mode.
            with_info: Returns information about the dataset alongside the actual
                dataset(s).
            **kwargs: Extra arguments for the specific mode.

        Returns:
            The dataset as specified by `mode` and the given extra arguments.

        Raises:
            InvalidModeError: If the given mode is not available for this dataset.
        """

        if mode is None:
            mode = self.default_mode

        # Replace characters:
        mode = mode.replace(".", "_").replace("-", "_")

        if mode not in self.available_modes:
            raise InvalidModeError(self, mode)

        # Remove force_update:
        if "force_update" in kwargs:
            del kwargs["force_update"]

        # Retrieve the method:
        load_fn = getattr(self, "load_" + mode)

        retvalue = load_fn(**kwargs)

        # Extract information from the returned value:
        try:
            assert len(retvalue) == 2
            assert isinstance(retvalue[1], dict)
            retvalue, info = retvalue
        except (TypeError, AssertionError):
            info = {}

        # If information are requested, returns it:
        if with_info:
            info.update(self._info)
            return retvalue, info

        return retvalue
