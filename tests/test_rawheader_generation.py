# Copyright 2025 ETH Zurich and University of Bologna.
# Licensed under the Apache License, Version 2.0, see LICENSE for details.
# SPDX-License-Identifier: Apache-2.0
#
# Author: Luca Colagrande <colluca@iis.ee.ethz.ch>

from conftest import INPUT_DIR, OUTPUT_DIR, check_header, generate_header


def test_array_c():
    generated = generate_header(INPUT_DIR / "array.rdl", "c")
    check_header(generated, OUTPUT_DIR / "array.h")


def test_array_ldh():
    generated = generate_header(INPUT_DIR / "array.rdl", "ldh")
    check_header(generated, OUTPUT_DIR / "array.ldh")


def test_array_ldh_no_memory():
    generated = generate_header(INPUT_DIR / "array.rdl", "ldh", ldh_no_memory=True)
    check_header(generated, OUTPUT_DIR / "array.no_memory.ldh")


def test_array_ldh_no_symbols():
    generated = generate_header(INPUT_DIR / "array.rdl", "ldh", ldh_no_symbols=True)
    check_header(generated, OUTPUT_DIR / "array.no_symbols.ldh")

def test_example_c():
    generated = generate_header(INPUT_DIR / "example.rdl", "c")
    check_header(generated, OUTPUT_DIR / "example.h")

def test_example_svh():
    generated = generate_header(INPUT_DIR / "example.rdl", "svh")
    check_header(generated, OUTPUT_DIR / "example.svh")

def test_example_svpkg():
    generated = generate_header(INPUT_DIR / "example.rdl", "svpkg")
    check_header(generated, OUTPUT_DIR / "example.sv")

def test_example_ldh():
    generated = generate_header(INPUT_DIR / "example.rdl", "ldh")
    check_header(generated, OUTPUT_DIR / "example.ldh")


def test_memory_attrs_ldh():
    generated = generate_header(INPUT_DIR / "memory_attrs.rdl", "ldh")
    check_header(generated, OUTPUT_DIR / "memory_attrs.ldh")


def test_example_ldh_no_prefix():
    generated = generate_header(INPUT_DIR / "example.rdl", "ldh", no_prefix=True)
    check_header(generated, OUTPUT_DIR / "example.no_prefix.ldh")
