class guess_display:
    """
    Prints the guess with feedback for the user based on the following three statuses for each letter
        OK -- the character is in the answer in the same location
        MOVE -- the character is in the answer, but not in the right place
        NO -- the character is not in the answer word
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
        """
        self.guess = guess
        self.answer = answer 
        self.colors = self.get_colors()
        self.letters = self.get_letter_statuses()



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
            # at the end of a letter to reset the color
            'END': '\033[0m'
            }
        return(colors)
    

    def get_letter_statuses(self, word = guess):
        """
        Input: successful object initialization, with guess and answer strings
        Output: a tuple of tuples with each letter of the guess, followed by its status
        """
        statuses = []
        for i in range(len(word)):
            if word[i] == self.answer[i]:
                statuses += ['OK']
            elif word[i] in self.answer:
                statuses += ['MOVE']
            else:
                statuses += ['NO']
        return(tuple(zip(word, statuses)))


    def display(self):
        """
        Input: successful object initialization, with guess and answer strings
        Output: a list of tuples with each letter of the guess, paired with it's status
        """

        ## generate the final string and print it
        print_string = ' '.join(
            [colors[l[1]] + ' ' + l[0] + ' ' + colors['END']
            for l in letters]
        )
        print(print_string)

    def display_keyboard(self, guesses):
        assert type(guesses) == list
        keyboard = 'QWERTYUIOP \n ASDFGHJKL \n ZXCVBNM'
        guessed_letters = [letter for word in guesses for letter in get_letter_statuses(word)]
        no = set([l[0] for l in guessed_letters if l[1] == 'NO'])
        ok = set([l[0] for l in guessed_letters if l[1] == 'OK'])
        move = set([l[0] for l in guessed_letters if l[1] == 'MOVE']) - ok
        for letter in move:
            keyboard.replace(letter, colors['MOVE'] + letter + colors['END'])
        for letter in ok:
            keyboard.replace(letter, colors['OK'] + letter + colors['END'])
        for letter in no:
            keyboard.replace(letter, colors['NO'] + letter + colors['END'])
        print(keyboard)


