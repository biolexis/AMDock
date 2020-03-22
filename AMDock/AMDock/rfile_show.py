from PyQt4.QtGui import *
from PyQt4.QtCore import *


class Result_File(QDialog):
    def __init__(self, parent=None):
        QDialog.__init__(self,parent)
        self.parent = parent

        self.setWindowTitle('AMDock: File Result')
        self.setWindowIcon(QIcon(QPixmap("amdock_icon.png")))

        layout = QVBoxLayout()
        self.label = QLabel(self)
        self.label.setObjectName("label")
        self.label.setText('<html><head/><body><p><span style="font-size:20pt;font-weight:600;font-family:times new '
                           'roman; text-decoration: underline; color:#000000;">AMDock</span><br><span style=" '
                           'color:#000000;font-size:14pt;font-family:times">  Assisted Molecular Docking with'
                           ' AutoDock4 and AutoDock Vina</span></p></body></html>')
        self.label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.label)
        layout.addSpacing(35)

        font = QFont('Courier New')
        font.setKerning(False)
        self.textedit = QTextEdit(self)
        self.textedit.setMinimumSize(680, 480)
        self.textedit.ensureCursorVisible()
        self.textedit.setLineWrapMode(QTextEdit.NoWrap)
        self.textedit.setTextInteractionFlags(Qt.NoTextInteraction)
        self.textedit.setFont(font)
        self.textedit.setReadOnly(True)
        layout.addWidget(self.textedit)
        self.setLayout(layout)
        self.finished.connect(self.finish)

    def finish(self):
        self.parent.only_one = 0
