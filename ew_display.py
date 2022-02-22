from ew_config import ew_config
(IS_IPHONE, environment) = ew_config()
if IS_IPHONE:
    from console import set_color
class letter_display():
    """ 
    Prints a single letter based on one of four statuses:
        OK   -- green background / black text, intended for the character is in the answer in the same location
        MOVE -- yellow background / black text, intended for the character is in the answer, but not in the right place
        NO   -- black background / grey bold text, intended for when we know the character is not in the answer word
        ?    -- default appearance (dark grey background / white text), intended for when the character has not been guessed yet, so we don't know
    """
    def __init__(self, letter=" ", status="?"):
        """ initialize a letter_display with a single letter and status. defaults to a space and unknown status """ 
        assert type(IS_IPHONE) == bool
        self.set_status(status)
        self.set_letter(letter)

    def set_status(self, status):
        """ choose one of four possible statuses for this letter: OK, MOVE, NO, or ? """
        assert status in ['OK', 'MOVE', 'NO', '?']
        self.status = status

    def set_letter(self, letter):
        """ set a single character to be displayed """
        assert type(letter) == str
        assert len(letter) == 1
        self.letter = letter

    def get_letter(self):
        return self.letter

    def get_status(self):
        return self.status

    def get_colors(self):
        """
        This just returns a constant dict with the color codes we'll use for different letter statuses
        """
        if IS_IPHONE == False: ## running on a laptop
            # ANSI color codes described here https://en.wikipedia.org/wiki/ANSI_escape_code
            # python code reference from https://stackoverflow.com/questions/287871/how-to-print-colored-text-to-the-terminal
            colors = {
                # the right letter in the right position -- green background, black text
                'OK': '\033[42m\033[30m',
                # a letter in the word, but not in the right position -- yellow background, black text
                'MOVE': '\033[43m\033[30m',
                # a letter not in the word -- black background, grey bold text
                'NO': '\033[40m\033[90m\033[1m',
                # at the end of a letter to reset the color, or if the letter status is unknown
                'END': '\033[0m',
                '?': '\033[0m'
                }
        elif IS_IPHONE == True:
            # http://omz-software.com/pythonista/docs/ios/console.html
            # here, we're returning the (r, g, b) tuple to set the consol color the way we want
            colors = {
                # the right letter in the right position -- green 
                'OK': [0.0, 1.0, 0.0],
                # a letter in the word, but not in the right position -- yellow 
                'MOVE': [1.0, 1.0, 0.0],
                # a letter not in the word -- grey
                'NO': [0.5, 0.5, 0.5],
                # at the end of a letter to reset the color, or if the letter status is unknown
                'END': [1.0, 1.0, 1.0],
                '?': [1.0, 1.0, 1.0]
            }      
        return(colors)

    def get_color(self):
        return self.get_colors()[self.get_status()]

    def __str__(self):
        """ 
        On the mac, where ansi colors work, this works really nicely: 
            Put one space on either side of the character and ansi colors for the status on either side of that
        On the iphone in pythonista:
            You lose the color and just get space + letter + space
        """
        if IS_IPHONE == False:
            return self.get_color() + ' ' + self.get_letter() + ' ' + self.get_colors()['END']
        elif IS_IPHONE == True:
            return ' ' + self.get_letter() + ' '

    def __add__(self, other):
        """ concatenate letters with space in between by adding them in the same way that you can with strings """
        return str(self) + ' ' + str(other) + ' '

    def display(self):
        """ prints the string version of the letter with status coloring, without any new line at the end """
        if IS_IPHONE == False:
            ## mac lap top can handle the unicode string
            print(self, end='')
        elif IS_IPHONE == True:
            ## iphone uses a list [r, g, b]
            ## I can't use ** because set_color won't take named parameters :(
            c = self.get_color()
            set_color(c[0], c[1], c[2])
            print(self, end='')
            set_color()
        else:
            print('Please check the environment and ew_config.py')

        

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
        assert type(IS_IPHONE) == bool
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
    keyboard = 'QWERTYUIOP ASDFGHJKL ZXCVBNM '
    vertical_border = '\u2551'
    if IS_IPHONE == False:
        top_border = '\u2554' + ('\u2550'*39) + '\u2557'
        bottom_border = '\u255A' + ('\u2550'*39) + '\u255D'
    elif IS_IPHONE == True:
        top_border = '\u2554' + ('\u2550'*30) + '\u2557'
        bottom_border = '\u255A' + ('\u2550'*30) + '\u255D'
    
    def __init__(self, answer, guesses = []):
        """
        Input: at least an answer, in case there aren't any guesses yet, but ideally an
            answer and a list of guesses that are all valid words. Any data quality issues (case, length, 
            alphas only) happens outside of the printer object.
        Output: successfully initializes the object
        TO DO: 
            put in place some assertions / checks to back up the input assumptions
            write nicer getter and setters
        """
        assert type(answer) == str
        assert type(IS_IPHONE) == bool
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
        for letter in keyboard_display.keyboard:
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
        Output: print the display_letters
        """
        line = 0
        lines = ['', '', '']
        for k in self.keyboard:
            if k.get_letter()==' ':
                line += 1
            else:
                lines[line] += str(k) + ' '
        return '\n' + keyboard_display.top_border \
            + '\n' + keyboard_display.vertical_border + lines[0][0:-1] + keyboard_display.vertical_border \
            + '\n' + keyboard_display.vertical_border + '  ' + lines[1][0:-1] + '  ' + keyboard_display.vertical_border \
            + '\n' + keyboard_display.vertical_border + '      ' + lines[2][0:-1] + '      ' + keyboard_display.vertical_border \
            + '\n' + keyboard_display.bottom_border \
            + '\n'

    def display(self):
        """
        Input: successful object initialization, with guess list and answer strings
        Output: print the display_letters
        """
        if IS_IPHONE == False:
            print(self)
        elif IS_IPHONE == True:
            line = 1
            line_padding = {1: ('', ''), 2: ('  ', ' '), 3:('     ', '    ')}
            line_start = True
            print(keyboard_display.top_border)
            for k in self.keyboard:
                ## beginning of line padding if needed, no matter the letter
                if line_start:
                    print(keyboard_display.vertical_border + line_padding[line][0], end='')
                    line_start = False
                ## line break in the keyboard string, print the end of the line and reset line_start
                if k.get_letter() == ' ':
                    print(line_padding[line][1] + keyboard_display.vertical_border)
                    line += 1
                    line_start = True
                ## just print the letter
                else:
                    k.display()
            print(keyboard_display.bottom_border)


if __name__ == '__main__':
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
