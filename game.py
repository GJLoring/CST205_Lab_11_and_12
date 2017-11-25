#!/usr/bin/python
# CST205 Lab 11
# November 22, 2017
#
# Team 5, Hopper
#  Jose Garcia Ledesma
#  Grace Alvarez
#  Christian Guerrero
#  Gabriel Loring


# Test for Lab 11 bullet 1, Title Screen
title = '''

 ████████╗██╗  ██╗███████╗    ██╗  ██╗███████╗██╗███████╗████████╗    
 ╚══██╔══╝██║  ██║██╔════╝    ██║  ██║██╔════╝██║██╔════╝╚══██╔══╝    
    ██║   ███████║█████╗      ███████║█████╗  ██║███████╗   ██║       
    ██║   ██╔══██║██╔══╝      ██╔══██║██╔══╝  ██║╚════██║   ██║       
    ██║   ██║  ██║███████╗    ██║  ██║███████╗██║███████║   ██║       
    ╚═╝   ╚═╝  ╚═╝╚══════╝    ╚═╝  ╚═╝╚══════╝╚═╝╚══════╝   ╚═╝       

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
NORTH = 1
EAST = 2
SOUTH = 3
WEST  = 4

# Global to describe how many empty commands before it assumed the player wants to quit
EMPTY_ENTERS_TO_BAIL_OUT = 3

# A global dictionary to hold player attributes
player = { "health" :  100, 
          "location": "start",    
          "inventory": "nothing"}

# Lab 12 item C requires a loose condition a Non player character may be useful
larry = { "health" :  100, 
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
map = [ [ "office", "lobby", "hall"],
        [ "hidden", "street", "safe"],
        [ "park", "start", "ally"]]

office = { "room_description" : "The room is XYZ, to the north is XYZ, to the east lies XYZ the south wall is blocked and to the east is y",
           "passable_NESW" : "NYYN",
           "npc" : larry,
           "object" : "nothing"}  
        
library = {
    "room_description": "The room is the library. The library holds books to the north, east, and west. Along these walls is a special book that leads to a hidden room. Find the book that hisses and slither and you will find the secret room.",
    "passable_NESW": "NYYY",
    "npc": larry,
    "object": "nothing"}

ballroom = {
    "room_description": "You have entered the ballroom. The ballroom is filled with 100 guests, all dancing. To the north is the staircase, to the east lies the library, to the west lies the billiards room. You must blend in with the party. Do not get caught as you make your way to the next room.",
    "passable_NESW": "NNCY",
    "npc": larry,
    "object": "nothing"}

hidden = {
    "room_description": "You've found the hidden room. Here lies the Catalina necklace in a locked wooden chest. To open the chest you must first unlock the secret ",
    "passable_NESW": "YNNN",
    "npc": larry,
    "object": "nothing"}

        
street = { "room_description" : "The room is XYZ, to the north is XYZ, to the east lies XYZ the south wall is blocked and to the east is y",
           "passable_NESW" : "YNYN",
           "npc" : larry,
           "object" : "nothing"}   
        
safe = {
    "room_description": "This is the safe vault room. To the north lies the vault. The east wall is blocked off, the west wall is blocked off. To exit return south. To open the vault type open.",
    "passable_NESW": "YNNN",
    "npc": larry,
    "object": "nothing"}

park = {   "room_description" : "The park is nice, a good place to take your dog, or to step in something left by somonelses dog. To the north is the back wall of the museum, east leads to the starting position and both south and west lead to the the edge of the game world",
           "passable_NESW" : "NYNN",
           "npc" : larry,
           "object" : "nothing"}  
        
start = {  "room_description" : "This is the staging area for your heist  to the north is a street, wide but with no visible traffic off to the east is an ally, west is the park and south is the edge of the game world",
           "passable_NESW" : "YYYN",
           "npc" : larry,
           "object" : "nothing"}  
        
ally = {    "room_description" : "An alley, bad things happen here",
           "passable_NESW" : "NNNY",
           "npc" : larry,
           "object" : "nothing"}  


rooms = {"office": office,
         "library": library,
         "ballroom": ballroom,
         "hidden": hidden,
         "street": street,
         "safe": safe,
         "park": park,
         "start": start,
         "ally": ally}

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
actions   = ["get", "take", "use", "open", "close", "examine", "look", "close", "show", "kick"]

directions = [ "left", "right", "forward", "ahead", "back", "up", "down", "north", "south", "east", "west" ]
items   = ["door", "gun", "safe", "map"]
people = ["self", "dog", "scooby", "larry"]

administrative = ["draw", "debug", "save", "help", "explain", "tutorial", "exit", "quit"]


# These next two functions are just for debug.  I wanted two global variables that would 
# be accessed and updated in a single function to create a debug log.
# This is a no-no in python.   So the first function static_var  is used by the decorators 
# to wrap around debugLog so I cankeep a long text string and count
def static_var(varname, value):
    def decorate(func):
        setattr(func, varname, value)
        return func
    return decorate
    
@static_var("string", "")      
@static_var("counter", 0)    
def debugLog(functionName, action, message):
    if functionName == "debugLog":
        print(debugLog.string)
    debugLog.counter +=1
    debugLog.string = ("%s\n%04d\t%s:\t%s:\t%s"%(debugLog.string, debugLog.counter, functionName, action, message))
#  End of debug log !!!
    
def titleMessage():
    print(title)
    return
 
def welcomeMessage():
    #print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
    #print(title)
    print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
    print("Welcome to The Heist")
    print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
    print("Type start to begin")
    print("Type help to learn how to play")
    print("Type exit to leave the game")
    print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
    return

def story():
    print("Larry is on a mission to find the Catalina necklace (worth 10 million).")
    print("He has studied the blueprints to the PyCharm Mansion.")
    print("A ball is being thrown at the PyCharm Mansion tonight.")
    print("Larry is entering the ball under the alias Jonathon Windsor")
    print("You must help Larry find the Catalina necklace, but be careful not to get caught.")
    print("As you go through the mansion you will find clues that lead you to a room with a hidden passage")
    print("Find that passage and you will find the necklace")
    return   
   
'''
def library():
    print("")
    print("You have just entered the library.")
    print("1 - North to book wall")
    print("2 - East to Office door")
    print("3 - West to Ballroom door")
    print("4 - South to Street door")
    print("Choose a direction")
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
  debugLog("parseInput", "input", caseCorrectedString)
  action = ""
  item = ""
  subject = ""
  for x in actions:
    if x in userString:
      action = x
  for x in travel:
    if x in userString:
      action = x
  for x in administrative:
    if x in userString:
      action = x

  for x in directions:
    if x in userString:
      item = x
  for x in items:
    if x in userString:
      item = x
    
  for x in people:
    if x in userString:
      subject = x

  debugLog("parseInput", "return", ("%s\t%s\t%s"%(action, item, subject)))
  return action, item, subject
    
def getUserInput(promptString = ""):
    userInput = ""
    count = 0
    while userInput == "" and count < EMPTY_ENTERS_TO_BAIL_OUT:
        userInput = input(promptString)
        count += 1
        
    return userInput.lower()
    

def isAdministrative(action="", item="", subject=""):
    if action == 'debug':
        debugLog("debugLog", item, subject)
        return True  
    if action == 'draw':
        debugLog("isAdministrative", "draw","map")
        drawMap()
        return True   
    if action == 'explain' or action == "help" or action == "tutorial":
        debugLog("isAdministrative", action,item)
        tutorial()
        return True   
    if (action in administrative):
        debugLog("isAdministrative", "COMMAND NOT IMPLIMENTED YET",action)
        return True
    debugLog("isAdministrative", "return","False")
    return False


def tutorial():
    print("\n\nTutorial\n\n")
    print("The Parser uderstands actions, items and objects\n The order of words does not matter\n")
    print("Valid commands could be \"Walk north\" or \"look at door\"\n")    
    print("\nActions the parser understands:")
    print(travel)  
    print(actions)   
    print("\nItems the parser understands:")
    print(items)  
    print("\nObjects the parser understands:")
    print(people) 
    print(directions)    
    print("\nAdministrative commands the parser understands:")
    print(administrative) 


def drawMap():
    canvas = "+---------------+---------------+---------------+\n"
    for row in map:
        canvas = canvas + "|"
        for room in row:
            canvas = canvas + "\t" + room + "\t|"
        canvas = canvas + "\n|\t\t|\t\t|\t\t|\n"
        canvas = canvas + "+---------------+---------------+---------------+\n"

    print(canvas)    
  
    
def isTravelCommand(action, item, subject):
    debugLog("isTravelCommand", "input", ("%s\t%s\t%s"%(action, item, subject)))
    if (action in travel) and ( item in directions ):
        debugLog("isTravelCommand", isTravelCommand,item)
        currentRoom = player["location"] 

        if item == "north" or item == "up":
            DIRECTION_INDEX = NORTH
            debugLog("isTravelCommand", "directions","NORTH")
        elif item == "east" or item == "right":
            DIRECTION_INDEX = EAST  
            debugLog("isTravelCommand", "directions","EAST")
        elif item == "south" or item == "down":
            DIRECTION_INDEX = SOUTH
            debugLog("isTravelCommand", "directions","SOUTH")
        elif item == "west" or directioitemns == "left":
            DIRECTION_INDEX = WEST  
            debugLog("isTravelCommand", "directions","WEST")
        
        passable = rooms[currentRoom]["passable_NESW"][DIRECTION_INDEX] 
        debugLog("isTravelCommand", "passable array",rooms[currentRoom]["passable_NESW"])
        debugLog("isTravelCommand", "passable selecgted",passable)
        if passable == 'Y' or passable == 'O':    # Yes passable or O for open door
            player["location"] = movePlayer(DIRECTION_INDEX)
            describeRoom()    
        elif passable == 'C':    # C is a closed door
            print("You try but the door is closed")
            debugLog("isTravelCommand", "report closed door","")
        else:
            print("You can not move in that direction")
            debugLog("isTravelCommand", "report could not travel","")
        
        return True
    debugLog("parseInput", "return","False")
    return False


def movePlayer(direction):
    currentRoom = player["location"] 
    currentRoomNumber = 0
    for row in map:
        for room in row:
            currentRoomNumber = currentRoomNumber + 1
            if currentRoom == room:
                break
                
    if direction == NORTH:
        currentRoomNumber = currentRoomNumber - 3
    elif direction == EAST:
        currentRoomNumber = currentRoomNumber + 1
    elif direction == SOUTH:    
        currentRoomNumber = currentRoomNumber + 3
    elif direction == WEST:
        currentRoomNumber = currentRoomNumber - 1
    else:
        raise "Error"

    count = 0
    for row in map:
        for room in row:
            count = count + 1
            if currentRoomNumber == count:
                return room
        
def describeRoom():
    currentRoom = player["location"] 
    debugLog("describeRoom", currentRoom,"")
    print("You are in the %s"%currentRoom)   
    print("%s"%rooms[currentRoom]["room_description"])

                
def door(action, item, subject):
    currentRoom = player["location"] 
    if "open" in action and 'door' in item:
        if 'north' in subject and rooms[currentRoom]["north_passable"] == "closed_door":
            rooms[currentRoom]["north_passable"] = "open"


    
def interactWithDoor(action, item, subject):
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
            pass
            continue
            
        # Are we interacting
        
        # Other
        
        # Administrative commands
        if isAdministrative(action, item, subject):      
          continue
              
    debugLog("gameLoop", "exit", ("gameOn:\t%s\tgameCycles:\t%s"%(gameOn,gameCycles)))   
    
    
    



gameLoop()
debugLog("debugLog", "", "")
