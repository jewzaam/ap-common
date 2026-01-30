"""
Constants for headers and directories used across ap-common tools.

This module centralizes all constants that are peppered throughout
related projects, making them easier to maintain and use consistently.

Generated to address GitHub Issue #9.
"""

# =============================================================================
# Directory Constants
# =============================================================================

# The canonical "accept" directory in file paths
# Used to identify where OBJECT names should be extracted from parent directory
DIRECTORY_ACCEPT = "accept"

# Directory suffix for stashed/excluded files
DIRECTORY_STASH = "_stash"

# =============================================================================
# FITS Header Constants - Standard Keys
# =============================================================================

# Date and time headers
HEADER_DATE_OBS = "DATE-OBS"

# Image type header
HEADER_IMAGETYP = "IMAGETYP"

# Telescope/Optic header
HEADER_TELESCOP = "TELESCOP"

# Focal ratio header
HEADER_FOCRATIO = "FOCRATIO"

# Camera/Instrument header
HEADER_INSTRUME = "INSTRUME"

# Object/Target header
HEADER_OBJECT = "OBJECT"

# Filter header
HEADER_FILTER = "FILTER"

# Exposure time headers (multiple alternatives)
HEADER_EXPOSURE = "EXPOSURE"
HEADER_EXPTIME = "EXPTIME"
HEADER_EXP = "EXP"

# Temperature headers
HEADER_CCD_TEMP = "CCD-TEMP"
HEADER_SETTEMP = "SETTEMP"
HEADER_SET_TEMP = "SET-TEMP"

# Location headers
HEADER_SITELAT = "SITELAT"
HEADER_SITELONG = "SITELONG"
HEADER_OBSGEO_B = "OBSGEO-B"
HEADER_OBSGEO_L = "OBSGEO-L"

# Readout mode header
HEADER_READOUTM = "READOUTM"

# =============================================================================
# Normalized Header Names (internal use)
# =============================================================================

NORM_DATE = "date"
NORM_DATETIME = "datetime"
NORM_TYPE = "type"
NORM_OPTIC = "optic"
NORM_FOCAL_RATIO = "focal_ratio"
NORM_CAMERA = "camera"
NORM_TARGETNAME = "targetname"
NORM_FILTER = "filter"
NORM_EXPOSURESECONDS = "exposureseconds"
NORM_TEMP = "temp"
NORM_SETTEMP = "settemp"
NORM_LATITUDE = "latitude"
NORM_LONGITUDE = "longitude"
NORM_READOUTMODE = "readoutmode"
NORM_PANEL = "panel"
NORM_FILENAME = "filename"
NORM_HFR = "hfr"
NORM_STARS = "stars"
NORM_RMSAC = "rmsac"

# =============================================================================
# Image Type Constants
# =============================================================================

TYPE_LIGHT = "LIGHT"
TYPE_DARK = "DARK"
TYPE_FLAT = "FLAT"
TYPE_BIAS = "BIAS"

# Calibration frame types (for grouping purposes)
CALIBRATION_TYPES = [TYPE_DARK, TYPE_FLAT, TYPE_BIAS]

# =============================================================================
# File Extension Constants
# =============================================================================

EXT_FITS = ".fits"
EXT_XISF = ".xisf"
EXT_CR2 = ".cr2"

# Default file patterns
DEFAULT_FITS_PATTERN = r".*\.fits$"
DEFAULT_XISF_PATTERN = r".*\.xisf$"
DEFAULT_CR2_PATTERN = r".*\.cr2$"
DEFAULT_IMAGE_PATTERNS = [DEFAULT_FITS_PATTERN]

# =============================================================================
# Filter Name Constants
# =============================================================================

# Filter name mappings for normalization
FILTER_BAADER_UVIR = "BaaderUVIRCut"
FILTER_BAADER_UVIR_SHORT = "UVIR"
FILTER_OPTOLONG_LEXTREME = "OptolongLeXtreme"
FILTER_OPTOLONG_LEXTREME_SHORT = "LeXtr"
FILTER_S2 = "S2"
FILTER_S2_SHORT = "S"
FILTER_HA = "Ha"
FILTER_HA_SHORT = "H"
FILTER_O3 = "O3"
FILTER_O3_SHORT = "O"
FILTER_RGB = "RGB"
FILTER_ASTRO = "Astro"
FILTER_DUO_BAND = "Duo-Band"
