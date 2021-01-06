import sys
import os
import pyautogui
import win32api, win32con
from PIL import ImageGrab
from configparser import ConfigParser

class MapData:
	def __init__(self):
		self.minX = 9
		self.minY = 61
		self.platformsNum = 0
		self.platforms = []
		self.ropesNum = 0
		self.ropes = []
		self.portalsNum = 0
		self.portals = []

		return

#creating Platform class
class Platform:
	def __init__(self, leftX, rightX, Y):
		self.leftX = leftX
		self.rightX = rightX
		self.Y = Y

		return

#creating Rope class
class Rope:
	def __init__(self, X, bottomY, topY):
		self.X = X
		self.bottomY = bottomY
		self.topY = topY

		return

#creating Portal class
class Portal:
	def __init__(self, X1, Y1, X2, Y2):
		self.X1 = X1
		self.Y1 = Y1
		self.X2 = X2
		self.Y2 = Y2

		return

#main menu
def menu():
	#resetting mapdata
	mapdata = MapData()

	#prompt user with menu
	mapName = input("Enter the name of the map: ")
	if(mapName == ""):
		configure = ConfigParser()
		configure.read("default.ini")
		mapName = configure.get("general", "map")
	#user input checking
	while (not(os.path.exists(os.path.join(mapdir, mapName + ".ini")))):
		mapName = input("Enter a valid map name: ")

	readFromFile(mapName)

	while (True):
		print('Enter "y" to get character position. Enter "q" to exit program.')
		choice = input(">> ")
		#user input checking
		while (choice != "y" and choice != "q"):
			choice = input("Enter a valid option: ")
		if (choice == "y"):
			charLoc = characterPos()
			print("Character position: " + str(charLoc[0]) + ", " + str(charLoc[1]))
		elif (choice == "q"):
			print("Exiting program")
			sys.exit()
		
	return

#reading map data from file
def readFromFile(mapName):
	#opening map file
	mapPath = os.path.join(mapdir, mapName + ".ini")
	configure = ConfigParser()
	configure.read(mapPath)

	#reading general section
	mapdata.mapName = configure.get("general", "mapName")
	mapdata.minX = configure.getint("general", "minX")
	mapdata.maxX = configure.getint("general", "maxX")
	mapdata.minY = configure.getint("general", "minY")
	mapdata.maxY = configure.getint("general", "maxY")
	mapdata.width = configure.getint("general", "width")
	mapdata.height = configure.getint("general", "height")
	mapdata.platformsNum = configure.getint("general", "platformsNum")
	mapdata.ropesNum = configure.getint("general", "ropesNum")
	mapdata.portalsNum = configure.getint("general", "portalsNum")

	#reading platforms section
	for i in range(mapdata.platformsNum):
		dataList = [int(value) for value in configure["platforms"]["platform" + str(i + 1)].split(', ')]
		mapdata.platforms.append(Platform(dataList[0], dataList[1], dataList[2]))

	#reading ropes section
	for i in range(mapdata.ropesNum):
		dataList = [int(value) for value in configure["ropes"]["rope" + str(i + 1)].split(', ')]
		mapdata.ropes.append(Rope(dataList[0], dataList[1], dataList[2]))
		
	#reading portals section
	for i in range(mapdata.portalsNum):
		dataList = [int(value) for value in configure["portals"]["portal" + str(i + 1)].split(', ')]
		mapdata.portals.append(Portal(dataList[0], dataList[1], dataList[2], dataList[3]))

	return

#getting character position on minimapdata
def characterPos():
	charLoc = pyautogui.locate(charMarker, pyautogui.screenshot(region=(mapdata.minX, mapdata.minY, mapdata.width, mapdata.height)))
	while (charLoc == None):
		charLoc = pyautogui.locate(charMarker, pyautogui.screenshot(region=(mapdata.minX, mapdata.minY, mapdata.width, mapdata.height)))
		
	return charLoc

#main function
def main():
	#setting global directory pats
	global maindir
	global mapdir
	global assets

	maindir = os.path.dirname(__file__)
	mapdir = os.path.join(maindir, "map data")
	assetsdir = os.path.join(maindir, "assets")

	#initializing global MapData class
	global mapdata
	mapdata = MapData()

	#initializing global character marker
	global charMarker
	charMarker = os.path.join(assetsdir, "characterminimap.png")

	#prompting user with menu
	while(True):
		menu()

	return

main()