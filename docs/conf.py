# Copyright 2025 ETH Zurich and University of Bologna.
# Licensed under the Apache License, Version 2.0, see LICENSE for details.
# SPDX-License-Identifier: Apache-2.0
#
# Sphinx configuration for the PeakRDL-rawheader documentation.
# See https://www.sphinx-doc.org/en/master/usage/configuration.html

import datetime

project = "PeakRDL-rawheader"
author = "Michael Rogenmoser, Tim Fischer"
copyright = f"{datetime.date.today().year}, ETH Zurich and University of Bologna"

exclude_patterns = ["_build"]

html_theme = "sphinx_book_theme"
html_theme_options = {
    "repository_url": "https://github.com/pulp-platform/PeakRDL-rawheader",
    "path_to_docs": "docs",
    "use_source_button": True,
    "use_repository_button": True,
    "use_issues_button": True,
}
