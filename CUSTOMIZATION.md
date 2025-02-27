# Customizing MisterLister

MisterLister was designed with customization in mind. This guide will help you tailor the application to your specific needs by showing you where and how to modify key parts of the codebase.

## Table of Contents
- [Modifying Table Structure](#modifying-table-structure)
- [Customizing Filename Processing](#customizing-filename-processing)
- [Adding Configuration Options](#adding-configuration-options)
- [Customizing the Bottom Bar](#customizing-the-bottom-bar)
- [Styling and UI Customization](#styling-and-ui-customization)

## Modifying Table Structure

### Changing Column Headers and Count

The table structure is defined in the `process_files` method of the `FileEditor` class. To modify the column headers or number of columns, locate this code in `mister_lister/editor.py`:

```python
# Initialize table headers with descriptive labels
self.table.setColumnCount(5)
self.table.setHorizontalHeaderLabels([
    "lastname", "firstname", "dob", "item", "date"
])
```

Change the column count and header labels to match your needs. For example, to create a 3-column table for music files:

```python
# Initialize table headers for music files
self.table.setColumnCount(3)
self.table.setHorizontalHeaderLabels([
    "artist", "album", "year"
])
```

### Modifying Row Processing

The row processing logic is also in the `process_files` method. This code determines how filenames are split and displayed in the table:

```python
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
```

Customize this to match your filename format. For example, to process music filenames in the format "Artist - Album (Year).mp3":

```python
for file_path in files:
    row_position = self.table.rowCount()
    self.table.insertRow(row_position)
    
    # Extract just the filename without extension
    filename = os.path.splitext(os.path.basename(file_path))[0]
    
    # Split by the standard format "Artist - Album (Year)"
    try:
        artist, rest = filename.split(" - ", 1)
        album, year = rest.rsplit(" (", 1)
        year = year.rstrip(")")
        
        self.table.setItem(row_position, 0, QTableWidgetItem(artist.strip()))
        self.table.setItem(row_position, 1, QTableWidgetItem(album.strip()))
        self.table.setItem(row_position, 2, QTableWidgetItem(year.strip()))
    except ValueError:
        # Fallback for non-standard formats
        self.table.setItem(row_position, 0, QTableWidgetItem(filename))
        self.table.setItem(row_position, 1, QTableWidgetItem(""))
        self.table.setItem(row_position, 2, QTableWidgetItem(""))
```

## Customizing Filename Processing

### Modifying File Parsing Logic

The core file parsing logic is in `mister_lister/utils/text_processing.py`. The `split_by_type` function determines how filenames are broken into segments:

```python
def split_by_type(s, *args):
    """
    Split string into segments based on character types.
    
    Args:
        s (str): String to split
        *args: Character types to use as split points (defaults to "A" and "1")
        
    Returns:
        list: List of string segments
    """
    if not s:
        return []
    
    args = args if args else ("A", "1")
    type_filters = {unicodedata.category(char) for char in args}
    
    result = []
    current_segment = s[0]
    prev_type = unicodedata.category(s[0])
    
    for char in s[1:]:
        char_type = unicodedata.category(char)
        if not args or prev_type in type_filters:
            if char_type != prev_type:
                result.append(current_segment)
                current_segment = char
            else:
                current_segment += char
        else:
            current_segment += char
        prev_type = char_type
    
    result.append(current_segment)
    return result
```

You can create your own custom parsing function for your specific filename format. For example, to parse filenames with specific delimiters:

```python
def split_by_delimiter(filename, delimiter=" - "):
    """
    Split filename by a specific delimiter.
    
    Args:
        filename (str): Filename to split
        delimiter (str): Delimiter to split by (default: " - ")
        
    Returns:
        list: List of filename segments
    """
    return [segment.strip() for segment in filename.split(delimiter)]
```

### Adding New Text Processing Functions

You can add new utility functions to handle specific formats. For example, to parse file creation dates:

```python
def get_file_creation_date(file_path):
    """
    Get file creation date in a readable format.
    
    Args:
        file_path (str): Path to the file
        
    Returns:
        str: Formatted creation date
    """
    try:
        created = os.path.getctime(file_path)
        date_obj = datetime.fromtimestamp(created)
        return date_obj.strftime("%m-%d-%Y")
    except Exception:
        return "Unknown date"
```

## Adding Configuration Options

### Adding a New Configuration Group

Configuration options are organized in groups in `mister_lister/ui/dialogs/config_groups.py`. To add a new group of settings, create a new class that inherits from `ConfigGroup`:

```python
class ViewConfigGroup(ConfigGroup):
    """View-related configuration options"""
    
    def setup_ui(self):
        # Show line numbers checkbox
        self.show_line_numbers = QCheckBox("show line numbers")
        self.layout.addWidget(self.show_line_numbers)
        
        # Alternating row colors checkbox
        self.alt_row_colors = QCheckBox("use alternating row colors")
        self.layout.addWidget(self.alt_row_colors)
        
        # Column width slider
        col_layout = QHBoxLayout()
        col_label = QLabel("default column width")
        self.col_width = QSlider(Qt.Orientation.Horizontal)
        self.col_width.setRange(50, 300)
        self.col_width.setValue(self.config.get_int('view/column_width', 100))
        col_layout.addWidget(col_label)
        col_layout.addWidget(self.col_width)
        self.layout.addLayout(col_layout)
        
        self.load_config()
        
    def save_config(self):
        """Save view configuration values"""
        self.config.set_value('view/show_line_numbers', self.show_line_numbers.isChecked())
        self.config.set_value('view/alt_row_colors', self.alt_row_colors.isChecked())
        self.config.set_value('view/column_width', self.col_width.value())
        
    def load_config(self):
        """Load view configuration values"""
        self.show_line_numbers.setChecked(self.config.get_bool('view/show_line_numbers', False))
        self.alt_row_colors.setChecked(self.config.get_bool('view/alt_row_colors', True))
        self.col_width.setValue(self.config.get_int('view/column_width', 100))
```

### Adding the New Group to the Config Dialog

Once you've created a new configuration group, add it to the main ConfigDialog in `mister_lister/ui/dialogs/config_dialog.py`:

```python
# In ConfigDialog.__init__
# First import your new group
from .config_groups import (
    PrintConfigGroup, FileConfigGroup,
    FormatConfigGroup, StartupConfigGroup,
    ViewConfigGroup  # Add your new group to imports
)

# Then add it to the dialog
# Create config groups
self.format_group = FormatConfigGroup("format", self.config)
self.print_group = PrintConfigGroup("print", self.config)
self.file_group = FileConfigGroup("files", self.config)
self.startup_group = StartupConfigGroup("startup", self.config)
self.view_group = ViewConfigGroup("view", self.config)  # Add your new group

# Add groups to layout
self.layout.addWidget(self.format_group)
self.layout.addWidget(self.print_group)
self.layout.addWidget(self.file_group)
self.layout.addWidget(self.startup_group)
self.layout.addWidget(self.view_group)  # Add your new group

# Don't forget to update save_and_close
def save_and_close(self):
    """Save all configuration values and close"""
    self.format_group.save_config()
    self.print_group.save_config()
    self.file_group.save_config()
    self.startup_group.save_config()
    self.view_group.save_config()  # Save your new group
    self.accept()
```

## Customizing the Bottom Bar

The bottom bar contains all the main action buttons for the application. You can customize it by adding new buttons, creating new button groups, or modifying existing ones.

### Available Icons

MisterLister uses the [pytablericons](https://github.com/niklashenning/pytablericons) package for its icons. When creating new buttons, you'll need to specify which icon to use. The available icons can be found in two categories:

- `OutlineIcon`: Outline-style icons (default style)
- `FilledIcon`: Filled-style icons (used for the "in-use" state)

You can browse the complete list of available icons at:
[https://github.com/niklashenning/pytablericons/tree/master/src/pytablericons/icons](https://github.com/niklashenning/pytablericons/tree/master/src/pytablericons/icons)

The icons are organized into two folders:
- `src/pytablericons/icons/filled` - Filled-style icons used for the "in-use" state
- `src/pytablericons/icons/outline` - Outline-style icons used by default

Example usage:
```python
from pytablericons import OutlineIcon, FilledIcon

# Creating buttons with different icons
save_btn = CircleButton(OutlineIcon.DEVICE_FLOPPY)
chart_btn = CircleButton(OutlineIcon.CHART_BAR)
export_btn = CircleButton(OutlineIcon.FILE_EXPORT)
```

### Adding New Buttons to the Bottom Bar

The bottom bar is defined in `mister_lister/ui/bottom_bar.py`. To add a new button, you'll need to:

1. Create a new CircleButton instance with an appropriate icon from pytablericons
2. Add it to an existing or new ButtonGroup
3. Connect it to an action

Here's how the existing buttons are created:

```python
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
```

And here's how you could add a new "Export" button to the Actions group:

```python
# Create new export button
self.export_btn = CircleButton(OutlineIcon.DOWNLOAD)
self.export_btn.setToolTip("Export as CSV")

# Add to existing actions group
self.actions_group.layout.addWidget(self.export_btn)

# Don't forget to update set_controls_enabled method
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
               self.clear_btn, self.export_btn]:  # Add your new button here
        btn.interactive = enabled
        btn.in_use = False  # Reset in_use state when disabling
        btn.update_style()
```

### Creating a New Button Group

To create an entirely new button group with new functionality, add it to the BottomBar's `__init__` method:

```python
# Create new sorting group
self.sorting_group = ButtonGroup("sort by")
self.sort_name_btn = CircleButton(OutlineIcon.SORT_ASCENDING)
self.sort_name_btn.setToolTip("Sort by Name")
self.sort_date_btn = CircleButton(OutlineIcon.CALENDAR)
self.sort_date_btn.setToolTip("Sort by Date")

self.sorting_group.layout.addWidget(self.sort_name_btn)
self.sorting_group.layout.addWidget(self.sort_date_btn)

# Add the new group to the main layout
# (Insert it between existing groups)
main_layout.addWidget(self.add_files_group)
main_layout.addStretch(1)
main_layout.addWidget(self.sorting_group)  # Add new group here
main_layout.addStretch(1)
main_layout.addWidget(self.font_group)
# ...rest of layout...
```

### Connecting Buttons to Actions

In the main `FileEditor` class, you'll need to connect the new buttons to their actions:

```python
# In FileEditor.setup_bottom_bar method:
self.bottom_bar.export_btn.clicked.connect(self.export_to_csv)
self.bottom_bar.sort_name_btn.clicked.connect(lambda: self.sort_table(0))  # Sort by column 0 (name)
self.bottom_bar.sort_date_btn.clicked.connect(lambda: self.sort_table(2))  # Sort by column 2 (date)

# Then implement the new methods:
def export_to_csv(self):
    """Export table data to CSV file"""
    filename, _ = QFileDialog.getSaveFileName(
        self, "Export CSV", "", "CSV Files (*.csv);;All Files (*)"
    )
    if not filename:
        return
        
    with open(filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        # Write headers
        headers = []
        for col in range(self.table.columnCount()):
            if not self.table.isColumnHidden(col):
                header = self.table.horizontalHeaderItem(col)
                headers.append(header.text() if header else "")
        writer.writerow(headers)
        
        # Write data
        for row in range(self.table.rowCount()):
            row_data = []
            for col in range(self.table.columnCount()):
                if not self.table.isColumnHidden(col):
                    item = self.table.item(row, col)
                    row_data.append(item.text() if item else "")
            writer.writerow(row_data)

def sort_table(self, column):
    """Sort the table by the specified column"""
    self.table.sortByColumn(column, Qt.SortOrder.AscendingOrder)
```

### Creating Custom Button Types

The buttons in MisterLister are based on the `CircleButton` class found in `mister_lister/ui/widgets/buttons.py`. You can customize the appearance of buttons or create new button types by extending this class:

```python
class SquareButton(CircleButton):
    """Square-shaped button variant for special actions"""
    
    def __init__(self, icon_type="", parent=None):
        super().__init__(icon_type, parent)
        # Override the size if needed
        self.setFixedSize(50, 50)
        
    def update_style(self):
        """Override style to use square shape instead of circular"""
        base_color = DARKER_TAN if self._interactive else INACTIVE_TAN
        self.update_icon(base_color)
        
        if self._interactive:
            self.setStyleSheet(f"""
                QPushButton {{
                    background: transparent;
                    border: none;
                    border-radius: 5px;  # Smaller radius for square shape
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
                    border-radius: 5px;
                }}
                QPushButton:disabled {{
                    background: transparent;
                }}
            """)
            self.setCursor(Qt.CursorShape.ArrowCursor)
```

## Styling and UI Customization

### Customizing the Application's Appearance

The main styling for the application is in various places, but one of the central ones is in the ConfigDialog's `_get_stylesheet` method:

```python
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
        /* More styles... */
    """
```

You can modify this stylesheet to change the look and feel of the dialog, and similar modifications can be made to other UI components.

For global application styling, look at the `update_window_style` method in `FileEditor`:

```python
def update_window_style(self):
    """Update the window's style"""
    self.setStyleSheet(f"""
        QMainWindow {{
            background-color: {WINDOW_BG};
        }}
    """)
```

You can expand this to include styling for all controls in the application:

```python
def update_window_style(self):
    """Update the window's style"""
    self.setStyleSheet(f"""
        QMainWindow {{
            background-color: {WINDOW_BG};
        }}
        QTableWidget {{
            background-color: #fafafa;
            gridline-color: #e0e0e0;
        }}
        /* Add more global styles here */
    """)
```

## Advanced Customizations

For more advanced customizations, explore the following areas:

1. **Table Context Menus**: Look at the `setup_table_context_menus`, `show_header_menu`, and `show_cell_menu` methods in `FileEditor` to customize right-click menu options.

2. **Print Formatting**: Modify the `print_table` method to change how data is formatted for printing.

3. **Drag and Drop Handling**: Enhance the `dragEnterEvent` and `dropEvent` methods to handle more file types or additional data formats.

4. **Keyboard Shortcuts**: Expand the `eventFilter` method to add more keyboard shortcuts and actions.

Remember to test your changes thoroughly, and don't hesitate to create a fork if you develop features that might be useful to others! 