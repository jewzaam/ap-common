# Test Plan

> This document describes the testing strategy for ap-common. It serves as
> the single source of truth for testing decisions and rationale.

## Overview

**Project:** ap-common
**Primary functionality:** Shared library providing FITS/XISF header reading, metadata normalization, file operations, calibration frame matching, logging, and progress utilities for the astrophotography pipeline.

## Testing Philosophy

This project follows the [ap-base Testing Standards](https://github.com/jewzaam/ap-base/blob/main/standards/testing.md).

Key testing principles for this project:

- Tests verify behavior, not implementation details; assertions check expected outcomes rather than internal state
- As a shared library, tests focus on the public API contract that downstream projects depend on
- External dependencies (astropy, xisf) are mocked to isolate unit tests from I/O and keep tests fast
- Test data is generated programmatically using `tmp_path` fixtures rather than stored as static files

## Test Categories

### Unit Tests

Tests for isolated functions with mocked dependencies.

| Module | Function | Test Coverage | Notes |
|--------|----------|---------------|-------|
| `fits.py` | `apply_file_naming_override()` | Conflict resolution, precedence, empty inputs | Tests raw key merging before normalization |
| `fits.py` | `get_file_headers()` | Filename parsing, profile extraction, object extraction, special cases | DATE-OBS, SET-TEMP, EXPOSURE suffix, CR2 default type |
| `fits.py` | `get_fits_headers()` | Basic reading, normalization, file naming override, non-string values | Mocks astropy FITS I/O |
| `fits.py` | `get_xisf_headers()` | Basic reading, HISTORY skip, empty values, normalization, override | Mocks xisf library |
| `fits.py` | `update_xisf_headers()` | Single/multiple updates, comments, check_existing, path normalization | Uses real XISF files via tmp_path |
| `normalization.py` | `normalize_filterName()` | Pass-through behavior | Transformations removed; verifies unchanged return |
| `normalization.py` | `normalize_date()` | Standard datetime, timezone variants, fractional seconds, date-only, custom formats | Explicit timezone offsets for deterministic results |
| `normalization.py` | `normalize_datetime()` | Standard datetime, date-only conversion, timezone, custom formats | |
| `normalization.py` | `normalize_target_name()` | Simple target, panel extraction, quote removal | |
| `normalization.py` | `normalize_headers()` | Basic normalization, DATE-OBS, target name, constants, None handling | Tests None-to-empty-string normalization for strict matching |
| `normalization.py` | `denormalize_header()` | Known headers, unknown headers | |
| `normalization.py` | `normalize_filename()` | BIAS/DARK/LIGHT paths, missing headers, optional headers, focal ratio handling | |
| `normalization.py` | `get_all_normalized_keys()` | Multi-key mapping (DATE-OBS), single-key mapping, unknown headers | |
| `normalization.py` | `get_normalized_keys_set()` | Single/multiple headers, conflicting keys, DATE-OBS | |
| `metadata.py` | `filter_metadata()` | String/int/float/function filters, missing keys, whitespace, numeric string comparison | Regression tests for decimal representation matching |
| `metadata.py` | `get_metadata()` | Basic loading, required properties, targetname always required | Mocks get_filenames, get_file_headers, enrich_metadata |
| `metadata.py` | `enrich_metadata()` | FITS/XISF/CR2 enrichment, profile building, missing keys, location validation | |
| `metadata.py` | `get_filtered_metadata()` | Basic filtering, filter keys added to required properties | |
| `metadata.py` | `group_by_directory()` | Basic grouping, empty data, single/nested directories | |
| `metadata.py` | `get_directories_with_lights()` | Light detection, no lights, empty data, case insensitive, missing type | |
| `metadata.py` | `build_normalized_filters()` | Extraction, None filtering, overrides, DSLR metadata, whitespace stripping | |
| `filesystem.py` | `copy_file()` | Basic copy, directory creation, dry run, metadata preservation | Uses tmp_path |
| `filesystem.py` | `move_file()` | Basic move, directory creation, dry run, debug logging | |
| `filesystem.py` | `delete_empty_directories()` | Single/nested empty dirs, dirs with files, dry run, env vars | |
| `utils.py` | `build_profile()` | All key combinations, None values, empty dict, extra keys | |
| `utils.py` | `replace_env_vars()` | None input, no vars, single/multiple replacement, case insensitive | |
| `utils.py` | `resolve_path()` | None input, absolute path, env vars, home expansion, relative paths | |
| `utils.py` | `camelCase()` | Simple/special chars, all caps, mixed case, empty, non-alphanumeric | |
| `utils.py` | `get_filenames()` | Basic finding, multiple patterns, recursive, stash ignore, env vars | |
| `logging_config.py` | `setup_logging()` | Logger creation, levels (debug/quiet/default), handlers, custom formats | |
| `logging_config.py` | `get_logger()` | Default logger, named logger, caching | |
| `progress.py` | `progress_iter()` | Enabled/disabled, generators, custom desc/unit, empty, desc_width | |
| `progress.py` | `ProgressTracker` | Context manager, set_status, set_description, manual mode, desc_width | |
| `calibration.py` | `find_matching_darks()` | Exact exposure, shorter allowed/rejected, longer rejected, no matches, recursive | Mocks get_metadata |
| `calibration.py` | `find_matching_flats()` | Basic matching, multiple matches, no matches, date matching | |
| `calibration.py` | `find_matching_bias()` | Basic matching, multiple matches, no matches | |
| `calibration.py` | `find_matching_*_from_cache()` | Cache-based filtering, no disk I/O, criteria filtering, numeric string comparison | Pure in-memory tests |

### Integration Tests

Tests for multiple components working together.

| Workflow | Components | Test Coverage | Notes |
|----------|-----------|---------------|-------|
| Logging output | `setup_logging` + `StreamHandler` | Message output, level filtering | Tests actual log output via StringIO capture |
| Progress alignment | `progress_iter` + `ProgressTracker` | Default width alignment across both APIs | Verifies consistent desc padding |
| XISF header round-trip | `update_xisf_headers` + `XISF.read/write` | Data preservation, header persistence | Uses real XISF files |
| File naming override | `get_fits_headers` + `apply_file_naming_override` + `normalize_headers` | DATE-OBS preservation, FOCALLEN override | End-to-end header pipeline |

## Untested Areas

| Area | Reason Not Tested |
|------|-------------------|
| `constants.py` | Pure constants with no logic; validated indirectly through all modules that use them |
| ZIP archive support in `get_filenames()` | Requires ZIP file fixtures; low-priority feature with minimal usage |
| `tqdm` visual output | Progress bar rendering is a cosmetic concern; tested via mock verification of tqdm calls |

## Bug Fix Testing Protocol

All bug fixes to existing functionality **must** follow TDD:

1. Write a failing test that exposes the bug
2. Verify the test fails before implementing the fix
3. Implement the fix
4. Verify the test passes
5. Verify reverting the fix causes the test to fail again
6. Commit test and fix together with issue reference

### Regression Tests

| Issue | Test | Description |
|-------|------|-------------|
| #15 | `test_fits_filename_override_takes_precedence` | Filename EXPOSURE overrides FITS header EXPOSURE |
| #15 | `test_fits_filename_override_with_different_raw_keys` | Filename EXPOSURE overrides FITS EXPTIME (different raw keys) |
| #15 | `test_xisf_filename_override_takes_precedence` | Same as above for XISF files |
| #15 | `test_xisf_filename_override_with_different_raw_keys` | Same as above for XISF with different raw keys |
| #13 | `test_light_filename_without_focal_ratio` | normalize_filename handles missing focal_ratio |
| #13 | `test_enrich_with_missing_profile_keys_and_print_status` | enrich_metadata handles missing profile keys |
| n/a | `test_date_obs_in_filename_normalized_correctly` | DATE-OBS in filename produces correct date, not "OBS" |
| n/a | `test_numeric_string_comparison_matches_different_decimal_representation` | '2032' matches '2032.0' in filter_metadata |
| n/a | `test_xisf_date_from_path_overrides_date_obs_from_header` | DATE from path overrides DATE-OBS from XISF header |

## Coverage Goals

**Target:** 80%+ line coverage

**Philosophy:** Coverage measures completeness, not quality. A test that
executes code without meaningful assertions provides no value. Focus on:

- Testing behavior, not implementation details
- Covering edge cases and error conditions
- Ensuring assertions verify expected outcomes

## Running Tests

```bash
# Run all tests
make test

# Run with coverage
make coverage

# Run specific test
pytest tests/test_module.py::TestClass::test_function
```

## Test Data

Test data is:

- Generated programmatically in fixtures where possible
- Created using `tmp_path` pytest fixture for filesystem isolation
- FITS/XISF file I/O is mocked using `unittest.mock` to avoid requiring real astronomical data files
- Real XISF files are created via `numpy` + `xisf.XISF.write()` only for `update_xisf_headers` tests

**No Git LFS** - all test data must be small (< 100KB) or generated.

## Maintenance

When modifying this project:

1. **Adding features**: Add tests for new functionality after implementation
2. **Fixing bugs**: Follow TDD protocol above (test first, then fix)
3. **Refactoring**: Existing tests should pass without modification (behavior unchanged)
4. **Removing features**: Remove associated tests

## Changelog

| Date | Change | Rationale |
|------|--------|-----------|
| 2026-02-15 | Initial test plan | Document existing testing strategy |
