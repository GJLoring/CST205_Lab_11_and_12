#!/usr/bin/python
# CST205 Final
# November 30, 2017
#
# Team 5, Hopper
#  Jose Garcia Ledesma
#  Grace Alvarez
#  Christian Guerrero
#  Gabriel Loring

import os
import java.awt.Font as Font
import time

gameScreenImages = {
    "title" : "HomeScreen.jpg",
    "office" : "OfficeRoom.jpg",
    "staircase" : "Staircase.jpg",
    "hidden" : "HiddenRoom.jpg",
    "billiards" : "BilliardsRoom.jpg",
    "ballroom" : "Ballroom.jpg",
    "library" : "Library.jpg",
    "park" : "Park.jpg",
    "start" : "Start.jpg",
    "getaway_vehicle" : "GetawayCar.jpg",
    "introduction" : "placeholder.jpg",  # If we want or have time for events we can do some, all or none from here down
    "win" : "Win.jpg",
    "loose" : "Mugged.jpg",
    "get_key" : "OfficeRoomkey.jpg",
    "get_secret" : "BilliardsRoomgetkey.jpg",
    "get_necklace" : "HiddenRoomNecklace.jpg",
    "open_book_case" : "Libraryopen.jpg",
    "open_door" : "Library.jpg",
    "fall_from_stairs" : "Staircasefall.jpg",
    "get_mugged" : "Mugged.jpg"
}

gameMapImages = {
    "title" : "placeholder.jpg",
    "office" : "map_office.jpg",
    "staircase" : "map_Staircase.jpg",
    "hidden" : "map_secret.jpg",
    "billiards" : "map_billiards.jpg",
    "ballroom" : "map_ballroom.jpg",
    "library" : "map_Library.jpg",
    "park" : "map_park.jpg",
    "start" : "map_start.jpg",
    "getaway_vehicle" : "map_getaway.jpg"
}

gameInventoryImages = {
    "nothing" : "inventory_empty.jpg",
    "key" : "inventory_key.jpg",
    "secret" : "inventory_secret.jpg",
    "necklace" : "inventory_necklace.jpg",
}

gameSounds = {
    "title" : "intro.wav",
    "office" : "office.wav",
    "staircase" : "stairs.wav",
    "hidden" : "placeholder.wav",
    "billiards" : "billiards.wav",
    "ballroom" : "ballroom.wav",
    "library" : "library.wav",
    "park" : "park.wav",
    "start" : "placeholder.wav",
    "getaway_vehicle" : "gataway_vehicler.wav",
    "introduction" : "intro.wav",  # If we want or have time for events we can do some, all or none from here down
    "win" : "win.wav",
    "loose" : "lose.wav",
    "get_key" : "get_key.wav",
    "get_secret" : "get_secret.wav",
    "get_necklace" : "get_necklace.wav",
    "open_book_case" : "open_book_case.wav",
    "open_door" : "open_door.wav",
    "fall_from_stairs" : "fall_from_stairs.wav",
    "get_mugged" : "get_mugged.wav"
}

# Test for Lab 11 bullet 1, Title Screen
title = '''
The Heist
An interactive test adventure by: Team 5, Hopper
Jose Garcia Ledesma  *  Grace Alvarez  *  Christian Guerrero  *  Gabriel Loring
'''

'''
Objective of the game is the find the Catalina necklace, worth 10 million.
The necklace is hidden in a secret chest.
Player takes 2 actions.
    1.) Player can move North, East, South, or West
    2.) and player can open door
If player does not find hidden necklace in the room entered return no jewels found.
Move to next room and repeat until jewels are found.
To win the game you must successfully find the Catalina necklace, exit the mansion, and get inside the getaway vehicle.


'''

# Globals to cover movment directions
NORTH = 0
EAST = 1
SOUTH = 2
WEST  = 3

MAP_WIDTH = 3

PAUSE_FOR_CUT_SCENE = 5.0

# Global to describe how many empty commands before it assumed the player wants to quit
EMPTY_ENTERS_TO_BAIL_OUT = 3

GAME_OUTPUT_CANVAS_COLOR = makeColor(0, 0, 0)
GAME_OUTPUT_CANVAS_WIDTH = 1024
GAME_OUTPUT_CANVAS_HEIGTH = 768

INVENTORY_LOCATION_X_AS_A_PERCENT_OF_SCREEN_WIDTH = 10
INVENTORY_LOCATION_Y_AS_A_PERCENT_OF_SCREEN_HEIGHT = 90

HEALTH_BAR_LOCATION_X_AS_A_PERCENT_OF_SCREEN_WIDTH = 10
HEALTH_BAR_LOCATION_Y_AS_A_PERCENT_OF_SCREEN_HEIGHT = 90
HEALTH_BAR_SIZE_X_AS_A_PERCENT_OF_SCREEN_WIDTH = 90
HEALTH_BAR_SIZE_Y_AS_A_PERCENT_OF_SCREEN_HEIGHT = 5

MAP_LOCATION_X_AS_A_PERCENT_OF_SCREEN_WIDTH = 10
MAP_LOCATION_Y_AS_A_PERCENT_OF_SCREEN_HEIGHT = 90

TEXT_LOCATION_X_AS_A_PERCENT_OF_SCREEN_WIDTH = 2
TEXT_LOCATION_Y_AS_A_PERCENT_OF_SCREEN_HEIGHT = 80

MAX_TEXT_WIDTH_IN_CHARS = 50
TEXT_HEIGHT = 24

HEALTHBAR_INSET_OFF_SIDES = 100
HEALTH_FONT_HEIGHT = 20
HEALTH_BAR_Y = 550
HEALTH_BAR_HEIGHT = HEALTH_FONT_HEIGHT + 4


TEXT_COLOR = makeColor(255, 255, 0)
TEXT_SHADOW = makeColor(128, 128, 128)
MAP_COLOR = makeColor(0, 255, 255)
COLOR_WHITE = makeColor(255, 255, 255)
COLOR_BLACK = makeColor(0, 0, 0)
COLOR_RED = makeColor(255, 0, 0)
COLOR_PURPLE = makeColor(128, 32, 192)
COLOR_GREEN = makeColor(0, 255, 0)

# A global dictionary to hold player attributes
player = {
    "health" :  100,
    "location": "start",
    "inventory": "nothing"}

# Lab 12 item C requires a loose condition a Non player character may be useful
larry = {
    "health" :  100,
    "location": "start",
    "inventory": "nothing"}


# OK apologies, the map is stored in triplicate!
#
# the first copy of the map is in the list map
# this is a list of rows and columns to lay out the "rooms" and their
# spacial arraingment.
#
# The 2nd is a dictionary for every room.  The dictionary holds the room description
# as well as a entry that describes the valid movments out of the room
# I have a place holder for a NPC and object
#
# The third copy of the map is in the rooms dictionary.  This lets me look
# up a specific rooms dictionary using its name.  not sure how happy I am with
# this, it is super hacky
map = [ [ "office",        "staircase", "hidden"],
        [ "billiards",     "ballroom",  "library"],
        [ "park",          "start",     "getaway_vehicle"]]

office = {
    "room_description" : "The office is a nice wood paneled room with portraits of stuffy old dudes on the North, West and South walls.  There is a desk with a key on it labeled 'Library_key' . Grab the key and continue on to find the locked chest holding the Catarina necklace.",
    "passable_NESW" : "NYNN",
    "npc" : larry,
    "object" : "library_key"}

staircase = {
    "room_description" : "The staircase is ornate and fancy. It is designed to allow someone to make a grand entrance. The stairs start on the south floor and exit to the west of the top floor. Exiting to the north or east would result in a nasty fall.",
    "passable_NESW" : "FFYY",
    "npc" : larry,
    "object" : "nothing"}

hidden = {
    "room_description": "You've found the hidden room. Here lies the Catalina necklace in a locked wooden chest. To open the chest you must first unlock the secret",
    "passable_NESW": "NNYN",
    "npc": larry,
    "object": "necklace"}

billiards = {
    "room_description": "The billiards room is filled with many games, but you won't find what you're looking for here. To open the vault type open.",
    "passable_NESW": "NYNN",
    "npc": larry,
    "object": "nothing"}

ballroom = {
    "room_description": "The ballroom is filled with 100 guests, all dancing. To the north is the staircase, to the east lies the library, to the west lies the billiards room. You must blend in with the party. Do not get caught as you make your way to the next room.",
    "passable_NESW": "YCYY",
    "npc": larry,
    "object": "nothing"}

library = {
    "room_description": "The room is the library. The library holds books along its walls. Along these walls is a special book that leads to a hidden room. Find the book that hisses and slithers and you will find the secret room.",
    "passable_NESW": "CNNY",
    "npc": larry,
    "object": "secret_book"}


park = {
    "room_description" : "The park used to be nice, a good place to take your dog, or to step in something left by someone else's dog.",
    "passable_NESW" : "NYNN",
    "npc" : larry,
    "object" : "nothing"}

start = {
    "room_description" : "This is the staging area for your heist. Your getaway vehicle is to the east.",
    "passable_NESW" : "YYNY",
    "npc" : larry,
    "object" : "nothing"}

getaway_vehicle = {
    "room_description" : "A 1973 Oldsmobile Delta 88, I wonder if Sam Raimi is directing this heist. Once you have the necklace, get and tell the driver to leave to win the game!",
    "passable_NESW" : "NNNY",
    "npc" : larry,
    "object" : "nothing"}


rooms = {
    "office": office,
    "staircase": staircase,
    "hidden": hidden,
    "billiards": billiards,
    "ballroom": ballroom,
    "library": library,
    "park": park,
    "start": start,
    "getaway_vehicle": getaway_vehicle}

# We need lists of words for the parser
#
# Words will break down to:
#    1. actions/ verbs
#        A) travel = travel  related words that tell us we should try to move the player
#        B) actions = Game verbs that will allow player interactions with the enviroment
#    2. Nouns / directions
#        A) directions = indicate how we shold translate the player to another room
#        B) items = things that cna be interacted with
#        C) people = NPCs?  not sure more of a place holder for the idea at the moment
#    3. Administrative
#        A) administrative = these are here for the program to see running program state and for the player to quit.
travel    = [ "go", "walk", "run", "skip", "get", "move", "travel", "head" ]
actions   = ["get", "take", "steal", "open", "close", "leave", "drive", "flee"]

directions = [ "left", "right", "forward", "ahead", "back", "up", "down", "north", "south", "east", "west" ]
items   = ["door", "gun", "safe", "map", "necklace", "key", "secret", "book" ]
people = ["self", "dog", "scooby", "larry"]

administrative = ["draw", "debug", "save", "help", "explain", "tutorial", "exit", "quit"]

gameScreen = makeEmptyPicture(GAME_OUTPUT_CANVAS_WIDTH,
                              GAME_OUTPUT_CANVAS_HEIGTH,
                              GAME_OUTPUT_CANVAS_COLOR)

def debugLog(functionName, action, message):
    pass
    if functionName == "debugLog":
        printNow(debugLog.string)
    #debugLog.counter +=1
    #debugLog.string = ("%s\n%04d\t%s:\t%s:\t%s"%(debugLog.string, debugLog.counter, functionName, action, message))

def openImage(imageFileName="placeholder.jpg"):
  '''
  Allow us to import image files from the programs image resource
  directory.  However since we do not know where on a users computer
  this program will be launched from, we first get our programs dir
  then join the audiopath so the user does not need to interact with
  a file or directory selection box
  '''
  dir_path = os.path.dirname(os.path.realpath(__file__))
  mediaImagesDir = os.path.join(dir_path, "images")
  print "Open Image:\n\tdir_path:\t\t%s\n\tmediaImagesDir:\t%s\n\timageFileName:\t%s"%(dir_path,mediaImagesDir,imageFileName) #TODO DEL ME
  setMediaPath(mediaImagesDir)
  imageObject = makePicture(getMediaPath(imageFileName))
  return imageObject

def openSound(soundFileName="placeholder.wav"):
  '''
  Allow us to import audio files from the programs audio resource
  directory.  However since we do not know where on a users computer
  this program will be launched from, we first get our programs dir
  then join the audiopath so the user does not need to interact with
  a file or directory selection box
  '''
  dir_path = os.path.dirname(os.path.realpath(__file__))
  mediaAudioDir = os.path.join(dir_path, "audio")
  print "Open Audio:\n\tdir_path:\t\t%s\n\tmediaAudioDir:\t%s\n\tsoundFileName:\t%s"%(dir_path,mediaAudioDir,soundFileName) #TODO DEL ME
  setMediaPath(mediaAudioDir)  
  soundObject = makeSound(getMediaPath(soundFileName))
  return soundObject

def pyCopy(source, targetX, targetY):
  '''
  Insert an alpha masked "Green Screen" image into the game
  '''
  #Make sure our destination is large enough
  if source.getWidth() > gameScreen.getWidth() or source.getHeight() >gameScreen.getHeight():
    raise #Image is to large to insert

  #Shift the image to fit inside destination if necessary
  if source.getWidth()+ targetX > gameScreen.getWidth():
    targetX = gameScreen.getWidth()-source.getWidth()
  if source.getHeight()+ targetY > gameScreen.getHeight():
    targetY = gameScreen.getHeight()-source.getHeight()

  #Actual insert
  for x in range (0, getWidth(source)):
    for y in range (0, getHeight(source)):
      pixelColor = getPixel(source, x, y)
      if getRed(pixelColor) > 250 and getBlue(pixelColor) > 250 or getGreen(pixelColor) > 250:
        continue
      if getRed(pixelColor) > 20 or getBlue(pixelColor) > 20 or getGreen(pixelColor) < 225:
        setColor( getPixel(gameScreen, x+targetX, y+targetY),getColor(pixelColor))

def drawInventory():
  '''
  Draw on screen player inventory
  '''
  imageFileName=gameInventoryImages[player["inventory"]]
  item = openImage(imageFileName=imageFileName)
  pyCopy(item, 900, 470)



def drawMap():
  '''
  Draw on screen map to help the player navigate the game
  '''
  imageFileName=gameMapImages[player["location"]]
  item = openImage(imageFileName=imageFileName)
  pyCopy(item, 700, 625)


def drawHealthBar():
  '''
  Draw and label on screen health indicator
  '''
  Health_POS = int((GAME_OUTPUT_CANVAS_WIDTH - (HEALTHBAR_INSET_OFF_SIDES*1) )* (float(player["health"])/100))
  #Draw Full health portion of the bar
  addRectFilled(gameScreen,
                HEALTHBAR_INSET_OFF_SIDES,
                HEALTH_BAR_Y,
                Health_POS,
                HEALTH_BAR_HEIGHT,
                COLOR_PURPLE)
  #Draw empty health portion of the bar
  addRectFilled(gameScreen,
                Health_POS,
                HEALTH_BAR_Y,
                GAME_OUTPUT_CANVAS_WIDTH-(2*HEALTHBAR_INSET_OFF_SIDES),
                HEALTH_BAR_HEIGHT,
                COLOR_BLACK)
  #Draw Boarder around health bar
  addRect(gameScreen,
          HEALTHBAR_INSET_OFF_SIDES,
          HEALTH_BAR_Y,
          GAME_OUTPUT_CANVAS_WIDTH-(2*HEALTHBAR_INSET_OFF_SIDES),
          HEALTH_BAR_HEIGHT,
          COLOR_RED)

  # Put the word Health on the bar with the health value
  msgString = ("Health: %i"%player["health"])
  xpos = int(GAME_OUTPUT_CANVAS_WIDTH * (float(50)/100))
  style = makeStyle("Courier", Font.BOLD, HEALTH_FONT_HEIGHT)
  addTextWithStyle(gameScreen, xpos, HEALTH_BAR_Y+HEALTH_FONT_HEIGHT, msgString, style, COLOR_WHITE)


def loadRoomImage(imageFileName):
  '''
  Draw on screen image into game canvas, center left to right, and align to top
  '''
  room = openImage(imageFileName=imageFileName)
  copyInto(room, gameScreen, 0, 0)
  repaint(gameScreen)
  return

def drawText(x,y,maxWidth,color,shadow,textString):
  '''
  Draw text on the screen to communicate with the user.  Draw text twice
  once in shadow color and then -1,-1 pixel offest in normal color
  '''
  ypos = int(GAME_OUTPUT_CANVAS_HEIGTH * (float(y)/100))
  xpos = int(GAME_OUTPUT_CANVAS_WIDTH * (float(x)/100))
  style = makeStyle("Courier", Font.BOLD, TEXT_HEIGHT)

  #Clear the area where we are going to draw our text
  addRectFilled(gameScreen,
                0,
                ypos-TEXT_HEIGHT,
                GAME_OUTPUT_CANVAS_WIDTH - 350 ,
                GAME_OUTPUT_CANVAS_HEIGTH-ypos,
                COLOR_BLACK)

  #Allow lines to wrap if they are too long
  count = 0
  tmp = ""
  for char in textString:
    if count == 0 and char.isalnum()==False and char != ' ':
      continue
    else:
      tmp = tmp + char
      count = count + 1

    #If we are getting close to the end of the line and see a
    # space it is probally a good idea to just go ahead and wrap
    # to a new line
    if count >= (maxWidth - 6) and char == ' ':
      count = 0
      tmp = tmp + '\n'

    # We are out of space and now must wrap even if it means splitting a word
    if count >= maxWidth:
      count = 0
      tmp = tmp + '\n'

  lengthLimitedText = tmp
  lines = lengthLimitedText.split("\n")
  for line in lines:
    addTextWithStyle(gameScreen, xpos+1, ypos+1, line, style, shadow)
    addTextWithStyle(gameScreen, xpos, ypos, line, style, color)
    ypos = ypos + TEXT_HEIGHT
  repaint(gameScreen)
  return

def playRoomSound():
  '''
  Play the ambient sound for the room when a room is entered
  '''
  file = openSound(gameSounds[player["location"]])
  play(file)

def refreshScreen():
  show(gameScreen)

def titleMessage():
    printNow(title)
    return

def welcomeMessage():
    welcomString =                "++++++++++++++++++++++++++++++++++++\n"
    welcomString = welcomString + "       Welcome to The Heist \n"
    welcomString = welcomString + "++++++++++++++++++++++++++++++++++++\n"
    welcomString = welcomString + "  Type help to learn how to play \n"
    welcomString = welcomString + "    Type exit to leave the game \n"
    welcomString = welcomString + "++++++++++++++++++++++++++++++++++++\n"
    outputStringToGraphic(welcomString)
    return

def story():
    storyString = "Larry is on a mission to find the Catalina necklace (worth 10 million).\n"
    storyString = storyString + "He has studied the blueprints to the PyCharm Mansion.\n"
    storyString = storyString + "A ball is being thrown at the PyCharm Mansion tonight.\n"
    storyString = storyString + "Larry is entering the ball under the alias Jonathon Windsor\n"
    storyString = storyString + "You must help Larry find the Catalina necklace, but be careful not to get caught.\n"
    storyString = storyString + "As you go through the mansion you will find clues that lead you to a room with a hidden passage\n"
    storyString = storyString + "Find that passage and you will find the necklace\n"
    showInformation(storyString)
    return

def parseInput(userString):
    '''
    This is a super basic parser.  It assumes we will never have a more complicated user command then
    Verb, Noun, Subject
    Give  Key Larry
    it also does not expect that all elements will be present
    Walk West
    It does this by looking at all of the word lists and seeing if there is a match in the user input.
    If multiple matches are found the last match is the one returned
    '''
    caseCorrectedString = userString.lower()

    action = find_action_words(userString)
    item = find_directions_or_nouns(userString)
    subject = find_subject_words(userString)

    debugLog("parseInput", "return", ("%s\t%s\t%s"%(action, item, subject)))
    return action, item, subject

def find_subject_words(userString):
    '''
    Search the user typed command for any word in our subject string list
    we do not respect SPACES so a substring match will still be a match.
    Also Note we run until we run out of words to search so if two words in the
    list match, we return the last match
    '''
    subject = ""
    for x in people:
        if x in userString:
            subject = x
    return subject

def find_directions_or_nouns(userString):
    '''
    Search the user typed command for any word in our subject string list
    we do not respect SPACES so a substring match will still be a match.
    Also Note we run until we run out of words to search so if two words in the
    list match, we return the last match
    '''
    item = ""
    for x in directions:
        if x in userString:
            item = x
    for x in items:
        if x in userString:
            item = x
    return item



def find_action_words(userString):
    '''
    Search the user typed command for any word in our subject string list
    we do not respect SPACES so a substring match will still be a match.
    Also Note we run until we run out of words to search so if two words in the
    list match, we return the last match
    '''
    action = ""
    for x in actions:
        if x in userString:
            action = x
    for x in travel:
        if x in userString:
            action = x
    for x in administrative:
        if x in userString:
            action = x
    return action

def getUserInput(promptString = "Which direction do you want to go?"):
    '''
    Prompt the user to type in a command and return a lower case string of what the user typed.
    If the user accidently hits enter for an empty string they will be prompted again.
    if the user hits enter EMPTY_ENTERS_TO_BAIL_OUT in a row then the function bails out and
    returns assuming the user is frusterated and does not know how to quit.
    '''
    userInput = ""
    count = 0
    while userInput == "" and count < EMPTY_ENTERS_TO_BAIL_OUT:
        userInput = requestString(promptString)
        count += 1

    caseCorrected = userInput.lower()
    return caseCorrected


def isAdministrative(action="", item="", subject=""):
    if action == 'debug':
        return True
    if action == 'draw':
        drawMap()
        return True
    if action == 'explain' or action == "help" or action == "tutorial":
        tutorial()
        return True
    if (action in administrative):
        debugLog("isAdministrative", "COMMAND NOT IMPLIMENTED YET",action)
        return True

    return False


def tutorial():
    printNow("\n\nTutorial\n\n")
    printNow("The Parser uderstands actions, items and objects\n The order of words does not matter\n")
    printNow("Valid commands could be \"Walk north\" or \"look at door\"\n")
    printNow("\nActions the parser understands:")
    printNow(travel)
    printNow(actions)
    printNow("\nItems the parser understands:")
    printNow(items)
    printNow("\nObjects the parser understands:")
    printNow(people)
    printNow(directions)
    printNow("\nAdministrative commands the parser understands:")
    printNow(administrative)


def drawMap_depricated():
    canvas = "+---------------+---------------+---------------+\n"
    for row in map:
        canvas = canvas + "|"
        for room in row:
            canvas = canvas + "\t" + room + "\t|"
        canvas = canvas + "\n|\t\t|\t\t|\t\t|\n"
        canvas = canvas + "+---------------+---------------+---------------+\n"

    outputStringToGraphic(canvas)


def isTravelCommand(action, item, subject):
    '''
    Check if the user command is travel or player motion related.  If it is and the motion is possible
    move the player, otherwise return
    '''
    debugLog("isTravelCommand", "input", ("%s\t%s\t%s"%(action, item, subject)))
    if (action in travel) and ( item in directions ):

        DIRECTION_INDEX = convert_direction_to_index(item)
        try_to_move_player_to_new_room(DIRECTION_INDEX)

        return True
    return False

def try_to_move_player_to_new_room(DIRECTION_INDEX):
    currentRoom = player["location"]
    passable = rooms[currentRoom]["passable_NESW"][DIRECTION_INDEX]
    if passable == 'Y' or passable == 'O':    # Yes passable or O for open door
        player["location"] = movePlayer(DIRECTION_INDEX)
        playRoomSound()
        describeRoom()
    elif passable == 'C':    # C is a closed door
        showInformation("You try but the door is closed")
    elif passable == 'F':    # Fall hazard
        player["health"] = player["health"] - 50
        file = openSound(gameSounds["fall_from_stairs"])
        play(file)
        loadRoomImage(imageFileName=gameScreenImages["fall_from_stairs"])
        outputStringToGraphic("You tumble down the stairs and lose health")
        time.sleep(PAUSE_FOR_CUT_SCENE)   #Pause so the player can see the update
    else:
        showInformation("You can not move in that direction")


def convert_direction_to_index(item):
    '''
    The player may express motion in multiple different ways, North, up or such, convert these to
    a index 1-2-3-4 that represents motion direction N-E-S-W
    '''
    if item == "north" or item == "up":
        DIRECTION_INDEX = NORTH
    elif item == "east" or item == "right":
        DIRECTION_INDEX = EAST
    elif item == "south" or item == "down":
        DIRECTION_INDEX = SOUTH
    elif item == "west" or item == "left":
        DIRECTION_INDEX = WEST
    return DIRECTION_INDEX


def movePlayer(direction):
    '''
    The player has requested a move and the the move has external to this function been
    determined to permissible.
    Take the users current room and then naigate relative North is up, East is Right and so on
    '''
    currentRoomNumber = find_current_room_number()
    destinationRoomNumber = find_room_by_relative_direction(direction, currentRoomNumber)
    destinationRoomName = convert_room_number_to_rooom_name(destinationRoomNumber)
    return destinationRoomName

def convert_room_number_to_rooom_name(roomNumber):
    '''
    For navigation we use the map list of list.  Rooms are numbered 1 - 9 Left to Right, Top to Bottom
    This function counts through the rooms and returns the room name for the room number
    '''
    count = 0
    for row in map:
        for roomName in row:
            count = count + 1
            if roomNumber == count:
                return roomName

def find_current_room_number():
    '''
    We are currently keeping track of the user position on the map using the name of the room
    convert that name back to a room index numbered 1-9 Left to right top to bottom on the map
    '''
    currentRoom = player["location"]
    currentRoomNumber = 0
    for row in map:
        for room in row:
            currentRoomNumber = currentRoomNumber + 1
            if currentRoom == room:
                return currentRoomNumber

    return

def find_room_by_relative_direction(direction, currentRoomNumber):
    if direction == NORTH:
        newRoom = currentRoomNumber - MAP_WIDTH # North moves one row up in the map
    elif direction == EAST:
        newRoom = currentRoomNumber + 1
    elif direction == SOUTH:
        newRoom = currentRoomNumber + MAP_WIDTH # South moves one row down in the map
    elif direction == WEST:
        newRoom = currentRoomNumber - 1
    else:
        raise "Error bad direction index"

    return newRoom

def describeRoom():
    '''
    Display the room description text for the current room
    '''
    currentRoom = player["location"]
    msgString = ("You are in the %s"%currentRoom)
    msgString = ("\n%s"%rooms[currentRoom]["room_description"])
    outputStringToGraphic(msgString)
    printMoveDirections()

def decodeValidMotionToStrings(index):
    '''
    Create a user friendly string to describe why, or why not
    motion in a given direction is or is not possible
    '''
    currentRoom = player["location"]
    roomBoarder = rooms[currentRoom]["passable_NESW"][index]
    if roomBoarder == 'N':
      return ("A wall")
    elif roomBoarder == 'F':
      return ("A dangerous edge ")

    # We should have bailed out if there is a wall to the side
    # this means we are ok to try to look to this side
    currentRoomNumber = find_current_room_number()
    adjacentRoomNumber = find_room_by_relative_direction(index, currentRoomNumber)
    adjacentRoomName = convert_room_number_to_rooom_name(adjacentRoomNumber)

    if roomBoarder == 'Y':
        return adjacentRoomName
    elif roomBoarder == 'O':
        return ("An open door leading to %s"%adjacentRoomName)
    elif roomBoarder == 'C':    # C is a closed door
        return ("An closed door leading to %s"%adjacentRoomName)

def printMoveDirections():
    '''
    Display a compase rose type description of each direction and if it is passable
    '''

    northString =    ("\t\tNorth: %s"%(decodeValidMotionToStrings(NORTH)))
    printNow(northString)
    eastWestString = ("West: %s\t\t\tEast: %s"%(decodeValidMotionToStrings(WEST),decodeValidMotionToStrings(EAST)))
    printNow(eastWestString)
    southString =    ("\t\tSouth: %s"%(decodeValidMotionToStrings(SOUTH)))
    printNow(southString)


def office_handler(action, item, subject):
    '''
    The room handle takes care of opening or closing doors, using inventor items, adding inventory items and NPC interactions
    '''
    if item == 'key':
        player["inventory"] = 'key'
        file = openSound(gameSounds["get_key"])
        play(file)
        loadRoomImage(imageFileName=gameScreenImages["get_key"])
        outputStringToGraphic("Sliding your hand over the key you palm it and let your arm fall to your side as your fingers loosen their grip allowing it to fall silently into your pocket.\n")
        time.sleep(PAUSE_FOR_CUT_SCENE)   #Pause so the player can see the update

def staircase_handler(action, item, subject):
    '''
    The room handle takes care of opening or closing doors, using inventor items, adding inventory items and NPC interactions
    '''
    outputStringToGraphic("Stairs are a good way to get where you are going, but trying anything else on them could get you hurt.\n")
    describeRoom()

def hidden_handler(action, item, subject):
    '''
    The room handle takes care of opening or closing doors, using inventor items, adding inventory items and NPC interactions
    '''
    if player["inventory"] != 'secret':
      outputStringToGraphic('You must first have the secret to the chest')
      time.sleep(PAUSE_FOR_CUT_SCENE)   #Pause so the player can see the update
      return

    if action == 'take' or action == 'get':
        player["inventory"] = 'necklace'
        file = openSound(gameSounds["get_necklace"])
        play(file)
        loadRoomImage(imageFileName=gameScreenImages["get_necklace"])
        outputStringToGraphic("Wasting no time you grab the necklace and conceal it in your jacket.\n")
        time.sleep(PAUSE_FOR_CUT_SCENE)   #Pause so the player can see the update

def billiards_handler(action, item, subject):
    '''
    The room handle takes care of opening or closing doors, using inventor items, adding inventory items and NPC interactions
    '''
    if action == 'open':
      if player["inventory"] == 'key':
        outputStringToGraphic("You can only hold one hidden item at a time, use the key you have to open the library then come back here")
        time.sleep(PAUSE_FOR_CUT_SCENE)   #Pause so the player can see the update
        return

      player["inventory"] = 'secret'
      file = openSound(gameSounds["get_secret"])
      play(file)
      loadRoomImage(imageFileName=gameScreenImages["get_secret"])
      outputStringToGraphic("Opening the vault to find the secret to the chest with the necklace.\n")
      time.sleep(PAUSE_FOR_CUT_SCENE)   #Pause so the player can see the update

def ballroom_handler(action, item, subject):
    '''
    The room handle takes care of opening or closing doors, using inventor items, adding inventory items and NPC interactions
    '''
    if player["inventory"] == 'key' and action == 'open':
      ballroom["passable_NESW"] = "YOYY"
      player["inventory"] = ''
      file = openSound(gameSounds["open_door"])
      play(file)
      loadRoomImage(imageFileName=gameScreenImages["open_door"])
      outputStringToGraphic("You take a quick glance around the room and then use your key to unlock the library door.\n")
      time.sleep(PAUSE_FOR_CUT_SCENE)   #Pause so the player can see the update

def library_handler(action, item, subject):
    '''
    The room handle takes care of opening or closing doors, using inventor items, adding inventory items and NPC interactions
    '''
    if item == 'book':
        library["passable_NESW"] = "YNNY"
        file = openSound(gameSounds["open_book_case"])
        play(file)
        loadRoomImage(imageFileName=gameScreenImages["open_book_case"])
        outputStringToGraphic("Grabbing the hissing book from the shelf you pull it out. Like any good episode of Scooby Doo a hidden panel slides open revealing a passage to the north.\n")
        time.sleep(PAUSE_FOR_CUT_SCENE)   #Pause so the player can see the update

def park_handler(action, item, subject):
    '''
    The room handle takes care of opening or closing doors, using inventor items, adding inventory items and NPC interactions
    '''
    msgString = "You really should not be wasting time in the park. Steal the necklace and you can spend the rest of your life in a park!\n"
    msgString = msgString + "While your are in the park you are mugged by a gang of unruly pensioners and loose 50 health!\n"
    outputStringToGraphic(msgString)
    player["health"] = player["health"] - 50
    file = openSound(gameSounds["get_mugged"])
    play(file)
    loadRoomImage(imageFileName=gameScreenImages["get_mugged"])
    describeRoom()
    time.sleep(PAUSE_FOR_CUT_SCENE)   #Pause so the player can see the update

def start_handler(action, item, subject):
    '''
    The room handle takes care of opening or closing doors, using inventor items, adding inventory items and NPC interactions
    '''
    #updateScreen("Game start")
    pass

def getaway_vehicle_handler(action, item, subject):
    '''
    The room handle takes care of opening or closing doors, using inventor items, adding inventory items and NPC interactions
    '''
    if player["inventory"] == 'necklace':
      player["inventory"] = 'complete'
      file = openSound(gameSounds["getaway_vehicle"])
      play(file)
      outputStringToGraphic("With a nod to the getaway driver you pull out the necklace as she floors the accelerator comleting your escape.")
    else:
      outputStringToGraphic("Getting in the getaway vehicle without the necklace seems to upset your getaway driver, she roughs you up costing you 50 health!")

    time.sleep(PAUSE_FOR_CUT_SCENE)   #Pause so the player can see the update

def playerLoseScreen(playerName):
    file = openSound(gameSounds["loose"])
    play(file)
    msgString = "\nSorry! %s You have lost too much health.  Please try again!\n\nGAME OVER!"%(playerName)
    outputStringToGraphic(msgString)

def playerWinsScreen(playerName):
    file = openSound(gameSounds["win"])
    play(file)
    msgString = "\nYou won %s! \n\nGAME OVER!"%(playerName)
    outputStringToGraphic(msgString)

def outputStringToGraphic(stringMsg):
  '''
  Wrapper function for the majority of user update and status text
  '''
  drawText(  TEXT_LOCATION_X_AS_A_PERCENT_OF_SCREEN_WIDTH,
             TEXT_LOCATION_Y_AS_A_PERCENT_OF_SCREEN_HEIGHT,
             MAX_TEXT_WIDTH_IN_CHARS,
             TEXT_COLOR,
             TEXT_SHADOW,
             stringMsg)

def gameLoop():
    '''
    Main Game loop
    '''
    file = openSound(gameSounds["introduction"])
    play(file)
    show(gameScreen)
    loadRoomImage(imageFileName=gameScreenImages["title"])

    titleMessage()
    welcomeMessage()
    story()
    playerName = requestString("Please enter your name")
    gameOn = True
    gameCycles = 0
    describeRoom() # Let the player know where they are starting from
    while gameOn:
        loadRoomImage(imageFileName=gameScreenImages[player["location"]])
        drawHealthBar()
        drawInventory()
        drawMap()
        describeRoom()
        #See if the player died
        if player["health"] < 0:
            gameOn = False
            playerLoseScreen(playerName)
            continue

        #See if player has won
        if player["inventory"] == 'complete':
            gameOn = False
            playerWinsScreen(playerName)
            continue

        gameCycles += 1
        userString = getUserInput()
        (action, item, subject) = parseInput(userString)

        # See if the user want to quit
        if action == 'quit' or userString == "" or userString == "exit":
            gameOn = False
            continue

        #Are we moving
        if isTravelCommand(action, item, subject):
            continue

        # Administrative commands
        if isAdministrative(action, item, subject):
            continue

        # each room gets its own function to deal with event in it
        if player["location"] == "office":
            office_handler(action, item, subject)
        elif player["location"] == "staircase":
            staircase_handler(action, item, subject)
        elif player["location"] == "hidden":
            hidden_handler(action, item, subject)
        elif player["location"] == "billiards":
            billiards_handler(action, item, subject)
        elif player["location"] == "ballroom":
            ballroom_handler(action, item, subject)
        elif player["location"] == "library":
            library_handler(action, item, subject)
        elif player["location"] == "park":
            park_handler(action, item, subject)
        elif player["location"] == "start":
            start_handler(action, item, subject)
        elif player["location"] == "getaway_vehicle":
            getaway_vehicle_handler(action, item, subject)
        else:
            raise "Error no room to handle events"


# Automatically Start the game for the player
gameLoop()
