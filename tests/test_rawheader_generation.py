# Copyright 2025 ETH Zurich and University of Bologna.
# Licensed under the Apache License, Version 2.0, see LICENSE for details.
# SPDX-License-Identifier: Apache-2.0
#
# Author: Luca Colagrande <colluca@iis.ee.ethz.ch>

from conftest import INPUT_DIR, OUTPUT_DIR, check_header, generate_header


def test_array_c():
    generated = generate_header(INPUT_DIR / "array.rdl", "c")
    check_header(generated, OUTPUT_DIR / "array.h")
