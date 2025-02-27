"""
Drop zone widget for MisterLister.
Provides a visual target for drag and drop file operations.
"""

from mister_lister.qt import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPainter, QColor, QFont, QDragEnterEvent, 
    QDropEvent, Qt
)
from mister_lister.constants import WINDOW_BG, WHITE

class DropZone(QWidget):
    """
    A widget that accepts file drops and displays instructions.
    Shows when no files are loaded in the application.
    """
    
    def __init__(self, parent=None):
        """
        Initialize the drop zone.
        
        Args:
            parent: Parent widget (typically FileEditor)
        """
        super().__init__(parent)
        self.editor = parent
        
        layout = QVBoxLayout(self)
        
        # Create and style the instruction label
        label = QLabel('drag files here or click <span style="padding-left: 5px; font-weight: bold;">add files</span>')
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Apply font settings
        font = QFont("Asap", 18)
        font.setStyleStrategy(QFont.StyleStrategy.PreferAntialias)
        font.setHintingPreference(QFont.HintingPreference.PreferFullHinting)
        label.setFont(font)
        label.setStyleSheet("""
            QLabel {
                color: #666;
            }
        """)
        
        layout.addWidget(label)
        
        self.setStyleSheet(f"""
            QWidget {{
                background-color: {WHITE};
                margin: 20px;
            }}
        """)
            
    def paintEvent(self, event):
        """Custom paint event to set background color"""
        painter = QPainter(self)
        painter.fillRect(self.rect(), QColor(WINDOW_BG)) 