"""
Constants and configuration values for MisterLister.
"""

# UI Colors
WINDOW_BG = "#F3F3F3"      # Windows native gray
INACTIVE_TAN = "#DECDB2"   # Inactive button icon color
DARKER_TAN = "#A69276"     # Active button icon color / Bottom bar border
NORMAL_TAN = "#EEDEC8"     # Standard tan color used throughout UI
HOVER_TAN = "#C4B393"      # Button background on hover
LIGHT_BLUE = "#4A90E2"     # Button background on click / Selection color
WHITE = "#FFFFFF"          # Icon color on hover/click

# Default Values
DEFAULT_FONT_SIZE = 12
DEFAULT_ROW_SPACING = 30
MIN_WINDOW_WIDTH = 800
MIN_WINDOW_HEIGHT = 600

# Default layout settings
DEFAULT_MARGIN = 0.5
DEFAULT_BORDER_STYLE = 'solid'
DEFAULT_BORDER_GRAY = 128

# Default behavior settings
DEFAULT_REMEMBER_DIR = True
DEFAULT_REMEMBER_LAYOUT = False
DEFAULT_SHOW_DIALOG = False

__all__ = [
    'WINDOW_BG', 'INACTIVE_TAN', 'DARKER_TAN',
    'NORMAL_TAN', 'HOVER_TAN', 'LIGHT_BLUE', 'WHITE',
    'DEFAULT_FONT_SIZE', 'DEFAULT_ROW_SPACING',
    'MIN_WINDOW_WIDTH', 'MIN_WINDOW_HEIGHT',
    'DEFAULT_MARGIN', 'DEFAULT_BORDER_STYLE', 'DEFAULT_BORDER_GRAY',
    'DEFAULT_REMEMBER_DIR', 'DEFAULT_REMEMBER_LAYOUT', 'DEFAULT_SHOW_DIALOG'
] 