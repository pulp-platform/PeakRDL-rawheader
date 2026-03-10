#!/usr/bin/env python3
# Copyright 2025 ETH Zurich and University of Bologna.
# Licensed under the Apache License, Version 2.0, see LICENSE for details.
# SPDX-License-Identifier: Apache-2.0
#
# Author: Michael Rogenmoser <michaero@iis.ee.ethz.ch>

import argparse
from importlib.resources import files

from mako.template import Template
from peakrdl.plugins.exporter import ExporterSubcommandPlugin
from systemrdl.node import AddrmapNode

from peakrdl_rawheader.rawheader_fns import get_enums, get_layout

class HeaderGeneratorDescriptor(ExporterSubcommandPlugin):
    short_desc = "Generate C header with block base addresses and register offsets via Mako"
    long_desc = (
        "Walk the RDL tree and render a C header file from a Mako template, "
        "indicating base addresses for each addrmap block and offsets for each register."
    )

    def add_exporter_arguments(self, arg_group):
        arg_group.add_argument(
            "--template", default=None,
            help="Path to the Mako template file (defaults to templates in plugin dir)"
        )
        arg_group.add_argument(
            "--base-name", default=None,
            help="Custom prefix for the header (defaults to top-level map name)"
        )
        # INFO(fischeti): To be deprecated in favor of `--base-name`,
        # but keep the old option for backward compatibility for now
        arg_group.add_argument(
            "--base_name", dest="base_name", default=None,
            help=argparse.SUPPRESS
        )
        arg_group.add_argument(
            "--format", default="c",
            choices=["c", "svh", "svpkg", "ldh"]
        )
        arg_group.add_argument(
            "--license-str", default=None,
            help="License string to include in the header file"
        )
        # INFO(fischeti): To be deprecated in favor of `--license-str`,
        # but keep the old option for backward compatibility for now
        arg_group.add_argument(
            "--license_str", dest="license_str", default=None,
            help=argparse.SUPPRESS
        )
        arg_group.add_argument(
            "--ldh-no-memory", action="store_true",
            help="When --format=ldh, do not emit linker MEMORY regions"
        )
        arg_group.add_argument(
            "--ldh-no-symbols", action="store_true",
            help="When --format=ldh, do not emit PROVIDE() symbols"
        )
        arg_group.add_argument(
            "--no-prefix", action="store_true",
            help="Omit the top-level addrmap name from generated symbol names"
        )

    @staticmethod
    def format(top_node: AddrmapNode, options):
        top_name = (options.base_name or top_node.inst_name)

        license_str = None
        if options.license_str:
            # Convert literal \n to actual newlines
            license_str = options.license_str.replace('\\n', '\n')

        # Load template
        if options.template:
            template_path = options.template
        else:
            template_path = files("peakrdl_rawheader") / "templates" / (options.format + ".mako")

        with open(template_path, "r") as tf:
            tmpl = Template(tf.read())

        # Gather data for the template
        blocks, registers, memories = get_layout(top_node)
        enums = get_enums(top_node)
        emit_ldh_memory = not getattr(options, "ldh_no_memory", False)
        emit_ldh_symbols = not getattr(options, "ldh_no_symbols", False)

        if getattr(options, "no_prefix", False):
            for item in blocks + registers + memories:
                item["name"] = item["name"][1:]

        # Render and write
        rendered = tmpl.render(
            top_name=top_name,
            blocks=blocks,
            registers=registers,
            memories=memories,
            emit_ldh_memory=emit_ldh_memory,
            emit_ldh_symbols=emit_ldh_symbols,
            license_str=license_str,
            enums=enums
        )
        return rendered

    def do_export(self, top_node: AddrmapNode, options):
        output_path = options.output
        rendered = HeaderGeneratorDescriptor.format(top_node, options)
        with open(output_path, "w") as f:
            f.write(rendered)
