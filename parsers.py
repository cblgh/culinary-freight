class ParserError (Exception):
    pass
    

class Sentence(object):

    def __init__(self, subject, verb, object, number):
        #we take ('noun', 'princess') tuples and convert them
        # added number parameter, not sure how to treat it
        self.subject = subject[1]
        self.verb = verb[1]
        self.object = object[1]
        self.number = number[1]

class Parser(object):

    def __init__(self, word_list):
        self.word_list = word_list
        # should probably add self to all methods. self is instead of instance name, to allow the methods to work. they essentially reference something that they don't know, I guess.
    def peek(self):
        if self.word_list:
            word = self.word_list[0]
            return word[0]
        else:
            return None


    def match(self, expecting):
        if self.word_list:
            word = self.word_list.pop(0)

            if word[0] == expecting:
                return word
            else:
                return "Sorry there, not sure what you mean with %s" % word[1]
                

    def skip(self, word_type):
        while self.peek() == word_type:
            self.match(word_type)
            

    def parse_verb(self):
        self.skip('stop')

        if self.peek() == 'verb':
            return self.match('verb')
        else:
            raise ParserError("Expected a verb next.")
            

    def parse_object(self):
        self.skip('stop')
        next = self.peek()

        if next == 'noun':
            return self.match('noun')
        elif next == 'direction':
            return self.match('direction')
        else:
            raise ParserError("Expected a noun or direction next.")

    def parse_number(self):
        self.skip('stop')
        next = self.peek()

        if next == 'number':
            return self.match('number')

        else:
            return ("number", None)


    def parse_subject(self, subj):
        verb = self.parse_verb()
        obj = self.parse_object()
        number = self.parse_number()

        return Sentence(subj, verb, obj, number)


    def parse_sentence(self):
        self.skip('stop')

        start = self.peek()

        if start == 'noun':
            subj = self.match('noun')
            return self.parse_subject(subj)
        elif start == 'verb':
            # assume the subject is the player
            return self.parse_subject(('noun', 'player'))
        #elif start == 'number':
            #number = self.match('number')
            #return self.parse_subject(number)
            # what should I return or do here to get numbers working? I need to pass it to the Sentence class. Look at what the parse_subject function really does.
        else:
            raise ParserError("Must start with subject, object or verb not: %s" % start)
