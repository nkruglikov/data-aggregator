from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtWebKit import *

class Browser:
    def __init__(self):
        self.app = QApplication([])
        self.win = QWidget()

        self.win.setWindowTitle('Authorization')
        self.layout = QVBoxLayout()
        self.win.setLayout(self.layout)

        self.web_view = QWebView()
        self.web_view.load(QUrl('http://ya.ru'))
        self.layout.addWidget(self.web_view)

        self.win.show()
        self.app.exec_()

br = Browser()
