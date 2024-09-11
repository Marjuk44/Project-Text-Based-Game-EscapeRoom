# define rooms
portugal = {#gameRoom
    "name": "portugal",
    "type": "room",}

uk = {#bedroom1
    "name": "uk",
    "type": "room",}

spain = {#bedroom 2
    "name": "spain",
    "type": "room",}

hall_of_fame = {#living room
    "name": "hall_of_fame",
    "type": "room",}

outside = {
  "name": "outside"}
#define items in the room
#room portugal
aroundpt = { #couch
    "name": "aroundpt",
    "type": "furniture",}

lisbon = {#piano
    "name": "lisbon",
    "type": "furniture",}

#room UK
manchester = { #queenbed
    "name": "manchester",
    "type": "furniture",}

#room spain
individual_glory = {#double bed
    "name": "individual_glory",
    "type": "furniture",}

team_glory = {#dresser
    "name": "team_glory",
    "type": "furniture",}

#room hall of fame
rest_relax = {#dining table
    "name": "rest_relax",
    "type": "furniture",}
#define doors
door_a = {
    "name": "door a",
    "type": "door",}

door_b = {
    "name": "door b",
    "type": "door",}

door_c = {
    "name": "door c",
    "type": "door",}

door_d = {
    "name": "door d",
    "type": "door",}
#define keys
key_a = {
    "name": "key for door a",
    "type": "key",
    "target": door_a,}

key_b = {
    "name": "key for door b",
    "type": "key",
    "target": door_b,}

key_c = {
    "name": "key for door c",
    "type": "key",
    "target": door_c,}

key_d = {
    "name": "key for door d",
    "type": "key",
    "target": door_d,}

all_rooms = [portugal, uk, spain, hall_of_fame, outside]

all_doors = [door_a, door_b, door_c, door_d]

# define which items/rooms are related
#this dictionare sets the items that the player can select!

object_relations = {
    #room portugal
    "portugal": [aroundpt, lisbon, door_a],
    "lisbon": [key_a],
    "aroundpt":[],#lisbon, door_a],
    
    #room UK
    "uk": [manchester, door_b, door_c],
    "manchester":[key_b],

    #room spain
    "spain":[individual_glory, team_glory, door_b],
    "individual_glory":[key_c],
    "team_glory":[key_d],

    #room hall_of_fame
    "hall_of_fame": [rest_relax, door_c, door_d],
    "rest_relax": [],#hall_of_fame, door_c, door_d],

    #possible acess take can be done in the doors
    "door a":[portugal, uk],
    "door b":[uk,spain],
    "door c":[uk, hall_of_fame],
    "door d":[hall_of_fame,outside],}

# define game state. Do not directly change this dict. 
# Instead, when a new game starts, make a copy of this
# dict and use the copy to store gameplay state. This 
# way you can replay the game multiple times.

INIT_GAME_STATE = {
    "current_room": portugal,
    "keys_collected": [],
    "target_room": outside,}
#code to define the rooms

def linebreak(): #add lines
    """
    Print a line break
    """
    print("\n\n")

def start_game(): #function that sets the initial parameters of the game!
    """
    Start the game
    """
    print("You born somewhere in Portugal and have the dream to become someone important. Start your journey in this adventure called life!") #initial message!
    play_room(game_state["current_room"]) #calls function play_room

def play_room(room):
    """
    Play a room. First check if the room being played is the target room.
    If it is, the game will end with success. Otherwise, let player either 
    explore (list all items in this room) or examine an item found here.
    """
    game_state["current_room"] = room
    if(game_state["current_room"] == game_state["target_room"]):
        print("To win this game, answer the following question?")
        answer=input("Who are you?")
        if answer == "Cristiano Ronaldo":
            print("Congratulations! SIIIIIIIIIIIIIIIIIIIIIIIUUUUUUUUUUUUU!!!!!!!!!!")
        else:
            print("Wrong answer! Play again.")
            start_game()
    else:
        print(f"\nYou are now in " + room["name"])
        intended_action = "examine"
        #intended_action = input(f"\nWhat would you like to do? Type 'explore' or 'examine'?").strip()
       #print(f"\nWhat would you like to do?")
        if intended_action == "explore":
            explore_room(room) 
            play_room(room)
        elif intended_action == "examine":
            explore_room(room)
            examine_item(input(f"\nWhat would you like to examine?").strip())  
        else:
            print("Not sure what you mean. Type 'explore' or 'examine'.")
            play_room(room)
        linebreak()

def explore_room(room):
    """
    Explore the country. List all items belonging to this country.
    """
    items = [i["name"] for i in object_relations[room["name"]]]
    print(f"\nIn " + room["name"] + " you found: " + ", ".join(items))

def get_next_room_of_door(door, current_room): #function to change rooms
    """
    From object_relations, find the two rooms connected to the given door.
    Return the room that is not the current_room.
    """
    connected_rooms = object_relations[door["name"]]
    for room in connected_rooms:
        if current_room != room:
            return room

def examine_item(item_name):
    """
    Examine an item which can be a door or furniture.
    First make sure the intended item belongs to the current room.
    Then check if the item is a door. Tell player if key hasn't been 
    collected yet. Otherwise ask player if they want to go to the next
    room. If the item is not a door, then check if it contains keys.
    Collect the key if found and update the game state. At the end,
    play either the current or the next room depending on the game state
    to keep playing.
    """
    
    current_room = game_state["current_room"]
    next_room = None
    output = None
    
    for item in object_relations[current_room["name"]]: #iterate the object_relations list
        if(item["name"] == item_name): #if the item in the list equals the parameter passsed in the function call
            output = "You examine " + item_name + ". " #print the message
            if(item["type"] == "door"):
                have_key = False
                for key in game_state["keys_collected"]:
                    if(key["target"] == item):
                        have_key = True
                if(have_key):
                    output += "You got access to the next country with the key you have."
                    next_room = get_next_room_of_door(item, current_room)
                else:
                    output += "You have no access to this country. Get a key to your future!"
            else: #if the item is not present in the list
                if(item["name"] in object_relations and len(object_relations[item["name"]])>0):
                    item_found = object_relations[item["name"]].pop()
                    game_state["keys_collected"].append(item_found)
                    output += "You found the " + item_found["name"] + "."
                else:
                    output += "There isn't anything interesting about it."
            print(output)
            break

    if(output is None):
        print("The item you requested is not found in the current country.")
    
    if(next_room and input("Do you want to move to the country? 'yes' or 'no'").strip() == 'yes'):
        play_room(next_room)
    else:
        play_room(current_room)

game_state = INIT_GAME_STATE.copy()

start_game()