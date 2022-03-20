""" Application gui """

class Window(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setGeometry(300, 300, 600, 400)
        self.setWindowTitle("Welcome")
        self.show()