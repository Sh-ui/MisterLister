"""
Custom button implementations for MisterLister.
Provides circular buttons with state-aware icons and styling.
"""

from mister_lister.qt import (
    QPushButton, QIcon, QSize, Qt
)
from mister_lister.constants import (
    NORMAL_TAN, HOVER_TAN, LIGHT_BLUE, 
    DARKER_TAN, INACTIVE_TAN, WHITE
)
from pytablericons import TablerIcons, OutlineIcon, FilledIcon

class CircleButton(QPushButton):
    """
    Circular button with icon that changes appearance based on state.
    
    Features:
    - Interactive/non-interactive states with distinct styling
    - In-use state with filled/outline icon switching
    - Hover and press effects when interactive
    - Custom color scheme that overrides Qt defaults
    """
    
    def __init__(self, icon_type="", parent=None):
        """
        Initialize button with specified icon type.
        
        Args:
            icon_type: TablerIcons icon type (OutlineIcon or FilledIcon)
            parent: Parent widget
        """
        super().__init__(parent)
        self.setFixedSize(60, 60)
        
        self._interactive = False
        self._in_use = False
        self._base_icon_type = icon_type
        
        self.update_style()

    @property
    def interactive(self):
        """Whether button responds to user interaction"""
        return self._interactive

    @interactive.setter
    def interactive(self, value):
        if self._interactive != value:
            self._interactive = value
            self.update_style()

    @property
    def in_use(self):
        """Whether button is currently in use (affects icon style)"""
        return self._in_use

    @in_use.setter
    def in_use(self, value):
        if self._in_use != value:
            self._in_use = value
            self.update_style()

    def get_icon_type(self):
        """
        Get current icon type based on in_use state.
        Falls back to outline version if filled version unavailable.
        """
        if self._in_use:
            try:
                return getattr(FilledIcon, self._base_icon_type.name)
            except AttributeError:
                print(f"Warning: No filled icon found for {self._base_icon_type.name}, using outline version")
                return self._base_icon_type
        return self._base_icon_type

    def update_icon(self, color):
        """
        Update button icon with specified color.
        Handles hover states and icon type switching.
        """
        if self._base_icon_type:
            current_icon_type = self.get_icon_type()
            
            # Override color with WHITE if button is both interactive and being hovered
            if self.underMouse() and self._interactive:
                color = WHITE
            
            icon = TablerIcons.load(
                current_icon_type,
                size=32,
                color=color,
                stroke_width=1.5
            )
            self.setIcon(QIcon(icon.toqpixmap()))
            self.setIconSize(QSize(32, 32))

    def update_style(self):
        """
        Update button appearance based on current state.
        Handles both interactive and non-interactive styling.
        """
        base_color = DARKER_TAN if self._interactive else INACTIVE_TAN
        self.update_icon(base_color)
        
        if self._interactive:
            self.setStyleSheet(f"""
                QPushButton {{
                    background: transparent;
                    border: none;
                    border-radius: 30px;
                }}
                QPushButton:hover {{
                    background: {HOVER_TAN};
                }}
                QPushButton:pressed {{
                    background: {LIGHT_BLUE};
                }}
                QPushButton:disabled {{
                    background: transparent;
                }}
            """)
            self.setCursor(Qt.CursorShape.PointingHandCursor)
        else:
            self.setStyleSheet(f"""
                QPushButton {{
                    background: transparent;
                    border: none;
                    border-radius: 30px;
                }}
                QPushButton:disabled {{
                    background: transparent;
                }}
            """)
            self.setCursor(Qt.CursorShape.ArrowCursor)

    def enterEvent(self, event):
        """Update icon color on mouse enter"""
        super().enterEvent(event)
        if self._interactive:
            self.update_icon(WHITE)

    def leaveEvent(self, event):
        """Restore normal icon color on mouse leave"""
        super().leaveEvent(event)
        base_color = DARKER_TAN if self._interactive else INACTIVE_TAN
        self.update_icon(base_color)

    def mousePressEvent(self, event):
        """Handle icon color change on mouse press"""
        super().mousePressEvent(event)
        if self._interactive:
            self.update_icon(WHITE)

    # Legacy support
    def set_interactive(self, enabled):
        """Legacy method for backward compatibility"""
        self.interactive = enabled 

class SmallIconButton(CircleButton):
    """
    Smaller version of CircleButton for use in configuration dialogs.
    Inherits core functionality but adjusts size and styling.
    """
    
    def __init__(self, icon_type="", parent=None):
        super().__init__(icon_type, parent)
        self.setFixedSize(24, 24)  # Smaller size
        
    def update_style(self):
        """Update button appearance based on current state"""
        base_color = DARKER_TAN if self._interactive else INACTIVE_TAN
        self.update_icon(base_color)
        
        # Always use circular styling for both states
        if self._interactive:
            self.setStyleSheet(f"""
                QPushButton {{
                    background: transparent;
                    border: none;
                    border-radius: 12px;
                }}
                QPushButton:hover {{
                    background: {HOVER_TAN};
                }}
                QPushButton:pressed {{
                    background: {LIGHT_BLUE};
                }}
            """)
            self.setCursor(Qt.CursorShape.PointingHandCursor)
        else:
            self.setStyleSheet(f"""
                QPushButton {{
                    background: transparent;
                    border: none;
                    border-radius: 12px;
                }}
                QPushButton:disabled {{
                    color: {INACTIVE_TAN};
                    background: transparent;
                }}
            """)
            self.setCursor(Qt.CursorShape.ArrowCursor)

    def update_icon(self, color):
        """Update button icon with specified color"""
        if self._base_icon_type:
            current_icon_type = self.get_icon_type()
            
            if self.underMouse() and self._interactive:
                color = WHITE
            
            icon = TablerIcons.load(
                current_icon_type,
                size=16,  # Smaller icon
                color=color,
                stroke_width=1.5
            )
            self.setIcon(QIcon(icon.toqpixmap()))
            self.setIconSize(QSize(16, 16))  # Smaller icon size 