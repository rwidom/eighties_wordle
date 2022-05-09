import string
import random
from ew_display import *
from ew_config import ew_platform
from ew_answer import all_the_words

class all_the_guesses:
    """
    Accumulates guesses and user progress through the game
    Input: 
        game_dictionary, initialized elsewhere
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
        if self.game_type == 'words':
            w = str(input(':')).upper()
        elif self.game_type == 'equations':
            w = ''.join([c for c in str(input(':')) if c != ' '])
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
        ## get the appropriate clear screen mechanism for this platform
        p = ew_platform()
        ## do the printing
        if len(self.guesses) == 0:
            p.clear()
            print("I'm thinking of a", self.word_length, \
                (self.game_type == 'words')*"letter word." + (self.game_type == 'equations')*"digit equation.", \
                "Start guessing!")
        elif len(self.hint_list)>0:
            p.clear()
            print("Possibilities:", ", ".join(self.hint_list))
        else:
            p.clear()
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

class elimination_guesses(all_the_guesses):
    """ 
    This is similar to absurdle (linked in readme), but it starts with a random guess,
    to make it non-deterministic.
    """

    def __init__(self, game_dictionary, game_length, first_guess = None):
        ## get the normal game stuff
        super(elimination_guesses, self).__init__(game_dictionary=game_dictionary, \
            game_length=game_length, game_type='words')
        ## modify for absurdle, re-initializes possible_words, answer, guesses, keyboard with a random guess
        self.possible_words = self.all_words
        if first_guess is None:
            self.prune_word_list() # don't pass a guess, start with random word choice
        else:
            self.prune_word_list(first_guess)

    def get_bucket_length(self, bucket_key):
        assert bucket_key in self.buckets
        return len(self.buckets[bucket_key])

    def get_alphabet_tuple(self, word):
        """
        Returns a 26 length tuple of tuples with the position(s) of each letter represented by 
        the position in the tuple
        """
        assert type(word) == str
        l = [tuple()]*26
        for (position, letter) in enumerate(word):
            l_index = string.ascii_uppercase.index(letter)
            l[l_index] += tuple([position])
        return tuple(l)

    def get_bucket_id(self, guess, answer):
        """ 
        Input: 
            - a guess and an answer, 26 position tuples from get_alphabet_tuple
        Output: a tuple of 26 values representing the known position(s) of each letter
            - 'x' means we know the letter is *not* in the answer
            - empty tuple means we don't know anything about the letter
            - length of the tuple means known slots for the letter
            - within the tuple, int values are known position(s), None values are unknown positions
        """
        assert type(guess) == tuple
        assert type(answer) == tuple
        bucket_id = [tuple()]*26
        for i in range(26):
            ## letter not in the answer, but in the guess
            if answer[i] == tuple() and guess[i] != tuple():
                bucket_id[i] = 'x'
            ## compare positions
            else:
                known_positions = set(guess[i]).intersection(set(answer[i]))
                unknown_positions = min(
                    len(set(answer[i]) - known_positions),
                    len(set(guess[i]) - known_positions)
                )
                bucket_id[i] = tuple(known_positions) + tuple([None]*unknown_positions)
        return tuple(bucket_id)

    def prune_word_list(self, new_guess = None):
        """ 
        Modifies the all possible words list to take the largest group with a single status, relative
        to the given guess. If no guess is specified, will take a random word.
        """
        if new_guess is None:
            new_guess = random.choice(self.possible_words)
        new_guess_tuple = self.get_alphabet_tuple(new_guess)
        ## create buckets based on relationship to new guess
        self.buckets = dict()
        for word in self.possible_words:
            ## tuple of statuses: 0 = not in word; 1 = in word, wrong place; 2 = in the right place
            word_tuple = self.get_alphabet_tuple(word)
            statuses = self.get_bucket_id(guess = word_tuple, answer = new_guess_tuple)
            ## add this word to the dict
            try:
                self.buckets[ statuses ] += [ word ]
            except:
                self.buckets[ statuses ] = [ word ]
        ## choose the biggest list
        most_common_pattern = sorted(self.buckets, key=self.get_bucket_length, reverse=True)[0]
        ## prune wordlist and act as if there is a new answer
        self.possible_words = self.buckets[most_common_pattern]
        self.answer = random.choice(self.possible_words)
        self.guesses += [new_guess]
        self.keyboard = keyboard_display(self.answer, self.guesses)
        
    def take_a_guess(self):
        """
        Input: guess is a word that the user typed in
        Output: None
        Side effects: Checks for acceptable guess, and 
        """
        print(len(self.possible_words),"possible words left.")
        w = str(input(':')).upper()
        if len(w) != self.word_length:
            msg = 'Please enter a '+str(self.word_length)+'-character guess.'
            self._try_again(w, msg)
        elif w in self.guesses:
            msg = "Please enter something you haven't already guessed."
            self._try_again(w, msg)
        elif w not in self.all_words:
            msg = 'Sorry, ' + w + ' is not in our dictionary. Please try again.'
            self._try_again(w, msg)
        else:
            self.prune_word_list(w)
        return None

if __name__ == '__main__':
    sample_games = \
        [
            ['REAVED', 'SERVED', 'POINTS', 'SQUIRT', 'SHIRTS', 'TRISTE', 'ARISTA' ],
            ['BURGLE', 'POINTS', 'HIGHLY', 'KITTEN', 'FASTER'],
            ['RAGGEE', 'POINTS', 'BILKED', 'PUSHED', 'UNKIND', 'UNBIND'],
            ['WEBBED', 'TROUGH', 'PLAINT', 'AILING', 'FAILED', 'MAKERS', 'YANKED', 'CANVAS', 'CANNAS'],
            ['ALIENS', 'LINKED', 'PASSES', 'FABLED', 'TARGET', 'RAMMED', 'HAMMER', 'JAMMER'],
            ['MERGER', 'POINTS', 'YOUTHS', 'HACKLY', 'DRAFTS', 'BUBBLY']
        ]
    for sg in sample_games:
        print("="*80)
        d = all_the_words(word_length=6)
        g = elimination_guesses(game_dictionary = d, game_length = 20, first_guess = sg[0])
        for turn in sg:
            print('-'*40)
            if turn != sg[0]:
                g.prune_word_list(turn)
            print('Pruned list of possible words based on',turn,'has',len(g.possible_words),'words, starting with...')
            print(', '.join(g.possible_words[:10]))
            print('Randomly chosen answer:', g.answer, '(', g.possible_words.index(g.answer), ')')
            for guess in g.guesses:
                disp = guess_display(guess, g.answer)
                disp.display()


