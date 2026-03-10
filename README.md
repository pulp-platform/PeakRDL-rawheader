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

## Installation

You can install the package via pip:

```bash
pip install peakrdl-rawheader
```

Or add it as a dependency in your `pyproject.toml` or `requirements.txt` e.g. with `uv`:

```bash
uv add peakrdl-rawheader
```

## Usage

### Example

Given the following SystemRDL input:

```systemrdl
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
```

The generated output will look like this:

#### C Header (`c`)

```c
#define TOP_STATUS_BASE_ADDR(status_idx) (0x00000000 + (status_idx * 0x00000004))
#define TOP_STATUS_NUM 0x00000002
// ...
#define state__IDLE 0
#define state__BUSY 1
```

#### SystemVerilog Header (`svh`)

```systemverilog
`define TOP_STATUS_BASE_ADDR(status_idx) (64'h0 + (status_idx * 64'h4))
`define TOP_STATUS_NUM 64'h2
// ...
`define STATE__IDLE 0
`define STATE__BUSY 1
```

#### SystemVerilog Package (`svpkg`)

```systemverilog
function automatic longint unsigned TOP_STATUS_BASE_ADDR(input int unsigned status_idx);
    return 64'h0 + (status_idx * 64'h4);
endfunction
// ...
typedef enum logic [0:0] {
    IDLE = 1'd0,
    BUSY = 1'd1
} state_e;
```

#### Linker Header (`ldh`)

```ld
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
```

`ldh` supports selectively disabling either section:

- `--ldh-no-memory`: skip `MEMORY { ... }` region emission
- `--ldh-no-symbols`: skip `PROVIDE(...)` symbol emission

`MEMORY` attributes are derived from memory properties:

- `sw` controls `r`/`w`
- user-defined boolean `executable` controls `x`

Example UDP declaration in SystemRDL:

```systemrdl
property executable {
  component = mem;
  type = boolean;
};
```

## Releasing

Release instructions are documented in [RELEASE.md](RELEASE.md).
