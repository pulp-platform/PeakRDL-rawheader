#!/usr/bin/env python3
# Copyright 2025 ETH Zurich and University of Bologna.
# Licensed under the Apache License, Version 2.0, see LICENSE for details.
# SPDX-License-Identifier: Apache-2.0
#
# Author: Michael Rogenmoser <michaero@iis.ee.ethz.ch>

from systemrdl.node import AddrmapNode, RegNode, MemNode, RegfileNode, FieldNode


def get_regs(node: AddrmapNode, prefix: str = ""):
    """Recursively get all registers in the addrmap tree."""
    start_basename = prefix + node.inst_name.upper()
    nodes = []
    block = []
    subblock = []

    # Create a list of nodes, from the nodes in an array node or from a single scalar node
    if node.is_array:
        nodes = node.unrolled()
    else:
        nodes = [node]

    # Iterate over subnodes
    for i, subnode in enumerate(nodes):

        # If subnode is part of an array, add the index within the array to its basename.
        # Also, add a block for the base address and total size of the array.
        basename = start_basename
        if node.is_array:
            for idx in subnode.current_idx:
                basename += "_" + str(idx)
            # absolute_address cannot be called on array nodes, so we get the information
            # from subnode 0
            if i == 0:
                block.append([])
                block.append([
                    {"name": start_basename + "_BASE_ADDR", "num": subnode.absolute_address},
                    {"name": start_basename + "_SIZE     ", "num": subnode.total_size}
                ])

        # Handle different subnode types
        if isinstance(subnode, RegNode):
            subblock.extend([{"name": basename + "_REG_ADDR  ", "num": subnode.absolute_address},
                             {"name": basename + "_REG_OFFSET", "num": subnode.address_offset}])
            block = [subblock]
        elif isinstance(subnode, AddrmapNode) or isinstance(node, RegfileNode):
            block.append([])
            block.append([{"name": basename + "_BASE_ADDR", "num": subnode.absolute_address},
                          {"name": basename + "_SIZE     ", "num": subnode.total_size}])
            for child in subnode.children():
                block.extend(get_regs(child, basename + "_"))
        elif isinstance(subnode, MemNode):
            block.append([])
            block.append([{"name": basename + "_BASE_ADDR", "num": subnode.absolute_address},
                          {"name": basename + "_SIZE     ", "num": subnode.size}])
        else:
            print(f"Unknown node type: {type(node)}")

    return block


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
