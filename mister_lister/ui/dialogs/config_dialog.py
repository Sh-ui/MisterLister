"""
Configuration dialog for MisterLister.
Provides user-configurable options through modular groups.
"""

from mister_lister.qt import (
    QDialog, QVBoxLayout, QHBoxLayout, QPushButton, QCheckBox
)
from mister_lister.constants import WHITE, NORMAL_TAN, HOVER_TAN, LIGHT_BLUE, DARKER_TAN
from mister_lister.utils.config import Config
from .config_groups import (
    PrintConfigGroup, FileConfigGroup,
    FormatConfigGroup, StartupConfigGroup
)

class ConfigDialog(QDialog):
    """
    Dialog for application configuration.
    Uses modular groups for different configuration categories.
    """
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Configuration")
        self.config = parent.config if parent else Config()
        
        # Set dialog styling
        self.setStyleSheet(self._get_stylesheet())
        
        # Main layout
        self.layout = QVBoxLayout(self)
        self.layout.setSpacing(12)
        self.layout.setContentsMargins(15, 15, 15, 15)
        
        # Create config groups
        self.format_group = FormatConfigGroup("format", self.config)
        self.print_group = PrintConfigGroup("print", self.config)
        self.file_group = FileConfigGroup("files", self.config)
        self.startup_group = StartupConfigGroup("startup", self.config)
        
        # Add groups to layout
        self.layout.addWidget(self.format_group)
        self.layout.addWidget(self.print_group)
        self.layout.addWidget(self.file_group)
        self.layout.addWidget(self.startup_group)
        
        # Add save/cancel buttons
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        
        self.save_btn = QPushButton("Save")
        self.save_btn.clicked.connect(self.save_and_close)
        button_layout.addWidget(self.save_btn)
        
        self.cancel_btn = QPushButton("Cancel")
        self.cancel_btn.clicked.connect(self.reject)
        button_layout.addWidget(self.cancel_btn)
        
        self.layout.addLayout(button_layout)
        
        # Set minimum width to prevent text cutoff
        self.setMinimumWidth(400)

    def _get_stylesheet(self):
        """Get consistent dialog styling"""
        return f"""
            QDialog {{
                background-color: {WHITE};
            }}
            QPushButton {{
                background-color: {NORMAL_TAN};
                border: none;
                border-radius: 15px;
                padding: 8px 16px;
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
                font-size: 14px;
            }}
            QGroupBox {{
                font-family: 'Asap';
                font-weight: bold;
                color: {DARKER_TAN};
                margin-top: 0px;     /* No space before section */
                padding-top: 20px;   /* Space for title */
                border: none;
            }}
            QGroupBox::title {{
                subcontrol-origin: margin;
                subcontrol-position: top left;
                padding: 0 10px;
                background-color: {WHITE};
            }}
            QLineEdit {{
                border: 1px solid {NORMAL_TAN};
                border-radius: 4px;
                padding: 4px 8px;
                color: {DARKER_TAN};
                font-family: 'Asap';
                background: {WHITE};
            }}
            QLineEdit:focus {{
                border-color: {LIGHT_BLUE};
            }}
            QComboBox {{
                border: 1px solid {NORMAL_TAN};
                border-radius: 4px;
                padding: 4px 8px;
                color: {DARKER_TAN};
                font-family: 'Asap';
                background: {WHITE};
            }}
            QComboBox:hover {{
                border-color: {HOVER_TAN};
            }}
            QComboBox::drop-down {{
                border: none;
            }}
            QSpinBox, QDoubleSpinBox {{
                border: 1px solid {NORMAL_TAN};
                border-radius: 4px;
                padding: 4px 8px;
                color: {DARKER_TAN};
                font-family: 'Asap';
                background: {WHITE};
            }}
            QSpinBox::up-button, QDoubleSpinBox::up-button {{
                subcontrol-origin: margin;
                subcontrol-position: center right;
                width: 20px;
                border: none;
                background: transparent;
                margin-right: 3px;
            }}
            QSpinBox::down-button, QDoubleSpinBox::down-button {{
                subcontrol-origin: margin;
                subcontrol-position: center left;
                width: 20px;
                border: none;
                background: transparent;
                margin-left: 3px;
            }}
            QSpinBox::up-button:hover, QDoubleSpinBox::up-button:hover,
            QSpinBox::down-button:hover, QDoubleSpinBox::down-button:hover {{
                background: {HOVER_TAN};
                border-radius: 2px;
            }}
            QSpinBox::up-button:pressed, QDoubleSpinBox::up-button:pressed,
            QSpinBox::down-button:pressed, QDoubleSpinBox::down-button:pressed {{
                background: {LIGHT_BLUE};
                border-radius: 2px;
            }}
            QCheckBox {{
                color: {DARKER_TAN};
                font-family: 'Asap';
                spacing: 8px;
            }}
            QCheckBox::indicator {{
                width: 18px;
                height: 18px;
                border: 1px solid {NORMAL_TAN};
                border-radius: 3px;
                background: {WHITE};
            }}
            QCheckBox::indicator:checked {{
                background: {LIGHT_BLUE};
                border-color: {LIGHT_BLUE};
            }}
            QSlider::groove:horizontal {{
                border: 1px solid {NORMAL_TAN};
                height: 6px;
                background: {WHITE};
                border-radius: 3px;
            }}
            QSlider::handle:horizontal {{
                background: {DARKER_TAN};
                border: none;
                width: 18px;
                height: 18px;
                margin: -6px 0;
                border-radius: 9px;
            }}
            QSlider::handle:horizontal:hover {{
                background: {HOVER_TAN};
            }}
        """

    def save_and_close(self):
        """Save all configuration values and close"""
        self.format_group.save_config()
        self.print_group.save_config()
        self.file_group.save_config()
        self.startup_group.save_config()
        self.accept() 