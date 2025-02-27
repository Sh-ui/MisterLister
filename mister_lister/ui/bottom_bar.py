"""
Bottom bar component containing application controls.
"""

from mister_lister.qt import (
    QFrame, QHBoxLayout, QWidget
)
from mister_lister.constants import (
    NORMAL_TAN, DARKER_TAN, INACTIVE_TAN, 
    HOVER_TAN, LIGHT_BLUE
)
from mister_lister.ui.widgets.buttons import CircleButton
from mister_lister.ui.widgets.groups import ButtonGroup
from pytablericons import OutlineIcon

class BottomBar(QFrame):
    """
    Bottom bar containing all application control buttons.
    Organized into labeled groups with consistent styling.
    """
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet(f"""
            QFrame {{
                background-color: {NORMAL_TAN};
                border-top: 1px solid {DARKER_TAN};
            }}
            QWidget {{
                border: none;
            }}
        """)
        self.setFixedHeight(100)
        
        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(20, 5, 20, 5)
        
        # Initialize buttons with consistent naming and initial states
        self.add_files_btn = CircleButton(OutlineIcon.FOLDER)
        self.add_files_btn.interactive = True  # Should be interactive by default
        
        self.font_minus_btn = CircleButton(OutlineIcon.MINUS)
        self.font_plus_btn = CircleButton(OutlineIcon.PLUS)
        self.spacing_minus_btn = CircleButton(OutlineIcon.MINUS)
        self.spacing_plus_btn = CircleButton(OutlineIcon.PLUS)
        self.preview_btn = CircleButton(OutlineIcon.EYE)
        self.print_btn = CircleButton(OutlineIcon.PRINTER)
        self.clear_btn = CircleButton(OutlineIcon.TRASH)
        self.config_btn = CircleButton(OutlineIcon.SETTINGS)
        
        # Add Files Group
        self.add_files_group = ButtonGroup("add files")
        self.add_files_group.layout.addWidget(self.add_files_btn)
        
        # Font Size Group
        self.font_group = ButtonGroup("font size")
        self.font_group.layout.addWidget(self.font_minus_btn)
        self.font_group.layout.addWidget(self.font_plus_btn)
        
        # Spacing Group
        self.spacing_group = ButtonGroup("row height")
        self.spacing_group.layout.addWidget(self.spacing_minus_btn)
        self.spacing_group.layout.addWidget(self.spacing_plus_btn)
        
        # Action Buttons Group
        self.actions_group = ButtonGroup("actions")
        self.actions_group.layout.addWidget(self.preview_btn)
        self.actions_group.layout.addWidget(self.print_btn)
        self.actions_group.layout.addWidget(self.clear_btn)

        # Config Group (separate, on far right)
        self.config_group = ButtonGroup("config")
        self.config_group.layout.addWidget(self.config_btn)
        
        # Add all groups to main layout
        main_layout.addWidget(self.add_files_group)
        main_layout.addStretch(1)
        main_layout.addWidget(self.font_group)
        main_layout.addStretch(1)
        main_layout.addWidget(self.spacing_group)
        main_layout.addStretch(1)
        main_layout.addWidget(self.actions_group)
        main_layout.addStretch(1)
        main_layout.addWidget(self.config_group)
        
        # Set tooltips with consistent naming
        self.add_files_btn.setToolTip("Add Files")
        self.font_minus_btn.setToolTip("Decrease Font Size")
        self.font_plus_btn.setToolTip("Increase Font Size")
        self.spacing_minus_btn.setToolTip("Decrease Row Height")
        self.spacing_plus_btn.setToolTip("Increase Row Height")
        self.preview_btn.setToolTip("Preview Print")
        self.print_btn.setToolTip("Print Filenames")
        self.clear_btn.setToolTip("Clear Filenames")
        self.config_btn.setToolTip("Configuration")
        
        # Set initial active states
        self.add_files_group.set_active(True)
        self.config_group.set_active(True)
        
        # Initially disable controls except add_files_btn and config_btn
        self.set_controls_enabled(False)
        self.config_btn.set_interactive(True)

    def set_controls_enabled(self, enabled):
        """Enable or disable control buttons and their groups"""
        # Update group states
        self.font_group.set_active(enabled)
        self.spacing_group.set_active(enabled)
        self.actions_group.set_active(enabled)
        
        # Make sure add_files_btn stays interactive and properly styled
        self.add_files_btn.interactive = True
        self.add_files_btn.in_use = False  # Reset in_use state when disabling
        self.add_files_btn.update_style()
        
        # Update all other buttons
        for btn in [self.font_minus_btn, self.font_plus_btn, 
                   self.spacing_minus_btn, self.spacing_plus_btn,
                   self.preview_btn, self.print_btn,
                   self.clear_btn]:
            btn.interactive = enabled
            btn.in_use = False  # Reset in_use state when disabling
            btn.update_style()
            
    def set_add_files_icon_state(self, has_files):
        """Update add files button icon based on whether files are loaded"""
        self.add_files_btn.in_use = has_files
        self.add_files_btn.update_style()

    def _get_button_stylesheet(self, interactive=True):
        """Get consistent button styling"""
        return f"""
            QPushButton {{
                background-color: {INACTIVE_TAN if not interactive else NORMAL_TAN};
                border: none;
                border-radius: 15px;
                padding: 8px;
            }}
            QPushButton:hover {{
                background-color: {HOVER_TAN if interactive else INACTIVE_TAN};
            }}
            QPushButton:pressed {{
                background-color: {LIGHT_BLUE if interactive else INACTIVE_TAN};
            }}
        """ 