# PeakRDL Raw Header

Generates a very basic header with addresses, sizes, and offsets from a SystemRDL file as a plugin to PeakRDL.

Currently supported formats:

|Format|Function|
|---|---|
|`c`|Simple C header file|
|`svh`|Simple SystemVerilog header file|
|`svpkg`|Simple SystemVerilog package|

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

## Publishing to PyPI

To create a new release on PyPI, follow the following steps:

1. Bump the version number in `pyproject.toml`. If you are using `uv`, you can do this with:

```bash
uv version --bump major|minor|patch
```

You can also do this manually by editing `pyproject.toml`, but make sure you run `uv lock` afterwards to update the lock file as well.

2. Edit the  the `CHANGELOG.md` to reflect the changes in this new version.

3. Commit the changes:

```bash
git add pyproject.toml uv.lock CHANGELOG.md
git commit -m "Release vX.Y.Z"
git push origin main
```

4. Optional: You can try out publishing the package to TestPypi first by running the `publish-test-pypi` CI job that has a manual `workflow_dispatch` trigger.

5. Create a new release on Github with the same version tag (e.g. `vX.Y.Z`).

This will automatially trigger a Github [workflow](.github/workflows/release.yml) to build and publish the package to PyPI using [Trusted Publishing](https://docs.pypi.org/trusted-publishers/).
