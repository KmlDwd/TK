from PyQt5.QtWidgets import QApplication, QMainWindow
from . import Window
import sys


def main():
    app = QApplication(sys.argv)
    window = Window()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()

