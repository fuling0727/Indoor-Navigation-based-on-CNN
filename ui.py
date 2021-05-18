import sys
from PyQt5.QtGui import QPixmap, QIcon, QFont, QImage
from PyQt5.QtWidgets import QMainWindow, QApplication, QLabel, QPushButton, QWidget
from PyQt5 import QtCore
from project_combine import *
from voice_test import *
from recog_place import *
class MainWindow(QMainWindow):

    def __init__(self):
        load_model()
        voice_set()
        setWalkingPathLoaction()
        super(MainWindow, self).__init__()
        #self.setGeometry(400,400,320,200)
        self.resize(791,1136) # smart phone size
        self.setStyleSheet("background-color:#FFECEC;")
        self.title = "Indoor Navigation"
        self.setWindowTitle(self.title)
        #title label
        label1 = QLabel(self)
        label1.setText("Indoor Navigation")
        #label1.setGeometry(319,10,519,31)
        #label1.setFixedWidth(791)
        #label1.setFixedHeight(90)
        label1.setStyleSheet("background-color:#FFECEC; color:#FF9999; border-radius: 5px")
        myFont=QFont("Arial Font",15,QFont.Bold)
        label1.setFont(myFont)
        label1.resize(791,130)
        label1.setAlignment(QtCore.Qt.AlignCenter)
        label1.move(0,0)
        #label1.setGeometry(0,30,200,100)
        #map
        self.label2 = QLabel(self)
        pixmap = QPixmap('D:\\Project\\ui\\building_map.jpg')
        self.label2.resize(pixmap.width(),pixmap.height())
        self.label2.move(0,110)
        #label2.setGeometry(0,80,pixmap.width(),90+pixmap.height())
        self.label2.setPixmap(pixmap)
        #self.setCentralWidget(label)
        #destination
        self.label3 = QLabel(self)
        self.label3.setText("目的地: ")
        myFont=QFont("Arial Font",13,QFont.Bold)
        self.label3.setStyleSheet("background-color:#FFECEC; color:#FF9999;")
        self.label3.setFont(myFont)
        self.label3.resize(200,40)
        self.label3.move(270,600)
        #departure
        self.label4 = QLabel(self)
        self.label4.setText("出發地: ")
        myFont=QFont("Arial Font",13,QFont.Bold)
        self.label4.setStyleSheet("background-color:#FFECEC; color:#FF9999;")
        self.label4.setFont(myFont)
        self.label4.resize(200,40)
        self.label4.move(270,650)
        #error message
        self.label5 = QLabel(self)
        self.label5.setText("尚未輸入目的地")
        myFont=QFont("Arial Font",13,QFont.Bold)
        self.label5.setStyleSheet("background-color:#EA0000; color:#FCFCFC;border-radius: 5px")
        self.label5.setAlignment(QtCore.Qt.AlignCenter)
        self.label5.setFont(myFont)
        self.label5.resize(250,40)
        self.label5.move(290,500)
        self.label5.setVisible(False)
        #video
        self.label6 = QLabel(self)
        self.label6.resize(750,400)
        self.label6.move(20,580)
        self.label6.setStyleSheet("background-color:#050505; color:#050505;border-radius: 5px")
        self.label6.setVisible(False)
        
        
        button1 = QPushButton(self)#結束程式 back
        button1.setText("RESET")  # 建立名字
        button1.setStyleSheet("background-color:#FF9999; color:#FFFFFF; border-radius: 15px")
        button1.resize(80,30)
        button1.move(705,15)  # 移動位置
        button1.clicked.connect(self.button1Clicked)

        self.button2 = QPushButton(self) #語音
        self.button2.setIcon(QIcon('D:\\Project\\ui\\record.png'))
        self.button2.setIconSize(QtCore.QSize(60,60))
        self.button2.resize(70,70)
        self.button2.setStyleSheet("background-color:#FCFCFC; border-radius: 5px")
        self.button2.move(299,720)  # 移動位置
        self.button2.clicked.connect(self.button2Clicked)

        self.button3 = QPushButton(self) #camera
        self.button3.setIcon(QIcon('D:\\Project\\ui\\camera1.png'))
        self.button3.setIconSize(QtCore.QSize(55,55))
        self.button3.resize(70,70)
        self.button3.setStyleSheet("background-color:#FCFCFC; border-radius: 5px;")
        self.button3.move(439,720)  # 移動位置
        self.button3.clicked.connect(self.button3Clicked)

        self.button4 = QPushButton(self)
        self.button4.setText("Start Navigate")
        self.button4.resize(250,40)
        self.button4.setStyleSheet("background-color:#FF9999; color:#FFFFFF; border-radius: 20px")
        myFont=QFont("Arial Font",12,QFont.Bold)
        self.button4.setFont(myFont)
        self.button4.move(280,820)  # 移動位置
        self.button4.clicked.connect(self.button4Clicked)


    def button1Clicked(self): # reset
        print('click reset')
        var.isreset = 1
        reset()
        self.label3.setText("目的地: ")
        self.label4.setText("出發地: ")
        self.label3.setVisible(True)
        self.label4.setVisible(True)
        self.label6.setVisible(False)
        self.button2.setVisible(True)
        self.button3.setVisible(True)
        self.button4.setVisible(True)
        
        
    def button2Clicked(self): # 語音
        # voice
        var.isreset = 0
        voice_output('請說出目的地')
        voice_detect_destination()
        self.label3.setText("目的地: " + place[var.destination_index])
    
    def button3Clicked(self): # camera
        print('camera')
        var.isreset = 0
        capture = cv2.VideoCapture("D:/project/4202_start.mp4") #"D:/project/4202_start.mp4"
        c = 1
        time_F = 10
        
        while(capture.isOpened()):
            # 顯示影片
            ret, frame = capture.read()            
            rgbImage = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            convertToQtFormat = QImage(rgbImage.data, rgbImage.shape[1], rgbImage.shape[0], QImage.Format_RGB888)
            convertToQtFormat = QPixmap.fromImage(convertToQtFormat)
            self.label2.setPixmap(convertToQtFormat)
            
            if c % time_F == 0:
                check_start_place(frame)
            c = c + 1
            if ret == False or len(start_place) > 5:
                break
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            if var.isreset == 1:
                break
        if var.preindex != -1:
            self.label4.setText("出發地: "+ place[var.preindex])
        capture.release()
        # 影片圖像改回來
        pixmap = QPixmap('D:\\project\\ui\\building_map.jpg')
        self.label2.setPixmap(pixmap)

    def button4Clicked(self): # start navigate
        print('start navigation')
        var.isreset = 0
        
        if var.preindex == -1 and var.destination_index == -1:
            self.label5.resize(310,40)
            self.label5.move(260,500)
            self.label5.setText('尚未設置出發地與目的地')
            self.label5.setVisible(True)
            cv2.waitKey(1000)
            self.label5.setVisible(False)
        elif var.preindex == -1:
            self.label5.resize(250,40)
            self.label5.move(290,500)
            self.label5.setText('尚未設置出發地')
            self.label5.setVisible(True)
            cv2.waitKey(1000)
            self.label5.setVisible(False)
        elif var.destination_index == -1:
            self.label5.resize(250,40)
            self.label5.move(290,500)
            self.label5.setText('尚未設置目的地')
            self.label5.setVisible(True)
            cv2.waitKey(1000)
            self.label5.setVisible(False)
        else:
            self.label3.setVisible(False)
            self.label4.setVisible(False)
            self.label6.setVisible(True)
            self.button2.setVisible(False)
            self.button3.setVisible(False)
            self.button4.setVisible(False)
            capture = cv2.VideoCapture("D:/project/4202_current.mp4") #"D:/project/4202_start.mp4"
            c = 1
            time_F = 40
        
            while(capture.isOpened()):
                # 顯示影片
                ret, frame = capture.read()            
                rgbImage = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                convertToQtFormat = QImage(rgbImage.data, rgbImage.shape[1], rgbImage.shape[0], QImage.Format_RGB888)
                convertToQtFormat = QPixmap.fromImage(convertToQtFormat)
                self.label6.setPixmap(convertToQtFormat)
                if c % time_F == 0:
                    check_current_place(frame)       
                    map_show()
                    
                    img = cv2.imread("D:\\project\\ui\\building_map.jpg")
                    cv2.circle(img,(var.centerx, var.centery),3,(0,0,0), -1)
                    rgbImage = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                    convertToQtFormat = QImage(rgbImage.data, rgbImage.shape[1], rgbImage.shape[0], rgbImage.shape[1]*rgbImage.shape[2], QImage.Format_RGB888)
                    convertToQtFormat = QPixmap.fromImage(convertToQtFormat)
                    self.label2.setPixmap(convertToQtFormat)
                    
                c = c + frame_correction
                if ret == False:
                    break
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
                if var.isreset == 1:
                    break
            if var.preindex != -1:
                self.label4.setText("出發地: "+ place[var.preindex])
            capture.release()
            self.label6.setStyleSheet("background-color:#050505; color:#050505;border-radius: 5px")
            reset()
            self.label3.setText("目的地: ")
            self.label4.setText("出發地: ")
            self.label3.setVisible(True)
            self.label4.setVisible(True)
            self.label6.setVisible(False)
            self.button2.setVisible(True)
            self.button3.setVisible(True)
            self.button4.setVisible(True)


app = QApplication(sys.argv)
w = MainWindow()
w.show()
sys.exit(app.exec_())