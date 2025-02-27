"""
Main entry point for MisterLister application.
"""

import os
import sys
import ctypes
from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QIcon
from mister_lister.editor import FileEditor

def set_app_icon(app):
    """Set application icon with proper Windows taskbar support"""
    if os.name == 'nt':  # Windows
        # Set app ID for Windows
        myappid = 'MisterLister.App.1.0'
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
    
    # Get the absolute path to the icon file
    if getattr(sys, 'frozen', False):
        # Running as compiled exe
        base_path = sys._MEIPASS
    else:
        # Running from source
        base_path = os.path.dirname(os.path.dirname(__file__))
    
    icon_path = os.path.join(base_path, 'MisterLister.ico')
    
    if os.path.exists(icon_path):
        app_icon = QIcon(icon_path)
        app.setWindowIcon(app_icon)
        
        # Force Windows to refresh the taskbar icon
        if os.name == 'nt':
            ctypes.windll.shell32.SHChangeNotify(
                0x08000000, 0x0000, None, None
            )
    else:
        print(f"Warning: Icon file not found at {icon_path}")

def main():
    """Initialize and run the application"""
    app = QApplication(sys.argv)
    
    # Set the application icon
    set_app_icon(app)
    
    # Create and show the main window
    window = FileEditor()
    window.show()
    
    sys.exit(app.exec())

if __name__ == '__main__':
    main() 