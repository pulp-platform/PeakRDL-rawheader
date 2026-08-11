Command Line Options
====================

PeakRDL-rawheader registers a ``raw-header`` subcommand with the
`PeakRDL command line tool <https://peakrdl.readthedocs.io/>`_:

.. code-block:: bash

    peakrdl raw-header <input.rdl> -o <output> [options]

In addition to the standard PeakRDL arguments (such as ``-o``/``--output`` for
the output path), the following exporter-specific options are available.


.. option:: --format {c,svh,svpkg,ldh}

    Select the built-in output format. Defaults to ``c``. See :doc:`formats`
    for a description of each. Ignored when :option:`--template` is given.


.. option:: --template <path>

    Path to a custom `Mako <https://www.makotemplates.org/>`_ template file to
    render instead of the built-in formats. See :doc:`templates`.


.. option:: --base-name <name>

    Custom prefix for the generated symbols and the include guard. Defaults to
    the name of the top-level ``addrmap``. Mutually exclusive with
    :option:`--no-prefix`.


.. option:: --no-prefix

    Omit the top-level ``addrmap`` name from the generated symbol names.
    Mutually exclusive with :option:`--base-name`.


.. option:: --params

    Also emit the SystemRDL parameters of each block and register, in addition
    to the address symbols. Symbols are named ``<path>_PARAM_<NAME>``, so they
    cannot collide with the address symbols.

    Parameter values are resolved by the compiler during elaboration and are
    **per instance**: a component type instantiated twice with different
    overrides contributes a different value under each instance path. Parameters
    of aggregate type (arrays, structs, component references) have no sensible
    representation in a raw header and are skipped.

    Integer parameters are emitted in decimal, unlike addresses and sizes, which
    stay hexadecimal.

    Has no effect with ``--format ldh``: a linker script has no use for
    parameter values, and consumers that need them can read them from the
    ``c`` header instead.


.. option:: --license-str <string>

    License string to embed at the top of the generated file. Literal ``\n``
    sequences are converted to newlines, so multi-line license headers can be
    passed on the command line.


.. option:: --ldh-no-memory

    Only meaningful with ``--format ldh``. Suppresses emission of the
    ``MEMORY { ... }`` regions.


.. option:: --ldh-no-symbols

    Only meaningful with ``--format ldh``. Suppresses emission of the
    ``PROVIDE(...)`` symbols.


.. option:: --ldh-no-registers

    Only meaningful with ``--format ldh``. Suppresses emission of the
    ``PROVIDE(...)`` symbols for registers, keeping those for blocks. Useful
    for register maps with large register arrays, where the per-element
    symbols dominate the output but linker scripts only reference block base
    addresses.


.. note::

    The deprecated aliases ``--base_name`` and ``--license_str`` (with
    underscores) are still accepted for backward compatibility, but
    :option:`--base-name` and :option:`--license-str` should be used instead.
