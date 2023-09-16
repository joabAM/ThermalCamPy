from PyQt4.QtCore import *
from PyQt4.QtGui  import *
import sys
import num_recog as nr
import cv2
import numpy as np
import os
import math as mt

path=""
pp = False
barra = 0
nframes = 0
count = 0

class Ventana(QMainWindow):

    def __init__(self,parent=None):

        super(Ventana, self).__init__(parent)
        self.setWindowTitle("Visor Termico")

        tb = QMainWindow.addToolBar(self,"File")
        self.abrir = QAction(QIcon("open.png"),"abrir",self)
        tb.addAction(self.abrir)
        tb.actionTriggered[QAction].connect(self.abrirPath)

        self.mywid = MainWidget(self)
        self.setCentralWidget(self.mywid)

    def abrirPath(self):
        self.fvideo = QFileDialog.getOpenFileName(self,'Abrir Video','C:\\',"Video files (*.avi)")
        path = os.path.normpath(self.fvideo)
        path = self.fvideo
        print(path,type(path))
        self.mywid.getVideo(path)

class MainWidget(QWidget):

    def __init__(self,parent):

        super(MainWidget,self).__init__(parent)
        self.pr = False
        self.q = 1
        self.tym = 80
        valueChanged = pyqtSignal(object)
        self.layout1 = QVBoxLayout(self)
        self.layout2 = QHBoxLayout(self)
        self.layout3 = QHBoxLayout(self)
        self.layout4 = QVBoxLayout(self)
        self.layout5 = QHBoxLayout(self)

        self.layout6 = QHBoxLayout(self)
        self.layout7 = QHBoxLayout(self)
        self.layout8 = QHBoxLayout(self)
        self.temp = QPushButton()
        self.temp.setIcon(QIcon(QPixmap(("thm.png"))))
        self.temp.setIconSize(QSize(44,44))


        self.tA = 0
        self.tB = 0
        self.T = QLabel("      ")

        self.TambText = QLabel(self)
        self.TambText.setText('T Ambiente:')
        self.T_amb_in = QLineEdit(self)
        self.T_amb_in.setText("25")


        self.EmText = QLabel(self)
        self.EmText.setText('Emisividad:')
        self.Emi_in = QLineEdit(self)
        self.Emi_in.setText("0.96")


        self.Dist = QLabel(self)
        self.Dist.setText('Distancia(cm):')
        self.Dist_in = QLineEdit(self)
        self.Dist_in.setText("100.0")


        self.Reg = QComboBox()
        self.Reg.addItems(['Ecuación Polinomial','Ecuación Plank'])

        self.img = QLabel()
        self.im = QImage(704,480,QImage.Format_RGB888)

        self.br=QRadioButton("Mostrar máx y min")
        self.br.setChecked(True)

        self.cr = QPushButton()
        self.cr.setText("Correcciones activas")


        self.speed=QSlider(Qt.Vertical)
        self.speed.setMinimum(0)
        self.speed.setMaximum(160)
        self.speed.setValue(80)

        self.speed.setTickPosition(QSlider.TicksBelow)
        self.speed.setTickInterval(40)
        self.speed.valueChanged.connect(self.velVideo)
        self.x = 0
        self.y = 0

        self.nroEcuacion = 0;
        self.Reg.currentIndexChanged.connect(self.selEcuacion)

        self.mostrarMinMax = True
        self.p = QPushButton(self)
        self.sp = QSlider(Qt.Horizontal)

        self.p.setCheckable(True)
        self.p.toggle()

        self.temp.clicked.connect(self.addPunto)
        self.p.clicked.connect(self.playVideo)
        self.sp.valueChanged.connect(self.slider)

        self.cr.clicked.connect(self.correcciones)
        self.layout2.addWidget(self.img)

        self.layout5.addWidget(self.temp)
        self.layout5.addWidget(self.T)

        self.layout6.addWidget(self.TambText)
        self.layout6.addWidget(self.T_amb_in)

        self.layout7.addWidget(self.EmText)
        self.layout7.addWidget(self.Emi_in)

        self.layout8.addWidget(self.Dist)
        self.layout8.addWidget(self.Dist_in)

        self.layout4.addLayout(self.layout5)
        self.layout4.addWidget(self.Reg)
        self.layout4.addLayout(self.layout6)
        self.layout4.addLayout(self.layout7)
        self.layout4.addLayout(self.layout8)
        self.layout4.addWidget(self.cr)
        self.layout4.addStretch()
        self.layout4.addWidget(self.br)
        self.layout4.addWidget(self.speed)
        self.layout2.addLayout(self.layout4)

        self.layout3.addWidget(self.p)
        self.layout3.addWidget(self.sp)


        self.layout1.addLayout(self.layout2)
        self.layout1.addLayout(self.layout3)


        self.setLayout(self.layout1)

        self._timer = QTimer(self)
        self._timer.timeout.connect(self.setframes)




    def getVideo(self, path):
        global nframes
        self.vid = cv2.VideoCapture(path)
        nframes = self.vid.get(cv2.CAP_PROP_FRAME_COUNT)
        print(nframes)
        self.sp.setMinimum(0)
        self.sp.setMaximum(nframes)


    def velVideo(self):
        if self._timer.isActive():
            self._timer.stop()
            self.tym = mt.fabs(self.speed.value() - 160)
            print("intervalo",self.tym)
            self._timer.start(self.tym)
        else:
            self.tym = mt.fabs(self.speed.value() - 160)
            print("interval",self.tym)

    def playVideo(self):
        global pp

        if  pp :
            pp = False
            self._timer.start(self.tym)
            self.p.setIcon(QIcon("pause.png"))
            self.p.setIconSize(QSize(34,34))
        else:
            pp = True
            self._timer.stop()
            self.p.setIcon(QIcon("play.png"))
            self.p.setIconSize(QSize(34,34))
        print(pp)

    def addPunto(self):
        if self.pr:
            self.pr = False
        else:
            self.pr = True
    def correcciones(self):
        if self.q:
            self.q = False
            self.cr.setText("correcciones desactivadas")
        else:
            self.q = True
            self.cr.setText("correcciones activadas")

    def selEcuacion(self,k):
        self.nroEcuacion = k
        if k :
            print("Ecuación de Plank") #igual a 1
        else :
            print("Ecuación Polinomial")#igual a 0

    def slider(self):
        global count
        if self.sp.value() == count :
            pass
        else :
            count = self.sp.value()
            self.sp.setValue(count)


    def setframes(self):
        global nframes
        global count
        count += 1
        self.vid.set(cv2.CAP_PROP_POS_FRAMES,count)
        self.ret,self.frame = self.vid.read()
        self.f = nr.recortaImagen(self.frame)
        self.minT, self.maxT = nr.extrae_numeros(self.frame)
        print("valores:",self.minT,self.maxT,self.x,self.y)
        if self.pr:
            self.f = nr.punto_caliente(self.f)

        self.T.setText( str('%.3f'%((nr.pixel_Temp(self.f,self.frame,self.tA, self.tB, self.x, self.y,self.nroEcuacion,self.Emi_in.text(),self.T_amb_in.text())))))
        if self.br.isChecked():
            self.f,self.tA,self.tB = nr.agrega_temperatura(self.f, self.minT, self.maxT,self.nroEcuacion, self.Emi_in.text(),self.T_amb_in.text(),self.q, self.Dist_in.text())

        self.f = nr.cursor(self.f,self.x,self.y)
        self.f = cv2.cvtColor(self.f, cv2.COLOR_BGR2RGB)
        self.im = QImage(self.f, self.f.shape[1], self.f.shape[0], QImage.Format_RGB888)
        self.pix = QPixmap.fromImage(self.im)


        self.img.setScaledContents(True);
        self.img.setPixmap(self.pix)

        self.img.setObjectName("img")
        self.img.mousePressEvent = self.getPos  #no lleva parentesis - evento

        self.sp.setValue(count)
        if count >= nframes-1 :
            count = 0
            self._timer.stop()
            self.vid.set(cv2.CAP_PROP_POS_FRAMES,count)


    def getPos(self , event):
        self.x = event.pos().x()
        self.y = event.pos().y()
        print (self.x, self.y)




def main():
    app = QApplication(sys.argv)
    win = Ventana()
    win.setGeometry(100,100,500,500)
    win.setWindowTitle("VideoVisorTermico")
    win.show()
    app.exec_()

if __name__ == "__main__" :

     sys.exit(main())
