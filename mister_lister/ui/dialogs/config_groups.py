"""
Configuration dialog group components.
Provides modular, consistent configuration UI elements.
"""

from mister_lister.qt import (
    QGroupBox, QVBoxLayout, QHBoxLayout, QLabel,
    QCheckBox, QDoubleSpinBox, QLineEdit, QPushButton,
    QSlider, QButtonGroup, Qt, QFileDialog, QPrinter, QPrinterInfo, QComboBox, QSpinBox, QIntValidator
)
from mister_lister.constants import (
    WHITE, NORMAL_TAN, HOVER_TAN, LIGHT_BLUE, DARKER_TAN,
    DEFAULT_FONT_SIZE, DEFAULT_ROW_SPACING
)
from mister_lister.ui.widgets.buttons import SmallIconButton
from pytablericons import OutlineIcon
import os

class ConfigGroup(QGroupBox):
    """
    Base class for configuration groups.
    Provides common functionality and consistent styling.
    """
    
    def __init__(self, title, config, parent=None):
        super().__init__(title, parent)
        self.config = config
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(12, 4, 12, 12)  # Reduced padding
        self.layout.setSpacing(8)  # Reduced spacing
        self.setup_ui()
        
    def setup_ui(self):
        """Setup the group's UI elements"""
        raise NotImplementedError("Subclasses must implement setup_ui")
        
    def save_config(self):
        """Save the group's configuration values"""
        raise NotImplementedError("Subclasses must implement save_config")
        
    def load_config(self):
        """Load the group's configuration values"""
        raise NotImplementedError("Subclasses must implement load_config")

class PrintConfigGroup(ConfigGroup):
    """Configuration group for print settings"""
    
    def setup_ui(self):
        """Setup print configuration UI elements"""
        # Border style controls
        border_layout = QHBoxLayout()
        border_layout.addWidget(QLabel("border"))
        
        # Style buttons in a button group
        style_buttons = QHBoxLayout()
        self.solid_btn = QPushButton("―――")
        self.dashed_btn = QPushButton("- - -")
        self.dotted_btn = QPushButton("•••")
        
        # Create button group for mutual exclusion
        self.border_style_group = QButtonGroup(self)
        
        for i, btn in enumerate([self.solid_btn, self.dashed_btn, self.dotted_btn]):
            btn.setFixedWidth(50)
            btn.setFixedHeight(30)
            btn.setCheckable(True)
            self.border_style_group.addButton(btn, i)
            btn.setStyleSheet(f"""
                QPushButton {{
                    background-color: {WHITE};
                    border: 1px solid {NORMAL_TAN};
                    border-radius: 4px;
                    color: {DARKER_TAN};
                    font-size: 16px;
                }}
                QPushButton:checked {{
                    background-color: {LIGHT_BLUE};
                    border-color: {LIGHT_BLUE};
                    color: {WHITE};
                }}
            """)
            style_buttons.addWidget(btn)
        
        # Set current style
        current_style = self.config.get_str('print/border_style', 'solid')
        getattr(self, f"{current_style}_btn").setChecked(True)
        
        border_layout.addLayout(style_buttons)
        border_layout.addSpacing(20)
        
        # Border color slider and preview
        self.border_slider = QSlider(Qt.Orientation.Horizontal)
        self.border_slider.setRange(0, 255)
        self.border_slider.setValue(self.config.get_int('print/border_gray', 128))
        
        # Preview box
        self.border_preview = QLabel()
        self.border_preview.setFixedSize(30, 30)
        self.border_preview.setStyleSheet("""
            QLabel {
                border: 1px solid #888;
                border-radius: 4px;
            }
        """)
        
        border_layout.addWidget(self.border_slider)
        border_layout.addWidget(self.border_preview)
        self.layout.addLayout(border_layout)
        
        # Connect border style signals
        self.border_slider.valueChanged.connect(self.update_border_preview)
        for btn in [self.solid_btn, self.dashed_btn, self.dotted_btn]:
            btn.clicked.connect(self.update_border_preview)
        
        self.layout.addSpacing(10)
        
        # Printer selection
        printer_layout = QHBoxLayout()
        printer_layout.setSpacing(6)
        printer_label = QLabel("printer")
        self.printer_combo = QComboBox()
        self.printer_list = QPrinterInfo.availablePrinterNames()
        self.printer_combo.addItems(self.printer_list)
        current_printer = self.config.get_str('print/printer_name')
        if current_printer in self.printer_list:
            self.printer_combo.setCurrentText(current_printer)
        printer_layout.addWidget(printer_label)
        printer_layout.addWidget(self.printer_combo)
        self.layout.addLayout(printer_layout)
        
        # Initial preview update
        self.update_border_preview()
        
    def update_border_preview(self):
        """Update the border preview with current style and color"""
        gray = self.border_slider.value()
        style = 'solid'
        if self.dashed_btn.isChecked():
            style = 'dashed'
        elif self.dotted_btn.isChecked():
            style = 'dotted'
            
        self.border_preview.setStyleSheet(f"""
            QLabel {{
                background: {WHITE};
                border: 2px {style} rgb({gray}, {gray}, {gray});
                border-radius: 4px;
            }}
        """)
        
    def save_config(self):
        """Save print configuration"""
        style = 'solid'
        if self.dashed_btn.isChecked():
            style = 'dashed'
        elif self.dotted_btn.isChecked():
            style = 'dotted'
            
        self.config.set_value('print/border_style', style)
        self.config.set_value('print/border_gray', self.border_slider.value())
        self.config.set_value('print/printer_name', self.printer_combo.currentText())
        
    def load_config(self):
        """Load print configuration values"""
        self.printer_combo.setCurrentText(self.config.get_str('print/printer_name'))
        self.border_slider.setValue(self.config.get_int('print/border_gray', 128))

class FileConfigGroup(ConfigGroup):
    """File configuration group"""
    
    def setup_ui(self):
        """Setup the UI elements"""
        # Remember directory checkbox
        self.remember_dir = QCheckBox("remember last used directory")
        self.layout.addWidget(self.remember_dir)
        
        # Default directory with browse button
        default_layout = QHBoxLayout()
        default_label = QLabel("Default directory:")
        default_label.setStyleSheet("""
            QLabel {
                font-size: 12px;
                padding-right: 8px;
            }
        """)
        self.default_dir = QLineEdit()
        self.default_browse = SmallIconButton(OutlineIcon.FOLDER)
        self.default_browse.set_interactive(True)
        self.default_browse.clicked.connect(lambda: self.choose_directory('default'))
        
        default_layout.addWidget(default_label)
        default_layout.addWidget(self.default_dir)
        default_layout.addWidget(self.default_browse)
        self.layout.addLayout(default_layout)
        
        # Backup directory with browse button
        backup_layout = QHBoxLayout()
        backup_label = QLabel("Backup directory:")
        backup_label.setStyleSheet("""
            QLabel {
                font-size: 12px;
                padding-right: 8px;
            }
        """)
        self.backup_dir = QLineEdit()
        self.backup_browse = SmallIconButton(OutlineIcon.FOLDER)
        self.backup_browse.set_interactive(True)
        self.backup_browse.clicked.connect(lambda: self.choose_directory('backup'))
        
        backup_layout.addWidget(backup_label)
        backup_layout.addWidget(self.backup_dir)
        backup_layout.addWidget(self.backup_browse)
        self.layout.addLayout(backup_layout)
        
        self.layout.addStretch()
        
        # Load initial values
        self.load_config()
        
    def choose_directory(self, dir_type):
        """Open directory chooser dialog"""
        line_edit = self.default_dir if dir_type == 'default' else self.backup_dir
        current_dir = line_edit.text() or os.path.expanduser("~")
        
        directory = QFileDialog.getExistingDirectory(
            self,
            f"Choose {dir_type.title()} Directory",
            current_dir,
            QFileDialog.Option.ShowDirsOnly
        )
        
        if directory:
            line_edit.setText(directory)
            
    def save_config(self):
        """Save file configuration values"""
        self.config.set_value('files/remember_dir', self.remember_dir.isChecked())
        self.config.set_value('files/default_dir', self.default_dir.text())
        self.config.set_value('files/backup_dir', self.backup_dir.text())
        
    def load_config(self):
        """Load file configuration values"""
        self.remember_dir.setChecked(self.config.get_bool('files/remember_dir'))
        self.default_dir.setText(self.config.get_str('files/default_dir'))
        self.backup_dir.setText(self.config.get_str('files/backup_dir'))

class FormatConfigGroup(ConfigGroup):
    """Format-related configuration options"""
    
    def setup_ui(self):
        # Font size input with buttons
        font_layout = QHBoxLayout()
        font_layout.setSpacing(8)
        font_label = QLabel("font size")
        font_label.setFixedWidth(100)
        
        # Add minus button
        self.font_minus = SmallIconButton(OutlineIcon.MINUS)
        self.font_minus.set_interactive(True)
        self.font_minus.clicked.connect(lambda: self.adjust_value(self.font_size, -1))
        font_layout.addWidget(font_label)
        font_layout.addWidget(self.font_minus)
        
        # Font size input
        self.font_size = QLineEdit()
        self.font_size.setPlaceholderText(str(DEFAULT_FONT_SIZE))
        self.font_size.setFixedWidth(60)
        self.font_size.setValidator(QIntValidator(8, 72))
        font_layout.addWidget(self.font_size)
        
        # Add plus button
        self.font_plus = SmallIconButton(OutlineIcon.PLUS)
        self.font_plus.set_interactive(True)
        self.font_plus.clicked.connect(lambda: self.adjust_value(self.font_size, 1))
        font_layout.addWidget(self.font_plus)
        
        font_layout.addStretch()
        self.layout.addLayout(font_layout)
        
        # Row height input with buttons
        row_layout = QHBoxLayout()
        row_layout.setSpacing(8)
        row_label = QLabel("row height")
        row_label.setFixedWidth(100)
        
        # Add minus button
        self.row_minus = SmallIconButton(OutlineIcon.MINUS)
        self.row_minus.set_interactive(True)
        self.row_minus.clicked.connect(lambda: self.adjust_value(self.row_height, -2))
        row_layout.addWidget(row_label)
        row_layout.addWidget(self.row_minus)
        
        # Row height input
        self.row_height = QLineEdit()
        self.row_height.setPlaceholderText(str(DEFAULT_ROW_SPACING))
        self.row_height.setFixedWidth(60)
        self.row_height.setValidator(QIntValidator(20, 100))
        row_layout.addWidget(self.row_height)
        
        # Add plus button
        self.row_plus = SmallIconButton(OutlineIcon.PLUS)
        self.row_plus.set_interactive(True)
        self.row_plus.clicked.connect(lambda: self.adjust_value(self.row_height, 2))
        row_layout.addWidget(self.row_plus)
        
        row_layout.addStretch()
        self.layout.addLayout(row_layout)
        
        # Remember settings checkbox
        self.remember_format = QCheckBox("remember formatting configuration")
        self.layout.addWidget(self.remember_format)
        
        self.load_config()
    
    def adjust_value(self, line_edit, delta):
        """Adjust the value in a line edit by delta amount"""
        try:
            current = int(line_edit.text() or line_edit.placeholderText())
            validator = line_edit.validator()
            new_value = current + delta
            if validator:
                if new_value >= validator.bottom() and new_value <= validator.top():
                    line_edit.setText(str(new_value))
        except ValueError:
            pass

    def save_config(self):
        """Save format configuration values"""
        # Always save current values to config
        if self.font_size.text():
            self.config.set_value('layout/font_size', float(self.font_size.text()))
            if hasattr(self.parent(), 'parent') and self.parent().parent():
                editor = self.parent().parent()
                editor.current_font_size = float(self.font_size.text())
                editor.adjust_font(0)  # Update with current size
                
        if self.row_height.text():
            self.config.set_value('layout/row_spacing', float(self.row_height.text()))
            if hasattr(self.parent(), 'parent') and self.parent().parent():
                editor = self.parent().parent()
                editor.current_spacing = float(self.row_height.text())
                editor.adjust_spacing(0)  # Update with current size
                
        # Save whether to remember these values between sessions
        self.config.set_value('layout/remember_config', self.remember_format.isChecked())
        
    def load_config(self):
        """Load format configuration values"""
        # Always load current values from editor if available
        editor = self.parent().parent() if hasattr(self.parent(), 'parent') else None
        
        if editor:
            self.font_size.setText(str(int(editor.current_font_size)))
            self.row_height.setText(str(int(editor.current_spacing)))
        else:
            # Fall back to config values or defaults
            self.font_size.setText(str(int(self.config.get_float('layout/font_size', DEFAULT_FONT_SIZE))))
            self.row_height.setText(str(int(self.config.get_float('layout/row_spacing', DEFAULT_ROW_SPACING))))
        
        # Load remember settings
        self.remember_format.setChecked(self.config.get_bool('layout/remember_config'))

class StartupConfigGroup(ConfigGroup):
    """Startup-related configuration options"""
    
    def setup_ui(self):
        self.show_dialog = QCheckBox("show 'add files' dialog on startup")
        self.layout.addWidget(self.show_dialog)
        
        self.remember_window = QCheckBox("remember window size and position")
        self.layout.addWidget(self.remember_window)
        
        self.load_config()
        
    def save_config(self):
        """Save startup configuration values"""
        self.config.set_value('startup/show_dialog', self.show_dialog.isChecked())
        self.config.set_value('layout/remember_window', self.remember_window.isChecked())
        
    def load_config(self):
        """Load startup configuration values"""
        self.show_dialog.setChecked(self.config.get_bool('startup/show_dialog'))
        self.remember_window.setChecked(self.config.get_bool('layout/remember_window')) 