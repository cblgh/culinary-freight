direction_list = ['north', 'south', 'east', 'west', 'n', 's', 'e', 'w']
verb_list = ['go', 'show', 'use', 'look', 'talk', 'speak', 'read', 'take']
noun_list = ['door', 'map', 'storyteller', 'character', 'carrot', 'key', 'shark', 'man', 'around', 'tomato', 'button', 'buttons', 'inventory']
stop_list = ['the', 'to', 'in', 'of', 'from', 'at', 'it', 'with', 'past', 'continue', 'to', 'up', 'is']

def scan(stuff):

    tuple_list = []
    words = stuff.split()

    for i in range(len(words)):
        if words[i].lower() in direction_list:
            word_type = ('direction', words[i].lower())
            tuple_list.append(word_type)
            
        elif words[i].lower() in verb_list:
            word_type = ('verb', words[i].lower())
            tuple_list.append(word_type)                    
            
        elif words[i].lower() in noun_list:
            word_type = ('noun', words[i].lower())
            tuple_list.append(word_type)
            
        elif words[i].lower() in stop_list:
            word_type = ('stop', words[i].lower())
            tuple_list.append(word_type)

        elif words[i].isdigit():
            word_type = ('number', int(words[i]))
            tuple_list.append(word_type)

        else:
            word_type = ('error', words[i])
            tuple_list.append(word_type)

            
    return tuple_list
