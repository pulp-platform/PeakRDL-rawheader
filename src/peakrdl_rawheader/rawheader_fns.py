#!/usr/bin/env python3
# Copyright 2025 ETH Zurich and University of Bologna.
# Licensed under the Apache License, Version 2.0, see LICENSE for details.
# SPDX-License-Identifier: Apache-2.0
#
# Authors:
# - Michael Rogenmoser <michaero@iis.ee.ethz.ch>
# - Tim Fischer <fischeti@iis.ee.ethz.ch>

from typing import Dict, List, Tuple

from systemrdl.node import AddrmapNode, FieldNode, MemNode, RegNode, RegfileNode


def get_layout(top_node: AddrmapNode) -> Tuple[List[Dict[str, int]], List[Dict[str, object]]]:
    """Return the hierarchical layout (blocks + register metadata)."""
    blocks: List[Dict[str, int]] = []
    registers: List[Dict[str, object]] = []
    _collect_node(top_node, [], [], blocks, registers)
    return blocks, registers


def _collect_node(node, name: List[str], array_info: List[Dict[str, int]], blocks, registers):

    match node:
        case FieldNode():
            # Fields do not contribute to layout at the moment
            return

        case RegNode():
            registers.append({
                "name": name + [node.inst_name],
                "addr": node.raw_absolute_address,
                "offset": node.raw_address_offset,
                "array_info": array_info + _build_array_info(node),
            })
            return


        case AddrmapNode() | RegfileNode() | MemNode():
            block = {
                "name": name + [node.inst_name],
                "addr": node.raw_absolute_address,
                "size": node.size,
                "array_info": array_info + _build_array_info(node),
            }
            if node.is_array:
                block["stride"] = node.array_stride
                block["total_size"] = node.total_size
            blocks.append(block)

    match node:
        case AddrmapNode() | RegfileNode():
            # `addrmap` and `regfile` can have children, which are handled recursively
            for child in node.children():
                _collect_node(child, name + [node.inst_name], array_info + _build_array_info(node), blocks, registers)

def _build_array_info(node):
    """Build array info dict for a node if it is an array."""
    if not node.is_array:
        return []
    return [{
        "base": node.raw_absolute_address,
        "idx_name": node.inst_name,
        "dim": node.array_dimensions,
        "stride": node.array_stride,
    }]

def get_enums(top_node: AddrmapNode):
    """Recursively get all enums in the addrmap tree."""

    # Collect unique enums
    seen_enum_keys = set()
    enums = []
    for node in top_node.descendants(FieldNode):
        if isinstance(node, FieldNode) and node.get_property("encode") is not None:
            enum = node.get_property("encode")

            if enum.type_name in seen_enum_keys:
                continue
            seen_enum_keys.add(enum.type_name)

            choices = []
            for enum_member in enum:
                choices.append({"name": enum_member.name.upper(), "value": enum_member.value, "desc": enum_member.rdl_desc})

            enums.append({
                "name": enum.type_name,
                "choices": choices
            })

    return enums
