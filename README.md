[![docs](https://github.com/pulp-platform/PeakRDL-rawheader/actions/workflows/docs.yml/badge.svg)](https://pulp-platform.github.io/PeakRDL-rawheader/)
[![ci](https://github.com/pulp-platform/PeakRDL-rawheader/actions/workflows/ci.yml/badge.svg)](https://github.com/pulp-platform/PeakRDL-rawheader/actions/workflows/ci.yml)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/peakrdl-rawheader.svg)](https://pypi.org/project/peakrdl-rawheader)

# PeakRDL Raw Header

Generates a very basic header with addresses, sizes, and offsets from a SystemRDL file as a plugin to PeakRDL.

Currently supported formats:

|Format|Function|
|---|---|
|`c`|Simple C header file|
|`svh`|Simple SystemVerilog header file|
|`svpkg`|Simple SystemVerilog package|
|`ldh`|Linker script header (`MEMORY` + `PROVIDE` symbols)|

Custom templates are also supported.

## Documentation

See the [PeakRDL-rawheader Documentation](https://pulp-platform.github.io/PeakRDL-rawheader/) for installation, usage, all output formats, command line options, and writing custom templates.

## Installation

Add the package as a dependency to your project with `uv`:

```bash
uv add peakrdl-rawheader
```

Or install it with `pip`:

```bash
pip install peakrdl-rawheader
```

## Quick Start

Given a SystemRDL input, generate a C header (the default format):

```bash
peakrdl raw-header top.rdl -o top.h
```

Select a different output format with `--format`:

```bash
peakrdl raw-header top.rdl -o top.svh --format svh
```

See the [documentation](https://pulp-platform.github.io/PeakRDL-rawheader/) for examples of each output format and the full list of options.

## Releasing

Release instructions are documented in [RELEASE.md](RELEASE.md).
