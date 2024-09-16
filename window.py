import sys

from PyQt6.QtCore import QSize, Qt
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QHBoxLayout, QLabel, QWidget, QComboBox

# Subclass QMainWindow to customize your application's main window
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("BMW Data")

        # Set fixed size
        self.setFixedSize(400, 300)

        # Main layout
        main_layout = QVBoxLayout()
        main_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        # Title label
        title = QLabel("BMW Data")
        title.setAlignment(Qt.AlignmentFlag.AlignTop)

        # Button and QCombobox layout
        button_layout = QHBoxLayout()
        model_box = QComboBox()
        model_box.setFixedSize(100, 20)
        model_box.addItem("E46")
        model_box.addItem("E90")

        button = QPushButton("Show Data")
        button.setFixedSize(100, 20)

        # Add model_box and button to layout
        button_layout.addWidget(model_box)
        button_layout.addWidget(button)
        button_layout.addStretch(1)

        # Add widgets to main layout
        main_layout.addWidget(title)
        main_layout.addLayout(button_layout)

        # Create a central widget to hold the other widgets and layouts
        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

        # Connect the button to a function
        button.clicked.connect(self.on_button_click)

    def on_button_click(self):
        print("Button clicked")


# Create the application instance
app = QApplication(sys.argv)

# Create the main window
window = MainWindow()
window.show()

# Run the event loop
sys.exit(app.exec())

