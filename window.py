import sys

from PyQt6.QtCore import QUrl, Qt
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QLabel, QWidget, QComboBox, QGridLayout
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtGui import QIcon
import plotly.figure_factory as ff
import sqlite3
import os
import pandas as pd

# Subclass QMainWindow to customize your application's main window
class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.years = None

        self.setWindowTitle("BMW Data")
        self.setWindowIcon(QIcon("icon.png"))

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
        select = QLabel("Select a BMW 3 Series specification")
        select.setStyleSheet("QLabel{font-size: 12pt;}")
        select.setAlignment(Qt.AlignmentFlag.AlignTop)

        # Grid layout for combo boxes and their labels
        grid = QGridLayout()
        grid.setAlignment(Qt.AlignmentFlag.AlignLeft)

        # Button label layout and labels
        generation = QLabel("Generation:")
        generation.setAlignment(Qt.AlignmentFlag.AlignLeft)
        year = QLabel("Year:")
        year.setAlignment(Qt.AlignmentFlag.AlignLeft)
        mod = QLabel("Modification:")
        mod.setAlignment(Qt.AlignmentFlag.AlignLeft)

        grid.addWidget(generation, 0, 0)
        grid.addWidget(year, 0, 1)
        grid.addWidget(mod, 0, 2)

        # Combo box for model generations
        self.gen_box = QComboBox()
        self.gen_box.setFixedSize(100, 20)
        self.gen_box.addItem("E46")
        self.gen_box.addItem("E90")
        # Set default value as empty
        self.gen_box.setCurrentIndex(-1)

        # Combo box for year
        self.year_box = QComboBox()
        self.year_box.setFixedSize(100, 20)
        self.year_box.setEnabled(False)

        # Combo box for modification
        self.mod_box = QComboBox()
        self.mod_box.setFixedSize(100, 20)
        self.mod_box.setEnabled(False)

        self.button = QPushButton("Show Data")
        self.button.setEnabled(False)
        self.button.setFixedSize(100, 20)

        self.clear_button = QPushButton("Clear")
        self.clear_button.setEnabled(False)
        self.clear_button.setFixedSize(100, 20)

        # WebEngineView for data table
        self.web_engine = QWebEngineView()
        self.loadPage()

        # Add model_box and button to layout
        grid.addWidget(self.gen_box, 1, 0)
        grid.addWidget(self.year_box, 1, 1)
        grid.addWidget(self.mod_box, 1, 2)
        grid.addWidget(self.button, 1, 3)
        grid.addWidget(self.clear_button, 1, 4)

        # Add widgets to main layout
        main_layout.addWidget(title)
        main_layout.addWidget(select)
        main_layout.addLayout(grid)
        main_layout.addWidget(self.web_engine)

        # Create a central widget to hold the other widgets and layouts
        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

        # Connect the button to a function
        self.button.clicked.connect(self.on_button_click)
        self.clear_button.clicked.connect(self.clear)
        self.gen_box.currentIndexChanged.connect(self.on_gen_change)
        self.year_box.currentIndexChanged.connect(self.on_year_change)
        self.mod_box.currentIndexChanged.connect(self.on_mod_change)

    def on_button_click(self):
        # Get the selected model from the combobox and display its name
        combo_gen = self.gen_box.currentText()
        combo_year = self.year_box.currentText()
        combo_mod = self.mod_box.currentText()
        data = self.find_data(combo_gen, combo_year, combo_mod)

        # Create a table for the car data
        # Source: https://plotly.com/python/table/


        # Name and Year together
        name_year = combo_gen + ", " + combo_year

    # Create table for car data
        table_data = [[name_year, combo_mod],
              ['Model', '3 Series'],
              ['Generation', combo_gen],
              ['Modification', data[0]],
              ['Production<br>Years', data[1]],
              ['Fuel', data[2]],
              ['HP', data[3] + ' hp'],
              ['Torque', data[4] + ' Nm'],
              ['0-100 km/h', data[5] + ' s'],
              ['Top Speed', data[6] + ' km/h'],
              ['Avg.<br>Fuel Consumption', data[7] + ' l/100km']]

        fig = ff.create_table(table_data, height_constant=60)

        # Show table in webengineview
        self.web_engine.setHtml(fig.to_html(include_plotlyjs='cdn'))

        self.clear_button.setEnabled(True)
    def on_gen_change(self):
        # If the generation is E46 get all the years from the database for the E46
        # Make them a set so that they do not repeat and add them to the year_box
        # Else, select the years for the E90 and add them to the year_box
        if self.gen_box.currentText() == "E46":
            # Clear the year_box
            self.year_box.clear()
            # Connect to database
            basedir = os.path.abspath(os.path.dirname(__file__))
            conn = sqlite3.connect(os.path.join(basedir, 'bmw_data.db'))
            # Get a list of the values in the db
            # Source: https://stackoverflow.com/questions/2854011/get-a-list-of-field-values-from-pythons-sqlite3-not-tuples-representing-rows 
            conn.row_factory = lambda cursor, row: row[0]
            cursor = conn.cursor()
            # Select all years from the E46 Table
            cursor.execute("SELECT Production FROM E46")
            # Make the years a set, so that they do not repeat
            self.years = set(cursor.fetchall())
            # Add these years to the year combo box
            for i in self.years:
                self.year_box.addItem(i)
            self.year_box.setCurrentIndex(-1)
            self.year_box.setEnabled(True)

        else:
            # Clear the year_box
            self.year_box.clear()
            # Connect to database
            basedir = os.path.abspath(os.path.dirname(__file__))
            conn = sqlite3.connect(os.path.join(basedir, 'bmw_data.db'))
            # Get a list of the values in the db
            # Source: https://stackoverflow.com/questions/2854011/get-a-list-of-field-values-from-pythons-sqlite3-not-tuples-representing-rows 
            conn.row_factory = lambda cursor, row: row[0]
            cursor = conn.cursor()
            # Select all years from the E90 Table
            cursor.execute("SELECT Production FROM E90")
            # Make the years a set, so that they do not repeat
            self.years = set(cursor.fetchall())
            # Add these years to the year combo box
            for i in self.years:
                self.year_box.addItem(i)
            self.year_box.setCurrentIndex(-1)
            self.year_box.setEnabled(True)

    def on_year_change(self):
        if self.year_box.currentText() != "":
            # If the gen box is not empty, get the current generation
            # Get the current generation 
            if self.gen_box.currentText() == "E46" or self.gen_box.currentText() == "E90":
                generation = self.gen_box.currentText()
                # For current year, get all the modifications from the database and add them to the mod_box
                # Once a year is selected, enable the mod_box
                # But if the year is not selected, disable the mod_box
                # Connect to database
                basedir = os.path.abspath(os.path.dirname(__file__))
                conn = sqlite3.connect(os.path.join(basedir, 'bmw_data.db'))
                # Get a list of the values in the db
                # Source: https://stackoverflow.com/questions/2854011/get-a-list-of-field-values-from-pythons-sqlite3-not-tuples-representing-rows
                conn.row_factory = lambda cursor, row: row[0]
                cursor = conn.cursor()
                # Select all modifications for the current year
                cursor.execute("SELECT Modification FROM " + generation + " WHERE Production = ?", (self.year_box.currentText(),))
                # Make the modifications a set, so that they do not repeat
                mods = set(cursor.fetchall())
                # Add these modifications to the mod combo box
                for i in mods:
                    self.mod_box.addItem(i)
                self.mod_box.setCurrentIndex(-1)
                self.mod_box.setEnabled(True)
            # Else return nothing so that clear works properly
            # When the combo boxes are cleared in the clear method, the year_box and mod_box combo boxes are reset, 
            # which may trigger the on_year_change method.
            else:
                return
        else:
            self.mod_box.clear()
            self.mod_box.setEnabled(False)
            self.button.setEnabled(False)

    def on_mod_change(self):
        # Enable the button when all options are selected
        if self.gen_box.currentIndex() != -1 and self.year_box.currentIndex() != -1 and self.mod_box.currentIndex() != -1:
            self.button.setEnabled(True)
        else:
            self.button.setEnabled(False)

    # Source: https://zetcode.com/pyqt/qwebengineview/
    def loadPage(self):
        # SHow the initial.html file in the QWebEngineView
        url = QUrl.fromLocalFile("/initial.html")
        self.web_engine.load(url)

    def clear(self):
        # Clear all combo boxes and disable the button
        self.gen_box.setCurrentIndex(-1)
        self.year_box.setCurrentIndex(-1)
        self.mod_box.setCurrentIndex(-1)
        self.button.setEnabled(False)

        # Disable year_box and mod_box
        self.year_box.setEnabled(False)
        self.mod_box.setEnabled(False)

        # Load the initial.html file
        self.loadPage()    

    def find_data(self, gen, year, mod):
        # Connect to database
        basedir = os.path.abspath(os.path.dirname(__file__))
        conn = sqlite3.connect(os.path.join(basedir, 'bmw_data.db'))
        cursor = conn.cursor()
        # Get the data from the database
        if gen == "E46":
        # Select the data from the table (gen) where the year is 2001-05 and the model is 320d
            # Source: https://stackoverflow.com/a/21734918/24109934 
            cursor.execute("SELECT * FROM E46 WHERE Production = ? AND Modification = ?", (year, mod))
        else:
            cursor.execute("SELECT * FROM E90 WHERE Production = ? AND Modification = ?", (year, mod))
        data = cursor.fetchall()
        # Result list of strings
        new_data = []
        for i in data[0]:
            new_data.append(str(i))
        return new_data


# Create the application instance
app = QApplication(sys.argv)

# Create the main window
window = MainWindow()
window.show()

# Run the event loop
sys.exit(app.exec())

