# Copyright 2025 ETH Zurich and University of Bologna.
# Licensed under the Apache License, Version 2.0, see LICENSE for details.
# SPDX-License-Identifier: Apache-2.0
#
# Author: Tim Fischer <fischeti@iis.ee.ethz.ch>


def fmt_hex(value: int, format: str = "svh"):
    """Format an integer as hexadecimal string for C or SystemVerilog headers."""
    match format:
        case "c" | "ldh":
            return f"0x{value:08X}"
        case "svh" | "svpkg":
            return f"64'h{value:X}"


def fmt_idx_expr(array_info: list[dict[str, int]], format: str = "svh"):
    """Format array index expressions for C or SystemVerilog headers."""
    match format:
        case "c" | "svh":
            return ", ".join([f"{a['idx_name']}_idx" for a in array_info])
        case "svpkg":
            return ", ".join(
                [f"input int unsigned {a['idx_name']}_idx" for a in array_info]
            )


def fmt_addr_expr(base: int, array_info: list[dict[str, int]], format: str = "svh"):
    """Format address expressions with array indices for C or SystemVerilog headers."""
    terms = [fmt_hex(base, format)]
    for a in array_info:
        stride_str = fmt_hex(a["stride"], format)
        terms.append(f"({a['idx_name']}_idx * {stride_str})")
    return " + ".join(terms)


def fmt_param_value(value, format: str = "svh"):
    """Format an elaborated parameter value as a literal.

    Handles the scalar types that `_build_params` collects; the `ldh` format
    does not emit parameters, so every value has a representation here.
    """
    match value:
        # `bool` is a subclass of `int`, so it has to be matched first
        case bool():
            if format == "svpkg":
                return "1'b1" if value else "1'b0"
            return "1" if value else "0"
        case int():
            # Parameters are values rather than addresses, so decimal reads better
            return str(value)
        case str():
            return f'"{value}"'
    return None


def fmt_param_type(value):
    """Format the SystemVerilog type of a parameter value (for `svpkg`)."""
    match value:
        # `bool` is a subclass of `int`, so it has to be matched first
        case bool():
            return "bit"
        case int():
            return "longint unsigned" if value >= 0 else "longint"
        case str():
            return "string"
    return None


def fmt_license(license_str: str, format: str = "svh"):
    """Format license string for inclusion in header files."""
    match format:
        case "ldh":
            return "\n".join(
                ["/* " + line + " */" for line in license_str.strip().splitlines()]
            )
        case _:
            return "\n".join(
                ["// " + line for line in license_str.strip().splitlines()]
            )


def clog2(x: int) -> int:
    """Compute the ceiling of log2(x)."""
    return (x - 1).bit_length()
