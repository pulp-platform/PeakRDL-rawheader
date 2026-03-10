# Copyright 2025 ETH Zurich and University of Bologna.
# Licensed under the Apache License, Version 2.0, see LICENSE for details.
# SPDX-License-Identifier: Apache-2.0
#
# Author: Luca Colagrande <colluca@iis.ee.ethz.ch>

from argparse import Namespace
from systemrdl import RDLCompiler
from peakrdl_rawheader.__peakrdl__ import HeaderGeneratorDescriptor
from pathlib import Path

INPUT_DIR = Path(__file__).parent / "input"
OUTPUT_DIR = Path(__file__).parent / "output"


def default_options(format, **overrides):
    options = {
        "template": None,
        "base_name": None,
        "format": format,
        "license_str": None,
        "ldh_no_memory": False,
        "ldh_no_symbols": False,
        "no_prefix": False,
    }
    options.update(overrides)
    return Namespace(**options)


def parse(file):
    rdlc = RDLCompiler()
    rdlc.compile_file(file)
    return rdlc.elaborate().top


def generate_header(file, format, **overrides):
    return HeaderGeneratorDescriptor().format(parse(file), default_options(format, **overrides))


def check_header(generated, expected):
    with open(expected, "r") as f:
        expected_content = f.read()
    assert generated == expected_content
