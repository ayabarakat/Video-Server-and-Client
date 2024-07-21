
# Welcome to PyShine
# lets make the client code
# In this code client is sending video to server
import socket,cv2, pickle,struct,subprocess
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


# global sk

server_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
host_ip = '192.168.33.100' # Here according to your server ip write the address


port = 18000
server_socket.connect((host_ip, port))


def convert_video_to_audio_moviepy(video_file, output_ext="wav"): #convert to audio 
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

current_proc = None

def stopCurrentVid():
    global current_proc
    if current_proc and current_proc.poll() is None:
        current_proc.kill()

def playVideo(vid):
    global current_proc
    # stopCurrentVid()
    # time.sleep(0.005)
    while (vid.isOpened()):
            try:
                img, frame = vid.read()
                frame = imutils.resize(frame, width=380)
                a = pickle.dumps(frame) # bada5al elframes bel tareteeb (series)
                message = struct.pack("Q",len(a))+a # bt7wleeha l bytes 
                time.sleep(0.031) # sync
                server_socket.sendall(message) # send all buffer you pass or throws an error (until everything is sent)
                key = cv2.waitKey(1) & 0xFF
                if key == ord("q"):
                    server_socket.close()
            except:
                print('VIDEO FINISHED!')
                break


def video():
    while True:
     if server_socket: 
        msg=server_socket.recv(5)
        print("\n","VIDEO", msg)
        if msg==b'v1':
            vid = cv2.VideoCapture('Videos/bmwd.mp4')
            sk = vid
            playVideo(vid)
        elif  msg==b'v2':
            vid = cv2.VideoCapture('Videos\Range Rover Velar.mp4')
            # convert_video_to_audio_moviepy('Videos\mared.mp4') 
            sk = vid
            playVideo(vid)
        elif  msg==b'v3':
            vid = cv2.VideoCapture('Videos\mer1.mp4')
            # convert_video_to_audio_moviepy('Videos/7ag.mp4')
            sk = vid
            playVideo(vid)
        elif  msg==b'v4':
            vid = cv2.VideoCapture('Videos\Porsche.mp4')
            sk = vid
            playVideo(vid)
        else:
            continue         



clientAudio_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
clientAudio_socket.connect((host_ip, port-1))

def playaudio(wf):
    CHUNK = 20000
    p = pyaudio.PyAudio()
    stream = p.open(format=p.get_format_from_width(wf.getsampwidth()), # setup a pyaudio stream to play or rec audio 
                    channels=wf.getnchannels(),
                    rate=wf.getframerate(),
                    input=True,
                    frames_per_buffer=CHUNK)
    while True:
        try:
            # print("Here always")
            data = wf.readframes(CHUNK) 
            a = pickle.dumps(data)
            message = struct.pack("Q",len(a))+a
            clientAudio_socket.sendall(message)
            if message==b'\x0f\x00\x00\x00\x00\x00\x00\x00\x80\x04\x95\x04\x00\x00\x00\x00\x00\x00\x00C\x00\x94.': # stopping condition 
                break 
        except:
            print('Audio FINISHED!')
            break  

def audio():
    while True:
        if clientAudio_socket:
            msg=clientAudio_socket.recv(5)
            print("\n","AUDIO",msg)
            if msg==b'v1':
                wf = wave.open("Videos/bmwd.wav", 'rb')
                # t1 = threading.Thread(target=playaudio(wf))
                # t1.start()
                playaudio(wf)
            elif  msg==b'v2':
                wf = wave.open("Videos\Range Rover Velar.wav", 'rb')
                # t1.start()
                playaudio(wf)
            elif msg==b'v3':
                wf = wave.open("Videos\mer1.wav", 'rb')
                playaudio(wf)
            elif msg==b'v4':
                wf = wave.open("Videos\Porsche.wav", 'rb')
                playaudio(wf)
            else:
                continue
        # else:
        #     break        


from concurrent.futures import ThreadPoolExecutor
with ThreadPoolExecutor(max_workers=3) as executor:
    executor.submit(audio)
    executor.submit(video)