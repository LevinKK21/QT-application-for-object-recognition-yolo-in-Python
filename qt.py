# -*- coding: utf-8 -*-
"""
Created on Wed Dec 28 21:49:10 2022

@author: LKK
"""

from serial.tools import list_ports
import serial
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QDate
import serial
import sys
import glob
from PyQt5 import QtCore,QtMultimedia
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtMultimediaWidgets import QVideoWidget
import cv2 as cv
import time






Form, Window = uic.loadUiType("nero.ui")


translate = QtCore.QCoreApplication.translate


app = QApplication([])
window = Window()
form = Form()

form.setupUi(window)
name=""
window.show()


#       Диалоговое окнно

def dialog():
    file = QFileDialog.getOpenFileName(None,"",'/Users/LKK/Desktop/учеба/диплом/нс')
    Name = file[0]
    splitname = Name.split("/")
    filename = splitname[len(splitname)-1]
    print (filename)
    return filename  






print(form.comboBox.currentIndex())
#       Пуск с файло нейронки
def pusk1():
    name = dialog()
    if form.comboBox.currentIndex() == 1:
         weights = 'war-obj_best.weights'
         cfg = 'war-obj.cfg'
         names = 'war.names'
    elif form.comboBox.currentIndex() == 0:
         weights = 'ship-obj_last.weights'
         cfg = 'war-obj.cfg'
         names = 'ship.names'
    index2 = form.comboBox_2.currentIndex()+1
    Conf_threshold,NMS_threshold = index2/10,index2/10
    print(str(Conf_threshold))
        
        

    COLORS = [(255, 0, 0), (0, 0, 255), (0, 255, 0),
              (255, 255, 0), (255, 0, 255), (0, 255, 255)]

    class_name = []
    with open(names, 'r') as f:
        class_name = [cname.strip() for cname in f.readlines()]
    # print(class_name)
    net = cv.dnn.readNet(weights, cfg)
    net.setPreferableBackend(cv.dnn.DNN_BACKEND_OPENCV)
    net.setPreferableTarget(cv.dnn.DNN_TARGET_CPU)

    model = cv.dnn_DetectionModel(net)
    model.setInputParams(size=(416, 416), scale=1/255, swapRB=True)


    cap = cv.VideoCapture(name)##########################пуск имени файла
    starting_time = time.time()
    frame_counter = 0
    while True:
        ret, frame = cap.read()
        frame_counter += 1
        if ret == False:
            break
        classes, scores, boxes = model.detect(frame, Conf_threshold, NMS_threshold)
        list=[]
        i=0
        for (classid, score, box) in zip(classes, scores, boxes):
            #print(class_name[classid])
            
            x_centr,y_centr =int( round((box[0]+box[2]/2),0)),int( round((box[1]+box[3]/2),0))
            centr=[class_name[classid]+str(i),x_centr,y_centr]
            
            #print(box)
            list.append(centr)
            
            color = COLORS[int(classid) % len(COLORS)]
            label = "%s : %f" % (class_name[classid]+str(i), score)
            cv.rectangle(frame, box, color, 5)
            
            cv.putText(frame, label, (box[0],box[1]-10),
                       cv.FONT_HERSHEY_COMPLEX, 0.5, color, 1)
            i =i+1
        
        #def check (n):
          #l = list[n]
          #cn = (l[1],l[2])
          #cv.circle(frame, (cn), 60,(0, 255, 255),  3)
          #print (l)
        #check (0)
        print(list)
        
        def text():
            form.textEdit.clear()
            for i in range (len(list)):
                l = list[i]
                tx=l[0]+":     "+str(l[1]) + "  ,  "+str(l[2])
                form.textEdit.append(tx)
            
            
        form.pushButton.clicked.connect(text)
        endingTime = time.time() - starting_time
        fps = frame_counter/endingTime
        # print(fps)
        cv.putText(frame, f'FPS: {fps}', (20, 50),
                   cv.FONT_HERSHEY_COMPLEX, 0.7, (0, 255, 0), 2)
        #cv.circle(frame, int(x_centr),int(y_centr), 50, )
        
        
        
        #for box in boxes:
            #print('координаты центра целей')
           # print (box[0]+box[2]/2,box[1]+box[3]/2)
            
        cv.imshow('frame', frame)
        key = cv.waitKey(1)
        if key == ord('q'):
            break
    cap.release()
    cv.destroyAllWindows()
form.pushButton_2.clicked.connect(pusk1)

#       Пуск с камеры нейронка
def pusk2():
    if form.comboBox.currentIndex() == 1:
         weights = 'war-obj_best.weights'
         cfg = 'war-obj.cfg'
         names = 'war.names'
    elif form.comboBox.currentIndex() == 0:
         weights = 'ship-obj_last.weights'
         cfg = 'war-obj.cfg'
         names = 'ship.names'
    index2 = form.comboBox_2.currentIndex()+1
    Conf_threshold,NMS_threshold = index2/10,index2/10
    COLORS = [(255, 0, 0), (0, 0, 255), (0, 255, 0),
              (255, 255, 0), (255, 0, 255), (0, 255, 255)]

    class_name = []
    with open(names, 'r') as f:
        class_name = [cname.strip() for cname in f.readlines()]
    # print(class_name)
    net = cv.dnn.readNet(weights, cfg)
    net.setPreferableBackend(cv.dnn.DNN_BACKEND_OPENCV)
    net.setPreferableTarget(cv.dnn.DNN_TARGET_CPU)

    model = cv.dnn_DetectionModel(net)
    model.setInputParams(size=(416, 416), scale=1/255, swapRB=True)


    cap = cv.VideoCapture(0)#######################################номер камеры
    starting_time = time.time()
    frame_counter = 0
    while True:
        ret, frame = cap.read()
        frame_counter += 1
        if ret == False:
            break
        classes, scores, boxes = model.detect(frame, Conf_threshold, NMS_threshold)
        list=[]
        i=0
        for (classid, score, box) in zip(classes, scores, boxes):
            #print(class_name[classid])
            
            x_centr,y_centr =int( round((box[0]+box[2]/2),0)),int( round((box[1]+box[3]/2),0))
            centr=[class_name[classid]+str(i),x_centr,y_centr]
            
            #print(box)
            list.append(centr)
            
            color = COLORS[int(classid) % len(COLORS)]
            label = "%s : %f" % (class_name[classid]+str(i), score)
            cv.rectangle(frame, box, color, 5)
            
            cv.putText(frame, label, (box[0],box[1]-10),
                       cv.FONT_HERSHEY_COMPLEX, 0.5, color, 1)
            i =i+1
        
        #def check (n):
          #l = list[n]
          #cn = (l[1],l[2])
          #cv.circle(frame, (cn), 60,(0, 255, 255),  3)
          #print (l)
        #check (0)
        print(list)
        
        def text():
            form.textEdit.clear()
            for i in range (len(list)):
                l = list[i]
                tx=l[0]+":     "+str(l[1]) + "  ,  "+str(l[2])
                form.textEdit.append(tx)
            
            
        form.pushButton.clicked.connect(text)
        endingTime = time.time() - starting_time
        fps = frame_counter/endingTime
        # print(fps)
        cv.putText(frame, f'FPS: {fps}', (20, 50),
                   cv.FONT_HERSHEY_COMPLEX, 0.7, (0, 255, 0), 2)
        #cv.circle(frame, int(x_centr),int(y_centr), 50, )
        
        
        
        #for box in boxes:
            #print('координаты центра целей')
           # print (box[0]+box[2]/2,box[1]+box[3]/2)
            
        cv.imshow('frame', frame)
        key = cv.waitKey(1)
        if key == ord('q'):
            break
    cap.release()
    cv.destroyAllWindows()

form.pushButton_3.clicked.connect(pusk2)

app.exec()
