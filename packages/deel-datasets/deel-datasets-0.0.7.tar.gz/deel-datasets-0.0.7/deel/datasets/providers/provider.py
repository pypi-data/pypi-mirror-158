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
import abc
import pathlib
import typing

from .exceptions import VersionNotFoundError


class Provider(abc.ABC):

    """
    The `Provider` class is an abstract interface for classes
    that provides access to dataset storages.

    The list of methods that should be overriden by all child classes
    are indicated with the `abc.abstractmethod` decorator. If a class
    requires specific clean-up, the `__enter__` and `__exit__` special
    functions can be overriden.
    """

    @abc.abstractmethod
    def list_datasets(self) -> typing.List[str]:
        """
        List the available datasets for this provider.

        Returns:
            The list of datasets available for this provider.
        """
        pass

    @abc.abstractmethod
    def list_versions(self, dataset: str) -> typing.List[str]:
        """
        List the available versions of the given dataset for this
        provider.

        Returns:
            The list of available versions of the given dataset for this
            provider.

        Raises:
            DatasetNotFoundError: If the given dataset does not exist.
        """
        pass

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        pass

    def get_version(self, version: str, versions: typing.List[str]) -> str:
        """
        Retrieve the version from the list of `versions` that best match
        the given one.

        Args:
            version: Version to retrieve. Can be an exact version, e.g., `"3.1.2"`,
            or a wildcard `"3.1.*"`, or `"latest"`.
            versions: List of versions to retrieve the version from. Versions should
            all be of the form `x.y.z`.

        Returns:
            The version in `versions` that best matches `version`.

        Raises:
            VersionNotFoundError: If the specified version did not match
            any version in `versions`.
        """

        # If the list of version is  not found:
        if not versions:
            raise VersionNotFoundError(version)

        versions = sorted(versions)

        # Special case for "latest":
        if version.lower() == "latest":
            return versions[-1]

        # Split the version:
        p = version.split(".")
        p += ["*"] * (3 - len(p))
        x, y, z = p

        # Best version (x, y, z)
        vu, vy, vz = "", "", ""

        for tversion in versions:

            # Special handler for old "latest":
            if tversion == "latest":
                continue

            cu, cy, cz = tversion.split(".")

            # The version does not match the one we are testing:
            if cu != x and x != "*" or cy != y and y != "*" or cz != z and z != "*":
                continue

            vu, vy, vz = max((cu, cy, cz), (vu, vy, vz))

        if vu == "":
            raise VersionNotFoundError(version)

        return "{}.{}.{}".format(vu, vy, vz)

    @abc.abstractmethod
    def get_folder(
        self,
        name: str,
        version: str = "latest",
        force_update: bool = False,
        returns_version: bool = False,
    ) -> typing.Union[pathlib.Path, typing.Tuple[pathlib.Path, str]]:
        """
        Retrieve the root folder for the given dataset.

        Args:
            name: Name of the dataset to retrieve the folder for.
            version: Version of the dataset to retrieve the folder for. Can be
                an exact version like `"3.1.2"`, or `"latest"`, or a wildcard, e.g.,
                `"3.1.*"`.
            force_update: Force the update of the local dataset if possible.
                May have no effect on some providers.
            returns_version: If `True`, the exact version of the dataset will be
                returned along the path.

        Returns:
            A path to the root folder for the given dataset name, or a tuple containing
            the path and the exact version.

        Raises:
            DatasetNotFoundError: If the requested dataset was not found by this
            provider.
            DatasetVersionNotFoundError: If the requested version of the dataset was
            not found by this provider.
        """
        pass
