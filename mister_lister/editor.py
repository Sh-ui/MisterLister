# Set up centralized __pycache__ directory before any imports
import os
import sys
import tempfile

# Set Python's cache directory to system temp
os.environ['PYTHONPYCACHEPREFIX'] = tempfile.gettempdir()

"""
Main editor component for MisterLister.
"""

from mister_lister.qt import (
    QMainWindow, QWidget, QVBoxLayout, QTableWidget,
    QTableWidgetItem, QHeaderView, QMenu, QAction,
    QDragEnterEvent, QDropEvent, QPrinter, 
    QPrintPreviewDialog, QTextDocument, QTextCursor,
    QDialog, Qt, QFileDialog, QFontDatabase, QSettings, QTimer, QPainter, QRectF, QColor, QMarginsF, QPageLayout,
    QFont, QIcon, QApplication
)
from mister_lister.constants import (
    WHITE, NORMAL_TAN, LIGHT_BLUE, WINDOW_BG,
    MIN_WINDOW_WIDTH, MIN_WINDOW_HEIGHT,
    DEFAULT_FONT_SIZE, DEFAULT_ROW_SPACING
)
from mister_lister.ui.widgets import DropZone
from mister_lister.ui.dialogs import ConfigDialog, ConfirmDialog
from mister_lister.ui.bottom_bar import BottomBar
from mister_lister.utils import split_by_type, convert_short_date, Config

class FileEditor(QMainWindow):
    """
    Main application window for MisterLister.
    Handles file processing, display, and user interactions.
    """
    
    def __init__(self):
        super().__init__()
        
        # Try loading Asap font family
        try:
            QFontDatabase.addApplicationFont("assets/fonts/Asap-Regular.ttf")
            QFontDatabase.addApplicationFont("assets/fonts/Asap-Medium.ttf")
            QFontDatabase.addApplicationFont("assets/fonts/Asap-Bold.ttf") 
            QFontDatabase.addApplicationFont("assets/fonts/Asap-Italic.ttf")
            QFontDatabase.addApplicationFont("assets/fonts/Asap-MediumItalic.ttf")
            QFontDatabase.addApplicationFont("assets/fonts/Asap-BoldItalic.ttf")
        except:
            print("Font files not found. Using system fonts.")
        
        # Initialize settings
        self.config = Config()
        self.setWindowTitle("MisterLister")
        self.setMinimumSize(MIN_WINDOW_WIDTH, MIN_WINDOW_HEIGHT)
        
        # Restore window geometry if enabled
        if self.config.get_bool('layout/remember_window'):
            geometry = self.config.get_str('layout/window_geometry')
            if geometry:
                self.restoreGeometry(bytes.fromhex(geometry))
        
        # Setup main widget and layout
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)
        self.layout.setSpacing(0)
        self.layout.setContentsMargins(0, 0, 0, 0)
        
        # Initialize UI components
        self.setup_drop_zone()
        self.setup_table()
        self.setup_bottom_bar()
        
        # Set initial values based on config
        if self.config.get_bool('layout/remember_config'):
            self.current_font_size = self.config.get_float('layout/font_size')
            self.current_spacing = self.config.get_float('layout/row_spacing')
        else:
            self.current_font_size = DEFAULT_FONT_SIZE
            self.current_spacing = DEFAULT_ROW_SPACING
        self.printer_name = self.config.get_str('print/printer_name')
        
        self.update_window_style()
        
        # Show add files dialog on startup if enabled
        if self.config.get_bool('startup/show_dialog'):
            QTimer.singleShot(0, self.add_files)  # Use QTimer to show dialog after window is ready
        
        # Pre-create dialogs
        self.confirm_dialog = None

    def setup_drop_zone(self):
        """Initialize the drop zone"""
        self.drop_zone = DropZone(self)
        self.layout.addWidget(self.drop_zone)

    def setup_table(self):
        """Initialize the table widget"""
        self.table = QTableWidget()
        self.table.setVisible(False)
        self.table.setSortingEnabled(True)
        
        # Set selection behaviors
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)  # Select whole rows
        self.table.setSelectionMode(QTableWidget.SelectionMode.ExtendedSelection)  # Allow multiple selection with modifiers
        
        # Set initial font size
        font = self.table.font()
        font.setPointSize(DEFAULT_FONT_SIZE)
        self.table.setFont(font)
        self.current_font_size = DEFAULT_FONT_SIZE
        
        # Set initial row height
        self.current_spacing = DEFAULT_ROW_SPACING
        
        # Set table style
        self.table.setStyleSheet(f"""
            QTableWidget {{
                background-color: {WHITE};
                border: none;
                gridline-color: #ddd;
            }}
            QHeaderView::section {{
                background-color: {NORMAL_TAN};
                padding: 5px;
                border: none;
                border-right: 1px solid #ddd;
                border-bottom: 1px solid #ddd;
                color: #666;
            }}
            QTableWidget::item {{
                color: black;
                background-color: {WHITE};
            }}
            QTableWidget::item:selected {{
                background-color: {LIGHT_BLUE};
                color: {WHITE};
            }}
        """)
        self.layout.addWidget(self.table)
        
        # Setup context menus
        self.setup_table_context_menus()
        
        # Enable copy/paste
        self.table.setSelectionMode(QTableWidget.SelectionMode.ExtendedSelection)
        
        # Install event filter for keyboard shortcuts
        self.table.installEventFilter(self)

    def setup_bottom_bar(self):
        """Initialize the bottom control bar"""
        self.bottom_bar = BottomBar()
        self.layout.addWidget(self.bottom_bar)
        
        # Connect button signals
        self.bottom_bar.add_files_btn.clicked.connect(self.add_files)
        self.bottom_bar.font_minus_btn.clicked.connect(lambda: self.adjust_font(-1))
        self.bottom_bar.font_plus_btn.clicked.connect(lambda: self.adjust_font(1))
        self.bottom_bar.spacing_minus_btn.clicked.connect(lambda: self.adjust_spacing(-2))
        self.bottom_bar.spacing_plus_btn.clicked.connect(lambda: self.adjust_spacing(2))
        self.bottom_bar.preview_btn.clicked.connect(self.preview_document)
        self.bottom_bar.print_btn.clicked.connect(self.print_document)
        self.bottom_bar.clear_btn.clicked.connect(self.clear_table)
        self.bottom_bar.config_btn.clicked.connect(self.show_config)

    def update_window_style(self):
        """Update the window's style"""
        self.setStyleSheet(f"""
            QMainWindow {{
                background-color: {WINDOW_BG};
            }}
        """)

    def add_files(self):
        """Open file dialog to add files"""
        files, _ = QFileDialog.getOpenFileNames(
            self,
            "Select Files",
            self.config.get_str('files/default_dir')
        )
        
        # If files were selected, process them and update directory
        if files:
            if self.config.get_bool('files/remember_dir'):
                self.config.set_value('files/default_dir', os.path.dirname(files[0]))
            self.process_files(files)
        # If this was called on startup and no files selected, show drop zone
        elif not self.table.isVisible():
            self.drop_zone.setVisible(True)
            self.table.setVisible(False)
            self.bottom_bar.set_controls_enabled(False)

    def process_files(self, files):
        """Process the list of files and add them to the table"""
        if not self.table.isVisible():
            self.table.setVisible(True)
            self.drop_zone.setVisible(False)
            self.bottom_bar.set_controls_enabled(True)
            
            # Initialize table headers with descriptive labels
            self.table.setColumnCount(5)
            self.table.setHorizontalHeaderLabels([
                "lastname", "firstname", "dob", "item", "date"
            ])
            header = self.table.horizontalHeader()
            for i in range(5):
                header.setSectionResizeMode(i, QHeaderView.ResizeMode.Stretch)
        
        # Update add_files button state
        self.bottom_bar.add_files_btn.in_use = True

        # Add new files to table
        for file_path in files:
            row_position = self.table.rowCount()
            self.table.insertRow(row_position)
            
            filename = os.path.basename(file_path)
            segments = split_by_type(filename)
            if len(segments) >= 6:
                segments = segments[:5]
                
            # Add segments to columns
            for col, segment in enumerate(segments):
                if col in [2, 4]:  # Convert dates in columns 3 and 5
                    item = QTableWidgetItem(convert_short_date(segment.strip()))
                else:
                    item = QTableWidgetItem(segment.strip())
                self.table.setItem(row_position, col, item)
                
            # Fill empty columns
            for col in range(len(segments), 5):
                self.table.setItem(row_position, col, QTableWidgetItem(""))
            
            # Set row height (convert to int)
            self.table.setRowHeight(row_position, int(self.current_spacing))

    def setup_table_context_menus(self):
        """Setup context menus for the table"""
        self.table.horizontalHeader().setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.table.horizontalHeader().customContextMenuRequested.connect(self.show_header_menu)
        self.table.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.table.customContextMenuRequested.connect(self.show_cell_menu)

    def show_header_menu(self, pos):
        """Show context menu for table header"""
        menu = QMenu(self)
        hide_action = QAction("Hide Column", self)
        hide_action.triggered.connect(lambda: self.table.hideColumn(
            self.table.horizontalHeader().logicalIndexAt(pos)
        ))
        menu.addAction(hide_action)
        
        show_all_action = QAction("Show All Columns", self)
        show_all_action.triggered.connect(self.show_all_columns)
        menu.addAction(show_all_action)
        
        menu.exec(self.table.horizontalHeader().mapToGlobal(pos))

    def show_cell_menu(self, pos):
        """Show context menu for table cells"""
        menu = QMenu(self)
        if self.table.selectedItems():
            copy_action = QAction("Copy", self)
            copy_action.triggered.connect(self.copy_selection)
            menu.addAction(copy_action)
            
            delete_action = QAction("Delete Selected", self)
            delete_action.triggered.connect(self.delete_selected_rows)
            menu.addAction(delete_action)
        menu.exec(self.table.mapToGlobal(pos))

    def show_all_columns(self):
        """Show all hidden columns"""
        for i in range(self.table.columnCount()):
            self.table.showColumn(i)

    def delete_selected_rows(self):
        """Delete selected rows from the table"""
        rows = set(item.row() for item in self.table.selectedItems())
        for row in sorted(rows, reverse=True):
            self.table.removeRow(row)
        
        if self.table.rowCount() == 0:
            self.table.setVisible(False)
            self.drop_zone.setVisible(True)
            self.bottom_bar.set_controls_enabled(False)
            self.bottom_bar.add_files_btn.in_use = False

    def show_config(self):
        """Show configuration dialog"""
        self.bottom_bar.config_btn.in_use = True
        self.config_dialog = ConfigDialog(self)
        
        # Set current values in dialog's format group
        self.config_dialog.format_group.font_size.setText(str(int(self.current_font_size)))
        self.config_dialog.format_group.row_height.setText(str(int(self.current_spacing)))
        
        self.config_dialog.exec()
        self.bottom_bar.config_btn.in_use = False

    def preview_document(self):
        """Show print preview dialog"""
        self.bottom_bar.preview_btn.in_use = True
        printer = QPrinter(QPrinter.PrinterMode.HighResolution)
        if self.printer_name:
            printer.setPrinterName(self.printer_name)
        
        preview = QPrintPreviewDialog(printer, self)
        preview.paintRequested.connect(self.print_table)
        
        # Create proper function for state change
        def reset_preview_state():
            self.bottom_bar.preview_btn.in_use = False
        
        preview.finished.connect(reset_preview_state)
        preview.exec()

    def print_document(self):
        """Print the document directly"""
        self.bottom_bar.print_btn.in_use = True
        printer = QPrinter(QPrinter.PrinterMode.HighResolution)
        if self.printer_name:
            printer.setPrinterName(self.printer_name)
        self.print_table(printer)
        
        # Create proper function for state change
        def reset_print_state():
            self.bottom_bar.print_btn.in_use = False
        
        # Simulate printing time
        QTimer.singleShot(2000, reset_print_state)

    def print_table(self, printer):
        """Print the table with current config"""
        # Get border config from config
        border_style = self.config.get_str('print/border_style')
        border_gray = self.config.get_int('print/border_gray')
        border_color = f"rgb({border_gray}, {border_gray}, {border_gray})"
        
        # Create HTML with explicit sizing
        html = f"""
            <style>
                body {{
                    font-size: {int(self.current_font_size)}pt;
                    font-family: 'Asap';
                    padding: 0;
                }}
                table {{
                    border-collapse: collapse;
                    width: 100%;
                    table-layout: fixed;
                }}
                tr {{
                    height: {int(self.current_spacing)}px !important;
                    line-height: {int(self.current_spacing)}px !important;
                }}
                td, th {{
                    padding: 4px;
                    border: 1px {border_style} {border_color};
                    text-align: center;
                    vertical-align: middle;
                    overflow: hidden;
                    height: {int(self.current_spacing)}px !important;
                }}
            </style>
            <table>
        """
        
        # Add headers
        html += "<tr>"
        for col in range(self.table.columnCount()):
            if not self.table.isColumnHidden(col):
                header = self.table.horizontalHeaderItem(col)
                html += f"<th>{header.text() if header else ''}</th>"
        html += "</tr>"
        
        # Add data rows
        for row in range(self.table.rowCount()):
            html += "<tr>"
            for col in range(self.table.columnCount()):
                if not self.table.isColumnHidden(col):
                    item = self.table.item(row, col)
                    html += f"<td>{item.text() if item else ''}</td>"
            html += "</tr>"
        
        html += "</table>"
        
        # Create document and print
        document = QTextDocument()
        document.setDefaultFont(self.table.font())
        document.setHtml(html)
        document.print(printer)

    def clear_table(self):
        """Clear all entries from the table after confirmation"""
        if self.table.rowCount() > 0:
            self.bottom_bar.clear_btn.in_use = True
            
            # Create dialog only if needed
            if not self.confirm_dialog:
                self.confirm_dialog = ConfirmDialog(self)
            
            result = self.confirm_dialog.exec()
            self.bottom_bar.clear_btn.in_use = False
            
            if result == QDialog.DialogCode.Accepted:
                self.table.setRowCount(0)
                self.table.setVisible(False)
                self.drop_zone.setVisible(True)
                self.bottom_bar.set_controls_enabled(False)

    def adjust_font(self, delta):
        """Adjust the font size"""
        self.current_font_size = max(8, min(72, self.current_font_size + delta))
        font = self.table.font()
        font.setPointSize(int(self.current_font_size))  # Convert to int for setPointSize
        self.table.setFont(font)
        
        # Update row heights to maintain proportions
        for row in range(self.table.rowCount()):
            self.table.setRowHeight(row, int(self.current_spacing))
            
        # Save to config if remember settings is enabled
        if self.config.get_bool('layout/remember_config'):
            self.config.set_value('layout/font_size', self.current_font_size)
        
        # Update any open config dialog
        if hasattr(self, 'config_dialog') and self.config_dialog.isVisible():
            self.config_dialog.format_group.font_size.setText(str(int(self.current_font_size)))

    def adjust_spacing(self, delta):
        """Adjust the row spacing"""
        self.current_spacing = max(20, min(100, self.current_spacing + delta))
        for row in range(self.table.rowCount()):
            self.table.setRowHeight(row, int(self.current_spacing))  # Convert to int
            
        # Save to config if remember settings is enabled
        if self.config.get_bool('layout/remember_config'):
            self.config.set_value('layout/row_spacing', self.current_spacing)
            
        # Update any open config dialog
        if hasattr(self, 'config_dialog') and self.config_dialog.isVisible():
            self.config_dialog.format_group.row_height.setText(str(int(self.current_spacing)))

    def dragEnterEvent(self, event: QDragEnterEvent):
        """Handle drag enter events for the main window"""
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()
            
    def dropEvent(self, event: QDropEvent):
        """Handle drop events for the main window"""
        files = [url.toLocalFile() for url in event.mimeData().urls()]
        self.process_files(files)

    def eventFilter(self, source, event):
        """Handle keyboard shortcuts"""
        if source is self.table and event.type() == event.Type.KeyPress:
            if event.modifiers() == Qt.KeyboardModifier.ControlModifier:
                if event.key() == Qt.Key.Key_C:
                    self.copy_selection()
                    return True
                elif event.key() == Qt.Key.Key_A:
                    self.table.selectAll()
                    return True
        return super().eventFilter(source, event)

    def copy_selection(self):
        """Copy selected cells to clipboard in TSV format"""
        selected = self.table.selectedRanges()
        if not selected:
            return
        
        # Check if entire table is selected (Ctrl+A case)
        all_selected = (
            len(selected) == 1 and
            selected[0].topRow() == 0 and
            selected[0].bottomRow() == self.table.rowCount() - 1 and
            selected[0].leftColumn() == 0 and
            selected[0].rightColumn() == self.table.columnCount() - 1
        )
        
        # Build text with tabs between columns and newlines between rows
        text = []
        
        # Add headers only if Ctrl+A was used
        if all_selected:
            headers = []
            for col in range(self.table.columnCount()):
                if not self.table.isColumnHidden(col):
                    header = self.table.horizontalHeaderItem(col)
                    headers.append(header.text() if header else "")
            text.append("\t".join(headers))
        
        # Add selected cell contents
        for range_ in selected:
            for row in range(range_.topRow(), range_.bottomRow() + 1):
                row_data = []
                for col in range(range_.leftColumn(), range_.rightColumn() + 1):
                    if not self.table.isColumnHidden(col):
                        item = self.table.item(row, col)
                        row_data.append(item.text() if item else "")
                text.append("\t".join(row_data))
        
        # Set clipboard content
        clipboard = QApplication.clipboard()
        clipboard.setText("\n".join(text))

    def closeEvent(self, event):
        """Handle window close event"""
        # Save window geometry if enabled
        if self.config.get_bool('layout/remember_window'):
            geometry = bytes(self.saveGeometry().data()).hex()
            self.config.set_value('layout/window_geometry', geometry)
        event.accept() 