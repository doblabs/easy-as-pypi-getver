# This file exists within 'easy-as-pypi-getver':
#
#   https://github.com/tallybark/easy-as-pypi-getver#🔢
#
# Copyright © 2018-2020 Landon Bouma. All rights reserved.
#
# Permission is hereby granted,  free of charge,  to any person obtaining a
# copy of this software and associated documentation files (the "Software"),
# to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge,  publish,  distribute, sublicense,
# and/or  sell copies  of the Software,  and to permit persons  to whom the
# Software  is  furnished  to do so,  subject  to  the following conditions:
#
# The  above  copyright  notice  and  this  permission  notice  shall  be
# included  in  all  copies  or  substantial  portions  of  the  Software.
#
# THE  SOFTWARE  IS  PROVIDED  "AS IS",  WITHOUT  WARRANTY  OF ANY KIND,
# EXPRESS OR IMPLIED,  INCLUDING  BUT NOT LIMITED  TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE  FOR ANY
# CLAIM,  DAMAGES OR OTHER LIABILITY,  WHETHER IN AN ACTION OF CONTRACT,
# TORT OR OTHERWISE,  ARISING FROM,  OUT OF  OR IN  CONNECTION WITH THE
# SOFTWARE   OR   THE   USE   OR   OTHER   DEALINGS  IN   THE  SOFTWARE.

"""Top-level package for this CLI-based application."""

import os

__all__ = (
    "get_version",
    # Private:
    #  '_version_from_tags',
)

# This version is substituted on poetry-build by poetry-dynamic-versioning.
# - Consequently, __version__ remains empty when installed in 'editable' mode.
__version__ = ""


def get_version(package_name, reference_file=None, include_head=False):
    """Return the installed package version, or '<none>'.

    In lieu of always setting __version__ -- and always loading pkg_resources --
    use a method to avoid incurring startup costs if the version is not needed.
    """

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

        # - This returns the version most recently pip-installed. That is, if
        #   you install local sources and have committed code but not run the
        #   pip-install again, this shows the older version.
        # - ORNOT/2023-11-13: Now that Poetry is the installer, including in
        #   'editable' mode, the package will be versioned, e.g., here's
        #   what I see importlib.metadata.version report is the version
        #   of this repo, before I've even version-tagged it (and where
        #   the pyproject.toml [tool.poetry] version = "0.0.0):
        #     '0.0.0.post19.dev0+d7c69ea'.
        try:
            return version(package_name)
        except PackageNotFoundError:
            # This would be really weird, no?
            # - ITWLD/2023-11-13: Per same-dated comment above, unlikely
            #   that importlib would ever report this on an installed
            #   package, whether 'editable' or not. It path should only
            #   happen on a package that's *not* installed.
            return "<none!?>"

    def version_from_repo():
        try:
            return _version_from_tags(reference_file)
        # Note: ModuleNotFoundError in Py3.6+, so using less specific ImportError.
        except ImportError:
            # No setuptools_scm package installed.
            return ""
        except LookupError:
            # Path containing .git/ not a repo after all.
            return "<none?!>"

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
            return setuptools_scm.get_version(root=cur_path)
    # No .git/ found. Package probably installed to site-packages/.
    return ""
