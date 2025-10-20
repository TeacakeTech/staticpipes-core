# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/en/1.0.0/)
and this project adheres to [Semantic Versioning](http://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Changed

The API to Pipes has been changed in a backwards incompatible manner!
Prepare stage removed and multiple build stages with different pass numbers introduced
https://github.com/TeacakeTech/staticpipes-core/issues/55

### Removed

- Dropped support for Python 3.9 as that isn't supported anymore.

### Fixed

- PipeLoadCollectionPythonDocs doesn't raise a false alert during watch stage

## [0.4.0] - 2025-09-14

### Added

- Added `output_mode` and `output_filename` options to `PipeCollectionRecordsProcess` https://github.com/StaticPipes/StaticPipes/issues/19
- Build command exits with sys.exit error codes if checks fail, so can use in CI https://github.com/StaticPipes/StaticPipes/issues/54
- Add check command to CLI. Exits with sys.exit error codes if checks fail, so can use in CI https://github.com/StaticPipes/StaticPipes/issues/54
- Added `arguments` to data collected in `PipeLoadCollectionPythonDocs` https://github.com/StaticPipes/StaticPipes/issues/26
- Added `ProcessRemoveHTMLExtension` https://github.com/StaticPipes/StaticPipes/issues/19
- Added `ProcessJinja2RenderSourceFile` (Same as old `ProcessJinja2`) and `ProcessJinja2RenderContents`

### Fixed

- More robust handling of dir strings
- Crash in `CheckHtmlWithTidy`
- `ProcessMarkdownYAMLToHTMLContext` - should set vars in process context, not context for whole site https://github.com/StaticPipes/StaticPipes/issues/32

### Changed / Deprecated

- `staticpipes.processes.jinja2.ProcessJinja2` has been renamed to `staticpipes.processes.jinja2_render_source_file.ProcessJinja2RenderSourceFile`, 
  but the old name still works.

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

