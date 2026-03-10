# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.2.4] - 2026-3-10

### Changed

- Added generation disclaimer comment in comment headers.

## [0.2.3] - 2026-3-10

### Added

- New `--ldh` format to generate header files for linker scripts.
- `--no-prefix` flag to cut top-level name from generated identifiers.

### Fixed

- Remove unnecessary whitespaces in generated code.

## [0.2.2] - 2026-1-15

### Fixed

- Corrected `c` template to use uppercase for enum names.

## [0.2.1] - 2025-12-16

### Added

- Render enums in `svh` and `svpkg` formats (previously only in `c`).
- Render array dimensions as `*_NUM`

### Changed

- Array instances now generate indexed macros/functions by default instead of enumerating every element.
- Changed behaviour of `SIZE` with array instances.

### Removed

- Removed `*_OFFSET` definitions for registers and register blocks.

## [0.1.3] - 2025-12-08

### Fixed

- Version in `pyproject.toml` updated to match the released version.

## [0.1.2] - 2025-12-08

### Fixed

- README and LICENSE files being included in the distribution.

## [0.1.1] - 2025-12-08

### Fixed

- Packaging templates correctly so they are included in the distribution.

## [0.1.0] - 2025-12-08

Initial release
