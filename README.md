# PeakRDL Raw Header

Generates a very basic header with addresses, sizes, and offsets from a SystemRDL file as a plugin to PeakRDL.

Currently supported formats:

|Format|Function|
|---|---|
|`c`|Simple C header file|
|`svh`|Simple SystemVerilog header file|
|`svpkg`|Simple SystemVerilog package|

Custom templates are also supported.

## Array handling

By default, arrayed components are emitted as indexed macros/functions so that large register files no longer need thousands of repeated `#define`s. For example, a register array now results in entries such as `FOO_REG_ADDR(i0, i1)` that compute the absolute address on demand. Pass `--flat` to keep the legacy behaviour that enumerates every array element explicitly.
