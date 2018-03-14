# coding=utf-8
#!/usr/bin/env python3
# NOTE: this example requires PyAudio because it uses the Microphone class

import speech_recognition as sr
import pyttsx3
import random
import os
import subprocess
import sys
import ctypes
import win32api
import win32con
import time
import webbrowser
import cv2
import win32api #needs the pywin32 module	 
import pyautogui

DETACHED_PROCESS = 0x00000008

keywordsList=[]



def loadKeywords():
	f=open('keywords.txt','r')
	x=f.readline()
	while(x!=""):
		keywordsList.append(x.rsplit()[0])
		x=f.readline()
	print("The list was populated with:")
	for c in keywordsList:
		print(c)
	print()
	



def checkIfShouldAct(listOfExpressions):
	
	for c in keywordsList:
		for x in listOfExpressions:
			if c in x:
				pyautogui.press('right')
				print("worked")
				return
	print("No action")




# this is called from the background thread
def callback(recognizer, audio):
	# received audio data, now we'll recognize it using Google Speech Recognition
	try:
		# for testing purposes, we're just using the default API key
		# to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
		# instead of `r.recognize_google(audio)`
		result=recognizer.recognize_google(audio,show_all=True, language = "pt-PT")
		
		try:
			listOfExpressions=[]

			for c in result.get('alternative'):
				listOfExpressions.append(c.get('transcript'))
			
			checkIfShouldAct(listOfExpressions)

		except Exception as e:
			print("No match")

		
	except sr.UnknownValueError:
		print("Google Speech Recognition could not understand audio")
	except sr.RequestError as e:
		print("Could not request results from Google Speech Recognition service; {0}".format(e))



def listenInBackground():

	loadKeywords()

	r = sr.Recognizer()
	m = sr.Microphone()
	with m as source:
		r.adjust_for_ambient_noise(source)  # we only need to calibrate once, before we start listening



	# start listening in the background (note that we don't have to do this inside a `with` statement)
	stop_listening = r.listen_in_background(m, callback)
	# `stop_listening` is now a function that, when called, stops background listening

	print("Listenning")

	# do some unrelated computations for 5 seconds
	for _ in range(50000): time.sleep(0.1)  # we're still listening even though the main thread is doing other things

	# calling this function requests that the background listener stop listening
	stop_listening(wait_for_stop=False)

	# do some more unrelated things
	while True: time.sleep(0.1)  # we're not listening anymore, even though the background thread might still be running for a second or two while cleaning up and stopping

listenInBackground()
#pontualTime()