import random
import string
from ast import literal_eval
from ew_config import ew_platform
p = ew_platform()
assert p.is_correct_directory()

# import logging
# logging.basicConfig(
#     filename='ew_log.txt',
#     filemode='a',    
#     format='%(asctime)s %(levelname)-8s %(message)s',
#     level=logging.INFO,
#     datefmt='%Y-%m-%d %H:%M:%S')

class all_the_words:
    """
    Gets a list of words matching the game word length and picks one for the user to guess
    Also has attributes about where the list comes from and all of that
    """

    def __init__(self, 
        word_length=5,
        word_list_file_loc='twl06.txt'):

        ## defaults and passed parameters
        self.word_length = word_length
        self.untested_file_location = word_list_file_loc

        ## massaging / generation
        self.file_location = self.get_file_location()
        self.word_list = self.get_words()
        self.answer = self._choose_answer()
        self.hint_tree = self._build_hint_tree()


    def get_file_location(self):
        """ 
        Where the word list file is saved relative to where the program is being run
        TO DO: some better path navigation maybe? This assumes that we're running this in
        the structure I have right now.
        """
        file_location = self.untested_file_location
        try:
            with open(file_location,'r') as f:
                1 == 1
        except:
            print("Uh-oh, where is the word list file? Are you running this from the eighties_wordle directory?")
            return(None)
        return file_location


    def get_words(self):
        """ 
        Gets the full list of valid words, and make it accessible outside the object 
        Words will all be upper case
        """
        word_list = []
        with open(self.file_location,'r', encoding='utf-8') as f:
        	for word in f:
        	  	if len(word) == self.word_length + 1:       # +1 for the line break
        	  		word_list += [ word.upper().strip() ]
        return word_list


    def _choose_answer(self):
        """ 
        Chooses a random word from the list of words. 
        This is internal only, because it should only happen once for each instance at
        initialization.
        After initialization, use the attribute, not a function.
        """
        return random.choice(self.word_list)


    def get_hint_index(self, word):
        """ 
        Generates an index a list of position / letter tuples for navigating the hint tree
        """
        return [ str(i).zfill(2)+word[i] for i in range(self.word_length) if word[i] != '_' ]

    def _build_hint_tree(self):
        """ 
        Takes the list of words, and transforms it into a hierarchy to use for quickly finding hints.
        The idea is from here: https://wdi.centralesupelec.fr/1CC1000/Hangman

        The hint tree is a dict:
        - key is a tuple of character and position
        - value is a set of words with that character and position

        The hint then is the intersection of all of the words with the known character, position pairs.

        So that we don't have to calculate this at the beginning of each game, it saves the last hint tree
        with word length. It will still recalculate if the word length changes. TO DO: add a check for dictionary
        changes.
        """
        assert type(self.word_list) == list
        try:
            # for this to work, file must exist, and it must be a dict for the game 
            # word length 
            with open("ew_hint_tree.txt", "r") as input_file:
                ew_hint_tree_data = input_file.read()
            ew_hint_tree = literal_eval(ew_hint_tree_data)
            # we read the types correctly
            assert isinstance(ew_hint_tree, dict)
            # we have the right word length
            assert self.word_length in ew_hint_tree
            hint_tree = ew_hint_tree[self.word_length]
        except:
            print('Give me a second to collect hints for you...')
            # if that's not true, we'll create the hint tree and write it to this file 
            # for next time
            hint_tree = {
                str(n).zfill(2) + l: set()
                for n in range(self.word_length)
                for l in string.ascii_uppercase
            }
            for w in self.word_list:
                for i in self.get_hint_index(w):
                    hint_tree[i].add(w)
            with open("ew_hint_tree.txt", "w") as output_file:
                output_file.write(str({self.word_length: hint_tree}))
        return(hint_tree)

    def collect_hints(self, my_word):
        '''
        my_word: string with _ characters, current guess of secret word
        hint_tree: custom nested dict representation of the word list returned by _build_hint_tree()
            acts as a hash index of the word list. 
        returns: a list of words from the dictionary that share length and letters in the positions 
            already guessed by the player, ignoring blanks / _ characters and letters guessed that
            do not appear in my_word and should disqualify some of these words
        '''
        assert type(self.hint_tree) == dict ## the hint tree has been defined and built
        assert type(my_word) == str
        hint_keys = self.get_hint_index( my_word )
        hints = self.hint_tree[hint_keys[0]]
        for k in hint_keys[1:]:
            hints = set.intersection(hints, self.hint_tree[k])
        hints = list(hints)
        hints.sort()
        return(hints)

class all_the_equations(all_the_words):
    def __init__(self, 
        word_length = 7,
        max_value = 150):
        ## defaults and passed parameters
        self.word_length = word_length
        self.max_value = max_value
        ## massaging / generation
        (self.word_list, self.answer) = self.get_equations()
        self.hint_tree = self._build_hint_tree()

    def get_equations(self):
        # TO DO: move this to configuration step
        try:
            assert len(str(self.max_value)+'*'+str(self.max_value)+'='+str(self.max_value^2)) >= self.word_length
        except:
            print('Oops! No equations fit those constraints. Please restart and lower the characters or raise the maximum number.')
            exit()
        answer_list = []
        other_list = []
        rand_start = random.getrandbits(1)
        for a in range(self.max_value + 1):
            for b in range(a, self.max_value + 1):
                ## calculate all possible answers, b is always >= a, so do both orders where possible
                a_add = str(a)+'+'+str(b)+'='+str(a + b)
                b_add = str(b)+'+'+str(a)+'='+str(b + a)
                a_sub = str(a)+'-'+str(b)+'='+str(a - b)
                b_sub = str(b)+'-'+str(a)+'='+str(b - a)
                a_mult = str(a)+'x'+str(b)+'='+str(a * b)
                b_mult = str(b)+'x'+str(a)+'='+str(b * a)
                ab_div = ''
                if a != 0:
                    if float(b) / float(a) == int(b / a):
                        ab_div = str(b)+'/'+str(a)+'='+str(int(b / a))
                ## pick some to be actual possible answers
                if rand_start:
                    answers = [a_add, a_sub, a_mult, b_mult, ab_div]
                    others = [b_add, b_sub]
                else:
                    answers = [b_add, b_sub, a_mult, b_mult, ab_div]
                    others = [a_add, a_sub]
                answer_list += [a for a in answers if len(a) == self.word_length]
                other_list += [a for a in others if len(a) == self.word_length]
                ## switch random start
                rand_start = not(rand_start)
        answer = random.choice(answer_list)
        word_list = answer_list + other_list
        return (word_list, answer)

    def get_words(self):
        return self.word_list

    def get_answer(self):
        return self.answer

if __name__ == '__main__':

    print("="*80)
    print("Get the min and max word length overall")
    print("="*80)
    a = all_the_words()
    min_len = 1000
    max_len = 0
    with open(a.get_file_location()) as f:
        for w in f:
            l = len(w) - 1
            if l > max_len: max_len = l
            if l < min_len: min_len = l
    print("The shortest word has",min_len,"letters.")
    print("The longest word has",max_len,"letters.")

    print("="*80)
    print("REGULAR WORDS")
    print("="*80)
    w = a.get_words()
    print('len:', len(w))
    print('min:', min(w))
    print('max:', max(w))
    print('sample words:',', '.join(random.sample(w, 20)))

    print("="*80)
    print("MATH VERSION")
    print("="*80)
    m = all_the_equations(word_length=10)
    w = m.get_words()
    print('len:', len(w))
    print('min:', min(w))
    print('max:', max(w))
    print('sample words:',', '.join(random.sample(w, 20)))

