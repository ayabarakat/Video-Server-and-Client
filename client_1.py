
# Welcome to PyShine
# lets make the client code
# In this code client is sending video to server
import socket,cv2, pickle,struct
import pyshine as ps # pip install pyshine
import imutils # pip install imutils
import time
import cv2, imutils, socket
import numpy as np
import base64
import threading, wave, pyaudio,pickle,struct
import sys
import queue
import os
from moviepy.editor import VideoFileClip
from os.path import exists



client_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
host_ip = '192.168.33.100' # Here according to your server ip write the address

port = 18000
client_socket.connect((host_ip,port))


def convert_video_to_audio_moviepy(video_file, output_ext="wav"):
    """Converts video to audio using MoviePy library
    that uses `ffmpeg` under the hood"""
    filename, ext = os.path.splitext(video_file)
    clip = VideoFileClip(video_file)
    clip.audio.write_audiofile(f"{filename}.{output_ext}")


isExistingVid1 = os.path.exists('Videos/bmwd.mp4')
isExistingVid2 = os.path.exists('Videos\Range Rover Velar.mp4')
isExistingVid3 = os.path.exists('Videos\mer1.mp4')
isExistingVid4 = os.path.exists('Videos\Porsche.mp4')




if isExistingVid1==False:
    convert_video_to_audio_moviepy('Videos/bmwd.mp4')
if isExistingVid2==False:    
    convert_video_to_audio_moviepy('Videos\Range Rover Velar.mp4') 
if isExistingVid3==False:
    convert_video_to_audio_moviepy('Videos\mer1.mp4')    
if isExistingVid4==False:
    convert_video_to_audio_moviepy('Videos\Porsche.mp4')    



def video():
    while True:
     if client_socket: 
        msg=client_socket.recv(5)
        print("\n","VIDEO",msg)

        if msg==b'v1':
            vid = cv2.VideoCapture('Videos/bmwd.mp4')
             
        elif  msg==b'v2':
            vid = cv2.VideoCapture('Videos\Range Rover Velar.mp4')
            # convert_video_to_audio_moviepy('Videos\mared.mp4') 

        elif  msg==b'v3':
            vid = cv2.VideoCapture('Videos\mer1.mp4')
            # convert_video_to_audio_moviepy('Videos/7ag.mp4')
             
        elif  msg==b'v4':
            vid = cv2.VideoCapture('Videos\Porsche.mp4') 
            
        elif msg==b'bye':
            client_socket.close()
        else:
            continue         

           
        # time.sleep(1)
        while (vid.isOpened()):
            try:
                img, frame = vid.read()
                frame = imutils.resize(frame,width=380)
                a = pickle.dumps(frame)
                message = struct.pack("Q",len(a))+a
                time.sleep(0.031)

                client_socket.sendall(message)
                # cv2.imshow(f"TO: {host_ip}",frame)
                key = cv2.waitKey(1) & 0xFF
                if key == ord("q"):
                    client_socket.close()
            except:
                print('VIDEO FINISHED!')
                break



clientAudio_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
clientAudio_socket.connect((host_ip,port-1))


def audio():

    CHUNK = 1024
    p = pyaudio.PyAudio()

    while True:
        if clientAudio_socket:
            msg=clientAudio_socket.recv(10)
            print("\n","AUDIO",msg)
            if msg==b'v1':  
                wf = wave.open("Videos/bmwd.wav", 'rb')
            elif  msg==b'v2':
                wf = wave.open("Videos\Range Rover Velar.wav", 'rb')
            elif msg==b'v3':
                wf = wave.open("Videos/mer1.wav", 'rb')
            elif msg==b'v4':
                wf = wave.open("Videos/Porsche.wav", 'rb')
            elif msg==b'bye':
                clientAudio_socket.close()
            else:
                continue
            stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                    channels=wf.getnchannels(),
                    rate=wf.getframerate(),
                    input=True,
                    frames_per_buffer=CHUNK)
            while True:
                data = wf.readframes(CHUNK)
                a = pickle.dumps(data)
                message = struct.pack("Q",len(a))+a
                clientAudio_socket.sendall(message)
        else:
            break        


from concurrent.futures import ThreadPoolExecutor
with ThreadPoolExecutor(max_workers=3) as executor:
    executor.submit(audio)
    executor.submit(video)