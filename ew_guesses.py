import string
from ew_display import guess_display
from ew_answer import all_the_words
 

class all_the_guesses:
    """
    Accumulates guesses and user progress through the game
    Input: 
        game_dictionary of type all_the_words, initialized elsewhere
        user typing in guesses
    """

    def __init__(self, game_dictionary, game_length = 6):

        self.game_length = game_length
        self.game_dictionary = game_dictionary
        self.all_words = game_dictionary.word_list
        self.answer = game_dictionary.answer
        self.word_length = game_dictionary.word_length
        self.hint_tree = game_dictionary.hint_tree
        self.guesses = []
        self.goofs = []
        self.game_over = False


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
            self._next_guess()

    
    def _next_guess(self):
        """
        Input: guess is a word that the user typed in
        Output: None
        Side effects: 
            - If the word is not a valid (case-insensitive) word in our game dictionary,
            it is added to the list of goofs, we ask the user to try again, and we check again.
            - If the word *IS* valid, we add it to the list of guesses in the last position.
        """
        w = str(input(':')).upper()
        if w.isnumeric():
            if int(w)>0 and int(w)<=len(self.guesses):
                letter_statuses = list(guess_display(self.guesses[int(w)-1], self.answer).get_letter_statuses())
                word_with_blanks = "".join([ \
                    char*(status == 'OK') + '_'*(status != 'OK') \
                    for (char, status) in letter_statuses
                    ])
                print(", ".join(self.game_dictionary.collect_hints(word_with_blanks)))
            else:
                msg = "For a hint, please enter the single digit turn number for the word you'd like to search."
                self._try_again(w, msg)
        elif not(w.isalpha()):
            msg = 'Please enter '+str(self.word_length)+' letters, no symbols or spaces.'
            self._try_again(w, msg)
        elif len(w) != self.word_length:
            msg = 'Please enter a '+str(self.word_length)+'-letter word.'
            self._try_again(w, msg)
        elif w in self.guesses:
            msg = "Please enter a word you haven't already guessed."
            self._try_again(w, msg)
        elif w not in self.all_words:
            msg = 'Sorry, ' + w + ' is not in our dictionary. Please try again.'
            self._try_again(w, msg)
        else:
            self.guesses += [w]
        return None


    def print_header(self):
        """ 
        print a line, notice of remaining guesses, and feedback on past guesses
        for the top of each turn 
        """
        divider = "-" * 4 * self.word_length
        remaining_guesses = self.game_length - len(self.guesses)
        if remaining_guesses == 1:
            print(divider, '1 guess left')
        else:
            print(divider, remaining_guesses, 'guesses left')
        ## if there aren't any guesses yet, this does nothing
        for g in self.guesses:
            guess_display(g, self.answer).display()
    

    def next_step(self):
        """
        Displays the normal prompt for the next guess and calls the validator.
        """        
        if len(self.guesses) == 0:
            print("I'm thinking of a", self.word_length, "letter word. Start guessing!")
            self.print_header()
            self._next_guess()
        else:
            self.print_header()
            if self.guesses[-1] == self.answer:
                print('Congratulations!!!')
                self.game_over = True
            elif len(self.guesses) == self.game_length:
                print("Sorry, that was your last guess. The word was", self.answer, ".")
                self.game_over = True
            else:
                self._next_guess()



