import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt, QSettings
from PyQt5.QtGui import QKeySequence
from PyQt5.QtWidgets import QShortcut

from crosshair import CrosshairOverlay
from control_panel import ControlPanel

class CrosshairApp:
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.settings = QSettings("CrosshairPro", "CrosshairOverlay")
        
        # Create main components
        self.overlay = CrosshairOverlay()
        self.control_panel = ControlPanel(self.overlay)
        
        # Setup global hotkeys
        self.setup_hotkeys()
        
        # Show initial windows
        self.overlay.show()
        self.control_panel.show()

    def setup_hotkeys(self):
        # Toggle overlay visibility
        toggle_shortcut = QShortcut(QKeySequence("Alt+X"), self.control_panel)
        toggle_shortcut.activated.connect(self.toggle_overlay)
        
        # Switch between presets
        for i in range(3):
            shortcut = QShortcut(QKeySequence(f"Alt+{i+1}"), self.control_panel)
            shortcut.activated.connect(lambda x=i: self.control_panel.preset_combo.setCurrentIndex(x))
        
        # Quick exit
        exit_shortcut = QShortcut(QKeySequence("Alt+Q"), self.control_panel)
        exit_shortcut.activated.connect(self.app.quit)

    def toggle_overlay(self):
        self.overlay.setVisible(not self.overlay.isVisible())

    def run(self):
        return self.app.exec_()

if __name__ == "__main__":
    app = CrosshairApp()
    sys.exit(app.run())
