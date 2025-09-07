# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/en/1.0.0/)
and this project adheres to [Semantic Versioning](http://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- Added `output_mode` and `output_filename` options to `PipeCollectionRecordsProcess` https://github.com/StaticPipes/StaticPipes/issues/19

### Fixed

- More robust handling of dir strings

## [0.3.0] - 2025-06-15

### Added

- Added new check `CheckHtmlWithTidy` https://github.com/StaticPipes/StaticPipes/issues/40
- Added `filters` option to `Jinja2Environment` https://github.com/StaticPipes/StaticPipes/issues/29
- Added `context_key_record_class` option to `PipeCollectionRecordsProcess` https://github.com/StaticPipes/StaticPipes/issues/37
- Added `--check` and `--no-check` options to `build` CLI.

## [0.2.0] - 2025-06-15

### Added

- Added binary mode to PipeProcess via new binary_content parameter

### Fixed

- CheckInternalLinks - stop various false positive alarms

## [0.1.0] - 2025-06-07

First major release

