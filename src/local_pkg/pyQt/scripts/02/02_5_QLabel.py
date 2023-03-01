''' QLabel의 주요 함수
==============================================
1. .test()
: Label에 쓰여있는 글자를 가져옵니다.

2. setTest(string)
: Label에 새롭게 글자를 작성합니다. Parameter에는 Label에 표시할 글자가 입력됩니다.

3. .clear()
: Label에 쓰여있는 글자를 지웁니다.

==============================================
'''

import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic

form_class = uic.loadUiType("../../uis/test.ui")[0]

class WindowClass(QDialog, form_class) :
    def __init__(self) :
        super().__init__()
        self.setupUi(self)

        #버튼에 기능을 할당하는 코드
        self.btn_changeText.clicked.connect(self.changeTextFunction)
        self.btn_printText.clicked.connect(self.printTextFunction)

    def changeTextFunction(self) :
        #self.Label이름.setText("String")
        #Label에 글자를 바꾸는 메서드
        self.lbl_Test.setText("This is Label - Change Text")

    def printTextFunction(self) :
        #self.Label이름.text()
        #Label에 있는 글자를 가져오는 메서드
        print(self.lbl_Test.text())

if __name__ == "__main__" :
    app = QApplication(sys.argv)
    myWindow = WindowClass()
    myWindow.show()
    app.exec_()