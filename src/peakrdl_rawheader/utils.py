# Copyright 2025 ETH Zurich and University of Bologna.
# Licensed under the Apache License, Version 2.0, see LICENSE for details.
# SPDX-License-Identifier: Apache-2.0
#
# Author: Tim Fischer <fischeti@iis.ee.ethz.ch>

from typing import Dict, List


def fmt_hex(value: int, format: str = "svh"):
    """Format an integer as hexadecimal string for C or SystemVerilog headers."""
    match format:
        case "c":
            return f"0x{value:08X}"
        case "svh" | "svpkg":
            return f"64'h{value:X}"

def fmt_idx_expr(array_info: List[Dict[str, int]], format: str = "svh"):
    """Format array index expressions for C or SystemVerilog headers."""
    match format:
        case "c" | "svh":
            return "".join([f"[{a['idx_name']}_idx]" for a in array_info])
        case "svpkg":
            return ", ".join([f"input int unsigned {a['idx_name']}_idx" for a in array_info])

def fmt_addr_expr(base: int, array_info: List[Dict[str, int]], format: str = "svh"):
    """Format address expressions with array indices for C or SystemVerilog headers."""
    terms = [fmt_hex(base, format)]
    for a in array_info:
        stride_str = fmt_hex(a['stride'], format)
        terms.append(f"({a['idx_name']}_idx * {stride_str})")
    return " + ".join(terms)

def fmt_license(license_str: str):
    """Format license string for inclusion in header files."""
    return "\n".join(["// " + line for line in license_str.strip().splitlines()])

def clog2(x: int) -> int:
    """Compute the ceiling of log2(x)."""
    return (x - 1).bit_length()
