import sys
import win32api
import win32con
import time

from PySide6.QtWidgets import QMainWindow, QApplication
from PySide6.QtNetwork import QTcpServer
from PySide6.QtCore import Slot

from threading import Thread, Event

from Server_form import Ui_MainWindow

class Mainwindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(Mainwindow, self).__init__()
        self.setupUi(self)
        self._clinet = None
        self.pushButton.clicked.connect(self.button_handler)
        self._server = QTcpServer()

        self._server.newConnection.connect(self.newConnection_handelr)
        self._server.listen(port = 9500)

        self._exit_event = Event()
        self._exit_event.clear()
        self._key_check_thread = Thread(target = self.key_check_proc)
        self._key_check_thread.start()

    def closeEvent(self, event) -> None:
        self._exit_event.set()
        return super().closeEvent(event)

    def key_check_proc(self):
        while self._exit_event.is_set() == False:
            if self.lineEdit.text():
                if win32api.GetAsyncKeyState(win32con.VK_RETURN) & 0x8000:
                    self.button_handler()
                    time.sleep(0.1)

    def disconnected_handler(self):
        self.label_1.setText(self.label_2.text())
        self.label_2.setText(self.label_3.text())
        self.label_3.setText(self.label_4.text())
        self.label_4.setText(self.label_5.text())
        self.label_5.setText("연결이 끊겼습니다 !")

    @Slot()
    def newConnection_handelr(self):
        self.label_1.setText(self.label_2.text())
        self.label_2.setText(self.label_3.text())
        self.label_3.setText(self.label_4.text())
        self.label_4.setText(self.label_5.text())
        self.label_5.setText("새로운 연결 감지 !")
        self._clinet = self._server.nextPendingConnection()
        self._clinet.disconnected.connect(self.disconnected_handler)
        self._clinet.readyRead.connect(self.client_readyRead_handler)
        
        
    @Slot()
    def client_readyRead_handler(self):
        if self._clinet.bytesAvailable:
            data = bytes(self._clinet.readAll())
            data = data.decode()
            self.label_1.setText(self.label_2.text())
            self.label_2.setText(self.label_3.text())
            self.label_3.setText(self.label_4.text())
            self.label_4.setText(self.label_5.text())
            self.label_5.setText(str(data))

    @Slot()
    def button_handler(self):
        text = self.lineEdit.text()
        self.label_1.setText(self.label_2.text())
        self.label_2.setText(self.label_3.text())
        self.label_3.setText(self.label_4.text())
        self.label_4.setText(self.label_5.text())
        self.label_5.setText(f"내가 보냄 : {text}")
        if self._clinet:
            self._clinet.write(f"서버에서 보냄 : {text}".encode())
        self.lineEdit.setText("")
        time.sleep(0.1)

    

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Mainwindow()
    window.show()
    app.exec()
