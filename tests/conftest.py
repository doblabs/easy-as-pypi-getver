# Author: Landon Bouma <https://tallybark.com/>
# Project: https://github.com/doblabs/easy-as-pypi-getver#🔢
# License: MIT

# Copyright (c) © 2018-2023 Landon Bouma. All Rights Reserved.

"""Test fixtures (none) for the ``easy-as-pypi-getver`` package tests."""

import pytest
from click.testing import CliRunner

import easy_as_pypi_getver


@pytest.fixture
def runner():
    """Provide a convenient fixture to simulate execution of (sub-) commands."""

    def runner(args=[], **kwargs):
        env = {}
        return CliRunner().invoke(easy_as_pypi_getver.cli, args, env=env, **kwargs)

    return runner
