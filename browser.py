import requests
import urllib.parse

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtWebKit import *


class Browser:
    def __init__(self, url, params=None):
        self.app = QApplication([])
        self.win = QWidget()

        self.win.setWindowTitle('Authorization')
        self.layout = QVBoxLayout()
        self.win.setLayout(self.layout)

        self.web_view = QWebView()

        self.session = requests.Session()
        responce = self.session.get(url, params=params)
        self.web_view.setHtml(responce.text)

        self.web_view.urlChanged.connect(self.get_token)
        self.layout.addWidget(self.web_view)

        self.win.show()
        self.app.exec_()

    def get_token(self):
        url = self.web_view.url().toString()
        fragment = urllib.parse.urldefrag(url).fragment
        access_token = urllib.parse.parse_qs(fragment)['access_token'][0]
        user_id = urllib.parse.parse_qs(fragment)['user_id'][0]
        self.data = (access_token, user_id)
        self.app.exit()

if __name__ == "__main__":
    br = Browser("http://ya.ru")
