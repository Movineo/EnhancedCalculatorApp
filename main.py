# Imports
from PyQt5.QtWidgets import QApplication, QWidget, QLineEdit, QLabel, QVBoxLayout, QPushButton, QHBoxLayout, QGridLayout, QCheckBox, QRadioButton, QComboBox, QSlider, QProgressBar, QScrollBar, QDial, QLCDNumber
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
import sys
import math

# App Settings
app = QApplication(sys.argv)
main_window = QWidget()
main_window.setWindowTitle("Enhanced Calculator")
main_window.setGeometry(100, 100, 600, 700)
main_window.setStyleSheet("background-color: #333333;")
main_window.show()
main_window.setLayout(QVBoxLayout())

# Display
lcd_display = QLCDNumber()
lcd_display.setDigitCount(10)
lcd_display.setSegmentStyle(QLCDNumber.Filled)
lcd_display.setStyleSheet("background-color: #FFFFFF; color: #000000;")
main_window.layout().addWidget(lcd_display)

# History Display
history_display = QLineEdit()
history_display.setReadOnly(True)
history_display.setAlignment(Qt.AlignRight)
history_display.setFont(QFont("Arial", 14))
main_window.layout().addWidget(history_display)

# Buttons
buttons = QWidget()
buttons.setLayout(QGridLayout())
main_window.layout().addWidget(buttons)

# Button Names
button_names = [
    "7", "8", "9", "/",
    "4", "5", "6", "*",
    "1", "2", "3", "-",
    "C", "0", "=", "+",
    "sqrt", "^", "%", "M+",
    "M-", "MR", "MC", "sin",
    "cos", "tan", "log", "ln",
    "!", "(", ")", " "
]

# Button Creation
row = 0
col = 0
for button_name in button_names:
    button = QPushButton(button_name)
    button.setStyleSheet("background-color: #666666; color: white;")
    button.setFont(QFont("Arial", 18))
    button.setFixedSize(80, 80)
    buttons.layout().addWidget(button, row, col)
    col += 1
    if col > 3:
        col = 0
        row += 1

# Memory variables
memory = 0

# Button Functionality
def on_button_click():
    global memory
    button = main_window.sender()
    button_text = button.text()
    display_text = history_display.text()
    
    if button_text == "C":
        lcd_display.display(0)
        history_display.setText("")
    elif button_text == "=":
        try:
            result = str(eval(display_text.replace('^', '**').replace('sqrt', 'math.sqrt')
                              .replace('sin', 'math.sin').replace('cos', 'math.cos')
                              .replace('tan', 'math.tan').replace('log', 'math.log10')
                              .replace('ln', 'math.log').replace('!', 'math.factorial')))
            history_display.setText(display_text + " = " + result)
            lcd_display.display(result)
        except Exception as e:
            history_display.setText("Error")
            lcd_display.display(0)
    elif button_text == "sqrt":
        history_display.setText(display_text + "sqrt(")
    elif button_text == "^":
        history_display.setText(display_text + "^")
    elif button_text == "%":
        history_display.setText(display_text + "*0.01")
    elif button_text == "M+":
        try:
            memory += float(display_text)
        except ValueError:
            history_display.setText("Error")
    elif button_text == "M-":
        try:
            memory -= float(display_text)
        except ValueError:
            history_display.setText("Error")
    elif button_text == "MR":
        history_display.setText(str(memory))
        lcd_display.display(memory)
    elif button_text == "MC":
        memory = 0
    elif button_text in ["sin", "cos", "tan", "log", "ln", "!"]:
        history_display.setText(display_text + button_text + "(")
    else:
        if display_text == "0":
            history_display.setText(button_text)
        else:
            history_display.setText(display_text + button_text)
        lcd_display.display(button_text)

for button in buttons.findChildren(QPushButton):
    button.clicked.connect(on_button_click)

# Slider for Font Size
def change_font_size(value):
    lcd_display.setFont(QFont("Arial", value))
    history_display.setFont(QFont("Arial", value - 10))

font_slider = QSlider(Qt.Horizontal)
font_slider.setRange(10, 40)
font_slider.setValue(24)
font_slider.valueChanged.connect(change_font_size)
main_window.layout().addWidget(font_slider)

# Theme ComboBox
def change_theme(value):
    themes = {
        "Dark": "#333333",
        "Light": "#FFFFFF",
        "Blue": "#0000FF",
        "Green": "#00FF00"
    }
    main_window.setStyleSheet(f"background-color: {themes[value]};")

theme_combo = QComboBox()
theme_combo.addItems(["Dark", "Light", "Blue", "Green"])
theme_combo.currentTextChanged.connect(change_theme)
main_window.layout().addWidget(theme_combo)

# Progress Bar
progress_bar = QProgressBar()
progress_bar.setRange(0, 100)
progress_bar.setValue(0)
main_window.layout().addWidget(progress_bar)

# Scroll Bar
scroll_bar = QScrollBar(Qt.Horizontal)
scroll_bar.setRange(0, 100)
scroll_bar.setValue(50)
scroll_bar.valueChanged.connect(lambda: lcd_display.display(scroll_bar.value()))
main_window.layout().addWidget(scroll_bar)

# Dial for Value Input
dial = QDial()
dial.setRange(0, 100)
dial.setValue(0)
dial.valueChanged.connect(lambda: lcd_display.display(dial.value()))
main_window.layout().addWidget(dial)

# Run the app
sys.exit(app.exec_())
