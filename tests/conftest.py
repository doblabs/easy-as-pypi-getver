# Author: Landon Bouma <https://tallybark.com/>
# Project: https://github.com/doblabs/easy-as-pypi-getver#🔢
# License: MIT

# Copyright (c) © 2018-2023 Landon Bouma. All Rights Reserved.

"""Test fixtures (none) for the ``easy-as-pypi-getver`` package tests."""

import sys


def get_version(root):
    """Fake setuptools_scm.get_version."""
    return "0.1.dev32+g187abdc.d20231114"


module_fake = type(sys)("setuptools_scm")
module_fake.get_version = get_version
sys.modules["setuptools_scm"] = module_fake
