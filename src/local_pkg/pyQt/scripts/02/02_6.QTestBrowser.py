''' QTestBrowser의 주요 함수
==============================================
1. .toPlainTest()
: TextBrowser에 쓰여있는 글자를 가져옵니다.

2. .setPlainTest(string)
: TextBrowser에 새롭게 글자를 작성합니다. Parameter에는
TextBrowser에 표시할 글자가 들어갑니다.

3. .append(string)
: TextBrowser에 글자를 추가합니다. 추가된 글자는 다음 줄에 표시됩니다.

4. .clear()
: TextBrowser에 쓰여있는 글자를 지웁니다.

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
        self.btn_Print.clicked.connect(self.printTextFunction)
        self.btn_setText.clicked.connect(self.changeTextFunction)
        self.btn_appendText.clicked.connect(self.appendTextFunction)
        self.btn_Clear.clicked.connect(self.clearTextFunction)

    def printTextFunction(self) :
        #self.Textbrowser이름.toPlainText()
        #Textbrowser에 있는 글자를 가져오는 메서드
        print(self.textbrow_Test.toPlainText())

    def changeTextFunction(self) :
        #self.Textbrowser이름.setPlainText()
        #Textbrowser에 있는 글자를 가져오는 메서드
        self.textbrow_Test.setPlainText("This is Textbrowser - Change Text")

    def appendTextFunction(self) :
        #self.Textbrowser이름.append()
        #Textbrowser에 있는 글자를 가져오는 메서드
        self.textbrow_Test.append("Append Text")

    def clearTextFunction(self) :
        #self.Textbrowser.clear()
        #Textbrowser에 있는 글자를 지우는 메서드
        self.textbrow_Test.clear()

if __name__ == "__main__" :
    app = QApplication(sys.argv)
    myWindow = WindowClass()
    myWindow.show()
    app.exec_()