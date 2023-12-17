# Author: Landon Bouma <https://tallybark.com/>
# Project: https://github.com/doblabs/easy-as-pypi-getver#🔢
# License: MIT

# Copyright (c) © 2018-2023 Landon Bouma. All Rights Reserved.

"""Top-level package for this CLI-based application."""

import os

__all__ = (
    "get_version",
    # Private:
    #  '_version_from_tags',
)

# This empty version value will be populated temporarily during poetry-build
# by poetry-dynamic-versioning.
# - Consequently, __version__ remains empty when installed in 'editable' mode
#   and accessed at runtime. So query get_version() instead, which uses
#   importlib to fetch the package version from when it was installed.
__version__ = ""

# - Note a few subtle differences between importlib and setuptools_scm:
#   - importlib.metadata.version returns the package version that was
#       installed, which might include Git tags, but the version is static
#       and won't track any repo changes.
#   - setuptools_scm, on the other hand, uses the latest commit to format
#       the version.
# - For example, let's say a repo has 27 commits and no version tag,
#   then you might see these versions:
#     - importlib:      0.0.0.post27.dev0+7c3df03 ("0.0.0" from pyproject.toml)
#     - setuptools_scm: 0.1.dev27+g7c3df03.d20231114 (starting itself at "0.1")
#   - Note that both versions indicate the distance (27) since the last
#     version (or since the first commit, in this case), and each version
#     contains the Git ref (7c3df03) of the latest commit.
#   - Now let's suppose you add 5 commits, Now you might see the versions:
#     - importlib:      0.0.0.post27.dev0+7c3df03 (unchanged)
#     - setuptools_scm: 0.1.dev32+g187abdc.d20231114 (changed)
#     As mentioned, importlib's version is still the unchanged package
#     version, whereas setuptools_scm indicates the new distance (32)
#     and a different Git ref (187abdc).


def get_version(package_name, reference_file=None, include_head=False):
    """Return the installed package version, or '<none>'."""
    # Note we lazy-load imports hereunder, though unsure that matters for built-ins.
    PACKAGE_NOT_FOUND_VERSION = "<none!?>"
    INVALID_REPOSITORY_VERSION = "<none?!>"

    def resolve_vers():
        dist_version = version_installed()
        if include_head:
            repo_version = version_from_repo()
            if repo_version:
                dist_version = "{} ({})".format(dist_version, repo_version)
        return dist_version

    def version_installed():
        # Ugh, this import is here and not file-level so that a test can mock
        # "version". / There's gotta be a better approach....
        from importlib.metadata import PackageNotFoundError, version

        # E.g, "1.2.3.post19.dev0+d7c69ea".
        try:
            return version(package_name)
        except PackageNotFoundError:
            return PACKAGE_NOT_FOUND_VERSION

    def version_from_repo():
        try:
            return _version_from_tags(reference_file)
        except ModuleNotFoundError:
            # No setuptools_scm package installed.
            return ""
        except LookupError:
            # Path containing .git/ not a repo after all.
            return INVALID_REPOSITORY_VERSION

    return resolve_vers()


def _version_from_tags(reference_file):
    # Try to get the version from SCM. Obvi, this is intended for devs,
    # as normal users will likely not have setuptools_scm installed.
    import setuptools_scm

    # For whatever reason, relative_to does not work, (lb) thought it would.
    #   return setuptools_scm.get_version(relative_to=__file__)
    # So figure out the root path of the repo. In lieu of something robust,
    # like `git rev-parse --show-toplevel`, look for '.git/' ourselves.
    cur_path = reference_file or __file__
    while cur_path and cur_path != os.path.dirname(cur_path):
        cur_path = os.path.dirname(cur_path)
        proj_git = os.path.join(cur_path, ".git")
        if os.path.exists(proj_git):
            # Get version from setuptools_scm, and git tags.
            # This is similar to a developer running, e.g.,
            #   python setup.py --version
            # Raises LookupError.
            return setuptools_scm.get_version(root=cur_path)
    # No .git/ found. Package probably installed to site-packages/.
    return ""
