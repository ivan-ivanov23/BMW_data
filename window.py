import sys

from PyQt6.QtCore import QSize, Qt
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QHBoxLayout, QLabel, QWidget, QComboBox
from PyQt6.QtWebEngineWidgets import QWebEngineView
import plotly.figure_factory as ff

# Subclass QMainWindow to customize your application's main window
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("BMW Data")

        # Set fixed size
        self.setFixedSize(600, 400)

        # Main layout
        main_layout = QVBoxLayout()
        main_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        # Title label
        title = QLabel("BMW Data")
        title.setStyleSheet("QLabel{font-size: 18pt; font: bold}")
        title.setAlignment(Qt.AlignmentFlag.AlignTop)

        # Select model label
        select = QLabel("Select a BMW 3 Series generation, year and modification:")
        select.setStyleSheet("QLabel{font-size: 12pt;}")
        select.setAlignment(Qt.AlignmentFlag.AlignTop)

        # Button label layout and labels
        button_label_layout = QHBoxLayout()
        generation = QLabel("Generation:")
        generation.setAlignment(Qt.AlignmentFlag.AlignLeft)
        year = QLabel("Year:")
        year.setAlignment(Qt.AlignmentFlag.AlignLeft)
        mod = QLabel("Modification:")
        mod.setAlignment(Qt.AlignmentFlag.AlignLeft)

        button_label_layout.addWidget(generation)
        button_label_layout.addWidget(year)
        button_label_layout.addWidget(mod)
        button_label_layout.addSpacing(2)

        # Button and QCombobox layout
        button_layout = QHBoxLayout()

        # Combo box for model generations
        self.gen_box = QComboBox()
        self.gen_box.setFixedSize(100, 20)
        self.gen_box.addItem("E46")
        self.gen_box.addItem("E90")
        # Set default value as empty
        self.gen_box.setCurrentIndex(-1)
        # When an option from box chosen, enable button
        # self.gen_box.currentIndexChanged.connect(self.on_model_changed)

        # Combo box for year
        self.year_box = QComboBox()
        self.year_box.setFixedSize(100, 20)
        self.year_box.addItem("2001-05")
        self.year_box.addItem("2005-10")
        # Set default value as empty
        self.year_box.setCurrentIndex(-1)
        self.year_box.setEnabled(False)

        # Combo box for modification
        self.mod_box = QComboBox()
        self.mod_box.setFixedSize(100, 20)
        self.mod_box.addItem("320d")
        self.mod_box.addItem("330d")
        # Set default value as empty
        self.mod_box.setCurrentIndex(-1)
        self.mod_box.setEnabled(False)

        self.button = QPushButton("Show Data")
        self.button.setEnabled(False)
        self.button.setFixedSize(100, 20)

        # WebEngineView for data table
        self.web_engine = QWebEngineView()
        self.loadPage()

        # Add model_box and button to layout
        button_layout.addWidget(self.gen_box)
        button_layout.addWidget(self.year_box)
        button_layout.addWidget(self.mod_box)
        button_layout.addWidget(self.button)
        button_layout.addStretch(1)

        # Add widgets to main layout
        main_layout.addWidget(title)
        main_layout.addWidget(select)
        main_layout.addLayout(button_label_layout)
        main_layout.addLayout(button_layout)
        main_layout.addWidget(self.web_engine)

        # Create a central widget to hold the other widgets and layouts
        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

        # Connect the button to a function
        self.button.clicked.connect(self.on_button_click)
        self.gen_box.currentIndexChanged.connect(self.on_combo_change)
        self.year_box.currentIndexChanged.connect(self.on_combo_change)
        self.mod_box.currentIndexChanged.connect(self.on_combo_change)

    def on_button_click(self):
        # Get the selected model from the combobox and display its name
        combo_name = self.gen_box.currentText()
        combo_year = self.year_box.currentText()
        combo_mod = self.mod_box.currentText()

        # Name and Year together
        name_year = combo_name + ", " + combo_year

        # Create table for car data
        table_data = [[name_year, combo_mod],
              ['Model', '3 Series'],
              ['Generation', 'E46'],
              ['Modification', '320d'],
              ['Production<br>Years', '2001-05'],
              ['Fuel', 'Diesel'],
              ['HP', 150],
              ['Torque', '330 Nm'],
              ['0-100 km/h', '8.9 sec'],
              ['Top Speed', '221 km/h'],
              ['Avg.<br>Fuel Consumption', '5.5 L/km']]

        fig = ff.create_table(table_data, height_constant=60)

        # Show table in webengineview
        self.web_engine.setHtml(fig.to_html(include_plotlyjs='cdn'))


    def on_combo_change(self):
        # Enable the button when all options are selected
        if self.gen_box.currentIndex() != -1 and self.year_box.currentIndex() != -1 and self.mod_box.currentIndex() != -1:
            self.button.setEnabled(True)

        # Enable year_box when gen_box has a valid option
        if self.gen_box.currentIndex() != -1:
            self.year_box.setEnabled(True)
        else:
            self.year_box.setEnabled(False)

        # Enable mod_box when year_box has a valid option
        if self.year_box.currentIndex() != -1:
            self.mod_box.setEnabled(True)
        else:
            self.mod_box.setEnabled(False)

    # Source: https://zetcode.com/pyqt/qwebengineview/
    def loadPage(self):
        # Load initial webengineview page
        with open('test.html', 'r') as f:

            html = f.read()
            self.web_engine.setHtml(html)


# Create the application instance
app = QApplication(sys.argv)

# Create the main window
window = MainWindow()
window.show()

# Run the event loop
sys.exit(app.exec())

