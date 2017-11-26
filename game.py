#!/usr/bin/python
# CST205 Lab 11 & 12
# November 22, 2017
#
# Team 5, Hopper
#  Jose Garcia Ledesma
#  Grace Alvarez
#  Christian Guerrero
#  Gabriel Loring


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

# Global to describe how many empty commands before it assumed the player wants to quit
EMPTY_ENTERS_TO_BAIL_OUT = 3

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
    "room_description" : "The the office is a nice wood paneled room with protraits of stuffy old dudeds on the North, West and South walls.  There is a desk with a key on it labled 'Library_key'",
    "passable_NESW" : "NYNN",
    "npc" : larry,
    "object" : "library_key"}

staircase = {
    "room_description" : "The saircase is ornaite and fancey designed to allow someone to make a grand entrance.  The stairs start on the south and exit to the west on the top floor.  Trying to exit to the north or east would result in a nasty fall",
    "passable_NESW" : "NNYY",
    "npc" : larry,
    "object" : "nothing"}

hidden = {
    "room_description": "You've found the hidden room. Here lies the Catalina necklace in a locked wooden chest. To open the chest you must first unlock the secret ",
    "passable_NESW": "NNYN",
    "npc": larry,
    "object": "necklace"}

billiards = {
    "room_description": "This is the billiards room. To the north, east and south walls are blocked off.To exit return east. To open the vault type open.",
    "passable_NESW": "NYNN",
    "npc": larry,
    "object": "secret_book"}

ballroom = {
    "room_description": "You have entered the ballroom. The ballroom is filled with 100 guests, all dancing. To the north is the staircase, to the east lies the library, to the west lies the billiards room. You must blend in with the party. Do not get caught as you make your way to the next room.",
    "passable_NESW": "YCYY",
    "npc": larry,
    "object": "nothing"}

library = {
    "room_description": "The room is the library. The library holds books to the north, south, and west. Along these walls is a special book that leads to a hidden room. Find the book that hisses and slither and you will find the secret room.",
    "passable_NESW": "CNNY",
    "npc": larry,
    "object": "nothing"}


park = {
    "room_description" : "The park is nice, a good place to take your dog, or to step in something left by somonelses dog. To the north is the back wall of the museum, east leads to the starting position and both south and west lead to the the edge of the game world",
    "passable_NESW" : "NYNN",
    "npc" : larry,
    "object" : "nothing"}

start = {
    "room_description" : "This is the staging area for your heist to the north is the ballroom, west is the park and south is the edge of the game world, your getaway vehicle is to the east.",
    "passable_NESW" : "YYNY",
    "npc" : larry,
    "object" : "nothing"}

getaway_vehicle = {
    "room_description" : "A 1973 Oldsmobile Delta 88, I wonder if Sam Raimi is directing this heist ",
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
actions   = ["get", "take", "steal", "lift", "snatch", "borrow", "use", "open", "close", "examine", "look", "close", "show", "kick"]

directions = [ "left", "right", "forward", "ahead", "back", "up", "down", "north", "south", "east", "west" ]
items   = ["door", "gun", "safe", "map", "necklace", "key", "secret" ]
people = ["self", "dog", "scooby", "larry"]

administrative = ["draw", "debug", "save", "help", "explain", "tutorial", "exit", "quit"]

def debugLog(functionName, action, message):
    pass
    if functionName == "debugLog":
        printNow(debugLog.string)
    #debugLog.counter +=1
    #debugLog.string = ("%s\n%04d\t%s:\t%s:\t%s"%(debugLog.string, debugLog.counter, functionName, action, message))

def titleMessage():
    printNow(title)
    return

def welcomeMessage():
    #printNow("++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
    #printNow(title)
    printNow("++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
    printNow("Welcome to The Heist")
    printNow("++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
    printNow("Type start to begin")
    printNow("Type help to learn how to play")
    printNow("Type exit to leave the game")
    printNow("++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
    return

def story():
    printNow("Larry is on a mission to find the Catalina necklace (worth 10 million).")
    printNow("He has studied the blueprints to the PyCharm Mansion.")
    printNow("A ball is being thrown at the PyCharm Mansion tonight.")
    printNow("Larry is entering the ball under the alias Jonathon Windsor")
    printNow("You must help Larry find the Catalina necklace, but be careful not to get caught.")
    printNow("As you go through the mansion you will find clues that lead you to a room with a hidden passage")
    printNow("Find that passage and you will find the necklace")
    return

'''
def library():
    printNow("")
    printNow("You have just entered the library.")
    printNow("1 - North to book wall")
    printNow("2 - East to Office door")
    printNow("3 - West to Ballroom door")
    printNow("4 - South to Street door")
    printNow("Choose a direction")
'''

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

def getUserInput(promptString = ""):
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


def drawMap():
    canvas = "+---------------+---------------+---------------+\n"
    for row in map:
        canvas = canvas + "|"
        for room in row:
            canvas = canvas + "\t" + room + "\t|"
        canvas = canvas + "\n|\t\t|\t\t|\t\t|\n"
        canvas = canvas + "+---------------+---------------+---------------+\n"

    printNow(canvas)


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
        describeRoom()
    elif passable == 'C':    # C is a closed door
        printNow("You try but the door is closed")
    else:
        printNow("You can not move in that direction")


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
    elif item == "west" or directioitemns == "left":
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
    printNow("You are in the %s"%currentRoom)
    printNow("%s\n\n"%rooms[currentRoom]["room_description"])


def office_handler(action, item, subject):
    '''
    The room handle takes care of opening or closing doors, using inventor items, adding inventory items and NPC interactions
    '''
    if item == 'key':
    	player["inventory"] = 'key'
    	printNow("Sliding your hand over the key you palm it and let your arm fall to your side as your fingers loosen their grip allowing it to fall silently into your pocket.\n")

def staircase_handler(action, item, subject):
    '''
    The room handle takes care of opening or closing doors, using inventor items, adding inventory items and NPC interactions
    '''
    printNow("Stairs are a good way to get where you are going, but trying anything else on them could get you hurt.\n")
    describeRoom()

def hidden_handler(action, item, subject):
    '''
    The room handle takes care of opening or closing doors, using inventor items, adding inventory items and NPC interactions
    '''
    if  action == 'take' or action == 'get':
    	player["inventory"] == 'necklace'
    	printNow("Wasting no time you grab the necklace and concel it in your jacket.\n")

def billiards_handler(action, item, subject):
    '''
    The room handle takes care of opening or closing doors, using inventor items, adding inventory items and NPC interactions
    '''
    printNow("Sure you could sit around and play a game by yourself, or you could maybe go steal a necklace.\n")
    describeRoom()

def ballroom_handler(action, item, subject):
    '''
    The room handle takes care of opening or closing doors, using inventor items, adding inventory items and NPC interactions
    '''
    if player["inventory"] == 'key' and action == 'open':
    	ballroom["passable_NESW"] = "YOYY"
    	printNow("You take a quick glance around the room and then use your key to unlock the library door.\n")


def library_handler(action, item, subject):
    '''
    The room handle takes care of opening or closing doors, using inventor items, adding inventory items and NPC interactions
    '''
    if  item == 'book':
    	library["passable_NESW"] = "YNNY"
    	printNow("Grabbing the hissing book from the shelf you pull it out. Like any good episode of Scooby Doo a hidden panel slides open revealing a passage to the north.\n")

def park_handler(action, item, subject):
    '''
    The room handle takes care of opening or closing doors, using inventor items, adding inventory items and NPC interactions
    '''
    printNow("You really shouldnot be wasting time in the park. Steal the necklace and you can spend the res of your life in a park!\n")
    describeRoom()

def start_handler(action, item, subject):
    '''
    The room handle takes care of opening or closing doors, using inventor items, adding inventory items and NPC interactions
    '''
    pass

def getaway_vehicle_handler(action, item, subject):
    '''
    The room handle takes care of opening or closing doors, using inventor items, adding inventory items and NPC interactions
    '''
    pass


def gameLoop():
    titleMessage()
    welcomeMessage()
    story()
    debugLog("gameLoop", "start", "")
    gameOn = True
    gameCycles = 0
    describeRoom() # Let the player know where they are starting from
    while gameOn:
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


    debugLog("gameLoop", "exit", ("gameOn:\t%s\tgameCycles:\t%s"%(gameOn,gameCycles)))






gameLoop()

