#!/usr/bin/env python3
# Copyright 2025 ETH Zurich and University of Bologna.
# Licensed under the Apache License, Version 2.0, see LICENSE for details.
# SPDX-License-Identifier: Apache-2.0
#
# Author: Michael Rogenmoser <michaero@iis.ee.ethz.ch>

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
            "--base_name", default=None,
            help="Custom prefix for the header (defaults to top-level map name)"
        )
        arg_group.add_argument(
            "--format", default="c",
            choices=["c", "svh", "svpkg"]
        )
        arg_group.add_argument(
            "--license_str", default=None,
            help="License string to include in the header file"
        )
        arg_group.add_argument(
            "--flat", action="store_true",
            help="Emit fully unrolled constants instead of the default indexed macros"
        )

    def do_export(self, top_node: AddrmapNode, options):
        output_path = options.output
        top_name = (options.base_name or top_node.inst_name)

        license_str = None
        if options.license_str:
            # Convert literal \n to actual newlines
            license_str = options.license_str.replace('\\n', '\n')

        # Load template
        if options.template:
            template_path = options.template
        else:
            tpl_dir = files("peakrdl_rawheader") / "templates"
            if options.format == "c":
                template_path = tpl_dir / "c_header.tpl"
            elif options.format == "svh":
                template_path = tpl_dir / "svh.tpl"
            elif options.format == "svpkg":
                template_path = tpl_dir / "svpkg.tpl"
            else:
                # Default to C header template (shouldn't happen due to choices constraint)
                template_path = tpl_dir / "c_header.tpl"
        with open(template_path, "r") as tf:
            tmpl = Template(tf.read())

        # Gather data for the template
        blocks, registers = get_layout(top_node, flat=options.flat)
        enums = get_enums(top_node)

        # Render and write
        rendered = tmpl.render(
            top_name=top_name,
            blocks=blocks,
            registers=registers,
            license_str=license_str,
            enums=enums,
            flat=options.flat,
        )
        with open(output_path, "w") as f:
            f.write(rendered)
