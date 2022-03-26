from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel, QFileDialog


class SelectDirectoryWidget(QWidget):
    def __init__(self, parent=None):
        super(SelectDirectoryWidget, self).__init__(parent)

        layout = QVBoxLayout()
        self.btn = QPushButton("Select directory")
        self.btn.clicked.connect(self.get_directory)
        self.label = QLabel('Selected directory: ')
        layout.addWidget(self.btn)
        layout.addWidget(self.label)
        self.setLayout(layout)

    def get_directory(self):
        dir_name = QFileDialog.getExistingDirectory(self, 'Select directory')
        self.label.setText('Selected directory: ' + dir_name)

