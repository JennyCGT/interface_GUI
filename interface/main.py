import pathlib
import sys
# from PyQt5 import (QtCore, QtWidgets, QtGui)
from threading import Thread, Lock, Event
from PyQt5.QtCore import QTimer, Qt, pyqtSlot, QTime, QDateTime, QEvent
from PyQt5.QtWidgets import (QApplication, QListWidget, QDateTimeEdit,QMenu,
         QGridLayout,  QHBoxLayout, QLabel, QDialog,QMainWindow,
        QPushButton, QTableWidget, QTableWidgetItem,QAbstractItemView ,
        QVBoxLayout, QWidget,QMessageBox)
from PyQt5.QtGui import QFont, QIcon
from datetime import datetime
import requests
stop_threads = False
stop_threads_1 = False 
frame = ''

URL = 'https://swapi.dev/api/people/'
class Screen(QMainWindow):
    def __init__(self, *args, **kwargs):
        # super(Screen, self).__init__(parent)
        super(Screen, self).__init__(*args, **kwargs)
        self.widget = QWidget()
        self.ui = self.principal_box()
        self.names = []
        timer1 = QTimer(self, interval=1000, timeout=self.showTime)
        timer1.start()
        self.showTime()
        self.widget.setLayout(self.ui)
        self.setWindowTitle('Postulante para ROBOTILSA S.A')
        self.resize(800,600)
        self.setCentralWidget(self.widget)
        self.widget.setAttribute(Qt.WA_DeleteOnClose)



    # ----------------------BOX LEFT--------------------------------------------------
    def principal_box(self):
        date_now = datetime.now()
        self.date_actual = QLabel(date_now.strftime('%d/%m/%Y'))
        self.date_actual.setAlignment(Qt.AlignCenter)
        self.date_actual.setFont(QFont ("Times",30,weight=QFont.Bold))

        self.hour_actual = QLabel(date_now.strftime('%H:%M:%S'))
        self.hour_actual.setAlignment(Qt.AlignCenter)
        self.hour_actual.setFont(QFont("Times",35,weight=QFont.Bold))
        self.connect_button = QPushButton('REQUEST')
        self.connect_button.setIcon(QIcon("assets/icons8-url-64.png"))
        self.connect_button.setStyleSheet("font-family:Times New Roman;")
        self.connect_button.setFixedSize(300,70)
        self.connect_button.clicked.connect(self.onConnect)


        self.tableWidget = QListWidget()
        self.tableWidget.installEventFilter(self)

        grid = QGridLayout()
        grid.addWidget(self.tableWidget, 0, 0,3,1)
        grid.addWidget(self.date_actual, 0, 1,1,1)
        grid.addWidget(self.hour_actual, 1, 1,1,1)
        grid.addWidget(self.connect_button, 2, 1,2,1)
        grid.setRowStretch(0,1)
        grid.setRowStretch(1,1)
        grid.setRowStretch(2,2)
        grid.setColumnStretch(0,1)        
        grid.setColumnStretch(1,1)        
        return grid
    #---------------------- FUNCTIONS -------------------------------------------------
    def showDialog(self, text):
        msgBox = QMessageBox()
        msgBox.setIcon(QMessageBox.Information)
        msgBox.setWindowTitle("Alert")
        msgBox.setText(text)
        msgBox.setStandardButtons(QMessageBox.Ok )

        returnValue = msgBox.exec()

    def onConnect(self, event):
        try:
            self.tableWidget.clear()
            for x in range(10):
                r = requests.get(URL+str(x+1))
                data = dict(r.json())
                self.names.append(data) 
                row = self.tableWidget.insertItem(x, data['name'] )
                # cell = QTableWidgetItem(data['name'])
                # print(data['name'], type(data['name']))
                # self.tableWidget.setItem(row, 0, cell)
            # print(r.json())
        except requests.exceptions.Timeout:
            print('timeout')
            # Maybe set up for a retry, or continue in a retry loop
        except requests.exceptions.TooManyRedirects:
            # Tell the user their URL was bad and try a different one
            print('redirect')
        except requests.exceptions.RequestException as e:
            # catastrophic error. bail.
            raise SystemExit(e)


    def eventFilter(self, source, event):
        if(event.type() == QEvent.ContextMenu and
           source is self.tableWidget):
            menu = QMenu()
            menu.addAction('Información del personaje')
            if menu.exec_(event.globalPos()):
                item = source.itemAt(event.pos())
                print(item.text())
                self.dialog =QDialog()
                self.dialog.setWindowTitle("Ventana secundaria")
                self.dialog.setFixedSize(200, 500)
                self.box = self.dialog_table(item)
                self.dialog.setLayout(self.box)
                self.dialog_table(item)
                self.dialog.show()
            return True
        return super(Screen, self).eventFilter(source, event)

    def dialog_table(self, data):
        data = ['height', 'mass','hair_color','skin_color','eye_color','birth_year','gender']
        layout = QVBoxLayout()
        information = self.search(data)
        for x in data:
            layout1 = QHBoxLayout()
            label = QLabel(x)
            label.setFont(QFont("Times",12,weight=QFont.Bold))
            layout1.addWidget(label)
            layout1.addStretch(1)
            layout1.addWidget(QLabel(information[x]))
            layout.addLayout(layout1)
        return layout

    def search(self, name):
        for x in self.names:
            return x

    @pyqtSlot()
    def showTime(self):
        time = QTime.currentTime()
        date = QDateTime.currentDateTime()
        hour = time.toString("HH mm ss" if time.second() % 2 == 0 else "HH:mm:ss")
        date = date.toString("d/MM/yyyy")
        self.hour_actual.setText(hour)
        self.date_actual.setText(date)



def main():
    global stop_threads, frame
    app = QApplication(sys.argv)
    frame = Screen()
    frame.show()

    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
