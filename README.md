# ap-common

[![Test](https://github.com/jewzaam/ap-common/workflows/Test/badge.svg)](https://github.com/jewzaam/ap-common/actions/workflows/test.yml) [![Coverage](https://github.com/jewzaam/ap-common/workflows/Coverage%20Check/badge.svg)](https://github.com/jewzaam/ap-common/actions/workflows/coverage.yml) [![Lint](https://github.com/jewzaam/ap-common/workflows/Lint/badge.svg)](https://github.com/jewzaam/ap-common/actions/workflows/lint.yml) [![Format](https://github.com/jewzaam/ap-common/workflows/Format%20Check/badge.svg)](https://github.com/jewzaam/ap-common/actions/workflows/format.yml) [![Type Check](https://github.com/jewzaam/ap-common/workflows/Type%20Check/badge.svg)](https://github.com/jewzaam/ap-common/actions/workflows/typecheck.yml)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/) [![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

Shared functionality package for astrophotography tools. Provides common utilities for FITS/XISF header reading, metadata normalization, file operations, calibration frame matching, and metadata extraction/filtering.

## Overview

This package extracts reusable functionality from astrophotography tools into a single installable package that can be shared across multiple projects. It provides:

- **FITS/XISF Header Reading**: Extract, parse, and update headers from FITS and XISF files
- **Header Normalization**: Standardize header names and values across different formats
- **Metadata Extraction**: Load and enrich metadata from files and filenames
- **Calibration Frame Matching**: Find matching darks, flats, and bias frames by metadata criteria
- **File Operations**: Move, copy, and manage files with directory creation
- **Progress & Logging**: Consistent progress bars and logging configuration for CLI tools
- **Shared Constants**: Centralized FITS header names, image types, and file patterns
- **Utility Functions**: Environment variable replacement, path resolution, string conversion, file finding

## Documentation

This tool is part of the astrophotography pipeline. For comprehensive documentation including workflow guides and integration with other tools, see:

- **[Pipeline Overview](https://github.com/jewzaam/ap-base/blob/main/docs/index.md)** - Full pipeline documentation
- **[Workflow Guide](https://github.com/jewzaam/ap-base/blob/main/docs/workflow.md)** - Detailed workflow with diagrams
- **[ap-common Reference](https://github.com/jewzaam/ap-base/blob/main/docs/tools/ap-common.md)** - API reference for this tool

## Installation

### Local Development (Editable Install)

```powershell
# In ap-common directory
pip install -e .
```

### Local Package Install

```powershell
# Build and install from local directory
cd ap-common
pip install .
```

### From Local Path (in other projects)

```toml
# In other project's pyproject.toml dependencies:
dependencies = [
    "ap-common @ file:///path/to/ap-common",
]
```

### From Git Repository

```toml
dependencies = [
    "ap-common @ git+https://github.com/yourusername/ap-common.git",
]
```

## Package Structure

```
ap_common/
├── __init__.py          # Package exports
├── calibration.py       # Calibration frame matching (darks, flats, bias)
├── constants.py         # Shared constants for headers, types, and file extensions
├── filesystem.py        # File operations (move, copy, delete_empty_dirs)
├── fits.py              # FITS/XISF header reading and writing
├── logging_config.py    # Logging setup and logger retrieval
├── metadata.py          # Metadata extraction and filtering
├── normalization.py     # Header normalization functions and data
├── progress.py          # Progress bar utilities for CLI tools
└── utils.py             # Utility functions
```

## Usage

### Basic Example

```python
from ap_common.fits import get_fits_headers
from ap_common.normalization import normalize_headers
from ap_common.metadata import get_filtered_metadata

# Read FITS headers
headers = get_fits_headers("image.fits", profileFromPath=True)

# Get filtered metadata
metadata = get_filtered_metadata(
    dirs=["/path/to/images"],
    filters={"type": "LIGHT", "camera": "DWARFIII"},
    profileFromPath=True
)
```

### Available Functions

#### FITS Header Reading (`ap_common.fits`)
- `get_fits_headers()` - Extract headers from FITS files
- `get_xisf_headers()` - Extract headers from XISF files
- `get_file_headers()` - Extract headers from filenames
- `update_xisf_headers()` - Update FITS keywords in XISF files

#### Normalization (`ap_common.normalization`)
- `normalize_headers()` - Normalize a dictionary of headers
- `normalize_date()` - Normalize date strings
- `normalize_datetime()` - Normalize datetime strings
- `normalize_filterName()` - Normalize filter names
- `normalize_target_name()` - Extract target and panel from target name
- `normalize_filename()` - Construct normalized filenames from headers
- `denormalize_header()` - Convert normalized header name back to FITS form
- `FILTER_NORMALIZATION_DATA` - Normalization mapping dictionary
- `CONSTANT_NORMALIZATION_DATA` - Constant value mappings

#### Filesystem (`ap_common.filesystem`)
- `move_file()` - Move files with directory creation
- `copy_file()` - Copy files with directory creation
- `delete_empty_directories()` - Recursively delete empty directories

#### Metadata (`ap_common.metadata`)
- `get_metadata()` - Load metadata for files in directories
- `enrich_metadata()` - Enrich metadata by reading file headers
- `get_filtered_metadata()` - Load and filter metadata
- `filter_metadata()` - Filter metadata dictionary by criteria
- `group_by_directory()` - Group metadata entries by parent directory
- `get_directories_with_lights()` - Find directories containing LIGHT frames

#### Calibration Matching (`ap_common.calibration`)
- `find_matching_darks()` - Find dark frames matching reference metadata
- `find_matching_flats()` - Find flat frames matching reference metadata
- `find_matching_bias()` - Find bias frames matching reference metadata
- `find_matching_darks_from_cache()` - Find matching darks from pre-loaded metadata
- `find_matching_flats_from_cache()` - Find matching flats from pre-loaded metadata
- `find_matching_bias_from_cache()` - Find matching bias from pre-loaded metadata

#### Utilities (`ap_common.utils`)
- `replace_env_vars()` - Replace environment variable placeholders
- `resolve_path()` - Resolve path with env vars, home expansion, and absolute conversion
- `camelCase()` - Convert strings to camelCase
- `get_filenames()` - Find files matching patterns

#### Progress (`ap_common.progress`)
- `progress_iter()` - Wrap an iterable with a progress bar
- `ProgressTracker` - Flexible progress tracker with dynamic status updates

#### Logging (`ap_common.logging_config`)
- `setup_logging()` - Configure and return a logger instance
- `get_logger()` - Get or create a logger by name

#### Constants (`ap_common.constants`)
- `DIRECTORY_ACCEPT` - Canonical "accept" directory name
- `HEADER_*` - Standard FITS header key constants (DATE_OBS, IMAGETYP, TELESCOP, etc.)
- `NORMALIZED_HEADER_*` - Normalized header name constants (date, type, camera, etc.)
- `TYPE_LIGHT`, `TYPE_DARK`, `TYPE_FLAT`, `TYPE_BIAS` - Raw frame type constants
- `TYPE_MASTER_LIGHT`, `TYPE_MASTER_DARK`, `TYPE_MASTER_FLAT`, `TYPE_MASTER_BIAS` - Master frame type constants
- `CALIBRATION_TYPES`, `MASTER_CALIBRATION_TYPES`, `ALL_CALIBRATION_TYPES` - Type lists
- `FILE_EXTENSION_*` - File extension constants
- `DEFAULT_*_PATTERN` - Default file matching patterns

## Dependencies

- `astropy` - For FITS file reading
- `tqdm` - For progress bar display
- `xisf==0.9.5` - For XISF file reading

## Project-Specific Configuration

Some functions accept project-specific parameters:

- `directory_accept` - The "accept" directory name (defaults to "accept")
- Date format overrides in normalization functions

Projects should pass their specific constants when calling these functions.

## Benefits

- ✅ Single source of truth for common functionality
- ✅ Easy to update - fix once, all tools benefit
- ✅ Version control - can pin specific versions
- ✅ Clean separation of concerns
- ✅ Easier testing of shared code
- ✅ Can publish to PyPI if desired
