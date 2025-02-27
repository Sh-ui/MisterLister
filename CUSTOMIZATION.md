# Customizing MisterLister

MisterLister was designed with customization in mind. This guide will help you tailor the application to your specific needs by showing you where and how to modify key parts of the codebase.

## Table of Contents
- [Core File Structure](#core-file-structure)
- [Modifying Table Behavior](#modifying-table-behavior)
- [Customizing File Processing](#customizing-file-processing)
- [Configuring the UI](#configuring-the-ui)
- [Adding New Features](#adding-new-features)

## Core File Structure

Understanding these key files will help you navigate the codebase:

* `mister_lister/main.py` - Application entry point
* `mister_lister/editor.py` - Core `FileEditor` class that controls most functionality
* `mister_lister/constants.py` - Colors, styles, and other constants
* `mister_lister/ui/bottom_bar.py` - Bottom toolbar with action buttons
* `mister_lister/ui/widgets/buttons.py` - Button implementations
* `mister_lister/ui/widgets/dropzone.py` - Initial file drop area
* `mister_lister/ui/dialogs/config_dialog.py` - Configuration dialog
* `mister_lister/ui/dialogs/config_groups.py` - Individual configuration groups
* `mister_lister/utils/text_processing.py` - Filename parsing functions
* `mister_lister/utils/config.py` - Configuration handling

## Modifying Table Behavior

### Change the Table Structure (Headers & Columns)

**File:** `mister_lister/editor.py`

Look for the `process_files` method in the `FileEditor` class. This method sets up the table and processes filenames:

```python
# Look for this section to change column headers
self.table.setColumnCount(5)
self.table.setHorizontalHeaderLabels([
    "lastname", "firstname", "dob", "item", "date"
])
```

### Change How Files Get Processed Into Table Rows

**Files to modify:**
1. `mister_lister/editor.py` - `process_files` method 
2. `mister_lister/utils/text_processing.py` - Parsing functions

The `process_files` method calls functions from `text_processing.py` to parse filenames:

```python
# In editor.py - This shows how files are added to the table
for file_path in files:
    row_position = self.table.rowCount()
    self.table.insertRow(row_position)
    
    filename = os.path.basename(file_path)
    segments = split_by_type(filename)  # This function is in text_processing.py
    # ...
```

## Customizing File Processing

### Modify Filename Parsing Logic

**File:** `mister_lister/utils/text_processing.py`

Key functions:
- `split_by_type()` - Splits text by character type changes
- `convert_short_date()` - Formats dates in a specific way

If you need to parse filenames differently, modify or replace the `split_by_type()` function. Make sure your changes match the column structure defined in `editor.py`.

### Add New Text Processing Functions

Add new helper functions in `text_processing.py` and then call them from the `process_files` method in `editor.py`.

## Configuring the UI

### Modify Colors and Styles

**File:** `mister_lister/constants.py`

This file contains all color definitions used throughout the application:

```python
# Color constants used for styling
WHITE = "#FFFFFF"
NORMAL_TAN = "#F5F5DC"
LIGHT_TAN = "#FAF9F6"
# ...
```

Changing these values will affect all UI elements that use them.

### Customize the Bottom Bar

**Files to modify:**
1. `mister_lister/ui/bottom_bar.py` - Defines the button bar
2. `mister_lister/editor.py` - Connects buttons to actions

The bottom bar is defined in `bottom_bar.py` and contains button groups. Each button needs:
1. Creation with an icon in `BottomBar.__init__()`
2. Connection to an action in `FileEditor.setup_bottom_bar()`

#### Available Icons

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

To add a new button:
```python
# 1. In bottom_bar.py - BottomBar.__init__()
self.new_button = CircleButton(OutlineIcon.SOME_ICON)
self.new_button.setToolTip("My New Action")
self.some_group.layout.addWidget(self.new_button)

# 2. In editor.py - FileEditor.setup_bottom_bar()
self.bottom_bar.new_button.clicked.connect(self.some_action)

# 3. Then implement your action in FileEditor
def some_action(self):
    # Your action logic here
    pass
```

### Modify Configuration Options

**Files to modify:**
1. `mister_lister/ui/dialogs/config_groups.py` - Contains setting groups
2. `mister_lister/ui/dialogs/config_dialog.py` - Organizes groups in the dialog

Each settings section is a separate class in `config_groups.py`. To add a new setting:

1. Find the appropriate group (e.g., `FormatConfigGroup`)
2. Add a new widget in the `setup_ui()` method
3. Update `save_config()` and `load_config()` methods

If you need an entirely new settings category, create a new class in `config_groups.py`, then add it to `config_dialog.py`.

## Adding New Features

### Add Right-Click Menu Options

**File:** `mister_lister/editor.py`

Look for these methods:
- `setup_table_context_menus()` - Sets up context menus
- `show_header_menu()` - Column header right-click menu
- `show_cell_menu()` - Cell right-click menu

### Extend Keyboard Shortcuts

**File:** `mister_lister/editor.py`

Find the `eventFilter()` method which handles key presses:

```python
def eventFilter(self, source, event):
    """Handle key events for the table"""
    if event.type() == QEvent.Type.KeyPress:
        if event.key() == Qt.Key.Key_A and event.modifiers() == Qt.KeyboardModifier.ControlModifier:
            # Ctrl+A selects all cells
            self.table.selectAll()
            return True
        # Add your shortcuts here
    return super().eventFilter(source, event)
```

### Add New UI Dialog

1. Create a new dialog class in `mister_lister/ui/dialogs/`
2. Import and use it in the relevant part of the application

Example of launching a dialog from `editor.py`:

```python
from mister_lister.ui.dialogs.your_new_dialog import YourNewDialog

# Later in some method
dialog = YourNewDialog(self)
if dialog.exec():
    # Handle dialog response
    pass
```

## Common Modifications Quick Reference

| Modification | Primary File(s) | Secondary File(s) | Notes |
|--------------|----------------|-------------------|-------|
| Table columns | `editor.py` | `text_processing.py` | Match parser with column count |
| Filename parsing | `text_processing.py` | `editor.py` | Ensure segments match table columns |
| Add button | `bottom_bar.py` | `editor.py` | Create in bottom_bar, connect in editor |
| Add config option | `config_groups.py` | `config.py` | Update save/load methods |
| Styling | `constants.py` | Various CSS in classes | Colors defined in constants |
| Context menus | `editor.py` | None | Look for context menu methods |

Remember that changes to one part of the application may require modifications in multiple files to maintain consistency across the UI. 