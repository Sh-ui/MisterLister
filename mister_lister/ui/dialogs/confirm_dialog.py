"""
Confirmation dialog for MisterLister.
Used for confirming potentially destructive actions.
"""

from mister_lister.qt import (
    QDialog, QVBoxLayout, QHBoxLayout, 
    QLabel, QPushButton, Qt, QWidget
)
from mister_lister.constants import (
    WHITE, NORMAL_TAN, HOVER_TAN, 
    LIGHT_BLUE, DARKER_TAN
)

class ConfirmDialog(QDialog):
    """
    Dialog for confirming table clearing operation.
    Provides clear visual feedback and requires explicit confirmation.
    """
    
    def __init__(self, parent=None):
        """Initialize confirmation dialog"""
        super().__init__(parent)
        self.setWindowTitle("Clear Table?")
        
        # Set dialog styling
        self.setStyleSheet(f"""
            QDialog {{
                background-color: {WHITE};
            }}
            QPushButton {{
                background-color: {NORMAL_TAN};
                border: none;
                border-radius: 15px;
                padding: 8px 16px;
                min-width: 120px;
                color: {DARKER_TAN};
                font-family: 'Asap';
                font-weight: bold;
                font-size: 13px;
            }}
            QPushButton:hover {{
                background-color: {HOVER_TAN};
                color: {WHITE};
            }}
            QPushButton:pressed {{
                background-color: {LIGHT_BLUE};
                color: {WHITE};
            }}
            QLabel {{
                color: {DARKER_TAN};
                font-family: 'Asap';
                font-weight: 500;
                font-size: 14px;
            }}
        """)
        
        # Main layout
        layout = QVBoxLayout(self)
        layout.setSpacing(15)  # Reduced spacing
        layout.setContentsMargins(15, 15, 15, 15)  # Tighter margins
        
        # Message
        message = QLabel("🗑 are you sure you want to\nclear these filenames?")
        message.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(message)
        
        # Create a container widget for the buttons
        button_container = QWidget()
        button_layout = QHBoxLayout(button_container)
        button_layout.setSpacing(15)  # Space between buttons
        button_layout.setContentsMargins(0, 0, 0, 0)
        
        yes_btn = QPushButton("YES clear 'em!")
        no_btn = QPushButton("NO leave 'em!")
        
        # Center the buttons
        button_layout.addStretch(1)
        button_layout.addWidget(yes_btn)
        button_layout.addWidget(no_btn)
        button_layout.addStretch(1)
        
        # Add the button container to main layout
        layout.addWidget(button_container)
        
        # Connect buttons
        yes_btn.clicked.connect(self.accept)
        no_btn.clicked.connect(self.reject)
        
        # Set fixed size - tighter now
        self.setFixedSize(350, 140)
        