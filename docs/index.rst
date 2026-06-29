Introduction
============

PeakRDL-rawheader is a free and open-source plugin for the
`PeakRDL command line tool <https://peakrdl.readthedocs.io/>`_ that generates
simple header files from a SystemRDL register description.

It walks the SystemRDL tree and emits the base addresses, sizes, offsets, array
strides, and enum encodings of your register map as plain ``#define`` macros,
SystemVerilog macros/packages, or GNU linker script fragments. The output is
intentionally minimal: it captures the *layout* of the register map so software
and hardware can share a single source of truth.

* Multiple built-in output formats (C, SystemVerilog header, SystemVerilog
  package, linker script)
* Custom output via user-provided `Mako <https://www.makotemplates.org/>`_
  templates
* Array-aware: emits indexing macros, strides, and element counts
* Renders ``enum`` encodings as named constants

Supported output formats:

================ ===============================================
Format           Description
================ ===============================================
``c``            Simple C header file
``svh``          Simple SystemVerilog header file
``svpkg``        Simple SystemVerilog package
``ldh``          Linker script header (``MEMORY`` + ``PROVIDE`` symbols)
================ ===============================================

See :doc:`formats` for examples of each, and :doc:`templates` for writing your
own.


Quick Start
-----------
The easiest way to use PeakRDL-rawheader is via the
`PeakRDL command line tool <https://peakrdl.readthedocs.io/>`_:

.. code-block:: bash

    # Install PeakRDL-rawheader along with the command-line tool, e.g. with uv
    uv add peakrdl-rawheader[cli]

    # ... or with pip
    python3 -m pip install peakrdl-rawheader[cli]

    # Export a C header!
    peakrdl raw-header atxmega_spi.rdl -o atxmega_spi.h

To select a different output format, use the ``--format`` option:

.. code-block:: bash

    peakrdl raw-header atxmega_spi.rdl -o atxmega_spi.svh --format svh

See :doc:`configuring` for the full list of command line options.


Links
-----

- `Source repository <https://github.com/pulp-platform/PeakRDL-rawheader>`_
- `Release Notes <https://github.com/pulp-platform/PeakRDL-rawheader/releases>`_
- `Issue tracker <https://github.com/pulp-platform/PeakRDL-rawheader/issues>`_
- `PyPi <https://pypi.org/project/peakrdl-rawheader>`_
- `SystemRDL Specification <http://accellera.org/downloads/standards/systemrdl>`_


.. toctree::
    :hidden:

    self
    formats
    configuring
    templates
    licensing
