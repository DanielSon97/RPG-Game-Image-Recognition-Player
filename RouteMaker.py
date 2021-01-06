import sys
import os
import pyautogui
import win32api, win32con
from configparser import ConfigParser

class RouteData:
	def __init__(self):
		self.routeNum = 0
		self.instructions = []

		return

class Instruction:
	def __init__(self, leftX, rightX, Y):
		self.leftX = leftX
		self.rightX = rightX
		self.Y = Y
		self.sequence = []

		return

#creating MapData class
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

#creating CharacterData class
class CharacterData:
	def __init__(self):
		self.skillsNum = 0
		self.buffsNum = 0
		self.skills = []
		self.buffs = []

		return

class Skill:
	def __init__(self, name, key):
		self.name = name
		self.key = key

		return

class Buff:
	def __init__(self, name, key, cooldown, waitTime, toggle):
		self.name = name
		self.key = key
		self.cooldown = cooldown
		self.waitTime = waitTime
		self.toggle = toggle

		return

def menu():
	#resetting mapdata, char, route
	mapdata = MapData()
	char = CharacterData()
	route = RouteData()

	#prompt user with menu
	print("MENU")
	print("1. Add new route")
	print("2. Edit route")
	print("3. Exit program")
	choice = int(input("Enter your choice: "))

	#user input checking
	while (choice != 1 and choice != 2 and choice != 3):
		choice = int(input("Enter a valid option: "))

	#if adding new character data
	if (choice == 1):
		menuAddRoute()

	#if editing character data
	if (choice == 2):
		menuEditRoute()

	#if exiting program
	if (choice == 3):
		exitProgram()
		
	return

#menu to add new route data
def menuAddRoute():
	#prompt user for character name
	charName = input("Enter character name: ")
	if(charName == ""):
		configure = ConfigParser()
		configure.read("default.ini")
		charName = configure.get("general", "character")

	#user input checking
	while (not(os.path.exists(os.path.join(chardir, charName + ".ini")))):
		charName = input("Enter a valid character name: ")

	#prompt user for map name
	mapName = input("Enter map name: ")
	if(mapName == ""):
		configure = ConfigParser()
		configure.read("default.ini")
		mapName = configure.get("general", "map")

	#user input checking
	while (not(os.path.exists(os.path.join(mapdir, mapName + ".ini")))):
		mapName = input("Enter a valid map name: ")

	#setting character and map, then writing to file
	route.charName = charName
	route.mapName = mapName
	writeToFile()

	return

#menu to edit route data
def menuEditRoute():
	#prompt user for character name
	charName = input("Enter character name: ")
	if(charName == ""):
		configure = ConfigParser()
		configure.read("default.ini")
		charName = configure.get("general", "character")

	#user input checking
	while (not(os.path.exists(os.path.join(chardir, charName + ".ini")))):
		charName = input("Enter a valid character name: ")

	#prompt user for map name
	mapName = input("Enter map name: ")
	if(mapName == ""):
		configure = ConfigParser()
		configure.read("default.ini")
		mapName = configure.get("general", "map")
		
	#user input checking
	while (not(os.path.exists(os.path.join(mapdir, mapName + ".ini")))):
		mapName = input("Enter a valid map name: ")

	#reading from file with input specified character and map
	readCharacterFromFile(charName)
	readMapFromFile(mapName)
	readFromFile(charName, mapName)

	#add section
	flag = True
	while (flag == True):
		menuAddSection()
		choice = input("Would you like to add another section? (y/n): ")

		#user input checking
		while (choice != "y" and choice != "n"):
			choice = input("Enter a valid option (y/n): ")

		if (choice == "n"):
			flag = False

	return

#function to add instructions to a section
def menuAddSection():
	#printing list of platforms
	printPlatforms()

	#prompt user input for section range
	while (True):
		inputList = list(map(int, input("Enter the section you want to add instructions to (x1, x2, y): ").split(",")))
		if (inputList[0] == "pos"):
			charLoc = characterPos()
			print("Character position: " + str(charLoc[0]) + ", " + str(charLoc[1]))
		else:
			while (len(inputList) != 3):
				inputList = list(map(int, input("Enter a valid range (x1, x2, y): ").split(",")))
			choice = input("Is X: " + str(inputList[0]) + " - " + str(inputList[1]) + " | Y: " + str(inputList[2]) + " a good range? (y/n): ")
			while (choice != "y" and choice != "n"):
				choice = input("Enter a valid option (y/n): ")
			if (choice == "y"):
				break

	route.instructions.append(Instruction(inputList[0], inputList[1], inputList[2]))

	#add new commands to sequence
	flag = True
	while (flag == True):
		flag = menuCommands()

	route.routeNum = route.routeNum + 1
	writeToFile()

	return

#command list menu
def menuCommands():
	#setting iterator to current instruction
	it = len(route.instructions) - 1

	#printing current command sequence
	print()
	print("The current sequence of command for this section is:")
	for i in range(len(route.instructions[it].sequence)):
		print(str(i + 1) + ". " + route.instructions[it].sequence[i])
	print()

	#get new command
	print("Add a new command")
	print("1. Basic commands")
	print("2. Skills")
	print("3. Wait")
	print("4. Finish adding")
	choice = int(input(">> "))

	#user input checking
	while (choice != 1 and choice != 2 and choice != 3 and choice != 4):
		choice = int(input("Enter a valid option: "))

	#if basic commands
	if (choice == 1):
		#print basic commands list
		basicCommandsList = ["hold (left, right, up, down)", "release (left, right, up, down)", "jump", "attack"]
		print("Add a basic command")
		for i in range(len(basicCommandsList)):
			print(str(i + 1) + ". " + basicCommandsList[i])

		#take user input
		userInput = input(">> ").split()
		while (userInput != ["jump"] and userInput != ["attack"]):
			if (len(userInput) != 2):
				userInput = input("Enter a valid command: ").split()
			elif (userInput[0] != "hold" and userInput[0] != "release"):
				userInput = input("Enter a valid command: ").split()
			elif (userInput[1] != "left" and userInput[1] != "right" and userInput[1] != "up" and userInput[1] != "down"):
				userInput = input("Enter a valid command: ").split()
			else:
				break	

		#add user input to sequence
		if (userInput[0] == "hold" or userInput[0] == "release"):
			route.instructions[it].sequence.append(userInput[0] + '("' + userInput[1] + '")')
		else:
			route.instructions[it].sequence.append(userInput[0] + "()")

	#if skills
	if (choice == 2):
		#print skills list
		print("LIST OF SKILLS")
		for i in range(char.skillsNum):
			print(str(i + 1) + ". " + char.skills[i].name)
		userInput = input(">> ")

		#check user input
		while (True):
			if (not(is_number(userInput))):
				userInput = input("Enter the number of the skill: ")
			elif (int(userInput) < 1 or int(userInput) > char.skillsNum):
				userInput = input("Enter the number of the skill: ")
			else:
				break

		#add user input to sequence
		route.instructions[it].sequence.append('useSkill("' + char.skills[int(userInput) - 1].name + '")')

	#if wait
	if (choice == 3):
		choice = input("Wait for how many seconds?: ")
		while (not(is_number(choice))):
			choice = input("Enter a valid number: ")
		route.instructions[it].sequence.append("wait(" + choice + ")")

	#if finish adding
	if (choice == 4):
		return False

	return True

#end program function
def exitProgram():
	#exiting program
	print("Exiting program")
	sys.exit()

	return

#reading character data from file
def readCharacterFromFile(charName):
	#opening character file
	charPath = os.path.join(chardir, charName + ".ini")
	configure = ConfigParser()
	configure.read(charPath)

	#reading general section
	char.charName = configure.get("general", "name")
	char.hpKey = configure.get("general", "hpKey")
	char.mpKey = configure.get("general", "mpKey")
	char.hpThreshold = configure.getint("general", "hpThreshold")
	char.mpThreshold = configure.getint("general", "mpThreshold")
	char.jumpKey = configure.get("general", "jumpKey")
	char.npcKey = configure.get("general", "npcKey")
	char.attackKey = configure.get("general", "attackKey")
	char.petFood = configure.get("general", "petFood")
	char.autoPetFood = configure.get("general", "autoPetFood")
	char.skillsNum = configure.getint("general", "skillsNum")
	char.buffsNum = configure.getint("general", "buffsNum")

	#reading skills section
	for i in range(char.skillsNum):
		dataList = [value for value in configure["skills"]["skill" + str(i + 1)].split(', ')]
		char.skills.append(Skill(dataList[0], dataList[1]))

	#reading buffs section
	for i in range(char.buffsNum):
		dataList = [value for value in configure["buffs"]["buff" + str(i + 1)].split(', ')]
		char.buffs.append(Buff(dataList[0], dataList[1], dataList[2], dataList[3], dataList[4]))

	return

#reading map data from file
def readMapFromFile(mapName):
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

#writing route data to file
def writeToFile():
	#opening route data file
	routePath = os.path.join(routedir, route.charName + "_" + route.mapName + ".ini")
	file = open(routePath, "w")

	#writing general section
	file.write("[general]\n")
	file.write("charName = " + route.charName + "\n")
	file.write("mapName = " + route.mapName + "\n")
	file.write("routeNum = " + str(route.routeNum) + "\n")
	file.write("\n")

	#writing routes
	file.write("[routes]\n")
	for i in range(route.routeNum):
		file.write("route" + str(i + 1) + "range" + " = " + str(route.instructions[i].leftX) + ", " + str(route.instructions[i].rightX) + ", " + str(route.instructions[i].Y) + "\n")
		file.write("route" + str(i + 1) + "sequence" + " = ")
		for j in range (len(route.instructions[i].sequence)):
			file.write(route.instructions[i].sequence[j])
			if (j + 1 != len(route.instructions[i].sequence)):
				file.write(", ")
		file.write("\n")

	#closing file
	file.close()

	#prompting user if successfully written
	print("Route data successfully written.")

	return

#reading route data from file
def readFromFile(charName, mapName):
	#opening route data file
	routePath = os.path.join(routedir, charName + "_" + mapName + ".ini")
	configure = ConfigParser()
	configure.read(routePath)

	#reading general section
	route.charName = configure.get("general", "charName")
	route.mapName = configure.get("general", "mapName")
	route.routeNum = configure.getint("general", "routeNum")

	#reading routes section
	for i in range(route.routeNum):
		rangeList = [int(value) for value in configure["routes"]["route" + str(i + 1) + "range"].split(", ")]
		route.instructions.append(Instruction(rangeList[0], rangeList[1], rangeList[2]))
		sequenceList = [value for value in configure["routes"]["route" + str(i + 1) + "sequence"].split(", ")]
		for j in range(len(sequenceList)):
			route.instructions[i].sequence.append(sequenceList[j])

	return

#function to print the list of platforms
def printPlatforms():
	print("LIST OF PLATFORMS")
	for i in range(mapdata.platformsNum):
		print("(" + str(i + 1) + ") X: " + str(mapdata.platforms[i].leftX) + " - " + str(mapdata.platforms[i].rightX) + " | Y: " + str(mapdata.platforms[i].Y))

	return

#function to check if input is a number
def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

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
	global chardir
	global routedir
	global assets

	maindir = os.path.dirname(__file__)
	mapdir = os.path.join(maindir, "map data")
	chardir = os.path.join(maindir, "character data")
	routedir = os.path.join(maindir, "route data")
	assetsdir = os.path.join(maindir, "assets")

	#initializing global classes
	global mapdata
	global char
	global route
	mapdata = MapData()
	char = CharacterData()
	route = RouteData()

	#initializing global character marker
	global charMarker
	charMarker = os.path.join(assetsdir, "characterminimap.png")

	#prompting user with menu
	while(True):
		menu()

	return

main()