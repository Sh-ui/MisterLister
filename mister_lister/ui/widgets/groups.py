"""
Button grouping widgets for MisterLister.
Provides labeled containers for organizing related buttons with consistent styling.
"""

from mister_lister.qt import (
    QWidget, QVBoxLayout, QHBoxLayout, 
    QLabel, Qt
)
from mister_lister.constants import INACTIVE_TAN, DARKER_TAN

class ButtonGroup(QWidget):
    """
    Groups related buttons together with a descriptive label.
    
    Features:
    - Vertical layout with buttons above label
    - Consistent spacing and margins
    - Active/inactive state affects label color
    - Transparent background to blend with bottom bar
    """
    
    def __init__(self, label, parent=None):
        """
        Initialize button group with label.
        
        Args:
            label (str): Text to display below buttons
            parent: Parent widget
        """
        super().__init__(parent)
        self.setStyleSheet("""
            QWidget {
                border: none;
                background: transparent;
            }
        """)
        
        # Main vertical layout
        layout = QVBoxLayout(self)
        layout.setSpacing(2)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Container for buttons with horizontal layout
        self.buttons_widget = QWidget()
        self.buttons_widget.setStyleSheet("border: none;")
        buttons_layout = QHBoxLayout(self.buttons_widget)
        buttons_layout.setSpacing(5)
        buttons_layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.buttons_widget)
        
        # Label below buttons
        self.label_widget = QLabel(label)
        self.label_widget.setStyleSheet(f"""
            QLabel {{
                color: {INACTIVE_TAN};
                font-family: 'Asap';
                font-weight: bold;  
                font-size: 14px;    
                margin-top: 0px;
                border: none;
            }}
        """)
        self.label_widget.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.label_widget)
        
        # Expose buttons layout for adding buttons
        self.layout = buttons_layout

    def set_active(self, active):
        """
        Set the active state of the group.
        
        Args:
            active (bool): True to use active color, False for inactive
        
        The active state changes the label color to provide visual feedback
        about which button groups are currently usable.
        """
        color = DARKER_TAN if active else INACTIVE_TAN
        self.label_widget.setStyleSheet(f"""
            QLabel {{
                color: {color};
                font-family: 'Asap';
                font-weight: bold;  
                font-size: 14px;    
                margin-top: 0px;
                border: none;
            }}
        """) 