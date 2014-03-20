import sys
from random import randint
from avion import avion
import time
from math import trunc
#from queue import PriorityQueue
from ModelImpl import *
import re
import operator
import os
import sys 
from PyQt4 import QtCore
from PyQt4.QtCore import QObject, pyqtSignal
from radar import Ui_RadarWidget
list_of_names = ['tunisair', 'airfrance', 'quatrairways', 'tarom']

class Simul2(QObject, Ui_RadarWidget):

	header = ['Nom', 'Priorite', 'Temps Estimee']
	def __init__(self, maxNumber, tempsTick, numPiste):
		super(Simul2, self).__init__()
		self.running = 0
		self.currentNumber = 0
		self.maxNumber = maxNumber
		self.tempsTick = tempsTick
		self.listOfairfrance = numPiste * [None]
		self.numPiste = numPiste
		self.arriverIn = []
		self.departIn = []
		self.departModel = None
		self.arriverModel = None
		self.__generateInitialData(self.maxNumber)
		self.temps = QTemps()
	def __setTempsTick(self, temps):
		self.tempsTick = (int)((100 - temps) / 50 * 1000)
		self.temps.setInterval(self.tempsTick)
		self.setRunning()
	def __generateInitialData(self, nr):
		toGenerate = randint(0, nr)
		self.currentNumber += toGenerate
		print('Generating... ' + str(toGenerate))
		if self.departModel is not None:
			self.departModel.triggerDataChanging()
			self.arriverModel.triggerDataChanging()


		for i in range(0, toGenerate):
			avion = avion.generateRandomavion()
			if avion.status == 0:
				self.departIn.append(avion)
			else:
				self.arriverIn.append(avion)
		self.departIn.sort()
		self.arriverIn.sort()
		if self.departModel is not None:
			self.departModel.triggerDataChanged()
			self.arriverModel.triggerDataChanged()


	def __bindUiToModel(self):
		if self is not None:
			for i in range(self.numPiste):
				airavion = self.listOfairfrance[i]
				if airavion is not None:
					getattr(self, 'runway' + str(i)).setValue(int(airavion.getPercentage() * 100))
					getattr(self, 'rwplane' + str(i)).setText(airavion.nom + ' - ' + airavion.getReadableStatus())
				else:
					getattr(self, 'runway' + str(i)).setValue(0)
					getattr(self, 'rwplane' + str(i)).setText('Libere')
			self.labelarriver.setText('arriver ' + str(len(self.arriverIn)))
			self.labeldepart.setText('depart ' + str(len(self.departIn)))

	def setGraphicalModel(self):
		self.departModel = MyTableModel(self.departiIn, Simul2.header,['nom', 'priorite', 'takeOffTemps'],  self.tabeldepart) 
		self.arriverModel = MyTableModel(self.arriverIn,  Simul2.header,['nom', 'priorite', 'landingTemps'], self.tabelarriver) 
		self.tabeldepart.setModel(self.departiModel)
		self.tabelarriver.setModel(self.arriverModel)
		self.__bindUiToModel()
		self.buttonStart.clicked.connect(self.setRunning)
		self.buttonStop.clicked.connect(self.setStopped)
		self.horizontalSlider.valueChanged[int].connect(self.__setTempsTick)
	def setStopped(self):
		self.running = 2
	def setRunning(self):
		self.running = 1
		if not self.temps.isActive():
			self.temps.timeout.connect(self.__runSimul)
		# Call f() every 1 seconds
			self.temps.start(self.tempsTick)

	def __consumeavion(self):
		freeSpots = [x for x in self.listOfairfrance if x is None]
		numavions = len(freeSpots)
		for x in range(numavions):
			if len(freeSpots) > 0:
				index = self.listOfairfrance.index(None)
			else:
				return
			if len(self.departIn) > 0:
				depavion = self.departIn[0]
			else:
				depavione = None
			if len(self.arriverIn) > 0:
				arravion = self.arriverIn[0]
			else:
				arravion = None
			if (arravion is None and depavion is None):
				return
			if arravion is None or (depavion is not None and depavion.priorite < arravion.priorite):
				self.listOfairfrance[index] = depavion
				self.departIn.pop(0)
			elif depavion is None or (arravion is not None and depavion.priorite > arravion.priorite):
				self.listOfairfrance[index] = arravion
				self.arriverIn.pop(0)
			else:
				if len(self.arriverIn) > len(self.departIn):
					self.listOfairfrance[index] = arravion
					self.arriverIn.pop(0)
				else:
					self.listOfairfrance[index] = arravion
					self.departIn.pop(0)
	def __checkForCompletion(self):
		for i in range(0, len(self.listOfairfrance)):
			if self.listOfairfrance[i] is not None:
				if self.listOfairfrance[i].status == 0:
					self.listOfairfrance[i].landingTemps-=1
				else:
					self.listOfairfrance[i].takeOffTemps-=1
				if self.listOfairfrance[i].takeOffTemps <= 0 or self.listOfairfrance[i].landingTemps<=0:
					self.listOfairfrance[i] = None

	def __runSimul(self):
		print('Sim temps is ' + str(self.tempsTick))
		if self.running != 0:
			self.currentNumber = len(self.arriverIn) + len(self.derpartIn)
			if self.running == 2:
				return
			self.__generateInitialData(self.maxNumber - self.currentNumber)
			self.__checkForCompletion()
			self.__consumePlane()
			self.__printModel()
			self.__bindUiToModel()
		else:
			temps.stop()
	def stopInit(self):
		self.running = 0
	def __printModel(self):
		for i in range(0, len(self.listOfairfrance)):
			if self.listOfairfrance[i] is not None:
				print ('RW:' + str(i) + ' --- ' + self.listOfairfrance[i].nom + ' --- ' + str(int(self.listOfairfrance[i].getPercentage() * 100)) + '%')
			else:
				print ('RW:' + str(i) + ' --- is free')
