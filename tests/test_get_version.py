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

"""Tests get_version() and related."""

import os
import re
from pkg_resources import DistributionNotFound

import pytest
from unittest import mock

import easy_as_pypi_getver
from easy_as_pypi_getver import get_version


__package_name__ = 'easy-as-pypi-getver'
__import_token__ = 'easy_as_pypi_getver'


class TestEasyAsPyPIGetVer:

    # *** Test API

    def test_get_version_requires_package_name(self):
        with pytest.raises(TypeError):
            get_version()

    # *** Response Validation

    def assert_is_version_string_headless(self, pkg_version):
        # (lb): Note that get_version replies differently if setuptools_scm
        # is available or not. And note also version (at least for DEVs) will
        # often be a non-release version, e.g., '3.0.2.dev9+gfba2058.d20200401'.
        assert re.match(r'^[0-9]+\.[0-9]+\.[a-z0-9+]+$', pkg_version)

    def assert_is_version_string_and_head(self, pkg_version):
        # E.g., '3.2.4.dev5+gd15b68dc.d20201209 (3.2.4.dev16+g2bd6b40e)'.
        assert re.match(r'^[0-9]+\.[0-9]+.* (.*)$', pkg_version)

    # *** Tests

    def test_get_version_given_this_package(self):
        # 2020-12-21: '0.1.dev3+gd19055b'
        pkg_version = get_version(__package_name__)
        self.assert_is_version_string_headless(pkg_version)

    def test_get_version_include_head_normal(self):
        # 2020-12-21: '0.1.dev3+gd19055b (0.1.dev3+gc70a108.d20201221)'
        pkg_version = get_version(__package_name__, include_head=True)
        self.assert_is_version_string_and_head(pkg_version)

    def test_get_version_include_head_known_postfix(self, mocker):
        # 2020-12-21: '0.1.dev3+gd19055b (foo)'
        mocker.patch.object(
            easy_as_pypi_getver, '_version_from_tags', return_value='foo',
        )
        pkg_version = get_version(__package_name__, include_head=True)
        self.assert_is_version_string_and_head(pkg_version)
        # The repo version is appended in (parentheses).
        assert pkg_version.endswith(' (foo)')

    _version_from_tags_object = '{}._version_from_tags'.format(__import_token__)

    def test_get_version_without_setuptools_scm(self):
        with mock.patch(self._version_from_tags_object) as import_scm_mock:
            import_scm_mock.side_effect = ImportError()
            pkg_version = get_version(__package_name__, include_head=True)
            # The result is still a version, but the user's repo version
            # will not be postfixed in (parentheses).
            self.assert_is_version_string_headless(pkg_version)

    def test_get_version_from_not_a_repo(self):
        with mock.patch(self._version_from_tags_object) as import_scm_mock:
            import_scm_mock.side_effect = LookupError()
            pkg_version = get_version(__package_name__, include_head=True)
            self.assert_is_version_string_and_head(pkg_version)
            assert pkg_version.endswith(' (<none?!>)')

    def test_get_version_get_distribution_fails(self):
        with mock.patch('pkg_resources.get_distribution') as get_distribution_mock:
            get_distribution_mock.side_effect = DistributionNotFound()
            pkg_version = get_version(__package_name__)
            assert pkg_version == '<none!?>'

    def test_get_version_include_head_no_git_found(self, mocker):
        mocker.patch.object(os.path, 'exists', return_value=False)
        pkg_version = get_version(__package_name__, include_head=True)
        self.assert_is_version_string_headless(pkg_version)

