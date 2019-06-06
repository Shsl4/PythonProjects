### Requires MatPlotLib, Django & SciPy

import sys
import os
import matplotlib.pylab as pylab
import matplotlib.pyplot as pyplot
from scipy import signal
import math
import wave
import struct
import time
from django.template.defaultfilters import slugify
import numpy as np
from enum import Enum

class reqType(Enum) :

    sineWaveReq = 1
    sawToothReq = 2
    triangleWaveReq = 3
    squareWaveReq = 4
    fileNameReq = 5
    menuReq = 6
    ampReq = 7
    freqReq = 8
    incorrectTypeReq = 9
    processReq = 10
    maxExceedReq = 11
    invalidNameReq = 12

freq = 100
sampleNumber = 48000
amplitude = 8000
samplingRate = 24000
fileName = ""
nframes=sampleNumber
comptype="NONE"
compname="Uncompressed"
nchannels=2
sampwidth=2

def prompter(inString = ""):

	returnString = input(">>> %s" % inString)
	print("")
	return returnString

def main():

	clearScreen()

	printLib(reqType.menuReq)

	inputString = prompter()
	inputString = inputString.lower()

	if inputString == "1" or inputString == "sinewave" :

		setupWaveVariables(reqType.sineWaveReq)

	elif inputString == "2" or inputString == "sawtooth" :

		setupWaveVariables(reqType.sawToothReq)

	elif inputString == "3" or inputString == "trianglewave" :

		setupWaveVariables(reqType.triangleWaveReq)

	elif inputString == "4" or inputString == "squarewave" :

		setupWaveVariables(reqType.squareWaveReq)

	else :

		main()


def createSineWave():

	t = np.linspace(0, 1, sampleNumber)

	sineWave = np.sin(2 * np.pi * freq * t)

	wavFile = wave.open(fileName, 'w')

	wavFile.setparams((nchannels, sampwidth, int(samplingRate), nframes, comptype, compname))

	for s in sineWave:

		wavFile.writeframes(struct.pack('h', int(s*amplitude)))

def createSawTooth():

	t = np.linspace(0, 1, sampleNumber)

	sawTooth = signal.sawtooth(2 * np.pi * freq * t)

	wavFile = wave.open(fileName, 'w')

	wavFile.setparams((nchannels, sampwidth, int(samplingRate), nframes, comptype, compname))

	for s in sawTooth:

		wavFile.writeframes(struct.pack('h', int(s*amplitude)))

def createSquareWave():

	t = np.linspace(0, 1, sampleNumber)

	squareWave = signal.square(2 * np.pi * freq * t)

	wavFile = wave.open(fileName, 'w')

	wavFile.setparams((nchannels, sampwidth, int(samplingRate), nframes, comptype, compname))

	for s in squareWave:

		wavFile.writeframes(struct.pack('h', int(s*amplitude)))


def createTriangleWave():

	t = np.linspace(0, 1, sampleNumber)

	triangleWave = signal.sawtooth(2 * np.pi * freq * t, width = .5)

	wavFile = wave.open(fileName, 'w')

	wavFile.setparams((nchannels, sampwidth, int(samplingRate), nframes, comptype, compname))

	for s in triangleWave:

		wavFile.writeframes(struct.pack('h', int(s*amplitude)))
				  
def setWavFile(inFileName):

	global fileName

	inFileName = slugify(inFileName)
	inFileName += ".wav"
	fileName = inFileName

	return True

def printLib(inReqType) :

	if inReqType == reqType.sineWaveReq :

		print("~~~~~~~~~~[ Sine Wave Configuration ]~~~~~~~~~~")
		print("")

	elif inReqType == reqType.sawToothReq:

		print("|/|/|/|/|/[ SawTooth Configuration ]\|\|\|\|\|")
		print("")

	elif inReqType == reqType.triangleWaveReq:

		print("/\/\/\/\/\[ Triangle Wave Configuration ]/\/\/\/\/\ ")
		print("")

	elif inReqType == reqType.squareWaveReq:

		print("[][][][][] [ Square Wave Configuration ] [][][][][] ")
		print("")

	elif inReqType == reqType.menuReq:

		print("[*] Welcome to WaveForm Generator! Pick an option below to generate a waveform :")
		print("")
		print("[*] 1. Sine Wave")
		print("[*] 2. SawTooth")
		print("[*] 3. Triangle Wave")
		print("[*] 4. Square Wave")
		print("")

	elif inReqType == reqType.ampReq:

		print("[*] Please enter an Amplitude (Recommended : 8000, Max = 22500) :")
		print("")

	elif inReqType == reqType.freqReq:

		print("[*] Please enter a frequency (Recommended : 100, Max = 10000) :")
		print("")

	elif inReqType == reqType.fileNameReq:

		print("[*] Please enter a file name : ")
		print("/!\ CAUTION : THIS WILL OVERWRITE ANY .WAV FILE WITH THE SAME NAME IN THIS DIRECTORY")
		print("")

	elif inReqType == reqType.incorrectTypeReq:

		print("[*] Error : Wrong variable type entered. Exiting...")
		print("")
		time.sleep(2)
		main()

	elif inReqType == reqType.processReq :

		print("[*] Generating your .wav file...")
		print("")

	elif inReqType == reqType.maxExceedReq :

		print("[*] Exceeding max value. Setting to max value...")
		print("")

	elif inReqType == reqType.invalidNameReq :

		print("[*] Error : Invalid file name. Exiting...")
		print("")
		time.sleep(2)
		main()



def setupWaveVariables(waveType):

	global freq
	global sampleNumber
	global samplingRate
	global amplitude

	clearScreen()

	printLib(waveType)
	printLib(reqType.fileNameReq)

	if setWavFile(prompter()) :

		printLib(reqType.ampReq)

		try :

			newAmp = float(prompter())

		except Exception :

			printLib(reqType.incorrectTypeReq)

		else :

			if newAmp > 22500 :

				printLib(reqType.maxExceedReq)

				newAmp = 22500
					
			amplitude = newAmp

			printLib(reqType.freqReq)

			try :

				newFreq = float(prompter())

			except Exception :

				printLib(reqType.incorrectTypeReq)

			else :

				if freq > 10000 :

					printLib(reqType.maxExceedReq)

					newFreq = 10000
					
				freq = newFreq

				printLib(reqType.processReq)

				if waveType == reqType.sineWaveReq :

					createSineWave()

				elif waveType == reqType.sawToothReq :

					createSawTooth()

				elif waveType == reqType.triangleWaveReq :

					createTriangleWave()

				elif waveType == reqType.squareWaveReq :

					createSquareWave()
				
				print("[*] Done!")
				print("")
				time.sleep(3)
				main()
	else :

		printLib(reqType.invalidNameReq)



### Function used to clear the console screen.
def clearScreen():

	### Check the OS and use its cleaning command.

	### Windows

	if sys.platform == 'win32':
		os.system("cls")

	### Linux or macOS

	elif sys.platform == 'Linux' or sys.platform == 'darwin':
		os.system("clear")
	else:
		print("")
		print("[*] Error : Unknown Operating System, unable to clear.")

	### Reprint Welcome message.

main()
