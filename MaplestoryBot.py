import sys
import os
import pyautogui
import keyboard
import random
import win32api, win32con
from configparser import ConfigParser
import time

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
		self.timer = []

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

class Potions:
	def __init__(self):
		#initializing variables
		self.minHP = int(890 + ((1054 - 890) * (char.hpThreshold / 100)))
		self.minMP = int(890 + ((1054 - 890) * (char.mpThreshold / 100)))
		self.hpKey = char.hpKey
		self.mpKey = char.mpKey

		return

	def checkPotions(self):
		im = pyautogui.screenshot()
		if(im.getpixel((self.minHP, 1039))[0] < 200):
			press(self.hpKey)
			wait(0.4)
		if(im.getpixel((self.minMP, 1055))[2] < 200):
			press(self.mpKey)
			wait(0.4)

		return

class Rune:
	def __init__(self):
		self.timer = time.perf_counter()
		self.status = 0
		self.x = None
		self.y = None

#main menu function
def menu():
	#resetting mapdata, char, route
	mapdata = MapData()
	char = CharacterData()
	route = RouteData()

	#prompt user with menu
	print("MENU")
	print("1. Run bot")
	print("2. Exit program")
	choice = int(input("Enter your choice: "))

	#user input checking
	while (choice != 1 and choice != 2):
		choice = int(input("Enter a valid option: "))

	#if running bot
	if (choice == 1):
		runBot()

	#if exiting program
	if (choice == 2):
		exitProgram()
		
	return

#pause menu function
def menuPause():
	#printing menu and receiving input
	print("PAUSE MENU")
	print("1. Continue Bot")
	print("2. Exit Bot")
	choice = int(input(">> "))

	#checking if choice is valids
	while(choice != 1 and choice != 2):
		choice = int(input("Enter a valid input: "))

	#exit bot
	if(choice == 2):
		print("Exiting bot")
		release('Left')
		release('Right')
		sys.exit()

	#continue bot
	print("Resuming bot")
	refresh()
	return

#run bot function
def runBot():
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
	readRouteFromFile(charName, mapName)
	global potions
	potions = Potions()


	#ready user for bot
	while (True):
		choice = input("You will have 2 seconds to tab into the game. Are you ready to start? (y/n): ")
		while (choice != "y" and choice != "n"):
			choice = input("Enter a valid option (y/n): ")
		if (choice == "y"):
			break
	wait(2)

	#initial buffs
	if (char.autoPetFood == "on"):
		press(char.petFood)
		char.petTimer = time.perf_counter() + 1000
		wait(0.2)
	initialBuffs()
	refresh()

	#run sequence
	while (True):
		runSequence()
		refresh()

	return

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
		char.buffs.append(Buff(dataList[0], dataList[1], float(dataList[2]), float(dataList[3]), dataList[4]))

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

#reading route data from file
def readRouteFromFile(charName, mapName):
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

#function to run buffs at bot start
def initialBuffs():
	for i in range(char.buffsNum):
		if(char.buffs[i].toggle == "on"):
			press(char.buffs[i].key)
			wait(char.buffs[i].waitTime)
			char.timer.append(time.perf_counter() + char.buffs[i].cooldown)
		else:
			char.timer.append(time.perf_counter() + char.buffs[i].cooldown)

	return

#function to cycle buffs and check for expired cooldowns
def checkBuffs():
	for i in range(char.buffsNum):
		if (char.buffs[i].toggle == "on"):
			if(time.perf_counter() > char.timer[i]):
				press(char.buffs[i].key)
				wait(char.buffs[i].waitTime)
				char.timer[i] = (time.perf_counter() + char.buffs[i].cooldown)

	return

#function to check pet food timer
def checkPetFood():
	if (char.autoPetFood == "on"):
		if (time.perf_counter() > char.petTimer):
			press(char.petFood)
			char.petTimer = time.perf_counter() + 1000
			wait(0.2)

	return

#checking for rune and navigating to it if it exists
def checkRune():
	#if rune does not exist
	if (rune.status == 0 and time.perf_counter() > rune.timer):
		runePos = pyautogui.locate(runeMarker, pyautogui.screenshot(region=(mapdata.minX, mapdata.minY, mapdata.width, mapdata.height)))
		#if rune does not exist, check in 1 min
		if (runePos == None):
			rune.timer = time.perf_counter() + 60
		#if rune is found
		else:
			rune.status = 1
			#mark rune position with offset
			rune.x = runePos[0] + 2
			rune.y = runePos[1] - 2
			#find rune platform
			for i in range(mapdata.platformsNum):
				if (rune.y == mapdata.platforms[i].Y and rune.x >= mapdata.platforms[i].leftX and rune.x <= mapdata.platforms[i].rightX):
					rune.platformID = i
					break

	#if rune exists already
	elif (rune.status == 1):
		charPos = characterPos()
		#if on same platform, move to it, else skip for now
		if (charPos[1] == mapdata.platforms[rune.platformID].Y and charPos[0] >= mapdata.platforms[rune.platformID].leftX and charPos[0] <= mapdata.platforms[rune.platformID].rightX):
			isRunePlatform = True
			while (isRunePlatform == True):
				potions.checkPotions()
				charPos = characterPos()
				#if fallen from platform, skip for now
				if (charPos[1] > rune.y + 2):
					break
				#if standing on rune, solve it
				if (charPos[1] == rune.y and charPos[0] >= rune.x - 1 and charPos[0] <= rune.x + 1):
					press(char.npcKey)
					wait(0.3)
					result = True #solveRune()
					#if solved
					if (result == True):
						rune.status = 0
						rune.timer = time.perf_counter() + 60
						return
				#if left of rune, move right
				elif (charPos[0] < rune.x):
					hold("right")
					wait(0.1)
					release("right")
				#if right of
				elif (charPos[0] > rune.x):
					hold("left")
					wait(0.1)
					release("left")

	return

#function to refresh and check variables in between sequences
def refresh():
	#check if pause key is pressed
	if(keyboard.is_pressed("F8")):
		menuPause()

	#potion check
	potions.checkPotions()

	#check buffs
	checkBuffs()

	#check pet food
	checkPetFood()

	#check rune
	#checkRune()

	return

#function to run a sequence step
def runSequence():
	#get player location
	charPos = characterPos()
	section = findSection(charPos)

	while(section == None):
		charPos = characterPos()
		section = findSection(charPos)

	#run sequence of the section
	for i in range(len(route.instructions[section].sequence)):
		exec(route.instructions[section].sequence[i])

	return

#getting character position on minimapdata
def characterPos():
	charPos = pyautogui.locate(charMarker, pyautogui.screenshot(region=(mapdata.minX, mapdata.minY, mapdata.width, mapdata.height)))

	return charPos

#finds the section of the character positiong
def findSection(charPos):
	if (charPos == None):
		return None

	for i in range (route.routeNum):
		if (route.instructions[i].Y == charPos[1] and route.instructions[i].leftX <= charPos[0] and route.instructions[i].rightX >= charPos[0]):
			return i
		
	return None

#function to wait x seconds
def wait(x):
	time.sleep(x)

#function to press a key
def press(key):
	keyboard.press(key)
	wait(0.05)
	keyboard.release(key)

#function to hold a key
def hold(key):
	keyboard.press(key)

#function to release a key
def release(key):
	keyboard.release(key)

#function to jump
def jump():
	press(char.jumpKey)

#function to attack
def attack():
	press(char.attackKey)

#function to use skill
def useSkill(name):
	for i in range(char.skillsNum):
		if (name == char.skills[i].name):
			press(char.skills[i].key)
			return

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
	global rune
	mapdata = MapData()
	char = CharacterData()
	route = RouteData()
	rune = Rune()

	#initializing global markers
	global charMarker
	global runeMarker
	charMarker = os.path.join(assetsdir, "characterminimap.png")
	runeMarker = os.path.join(assetsdir, "runeminimap.png")

	#prompting user with menu
	while(True):
		menu()

	return

main()