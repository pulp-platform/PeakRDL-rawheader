#!/usr/bin/env python3
# Copyright 2025 ETH Zurich and University of Bologna.
# Licensed under the Apache License, Version 2.0, see LICENSE for details.
# SPDX-License-Identifier: Apache-2.0
#
# Author: Michael Rogenmoser <michaero@iis.ee.ethz.ch>

from typing import Dict, List, Sequence, Tuple

from systemrdl.node import AddrmapNode, FieldNode, MemNode, RegNode, RegfileNode


def get_regs(node: AddrmapNode, prefix: str = ""):
    """Backward-compatible helper that returns the previous flat layout."""
    return _get_flat_blocks(node, prefix)


def _get_flat_blocks(node: AddrmapNode, prefix: str = ""):
    """Recursively get all registers in the addrmap tree using the legacy flat view."""
    start_basename = prefix + node.inst_name.upper()
    if node.is_array:
        nodes = list(node.unrolled())
    else:
        nodes = [node]

    block: List[List[Dict[str, int]]] = []
    subblock: List[Dict[str, int]] = []

    for i, subnode in enumerate(nodes):
        basename = start_basename
        if node.is_array:
            for idx in subnode.current_idx:
                basename += "_" + str(idx)
            if i == 0:
                block.append([])
                block.append([
                    {"name": start_basename + "_BASE_ADDR", "num": subnode.absolute_address},
                    {"name": start_basename + "_SIZE     ", "num": subnode.total_size},
                    {"name": start_basename + "_STRIDE   ", "num": subnode.array_stride},
                ])

        if isinstance(subnode, RegNode):
            subblock.extend([
                {"name": basename + "_REG_ADDR  ", "num": subnode.absolute_address},
                {"name": basename + "_REG_OFFSET", "num": subnode.address_offset},
            ])
            block = [subblock]
        elif isinstance(subnode, AddrmapNode) or isinstance(node, RegfileNode):
            block.append([])
            block.append([
                {"name": basename + "_BASE_ADDR", "num": subnode.absolute_address},
                {"name": basename + "_SIZE     ", "num": subnode.size},
            ])
            for child in subnode.children():
                block.extend(_get_flat_blocks(child, basename + "_"))
        elif isinstance(subnode, MemNode):
            block.append([])
            block.append([
                {"name": basename + "_BASE_ADDR", "num": subnode.absolute_address},
                {"name": basename + "_SIZE     ", "num": subnode.size},
            ])
        else:
            raise TypeError(f"Unknown node type: {type(node)}")

    return block


def get_layout(top_node: AddrmapNode, flat: bool = False) -> Tuple[List[List[Dict[str, int]]], List[Dict[str, object]]]:
    """Return the hierarchical layout (blocks + register metadata) or the legacy flat list."""
    if flat:
        return _get_flat_blocks(top_node), []

    blocks: List[List[Dict[str, int]]] = []
    registers: List[Dict[str, object]] = []
    _collect_node(top_node, "", [], blocks, registers)
    return blocks, registers


def _collect_node(node, prefix: str, addr_dims: Sequence[Dict[str, int]], blocks, registers):
    start_basename = prefix + node.inst_name.upper()

    if isinstance(node, RegNode):
        registers.append(_build_reg_entry(start_basename, node, addr_dims))
        return

    if isinstance(node, FieldNode):
        return

    if isinstance(node, (AddrmapNode, RegfileNode, MemNode)):
        entries = [
            {"name": start_basename + "_BASE_ADDR", "num": node.raw_absolute_address},
            {"name": start_basename + "_SIZE     ", "num": _node_size(node)},
        ]
        stride = _array_stride(node)
        if node.is_array and stride is not None:
            entries.append({"name": start_basename + "_STRIDE   ", "num": stride})
        blocks.append(entries)
    else:
        raise TypeError(f"Unknown node type: {type(node)}")

    if isinstance(node, (AddrmapNode, RegfileNode)):
        new_dims = list(addr_dims) + _compute_dim_info(node)
        for child in node.children():
            _collect_node(child, start_basename + "_", new_dims, blocks, registers)


def _node_size(node):
    return node.total_size if node.is_array else node.size


def _array_stride(node):
    if not getattr(node, "is_array", False):
        return None
    stride = getattr(node, "array_stride", None)
    if stride is not None:
        return stride

    dims = getattr(node, "array_dimensions", [])
    if not dims:
        return None
    elem_count = 1
    for dim in dims:
        elem_count *= dim
    total_size = getattr(node, "total_size", None)
    if total_size is None or elem_count == 0:
        return None
    return total_size // elem_count


def _compute_dim_info(node):
    if not getattr(node, "is_array", False):
        return []

    dims = list(getattr(node, "array_dimensions", []) or [])
    if not dims:
        return []

    base_stride = _array_stride(node)
    if base_stride is None:
        return []

    strides = [0] * len(dims)
    running = base_stride
    for idx in range(len(dims) - 1, -1, -1):
        strides[idx] = running
        running *= dims[idx]

    return [{"length": dim, "stride": stride} for dim, stride in zip(dims, strides)]


def _build_reg_entry(name: str, node: RegNode, addr_dims: Sequence[Dict[str, int]]):
    reg_dims = _compute_dim_info(node)
    full_dims = list(addr_dims) + reg_dims

    params = [{"name": f"i{idx}", "stride": dim["stride"]} for idx, dim in enumerate(full_dims)]
    return {
        "name": name,
        "addr_base": node.raw_absolute_address,
        "offset_base": node.raw_address_offset,
        "addr_params": params,
        "reg_param_offset": len(addr_dims),
    }


def get_enums(top_node: AddrmapNode, prefix: str = ""):
    """Recursively get all enums in the addrmap tree."""

    # Collect unique enums
    seen_enum_keys = set()
    enums = []
    for node in top_node.descendants(FieldNode):
        if isinstance(node, FieldNode) and node.get_property("encode") is not None:
            enum = node.get_property("encode")
            enum_name = enum.type_name.upper()
            qualified_name = f"{enum_name}"

            if qualified_name in seen_enum_keys:
                continue
            seen_enum_keys.add(qualified_name)

            choices = []
            for enum_member in enum:
                choices.append({"name": enum_member.name.upper(), "value": enum_member.value, "desc": enum_member.rdl_desc})

            enums.append({
                "name": qualified_name,
                "choices": choices
            })

    return enums
