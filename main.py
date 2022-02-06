import webbrowser
from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from os import path
from PyQt5.uic import loadUiType
from service import all_sales_report, open_report_dir
from services.configs.database import connect_db
import sys
import threading
import os
mydir = os.getcwd()

FORM_CLASS,_=loadUiType(path.join(path.dirname("__file__"), "main.ui"))
class Main(QMainWindow, FORM_CLASS,):
    def __init__(self, parent=None):
        super(Main, self).__init__(parent)
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.Handel_Buttons()
        self.open_dir = self.open_dir
        self.list_result = []
        # Database
        self.connections = { 'mysql': {'conn': None, 'msg': "Mysql -> CONECTING"} }
        self.thread_conn = threading.Thread(target=connect_db, args=(self,)).start()

    def Handel_Buttons(self):
        self.all_sales_generate_report_btn.clicked.connect(self.SALES_REPORT_ALL_CLIENT_FLEET)
    
    def SALES_REPORT_ALL_CLIENT_FLEET(self):
        all_sales_report(self)

    def open_dir(self):
        open_report_dir()
   
   
def main():
    app=QApplication(sys.argv)
    window=Main()
    window.show()
    app.exec_()

if __name__ == '__main__':
    main()