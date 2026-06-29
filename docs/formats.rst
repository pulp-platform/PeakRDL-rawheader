Output Formats
==============

PeakRDL-rawheader ships with four built-in output formats, selected with the
:option:`--format` command line option. All of them are rendered from
`Mako <https://www.makotemplates.org/>`_ templates bundled with the plugin, so
their structure can also serve as a starting point for :doc:`custom templates
<templates>`.

The examples below all use the following SystemRDL input:

.. code-block:: systemrdl

    addrmap top {
        enum state {
            IDLE = 0;
            BUSY = 1;
        };

        reg status_reg {
            field {
                encode = state;
            } fld;
        };

        status_reg status[2];
    };


C Header (``c``)
----------------

The default format. Emits base addresses, sizes, offsets, and enum encodings as
C preprocessor ``#define`` macros, wrapped in an include guard.

.. code-block:: bash

    peakrdl raw-header top.rdl -o top.h

.. code-block:: c

    #define TOP_STATUS_BASE_ADDR(status_idx) (0x00000000 + (status_idx * 0x00000004))
    #define TOP_STATUS_NUM 0x00000002
    // ...
    #define state__IDLE 0
    #define state__BUSY 1


SystemVerilog Header (``svh``)
------------------------------

The same information as the C header, emitted as SystemVerilog `` `define ``
macros for inclusion in RTL or testbenches.

.. code-block:: bash

    peakrdl raw-header top.rdl -o top.svh --format svh

.. code-block:: systemverilog

    `define TOP_STATUS_BASE_ADDR(status_idx) (64'h0 + (status_idx * 64'h4))
    `define TOP_STATUS_NUM 64'h2
    // ...
    `define STATE__IDLE 0
    `define STATE__BUSY 1


SystemVerilog Package (``svpkg``)
---------------------------------

Emits a SystemVerilog package where address calculations are exposed as
``automatic`` functions and enum encodings as ``typedef enum`` types.

.. code-block:: bash

    peakrdl raw-header top.rdl -o top_pkg.sv --format svpkg

.. code-block:: systemverilog

    function automatic longint unsigned TOP_STATUS_BASE_ADDR(input int unsigned status_idx);
        return 64'h0 + (status_idx * 64'h4);
    endfunction
    // ...
    typedef enum logic [0:0] {
        IDLE = 1'd0,
        BUSY = 1'd1
    } state_e;


Linker Script Header (``ldh``)
------------------------------

Emits a GNU linker script fragment with a ``MEMORY`` region for each memory in
the register map and ``PROVIDE(...)`` symbols for register addresses, strides,
and counts.

.. code-block:: bash

    peakrdl raw-header top.rdl -o top.ldh --format ldh

.. code-block:: text

    /* Memories */
    MEMORY {
      top_array_0 (rw) : ORIGIN = 0x70000000, LENGTH = 0x00100000
      top_imem (rx) : ORIGIN = 0x00000000, LENGTH = 0x00001000
    }

    /* Registers */
    PROVIDE(__top_status_0_base_addr__ = 0x00000000);
    PROVIDE(__top_status_1_base_addr__ = 0x00000004);
    PROVIDE(__top_status_num__ = 0x00000002);
    PROVIDE(__top_status_stride__ = 0x00000004);

Either section can be disabled selectively:

* :option:`--ldh-no-memory`: skip ``MEMORY { ... }`` region emission
* :option:`--ldh-no-symbols`: skip ``PROVIDE(...)`` symbol emission

The attributes of each ``MEMORY`` region are derived from the memory's
SystemRDL properties:

* ``sw`` controls the ``r`` / ``w`` flags
* a user-defined boolean property named ``executable`` controls the ``x`` flag

The ``executable`` property is not part of the SystemRDL standard, so it must be
declared as a user-defined property (UDP) before use:

.. code-block:: systemrdl

    property executable {
      component = mem;
      type = boolean;
    };
