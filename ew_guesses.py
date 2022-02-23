import string
from ew_display import *
from ew_config import *
from ew_answer import all_the_words

class all_the_guesses:
    """
    Accumulates guesses and user progress through the game
    Input: 
        game_dictionary of type all_the_words, initialized elsewhere
        user typing in guesses
    """

    def __init__(self, game_dictionary, game_length = 6, game_type='words'):
        assert game_type in ('words', 'equations')

        self.game_length = game_length
        self.game_dictionary = game_dictionary
        self.all_words = game_dictionary.word_list
        self.answer = game_dictionary.answer
        self.word_length = game_dictionary.word_length
        self.hint_tree = game_dictionary.hint_tree
        self.hint_list = []
        self.guesses = []
        self.goofs = []
        self.game_over = False
        self.game_type = game_type
        if game_type=='words':
            self.keyboard = keyboard_display(self.answer, [])
        elif game_type=='equations':
            self.keyboard = numpad_display(self.answer, [])


    def _try_again(self, word, instruction):
        """
        what to do when there is a goof
        """  
        self.goofs += [word]
        remaining_goofs = self.game_length - len(self.goofs)
        if remaining_goofs <= 0:
            bad_guess = word[:self.word_length] \
                .lower().strip() \
                .rjust(self.word_length,'*')
            self.guesses += [ bad_guess ]
            self.next_step()
        else:
            print(instruction," (You have",remaining_goofs,"remaining warnings.)")
            self.take_a_guess()

    
    def take_a_guess(self):
        """
        Input: guess is a word that the user typed in
        Output: None
        Side effects: 
            - If the word is not a valid (case-insensitive) word in our game dictionary,
            it is added to the list of goofs, we ask the user to try again, and we check again.
            - If the word *IS* valid, we add it to the list of guesses in the last position.
        """
        w = str(input(':')).upper()
        if (w.isnumeric() and len(w)<=2) or w=='*':
            ## only look at turns with valid words and at least one ok letter
            valid_turns = []
            for (i, guess) in enumerate(self.guesses):
                if guess in self.all_words and \
                    max( [ g==a for (g, a) in zip(guess, self.answer) ] ):
                    valid_turns += [ i + 1 ]
            ## get a possible index for the guesses list
            turn = 0
            if len(valid_turns)==0:
                self.print_header()
                print("Sorry, you need a turn with at least one thing in the right position to get a hint.")
                self.take_a_guess()
            elif w=='*':
                turn = valid_turns[-1]
            elif int(w) in valid_turns:
                turn = int(w)
            else:
                self.print_header()
                print("For a hint, please choose from one of these turns -- "+", ".join([str(t) for t in valid_turns]))
                self.take_a_guess()
            ## generate the hint list
            if turn > 0:
                word_with_blanks = guess_display(self.guesses[turn - 1], self.answer) \
                    .get_correct_letters_plus_blanks()
                self.hint_list = self.game_dictionary.collect_hints(word_with_blanks)
        elif len(w) != self.word_length:
            msg = 'Please enter a '+str(self.word_length)+'-character guess.'
            self._try_again(w, msg)
        elif w in self.guesses:
            msg = "Please enter something you haven't already guessed."
            self._try_again(w, msg)
        elif w not in self.all_words:
            msg = 'Sorry, ' + w + ' is not in our dictionary. Please try again.'
            self._try_again(w, msg)
        else:
            self.guesses += [w]
            self.keyboard.add_guess(w)
        return None


    def print_header(self):
        """ 
        print a line, notice of remaining guesses, and feedback on past guesses
        for the top of each turn 
        """
        if len(self.guesses) == 0:
            _ = clear()
            print("I'm thinking of a", self.word_length, \
                (self.game_type == 'words')*"letter word." + (self.game_type == 'equations')*"digit equation.", \
                "Start guessing!")
        elif len(self.hint_list)>0:
            _ = clear()
            print("Possibilities:", ", ".join(self.hint_list))
        else:
            _ = clear()
        remaining_guesses = self.game_length - len(self.guesses)
        if remaining_guesses == 1:
            print('You have 1 guess left.')
        else:
            print('You have', remaining_guesses, 'guesses left.')
        ## if there aren't any guesses yet, this does nothing
        for g in self.guesses:
            d = guess_display(g, self.answer)
            d.display()
        ## display the keyboard
        self.keyboard.display()

    def next_step(self):
        """
        Displays the normal prompt for the next guess and calls the validator.
        Won't work at the very beginning of the game, need to call print header and take_a_guess
        """
        assert len(self.guesses)>0
        self.print_header()
        if self.guesses[-1] == self.answer:
            print('Congratulations!!!')
            self.game_over = True
        elif len(self.guesses) == self.game_length:
            print("Sorry, that was your last guess. The word was", self.answer, ".")
            self.game_over = True
        else:
            self.take_a_guess()



