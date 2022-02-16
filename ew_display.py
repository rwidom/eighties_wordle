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
        This just returns a constant dict with the ANSI color codes we'll use for different letter statuses
        """
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
        return(colors)

    def get_color(self, status):
        return self.get_colors()[status]

    def __str__(self):
        """ put one space on either side of the character and ansi colors for the status on either side of that"""
        return str(self.get_color(self.get_status()) + ' ' + self.get_letter() + ' ' + self.get_color('END'))

    def __add__(self, other):
        """ concatenate letters with space in between by adding them in the same way that you can with strings """
        return str(self) + ' ' + str(other) + ' '

    def display(self):
        """ prints the string version of the letter with status coloring """
        print(self)

        

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

    def get_letter_statuses(self):
        """
        Input: successful object initialization, with guess and answer strings
        Output: a list of letter_displays with appropriate statuses
        """
        letter_displays = []
        for (location, letter) in enumerate(self.guess):
            if letter == self.answer[location]:
                letter_displays += [ letter_display(letter, 'OK') ]
            elif letter in self.answer:
                letter_displays += [ letter_display(letter, 'MOVE') ]
            else:
                letter_displays += [ letter_display(letter, 'NO') ]
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
        print(str(self))

class keyboard_display:
    """
    Prints the QWERTY keyboard with letters color coded based on their best guess status
    within the game.
    """
    keyboard = 'QWERTYUIOP ASDFGHJKL ZXCVBNM'
    top_border = '\u2554' + ('\u2550'*39) + '\u2557'
    bottom_border = '\u255A' + ('\u2550'*39) + '\u255D'
    vertical_border = '\u2551'
    
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
        assert type(answer)==str
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
        values are the positions where those letter has appeared
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
        print(str(self))
