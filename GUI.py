from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5 import QtCore, QtWidgets,QtGui , QtMultimedia
import sys
import subprocess
from threading import *
from multiprocessing.connection import Listener
from vidgear.gears import NetGear
from imutils import build_montages
import cv2
import pygame
from socket import *
from socket import socket
import socket
import struct
import pickle
import time
import cv2, imutils, socket
import numpy as np
import time
import base64
import threading, wave, pyaudio,pickle,struct, queue
from PyQt5.QtCore import QThread, QObject, pyqtSignal, pyqtSlot
import os
import time
from datetime import datetime
import pyshine as ps 
import designer

class UI(QMainWindow):
    def __init__(self):
        super(UI,self).__init__()
        #Load UI file
        uic.loadUi("GUI.ui", self)


        self.vid1=b'space1'
        self.pushButton_v1=self.findChild(QPushButton,"pushButton_v1")
        self.pushButton_v1.clicked.connect(self.clickVideo1)

        self.pushButton_v2=self.findChild(QPushButton,"pushButton_v2")
        self.pushButton_v2.clicked.connect(self.clickVideo2)
        self.thread={}
        q = queue.Queue(maxsize=2000)

        self.pushButton_v3=self.findChild(QPushButton,"pushButton_v3")
        self.pushButton_v3.clicked.connect(self.clickVideo3)
        self.pushButton_v4=self.findChild(QPushButton,"pushButton_v4")
        self.pushButton_v4.clicked.connect(self.clickVideo4)
        self.Camera_representation=self.findChild(QLabel,"label_3")

        self.clientvid1=False
        self.clientvid2=False
        self.video=False
        self.t2 = Thread(target=self.AudioClient_thread)
        self.t2.start()
        self.t1 = Thread(target=self.Client_thread)
        self.t1.start()
       
       
       
        self.show()
    def clickVideo1(self):
        if self.video==True:
            # if self.client_socket and self.clientAudio_socket:
            #     self.client_socket.send(bytes('bye',"utf-8"))
                
            #     self.clientAudio_socket.send(bytes('bye',"utf-8"))
            self.client_socket.close()
            self.clientAudio_socket.close()
            # else:
            #     self.client_socket.send(bytes('v1',"utf-8"))
            #     self.clientAudio_socket.send(bytes('v1',"utf-8"))    

        cmd='python client_1.py'
        self.client_1=subprocess.Popen(cmd,shell=True)
        self.v='v1'     
        # cmd='python client_1.py'
        # self.client_1=subprocess.Popen(cmd,shell=True)
       
        

    def clickVideo2(self):
        if self.video==True:
            # if self.client_socket and self.clientAudio_socket:
            #     self.client_socket.send(bytes('bye',"utf-8"))
            #     self.clientAudio_socket.send(bytes('bye',"utf-8"))
            self.client_socket.close()
            self.clientAudio_socket.close()
            # else:
            #     self.client_socket.send(bytes('v2',"utf-8"))
            #     self.clientAudio_socket.send(bytes('v2',"utf-8"))
        cmd='python client_1.py'
        self.client_1=subprocess.Popen(cmd,shell=True)
        self.v='v2'
        # cmd='python client_2.py'
        # self.client_2=subprocess.Popen(cmd,shell=True)
      
    def clickVideo3(self):
        if self.video==True:
            
            # self.client_socket.send(bytes('bye',"utf-8"))
            # self.clientAudio_socket.send(bytes('bye',"utf-8"))
            self.client_socket.close()
            self.clientAudio_socket.close()
        cmd='python client_1.py'
        self.client_1=subprocess.Popen(cmd,shell=True)
        self.v='v3'
        # cmd='python client_3.py'
        # self.client_3=subprocess.Popen(cmd,shell=True)
    def clickVideo4(self):
        if self.video==True:
            
            # self.client_socket.send(bytes('bye',"utf-8"))
            # self.clientAudio_socket.send(bytes('bye',"utf-8"))
            self.client_socket.close()
            self.clientAudio_socket.close()
        cmd='python client_1.py'
        self.client_1=subprocess.Popen(cmd,shell=True)
        self.v='v4'
    def AudioClient_thread(self):
        # server_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        # host_name  = socket.gethostname()
        host_ip = 'localhost'#socket.gethostbyname(host_name)
        # print('HOST IP:',host_ip)
        port = 18000
        # socket_address = (host_ip,port)
        # server_socket.bind(socket_address)
        # server_socket.listen()
        # print("Listening at",socket_address)
         # create socket
        serverAudio_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        socketAudio_address = (host_ip,port-1)
        print('server listening at',socketAudio_address)
        # serverAudio_socket.connect(socketAudio_address) 
        serverAudio_socket.bind(socketAudio_address)
        serverAudio_socket.listen()
        print("CLIENT CONNECTED TO",socketAudio_address)
        
        while True:
            # self.client_socket,addr = server_socket.accept()
            self.clientAudio_socket,addr2 = serverAudio_socket.accept()
            # print(self.clientAudio_socket)
            

            # thread = threading.Thread(target=self.show_client, args=(addr,self.client_socket))
            # thread.start()
            
            thread2 = threading.Thread(target=self.audio_stream, args=(addr2,self.clientAudio_socket))
            thread2.start()
            print("TOTAL Audio CLIENTS ",threading.active_count() - 1)    
        
     
    def Client_thread(self):
        server_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        host_name  = socket.gethostname()
        host_ip = 'localhost'#socket.gethostbyname(host_name)
        print('HOST IP:',host_ip)
        port = 18000
        socket_address = (host_ip,port)
        server_socket.bind(socket_address)
        server_socket.listen()
        print("Listening at",socket_address)
         # create socket
        # serverAudio_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        # socketAudio_address = (host_ip,port-1)
        # print('server listening at',socketAudio_address)
        # # serverAudio_socket.connect(socketAudio_address) 
        # serverAudio_socket.bind(socketAudio_address)
        # serverAudio_socket.listen()
        # print("CLIENT CONNECTED TO",socketAudio_address)
        
        while True:
            self.client_socket,addr = server_socket.accept()
            # self.clientAudio_socket,addr2 = serverAudio_socket.accept()
            # print(self.clientAudio_socket)
            
            thread = threading.Thread(target=self.show_client, args=(addr,self.client_socket))
            thread.start()
            
            # thread2 = threading.Thread(target=self.audio_stream, args=(addr2,self.clientAudio_socket))
            # thread2.start()
            print("TOTAL CLIENTS ", threading.active_count() - 1)

    def audio_stream(self,addr2,clientAudio_socket):
        BREAK = False
        p = pyaudio.PyAudio()
        CHUNK = 1024
        stream = p.open(format=p.get_format_from_width(2),
                        channels=2,
                        rate=44100,
                        output=True,
                        frames_per_buffer=CHUNK)
        data = b""
        payload_size = struct.calcsize("Q")
        # self.clientAudio_socket.send(bytes(self.v,"utf-8"))
        while True:
            if self.clientAudio_socket :
                self.clientAudio_socket.send(bytes(self.v,"utf-8"))
            else:
                 continue
            try:
                while len(data) < payload_size:
                    packet = self.clientAudio_socket.recv(4*1024) # 4K
                    # print(packet)
                    if not packet: break
                    data+=packet
                packed_msg_size = data[:payload_size]
                data = data[payload_size:]
                msg_size = struct.unpack("Q",packed_msg_size)[0]
                while len(data) < msg_size:
                    data += self.clientAudio_socket.recv(4*1024)
                frame_data = data[:msg_size]
                data  = data[msg_size:]
                frame = pickle.loads(frame_data)
                stream.write(frame)

            except:
                
                break

        self.clientAudio_socket.close()
        print('Audio closed',BREAK)        

    def show_client(self,addr, client_socket):
        # server_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        # host_name  = socket.gethostname()
        # host_ip = '192.168.1.141'#socket.gethostbyname(host_name)
        # print('HOST IP:',host_ip)
        # port = 9999
        # socket_address = (host_ip,port)
        # server_socket.bind(socket_address)
        # server_socket.listen()
        # print("Listening at",socket_address)
        self.video=True
        fourcc =0x7634706d 
        now = datetime.now()
        time_str = now.strftime("%d%m%Y%H%M%S")
        time_name = '_Rec_'+time_str+'.mp4'
        fps = 30
        frame_shape = False
        try:
            # print("1")
            # self.client_socket.send(bytes(self.v,"utf-8"))
            print('CLIENT {} CONNECTED!'.format(addr))
            if self.client_socket: # if a client socket exists
                data = b""
                payload_size = struct.calcsize("Q")
                while True:
                    if self.client_socket:
                      self.client_socket.send(bytes(self.v,"utf-8"))
                    else:
                         continue
                    while len(data) < payload_size:
                        # print('Ana el len <')
                        packet = self.client_socket.recv(2000000) # 4K
                        if not packet: break
                        data+=packet
                    packed_msg_size = data[:payload_size]
                    data = data[payload_size:]
                    msg_size = struct.unpack("Q",packed_msg_size)[0]
                    
                    while len(data) < msg_size:
                        print('Ana el len < 22')
                        data += self.client_socket.recv(2000000)
                    frame_data = data[:msg_size]
                    data  = data[msg_size:]
                    frame = pickle.loads(frame_data)
                    text  =  f"CLIENT: {addr}"
                    # time_now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                    # frame =  ps.putBText(frame,time_now,10,10,vspace=10,hspace=1,font_scale=0.7, background_RGB=(141,0,0),text_RGB=(141,250,250))
                    
                    if not frame_shape:
                        
                        # video_file_name  = str(addr) + time_name
                        # out = cv2.VideoWriter(video_file_name, fourcc, fps, (frame.shape[1], frame.shape[0]), True)
                        frame_shape = True
                    # out.write(frame)
                    # cv2.imshow(f"FROM {addr}",frame)
                    frame= cv2.resize(frame,[765,575])
                    # frame=cv2.

                    converted = QImage(frame, frame.shape[1],
                                frame.shape[0], frame.shape[1] * 3,QImage.Format_RGB888).rgbSwapped()
                    
                    self.Camera_representation.setPixmap(QPixmap.fromImage(converted))
                    # if self.clientvid1==True:
                    #     converted = QImage(frame, frame.shape[1],
                    #             frame.shape[0], frame.shape[1] * 3,QImage.Format_RGB888).rgbSwapped()
                    #     self.Camera_representation.close()
                    #     self.Camera_representation_2.setPixmap(QPixmap.fromImage(converted))
                    # elif self.clientvid2==True:
                    #     converted = QImage(frame, frame.shape[1],
                    #             frame.shape[0], frame.shape[1] * 3,QImage.Format_RGB888).rgbSwapped()
                    #     self.Camera_representation_2.close()
                    #     self.Camera_representation.show()
                    #     self.Camera_representation.setPixmap(QPixmap.fromImage(converted))
                         
                    key = cv2.waitKey(1) & 0xFF
                    if key  == ord('q'):
                        break
                
                self.client_socket.close()
            # else:
            #      self.client_socket.send(bytes(b'bye',"utf-8"))
                     
        except Exception as e:
            self.video=False
            print(f"CLINET {addr} DISCONNECTED")
            pass       
        

app = QApplication(sys.argv)
UiWindow = UI()
app.exec_()            