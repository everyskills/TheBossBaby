#!/usr/bin/python3

from PyQt5.QtGui import QFont, QHideEvent, QKeyEvent, QMouseEvent
from PyQt5.QtWidgets import QGridLayout, QWidget, QApplication, QLabel
from PyQt5.QtCore import QTimer, Qt

class TBB_Larg_Text(QWidget):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        QWidget.__init__(self)

        self.p = parent

        self.resize(800, 600)
        self.setWindowFlags(self.windowFlags() 
        | Qt.FramelessWindowHint)

        self.setWindowOpacity(0.8)
        
        self.setStyleSheet("""
        QWidget, #Form {
            padding: 6px 0px;
            border-radius: 8px;
            background-color: #0d0d0d;
        }
        """)
        
        ## Create Qt Widgetes
        self.glayout = QGridLayout(self)
        self.text = QLabel(self)
        self.timer = QTimer(self)
        self.font = QFont()

        ## Custom QLabel
        self.text.setAlignment(Qt.AlignCenter)

        self.glayout.addWidget(self.text, 0, 0, 0, 0, Qt.AlignCenter)
        self.setLayout(self.glayout)

    def larg_text(self, text: str, font_size: int=50, timeout: int=5000):
        try:
            self.text.setText(str(text))

            self.font.setBold(True)

            self.font.setPixelSize(font_size)
            self.text.setFont(self.font)
            
            self.timer.singleShot(int(timeout), self.close)
            self.p.hide()
            self.show()

        except Exception as err:
            print("Error-Larg-Text: ", str(err))

    def keyPressEvent(self, a0: QKeyEvent) -> None:
        self.close()

    def mousePressEvent(self, a0: QMouseEvent) -> None:
        self.close()

def main():
    app = QApplication([])
    win = TBB_Larg_Text()
    win.larg_text("Test Larg Text Ok")
    win.show()
    exit(app.exec_())

if __name__ == "__main__":
    main()
