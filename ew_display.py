from ew_config import *
p = ew_platform()        

class guess_display:
    """
    Prints the guess with feedback for the user using letter_display for each letter.
    """

    def __init__(self, guess, answer):
        """
        Input: guess and answer are both valid words. Any data quality issues (case, length, 
            alphas only) happens outside of the printer object.
        Output: successfully initializes the object
        TO DO: 
            not sure how the actual game behaves when the same letter appears in a word 
                more than once, need to check.
            put in place some assertions / checks to back up the input assumptions
            write nicer getter and setters
        """
        self.guess = guess
        self.answer = answer  

    def get_string_dict(self, input_string=False):
        """
        Returns a dict with the key of each letter, and values of a list of positions for that letter
        By default returns a dict for the answer, but can take any string as a parameter 
        """
        ## initialize the dictionary
        d = dict()
        ## check for the input string
        if input_string==False:
            input_string = self.answer
        else:
            assert type(input_string) == str
        ## loop through to pick up locations
        for (location, letter) in enumerate(input_string):
            if letter in d:
                d[letter] += [location]
            else:
                d[letter] = [location]
        ## and we're done!
        return d
        

    def get_letter_statuses(self):
        """
        Input: successful object initialization, with guess and answer strings
        Output: a list of letter_displays with appropriate statuses
        """
        if self.guess == self.answer:
            letter_displays = [letter_display(letter, 'OK') for letter in self.guess]
        else:
            ## get guess and answer dictionaries
            guess_dict = self.get_string_dict(self.guess)
            answer_dict = self.get_string_dict()
            letter_tuple_list = []
            ## loop through guess letters to get locations by status
            for (letter, locations) in guess_dict.items():
                ok = []
                move = []
                no = []
                if letter in answer_dict:
                    answer_locations = answer_dict[letter]
                    ## file the ones in the right location
                    ok = list(set(locations).intersection(set(answer_locations)))
                    ## what are the locations we guessed, excluding the ones that were correct?
                    all_moves = list(set(locations).difference(set(answer_locations)))
                    ## how many of those do we actually want to highlight to move?
                    num_to_move = min( len(answer_locations) - len(ok), len(all_moves) )
                    ## put them where they belong for move vs no statuses
                    move = all_moves[:num_to_move]
                    no = all_moves[num_to_move:]
                else:
                    no = locations
                letter_tuple_list += [ (location, letter_display(letter,'OK')) for location in ok ]
                letter_tuple_list += [ (location, letter_display(letter,'MOVE')) for location in move ]
                letter_tuple_list += [ (location, letter_display(letter,'NO')) for location in no ]
            ## convert the tuple list back into a list
            letter_tuple_list.sort()
            letter_displays = [ ld for (i, ld) in letter_tuple_list ]
        return letter_displays

    def __str__(self):
        """ 
        Input: successful object initialization
        Output: a string to use for printing
        """
        return ' '.join([str(l) for l in self.get_letter_statuses()])

    def display(self):
        """
        Input: successful object initialization, with guess and answer strings
        Output: print the display_letters
        """
        for l in self.get_letter_statuses():
            l.display()
        print()            

    def get_correct_letters_plus_blanks(self):
        """ 
        given a guess and the answer, returns the characters in the right 
        place and _ in the other positions
        """
        return "".join([ g*(g == a) + '_'*(g != a) for (g, a) in zip(self.guess, self.answer) ])

class keyboard_display:
    """
    Prints the QWERTY keyboard with letters color coded based on their best guess status
    within the game.
    """

    def __init__(self, answer, guesses = []):
        """
        Input: at least an answer, in case there aren't any guesses yet, but ideally an
            answer and a list of guesses that are all valid words. Any data quality issues (case, length, 
            alphas only) happens outside of the printer object.
        Output: successfully initializes the object
        TO DO: 
            write nicer getter and setters
        """
        assert type(answer) == str

        ## standards for the whole class, written here so they can be easily overwritten in the subclass
        self.keys = 'QWERTYUIOP ASDFGHJKL ZXCVBNM '
        self.vertical_border = '\u2551'
        if p.IS_IPHONE == False:
            self.top_border = '\u2554' + ('\u2550'*40) + '\u2557'
            self.bottom_border = '\u255A' + ('\u2550'*40) + '\u255D'
            self.line_padding = {1: ('', ''), 2: ('  ', '  '), 3:('      ', '      ')}
        elif p.IS_IPHONE == True:
            self.top_border = '\u2554' + ('\u2550'*21) + '\u2557'
            self.bottom_border = '\u255A' + ('\u2550'*21) + '\u255D'
            self.line_padding = {1: (' ', ''), 2: ('  ', ' '), 3:('    ', '   ')}

        ## for this specific instance
        self.guesses = guesses
        self.answer = answer
        self.keyboard = self.get_letter_displays()

    def add_guess(self, guess):
        self.guesses += [ guess ]
        self.keyboard = self.get_letter_displays()

    def get_letter_locations(self):
        """ 
        Input: List of words guessed
        Output: A dictionary where the keys are every letter that has been guessed and the 
        values are the positions where the letter has appeared
        """
        letter_locations = dict()
        for word in self.guesses:
            for location, letter in enumerate(word):
                if letter in letter_locations:
                    letter_locations[letter].add(location)
                else:
                    letter_locations[letter] = set([location])
        return letter_locations

    def get_letter_displays(self):
        """
        Input: successful object initialization, with guess and answer strings
        Output: a list of letter_displays with appropriate statuses
        """
        letter_displays = []
        guess_locations = self.get_letter_locations()
        for letter in self.keys:
            if letter in guess_locations:
                ## guessed but not in the answer anywhere
                if letter not in self.answer:
                    letter_displays += [ letter_display(letter, 'NO') ]
                ## guessed in the right position, the intersection of these sets is truthy / not empty
                elif guess_locations[letter] \
                    .intersection(set([i for i, l in enumerate(self.answer) if l == letter])):
                    letter_displays += [ letter_display(letter, 'OK') ]
                ## guessed and it's in the answer, but never guessed in the right position
                else:
                    letter_displays += [ letter_display(letter, 'MOVE') ]
            ## not guessed yet
            else: ## have to make sure that \n is read as one character and not in any of the guesses
                letter_displays += [ letter_display(letter, '?') ]
        return letter_displays

    def __str__(self):
        """
        Input: successful object initialization, with guess list and answer strings
        Output: printable characters (with color on mac, b/w on iphone)
        """
        lines = [ self.top_border ] \
            + ['']*len(self.line_padding) \
            + [ self.bottom_border ]
        line = 1
        line_start = True
        for k in self.keyboard:
            ## beginning of line padding if needed, no matter the letter
            if line_start:
                lines[line] += self.vertical_border + self.line_padding[line][0]
                line_start = False
            ## line break in the keyboard string, print the end of the line and reset line_start
            if k.get_letter() == ' ':
                lines[line] += self.line_padding[line][1] + self.vertical_border
                line += 1
                line_start = True
            ## just print the letter
            else:
                lines[line] += str(k) + ' '
        return '\n'.join(lines)

    def display(self):
        """
        Input: successful object initialization, with guess list and answer strings
        Output: print the display_letters
        """
        if p.IS_IPHONE == False:
            print(self)
        elif p.IS_IPHONE == True:
            line = 1
            line_start = True
            print(self.top_border)
            for k in self.keyboard:
                ## beginning of line padding if needed, no matter the letter
                if line_start:
                    print(self.vertical_border + self.line_padding[line][0], end='')
                    line_start = False
                ## line break in the keyboard string, print the end of the line and reset line_start
                if k.get_letter() == ' ':
                    print(self.line_padding[line][1] + self.vertical_border)
                    line += 1
                    line_start = True
                ## just print the letter
                else:
                    k.display()
            print(self.bottom_border)
class numpad_display(keyboard_display):

    def __init__(self, answer, guesses = []):

        assert type(answer) == str

        ## standards for the whole class
        self.keys = '123+ 456- 789x 0/= '
        self.vertical_border = '\u2551'
        if p.IS_IPHONE == False:
            self.top_border = '\u2554' + ('\u2550'*17) + '\u2557'
            self.bottom_border = '\u255A' + ('\u2550'*17) + '\u255D'
            self.line_padding = {1: (' ', ''), 2: (' ', ''), 3:(' ', ''), 4:('   ','  ')}
        elif p.IS_IPHONE == True:
            self.top_border = '\u2554' + ('\u2550'*9) + '\u2557'
            self.bottom_border = '\u255A' + ('\u2550'*9) + '\u255D'
            self.line_padding = {1: (' ', ''), 2: (' ', ''), 3:(' ', ''), 4:('   ','')}

        ## for this specific instance
        self.guesses = guesses
        self.answer = answer
        self.keyboard = self.get_letter_displays()


if __name__ == '__main__':
    print("-"*80)
    print("LETTER DISPLAY")
    print("-"*80)
    a = letter_display("A", "OK")
    a.display()
    print(' -- ok')
    b = letter_display("B", "MOVE")
    b.display()
    print(' -- move')
    c = letter_display("C", "NO")
    c.display()
    print(' -- no')
    d = letter_display("D", "?")
    d.display()
    print(' -- ?')

    print("-"*80)
    print("KEYBOARD DISPLAY")
    print("-"*80)
    k = keyboard_display('PIPER',['AGAIN','PLEASE','QUEST'])
    k.display()
    
    print("-"*80)
    print("NUMPAD DISPLAY")
    print("-"*80)
    n = numpad_display('20+30=50',['20+20=40','70-40=30'])
    n.display()
    