import sys
import win32api
import win32con
import time

from PySide6.QtWidgets import QMainWindow, QApplication
from PySide6.QtNetwork import QTcpSocket
from PySide6.QtCore import Slot

from threading import Thread, Event

from Client_form import Ui_MainWindow

class Mainwindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(Mainwindow, self).__init__()
        self.setupUi(self)
        self._ip = "000.000.000.000"
        self.pushButton.clicked.connect(self.button_handler)
        
        self._sock = QTcpSocket()
        self._sock.connectToHost(self._ip,  9500)
        self._sock.readyRead.connect(self.readyRead_handler)
        self._sock.errorOccurred.connect(self.error_handler)
        self._sock.connected.connect(self.connected_handler)

        self._exit_event = Event()
        self._exit_event.clear()
        self._key_check_thread = Thread(target = self.key_check_proc)
        self._key_check_thread.start()

    def key_check_proc(self):
        while self._exit_event.is_set() == False:
            if self.lineEdit.text():
                if win32api.GetAsyncKeyState(win32con.VK_RETURN) & 0x8000:
                    self.button_handler()
                    time.sleep(0.1)
                    

    @Slot()
    def connected_handler(self):
        self.label_1.setText(self.label_2.text())
        self.label_2.setText(self.label_3.text())
        self.label_3.setText(self.label_4.text())
        self.label_4.setText(self.label_5.text())
        self.label_5.setText("연결 되었습니다 !")

    @Slot(QTcpSocket.SocketError)
    def error_handler(self, error_code : QTcpSocket.SocketError):
        if error_code == QTcpSocket.SocketError.ConnectionRefusedError:
            self.label_1.setText(self.label_2.text())
            self.label_2.setText(self.label_3.text())
            self.label_3.setText(self.label_4.text())
            self.label_4.setText(self.label_5.text())
            self.label_5.setText("연결 중입니다 . . ")
            self._sock.connectToHost(self._ip, 9500)

    @Slot()
    def readyRead_handler(self):
        if self._sock.bytesAvailable():
            data = bytes(self._sock.readAll())
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
        self._sock.write(f"클라이언트에서 보냄 : {text}".encode())
        self.lineEdit.setText("")
        time.sleep(0.1)

    def closeEvent(self, event) -> None:
        self._sock.disconnectFromHost()
        self._exit_event.set()
        return super().closeEvent(event)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Mainwindow()
    window.show()
    app.exec()
