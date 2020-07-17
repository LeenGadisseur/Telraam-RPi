import warnings
import numpy as np
import cv2
import time
import socket
import argparse
import pathlib
import subprocess
import uuid
import json
import requests
import sys
import backEstimation as be
import copy
import os

X_RESOLUTION = 1280
Y_RESOLUTION = 720
VIDEO_FPS = 40  # 40 FPS is the top value for larger FOV at 720p, at FPS > 40 the FOV gets narrower!
X_RESIZE_PERCENTAGE = 50  # Horizontal processing resolution in percentage of the recording resolution
Y_RESIZE_PERCENTAGE = 50  # Vertical processing resolution in percentage of the recording resolution
X_RESIZED = int(X_RESOLUTION * (X_RESIZE_PERCENTAGE / 100.))
Y_RESIZED = int(Y_RESOLUTION * (X_RESIZE_PERCENTAGE / 100.))

def backgroundEstimate(back_est, frame):
	frame_small = cv2.resize(frame, (X_RESIZED, Y_RESIZED), interpolation=cv2.INTER_LINEAR)
	frame_gray = cv2.cvtColor(frame_small, cv2.COLOR_BGR2GRAY)
	rows, cols = frame_gray.shape
	for r in range(rows):
		for c in range(cols):
			if((frame_gray[r,c] - back_est[r,c]) >= 0):
				back_est[r,c] = back_est[r,c] + 1
			else:
				back_est[r,c] = back_est[r,c] - 1
	cv2.imshow('Backest', back_est)
	return back_est

def main():
	#cap = cv2.VideoCapture("/home/leen/Videos/MAH00199_reduced.avi")#0 voor camera
	cap = cv2.VideoCapture("/home/leen/Videos/opname_pi4_mpeg4.avi")#0 voor camera
	ret, frame = cap.read()
	frame_small = cv2.resize(frame, (X_RESIZED, Y_RESIZED), interpolation=cv2.INTER_LINEAR)
	frame_gray = cv2.cvtColor(frame_small, cv2.COLOR_BGR2GRAY)
	#back_est = backgroundEstimate(frame_gray, frame)
	rows, cols = frame_gray.shape
	#print("type frame:", frame_gray.dtype)
	#back = be.backEstimationDev(frame, back))
	back = copy.deepcopy(frame_gray)
	#print("voor estimate", back[0,0])
	be.backEstimation(frame_gray,back)
	#print("na estimate", back[0,0])
	#print("type back: ", back.dtype)
	#print("type frame: ", frame.dtype)
	while(1):
		ret, frame = cap.read()
		frame_small = cv2.resize(frame, (X_RESIZED, Y_RESIZED), interpolation=cv2.INTER_LINEAR)
		frame_gray = cv2.cvtColor(frame_small, cv2.COLOR_BGR2GRAY)
		print("type frame:", frame_gray.dtype)
		print("type back:", back.dtype)
		print("Reference count back: ",sys.getrefcount(back))
		print("Reference count frame: ",sys.getrefcount(frame))
		be.backEstimation(frame_gray, back)
		if cv2.waitKey(1) & 0xFF == ord('q'):  # Stop process when 'q' is pressed
			cap.release()
			cv2.destroyAllWindows()
		cv2.waitKey(1)
		cv2.imshow('Backest', back)
		#print(back)
		print("Frame nr funct: " + str(cap.get(cv2.CAP_PROP_POS_FRAMES)))
		
		
main()
