#!/usr/bin/python
# CST205 Lab 11
# November 22, 2017
#
# Team 5, Hopper
#  Jose Garcia Ledesma
#  Grace Alvarez
#  Christian Guerrero
#  Gabriel Loring


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
NORTH = 1
EAST = 2
SOUTH = 3
WEST  = 4

EMPTY_ENTERS_TO_BAIL_OUT = 3

player ={ "health" :  100, 
          "location": "start",
          "inventory": "nothing"}

larry ={ "health" :  100, 
                    "location": "start",
                    "inventory": "nothing"}

map = [ [ "office", "lobby", "hall"],
        [ "hidden", "street", "safe"],
        [ "park", "start", "ally"]]

office = { "room_description" : "The room is XYZ, to the north is XYZ, to the east lies XYZ the south wall is blocked and to the east is y",
           "passable_NESW" : "NYYN",
           "npc" : larry,
           "object" : "nothing"}  
        
lobby = { "room_description" : "The room is XYZ, to the north is XYZ, to the east lies XYZ the south wall is blocked and to the east is y",
           "passable_NESW" : "NYYY",
           "npc" : larry,
           "object" : "nothing"}      


hall = { "room_description" : "The room is XYZ, to the north is XYZ, to the east lies XYZ the south wall is blocked and to the east is y",
           "passable_NESW" : "NNCY",
           "npc" : larry,
           "object" : "nothing"}   
        
hidden = { "room_description" : "The room is XYZ, to the north is XYZ, to the east lies XYZ the south wall is blocked and to the east is y",
           "passable_NESW" : "YNNN",
           "npc" : larry,
           "object" : "nothing"}  
        
street = { "room_description" : "The room is XYZ, to the north is XYZ, to the east lies XYZ the south wall is blocked and to the east is y",
           "passable_NESW" : "YNYN",
           "npc" : larry,
           "object" : "nothing"}   
        
safe = { "room_description" : "The room is XYZ, to the north is XYZ, to the east lies XYZ the south wall is blocked and to the east is y",
           "passable_NESW" : "YNNN",
           "npc" : larry,
           "object" : "nothing"}   

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


rooms ={"office": office,
        "lobby": lobby,
        "hall": hall,
        "hidden": hidden,
        "street": street,
        "safe": safe,
        "park": park,
        "start": start,
        "ally": ally}
    
travel    = [ "go", "walk", "run", "skip", "get", "move", "travel", "head" ]
actions   = ["get", "take", "use", "open", "close", "examine", "look", "close", "show", "kick"]
administrative = ["draw", "debug", "save", "help", "explain", "tutorial", "exit", "quit"]

directions = [ "left", "right", "forward", "ahead", "back", "up", "down", "north", "south", "east", "west" ]
items   = ["door", "gun", "safe", "map"]
people = ["self", "dog", "scooby"]


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

    
def welcomeMessage():
    print(title)


def parseInput(userString):
    caseCorrectedString = userString.lower()
    debugLog("parseInput", "input", caseCorrectedString)
    action = ""
    item = ""
    person = ""
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
            person = x

    debugLog("parseInput", "return", ("%s\t%s\t%s"%(action, item, person)))
    return action, item, person
    
def getUserInput(promptString = ""):
    userInput = ""
    count = 0
    while userInput == "" and count < EMPTY_ENTERS_TO_BAIL_OUT:
        userInput = input(promptString)
        count += 1
        
    return userInput.lower()
    

def isAdministrative(action="", item="", person=""):
    if action == 'debug':
        debugLog("debugLog", item, person)
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
  
    
def isTravelCommand(action, item, person):
    debugLog("isTravelCommand", "input", ("%s\t%s\t%s"%(action, item, person)))
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

                
def door(action, item, person):
    currentRoom = player["location"] 
    if "open" in action and 'door' in item:
        if 'north' in person and rooms[currentRoom]["north_passable"] == "closed_door":
            rooms[currentRoom]["north_passable"] = "open"


    
def interactWithDoor(action, item, person):
    pass 
    



def gameLoop():
    welcomeMessage()
    debugLog("gameLoop", "start", "")
    gameOn = True
    gameCycles = 0
    describeRoom() # Let the player know where they are starting from
    while gameOn:
        gameCycles += 1
        userString = getUserInput()
        (action, item, person) = parseInput(userString)
        
        # See if the user want to quit
        if action == 'quit' or userString == "" or userString == "exit":
            gameOn = False  
            continue
            
        #Are we moving
        if isTravelCommand(action, item, person):
            pass
            continue
            
        # Are we interacting
        
        # Other
        
        # Administrative commands
        if isAdministrative(action, item, person):      
          continue
              
    debugLog("gameLoop", "exit", ("gameOn:\t%s\tgameCycles:\t%s"%(gameOn,gameCycles)))   
    
    
    



gameLoop()
debugLog("debugLog", "", "")