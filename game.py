import parsers, lexicon, random, os

class Entity(object):

    def __init__(self, name):
        self.name = name

    def rand_elem(self, list_name):
        return random.randint(0, len(list_name)-1)

    
class Player(Entity):

    def __init__(self, name):
        super(Player, self).__init__(name)
        self.inventory = []
        self.unlocked_rooms = []
        
    def print_inventory(self):
        print "Your inventory:", self.inventory

    def remove_item(self, item):
        if (item in self.inventory):
            self.inventory.remove(item)
            
    
    def unlock_room(self, room_nr, text):
        self.unlocked_rooms.append(room_nr)
        print text


class Character(Entity):

    def __init__(self, name):
        super(Character, self).__init__(name)
        self.stories = ["'Let me tell you a story, boyo. One of the greatest finds in my life concerned\nthe discovery of an /island/. But it wasn't any ordinary island, no no, this\nisland was special. It was a secret island known to no one but the Galaxy\nMasters!'\n%s continues with his story but you lose interest and stop listening." % self.name, "'Boyo! You're one of the newest arrivals yeah? If you're lucky you can get to\nyour ship before it ends up with the others down in the hangar.", "I was a great man once, boyo. Everyone spoke about me; I was famous! I ended up being a myth, still spoken about in some circles. Nobody would've thought that\nwhen I first showed up, no siree!"]

    def tell_story(self):
        if len(self.stories) > 0:
            print "\n", self.stories.pop(self.rand_elem(self.stories)), "\n"
        else:
            print "I'm afraid that's all these poor bones have to tell."
            

class Enemy(Entity): # Implement enemies as puzzles; take vegetables and give it to the appropriate 
                     # enemy. 
                     # Descriptions around the rooms/storyteller to leak the different enemies's weaknesses 
                     # to the vegetable that will kill them/make them drowsy?

    def __init__(self, name):
        super(Enemy, self).__init__(name)
        self.moved = False
        self.reactions = ["'Hm, what was that?'", "'Anybody there?'", "'Check yoself before you wreck yoself!'"]

    def move(self):
        if self.moved:
            print "You've already done that."
        else:
            self.moved = True
            print "%s says " %self.name, self.reactions[self.rand_elem(self.reactions)]
            

class Items(object):

    def __init__(self):
        room1_items = ['key']
        room2_items = ['carrot']
        room3_items = []
        room4_items = []
        room5_items = []
        room6_items = []
        room7_items = ['tomato']
        room8_items = []
        room9_items = []
        room10_items = []
        self.item_dict = {1: room1_items, 2: room2_items, 3: room3_items, 4: room4_items, 5: room5_items,
        6: room6_items, 7: room7_items, 8: room8_items, 9: room9_items, 0: room10_items}

    def check_item(self, room_nr, item):
        return item in self.item_dict[room_nr]

    def print_items(self, room_nr):
        print self.item_dict[room_nr]
        
    def remove_item(self, room_nr, item):
        if item in self.item_dict[room_nr]:           
            self.item_dict[room_nr].remove(item)

    
class Room(object):

    def __init__(self, room_nr, description):
        self.room_nr = room_nr
        self.description = description
        
    def death(self):
        print "Game over!"
        exit(0)

    def look(self, description):
        print description
        
    def invalid_input(self):
        print "Not /quite/ valid enough, sorry."

    def repeat_action(self):
        print "You've already done that."

    def add_item(self, item):
            player.inventory.append(item)
            i.remove_item(self.room_nr, item)
            print "%s was added to the inventory!" % item.capitalize()

    """The method print_map takes the room the player's currently in as an argument. It then searches   
    for the number corresponding to that room in the map and replaces it with an x, to signify the 
    current position on the map. """  
    def print_map(self, position):
        game_map = """
                    +--+      +--+
                    |00|      |99|
                    +--+      +--+
                     |         |
                    +--+ +--+ +--+ +--+
                    |88| |77|-|66|-|55|
                    +--+ +--+ +--+ +--+
                     |    |
               +--+ +--+ +--+
               |44|-|33|-|22|
               +--+ +--+ +--+     
                          |
                         +--+
                         |11|
                         +--+ """

        self.position = position                    

        for num in range(10):
            if self.position == num:
                game_map = game_map.replace(str(num), "x")
            else:
                game_map = game_map.replace(str(num), " ")
        print game_map

    def room_text(self):
        os.system('cls')
        self.print_map(self.room_nr)
        print self.description

    def look(self, environment_description):
        print environment_description
        
    """ This method receives the input from the users, checks it against the lexicon to see if it
    exists. If the sentence exists, it then goes on to the parser for parsing."""    
    def user_input(self, room_nr):
        while True:
            try:
                action = raw_input("> ")
                
                if action == "quit" or action == "exit":
                    self.quit()
                    
                p = parsers.Parser(lexicon.scan(action))
                s = p.parse_sentence()

                if s.verb == "show" and s.object == "inventory":
                    player.print_inventory()
                elif s.verb == "read" and s.object == "map" or s.verb == "show"  and s.object == "map":
                    self.print_map(self.room_nr)
                elif s.verb == "take" and i.check_item(self.room_nr, s.object) == True:
                    self.add_item(s.object)
                else:
                    break
                    
            except parsers.ParserError:
                self.invalid_input()
        return s
        
    def quit(self):
        print "Exiting the game..."
        exit(0)

class Start(Room):

    def __init__(self):
        super(Start, self).__init__(None, None)

    def room(self):
        os.system('cls')
        print "It's been quite a hectic of a day, hasn't it? First, the crate of radishes some-how came unloose and almost ruptured a ventilation drum. Then the fuel guage\nstarted acting up once again, almost causing a heart attack until you realized\nthat it is, in fact, a broken POS not to be trusted. And now this.\
        \n\nHere you are struck by Vegetus Inc. thugs and stuck in a poorly ventilated room red like therenegade radishes from earlier today. And to think that all you\nwanted to do today was ship your precious vegetables to the outer colonies\nwhile gazing out peacefully at the immense void in front of you.\
        \n\nYou know where you are, on a Vegetus Inc. mobship, and why you're here, because they're a corrupt bunch who want nothing more than to maintain their monopoly onthe vegetable trade. You also know that all you want is to get your ship back,\nto hear your trusty POS fuel guage beep erroneously yet again while cruising\nwith but the stars as companions.\n\nType anything to continue."
        raw_input("> ")
        return Room_1()
        

class Room_1(Room): 
                    
    def __init__(self):
        super(Room_1, self).__init__(1, "You're in a derelict compartment with poorly maintenanced metal panels\ninterspersing the fusty smell.\nThe only exit in sight is the metal door to the north.") 

    def room(self):
        self.room_text()
        
        while True:
            s = self.user_input(self.room_nr)
            if s.verb == "go" and s.object == "north" and self.room_nr in player.unlocked_rooms or s.verb == "go" and s.object == "n" and self.room_nr in player.unlocked_rooms:
                return Room_2()
            elif s.verb == "look" and s.object == "around" and "key" not in player.inventory:
                self.look("You look at the metal door and notice it's locked. You also notice a moldy green key lying beneath a shabby table in the corner of the fusty room.")
            elif s.verb == "look" and s.object == "around" and self.room_nr not in player.unlocked_rooms:
                self.look("All you see is the key in your hand and the beckoning door in front of you.")            
            elif "look" and s.object == "around" and self.room_nr in player.unlocked_rooms:
                self.look("You stare at the open door; at the path to your ship.")
            elif s.verb == "use" and s.object == "key" and self.room_nr in player.unlocked_rooms:
                self.repeat_action()
            elif s.verb == "use" and s.object == "key":
                player.unlock_room(self.room_nr, "You use the moldy key to unlock the metal door. You can hear the lock mechanism do its magic to unlock the door.")                          
            else:
                self.invalid_input()


class Room_2(Room):

    def __init__(self):
        super(Room_2, self).__init__(2, "You enter a humid and dimly lit space filled with crates upon crates, and a man.The man stands in the farside of the room. He seems a bit Off.\nThere are exits to the north, south and west.")
        
    def room(self):
        self.room_text()
        
        while True:
            s = self.user_input(self.room_nr)
            if s.verb == "go" and s.object == "west" or s.object ==  "w":
                return Room_3()
            elif s.verb == "look" and s.object == "around" and "carrot" not in player.inventory:
                self.look("You see a man in the corner, staring at you as if he wanted to talk but was too afraid to be the one to approach.\nYou also notice a carrot, lying beside the weird man.\nYou take note of exits to the north, south and west. Just in case the man is\n/too/ Off.")
            elif s.verb == "look" and s.object == "around" and "carrot" in player.inventory:
                self.look("The man's still there, looking anxiously as ever in your direction.")
            elif s.verb == "talk" and s.object == "man" or s.object == "shark":
                storyteller.tell_story()  
            elif s.verb == "go" and s.object == "north" or s.object == "n":
                return Room_7()
            elif s.verb == "go" and s.object == "south" or s.object == "s":
                return Room_1()
            else:
                self.invalid_input()


class Room_3(Room):

    def __init__(self):
        super(Room_3, self).__init__(3, "As you join the room's musty odors you notice it's a kind of make-\nshift hydroponic farm. There are exits to the north, east and west.")

    def room(self):
        self.room_text()

        while True:
            s = self.user_input(self.room_nr)
            if s.verb == "go" and s.object == "west" or s.object == "w":
                return Room_4()
            elif s.verb == "look" and s.object == "around" and not hydroponic_enemy.moved:
                self.look("You see an enemy, tending to the plants in the northern area of the room.\nYou also notice a light switch besides you. Sadly it's of the \nslightly-out-of-reach variety.")
            elif s.verb == "look" and s.object == "around" and hydroponic_enemy.moved:
                print "You see", hydroponic_enemy.name, " standing in a corner, examining the\nmysteriously darkened light. He doesn't seem very bright."
            elif s.verb == "use" and s.object == "carrot" and s.object in player.inventory and not hydroponic_enemy.moved:
                print "You use the carrot to reach the previously slightly-of-reach light switch!"
                hydroponic_enemy.move()
                print "He moves away from the hydroponic farm to examine the light in the southern\npart of the musty room."
            elif s.verb == "use" and s.object == "carrot" and hydroponic_enemy.moved:
                hydroponic_enemy.move()
            elif s.verb == "go" and s.object == "north" or s.object == "n" and hydroponic_enemy.moved:
                return Room_8()
            elif s.verb == "go" and s.object == "north" or s.object == "n" and not hydroponic_enemy.moved:
                print hydroponic_enemy.name, "is in the way."
            elif s.verb == "go" and s.object == "east" or s.object == "e":
                return Room_2()
            else:
                self.invalid_input()


class Room_4(Room):

    def __init__(self):
        super(Room_4, self).__init__(4, "You're greeted by your good old sparkly friends as you enter the room. It seems to be dedicated to star-gazing; the chairs are opposite of the monolithic\nwindow much like cinemas of the past were built.\nThe only exit is whence you came from; the east.")

    def room(self):
        self.room_text()

        while True:
            s = self.user_input(self.room_nr)
            if s.verb == "go" and s.object == "east" or s.object == "e":
                return Room_3()
            elif s.verb == "look" and s.object == "around":
                self.look("You take a seat in one of the chairs and gaze out into the starry void. When you get up out of the chair you're strangely unaware of how much time has passed since you first sat down.")
            else:
                self.invalid_input()


class Room_5(Room):

    def __init__(self):
        super(Room_5, self).__init__(5, "You enter glass-paned wall. As you peer down through the glass you see a hangar full\nof what seems to be plundered ships. Yours, luckily, seems to still be missing.\nThe only door available is the one you came through from the west.")
    
    def room(self):
        self.room_text()      

        while True:
            s = self.user_input(self.room_nr)
            if s.verb == "go" and s.object == "west" or s.object == "w":
                return Room_6()
            elif s.verb == "look" and s.object == "around":
                self.look("You gaze down upon the plundered, derelict ships and shudder at the thought of what fate lies waiting for your dearest if you don't get back to it in time.")
            else:
               self.invalid_input()
       

class Room_6(Room):

    def __init__(self):
        super(Room_6, self).__init__(6, "When you enter the room a wift of grease-filled air enters your\nnostrils; you seem to have entered the kitchen.\nThe exits are to the north, east and west.")

    def room(self):
        self.room_text()

        while True:
            s = self.user_input(self.room_nr)
            if s.verb == "go" and s.object == "west" or s.object == "w":
                return Room_7()
            elif s.verb == "look" and s.object == "around" and not kitchen_enemy.moved : 
                self.look("You look around the greasy kitchen and spot a man cooking food, presumably a \nVegetus thug.\nA glance to the back of the room also reveals an electrical socket.")
            elif s.verb == "look" and s.object == "around":
                self.look("You look around the kitchen trying to discern shapes. You spot the cook cowering on the floor. He seems to be afraid of the dark. Quaint.")
            elif s.verb == "use" and s.object == "carrot" and s.object in player.inventory and not kitchen_enemy.moved:
                print "You hear a 'Fzzpt' as you stick the carrot in the socket; the room goes dark and you hear a loud thud."
                kitchen_enemy.move()
            elif s.verb == "use" and s.object == "carrot" and kitchen_enemy.moved:
                kitchen_enemy.move()
            elif s.verb == "go" and s.object == "north" or s.object == "n" and not kitchen_enemy.moved:
                print "You try to sneak past the cook, but your legs refuse to move while he's standing there."
            elif s.verb == "go" and s.object == "east" or s.object == "e" and not kitchen_enemy.moved:
                print "You try to sneak past the cook to the east, but your legs fail you."
            elif s.verb == "go" and s.object == "north" or s.object == "n":
                return Room_9()
            elif s.verb == "go" and s.object == "east" or s.object == "e":
                return Room_5()
            else:
                self.invalid_input()  


class Room_7(Room):

    def __init__(self):
        super(Room_7, self).__init__(7, "You enter a corridor absolutely lined with beautiful plants that smell\ngood, which is in stark contrast to everything else on the ship.\nYou see two doors, one to the east and one south.")
        
    def room(self):
        self.room_text()

        while True:
            s = self.user_input(self.room_nr)
            if s.verb == "go" and s.object == "east" or s.object == "e":
                return Room_6()
            elif s.verb == "look" and s.object == "around" and "tomato" not in player.inventory:
                self.look("You see a man tending gingerly to the plants.\nYou assume he's a Vegetus mobster, though he seems to be quite unlike\nthe others you've encountered. In the other end of the room you see a\nvast tomato plant, drooping with ripe tomatoes yearning to be plucked.")
            elif s.verb == "look" and s.object == "around" and "tomato" in player.inventory:
                self.look("The man's still tending to the tomatoes, seemingly oblivious of your existence.") 
            elif s.verb == "take" and s.object == "tomato" and s.object in player.inventory:
                self.repeat_action()
            elif s.verb == "go" and s.object == "south" or s.object == "s":
                return Room_2()
            else:   
                self.invalid_input()


class Room_8(Room):

    def __init__(self):
        super(Room_8, self).__init__(8, "You enter a large hall, the walls are decked with shelves and what seems to be\nclimbing gear of some sort. On the shelves you see an extraordinary amount of\ndifferent kind of Coffee tins.\nThere appears to be exits to the north and south. The exit to the north has a handmade sign that reads 'Airlock Bay'.")

    def room(self):
        self.room_text()

        while True:
            s = self.user_input(self.room_nr)
            if s.verb == "go" and s.object == "north" or s.object == "n" and self.room_nr in player.unlocked_rooms:
                return Room_10()
            if s.verb == "go" and s.object == "north":
                print "The doors are locked."
            elif s.verb == "look" and s.object == "around":
                self.look("While looking around the room, you spot a pair of broken shears alongside a stack of sheared feathers. Quaint, you think.")
            elif s.verb == "go" and s.object == "south" or s.object == "s":
                return Room_3()
            else:
                self.invalid_input()


class Room_9(Room):

    def __init__(self):
        super(Room_9, self).__init__(9, "You enter a room seething with various control panels.\nThe only exit is to the south.")
        self.button_pressed = False

    def room(self):
        self.room_text()

        while True:
            s = self.user_input(self.room_nr)
            if s.verb == "go" and s.object == "s" and self.button_pressed or s.verb == "go" and s.object == "south" and self.button_pressed:
                print "The door is still locked."
            elif s.verb == "go" and s.object == "south" or s.object == "s":
                return Room_6()
            elif s.verb == "look" and s.object == "around" and self.button_pressed:
                self.look("You see a tomato on a button.\nThe door you came from appears to have been locked when you placed the tomato.")
            elif s.verb == "look" and s.object == "around":
                self.look("You franctically look around the room for anything pertaining to your ship.\nYou see a panel named 'Evacuation Precautions' with a set of buttons and screens beneath the title.\nOne of the buttons read 'Sunder Doors' and the other 'Airlock Bay' . Bingo.")
            elif s.verb == "use" and s.object == "buttons" and not self.button_pressed or s.verb == "use" and s.object == "button" and not self.button_pressed:
                print "You try to press one of the buttons needed; nothing happens."
            elif s.verb == "use" and s.object == "buttons" and 8 in player.unlocked_rooms or s.verb == "use" and s.object == "button" and 8 in player.unlocked_rooms:
                self.repeat_action()
            elif s.verb == "use" and s.object == "buttons" or s.object == "button":
                player.unlock_room(8, "With the tomato on one button you press down on the other;\nthe doors guarding your ship are unlocked.")
            elif s.verb == "use" and s.object == "tomato" and self.button_pressed:
                self.repeat_action()
            elif s.verb == "use" and s.object == "tomato":
                print "You place the tomato upon one of the buttons.\nThe door behind you makes a noise and the other button shines up."
                self.button_pressed = True
                player.remove_item("tomato")
            elif s.verb == "take" and s.object == "tomato" and s.object not in player.inventory:
                print "You retrieve the tomato from its temporary throne."
                self.button_pressed = False
                self.add_item("tomato")
            else:
                self.invalid_input()


class Room_10(Room):

    def __init__(self):
        super(Room_10, self).__init__(0, "Your ship. Finally, you've been reunited.\n\nDo you want to play again? (Y/N)") 
        # self.room_nr is 0 because of how the 
        # print_map method is implemented
    def room(self):
        self.room_text()  

        while True:
            choice = raw_input("> ").lower()

            if choice == "y":
                del player.inventory[:]
                del player.unlocked_rooms[:]
                return Start()
            elif choice == "n":
                self.quit()
            else:
                self.invalid_input()      
        
       
class Game(object):

    def __init__(self, start):
        self.start = start 
        
    def play(self):        
        next = self.start
        
        while True:
            next = next.room()
                              
    def check_item(self, room_nr, item):
        return item in self.item_dict[room_nr]



player = Player("Nameless Hero")
storyteller = Character("Shark")
kitchen_enemy = Enemy("Vegetable Fiend, Frank")
corridor_enemy = Enemy("Caretaker of Plants, Chester")
hydroponic_enemy = Enemy("Hydroponic Man, Harald")
i = Items()    
g = Game(Start())
g.play()


"""
make a Start room *
Start gives the essential parts of the story, who you are, where you are and why *
identify the enemies and their weaknesses
    make them human, as relatable as a text-only character can be. allow them to procrastinate, stress over everyday ordeals, do inane stuff, waste time, complain about 'the weather', be delighted by the smallest of things
    I don't want to kill them, I think. The player is but a Vegetable Farmer, not a Ph.D. in Theoretical Physics. Have player distract them, essential 'move them'.
    Really though, just make them simple.  
    don't  have too many of them; have them in places that /makes sense/ <-- key phrase yo, in places that doesn't disturb the exploration of the player

    if Enemy.moved:
        print text that says so 
        allow player to pick up item in room
    elif not Enemy.moved:
        print text that says he's in the way.
    enemy rooms:
    6. the kitchen
    7. corridor with plants
    9. control room
    
give storyteller stories to tell, relating to the enemies and how he came onboard the ship *
give enemies inventory items to drop
make sure that enemies drop the items needed for progression
hinder progression in rooms until requirements (items in inventory or used, enemies dead) are fulfilled
give each room their own backdrop * 
give some rooms enemies *
make a look method to give clues to the player *
make the look method depend on what's been changed, e.g. Enemy.moved and item removed from room


STORY
You're the diary of the adventurer, thus the texty format.
"""
