import random
from ew_config import ew_platform
p = ew_platform()
assert p.is_correct_directory()

class all_the_words:
    """
    Gets a list of words matching the game word length and picks one for the user to guess
    Also has attributes about where the list comes from and all of that
    """

    def __init__(self, 
        word_length=5,
        word_list_file_loc='wordlist.txt'):
        """ Wordle uses five letter words, as far as I know, but in case we want to do
        something different in the future, let's make it possible to set that here.
        All words are upper case. """

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


    def get_citation(self, print=True):
        """ 
        Just a place to acknowledge the source of the word list.
        By default it just prints the citation, but if print=False, it will return the 
        citation string.
        """
        citation = \
            "We're using the word list stored at " + self.file_location \
            + "\nIt comes from the list of words appearing in at least 10 sources compiled " \
            + "\nby Keith at https://www.keithv.com/software/wlist/" \
            + "\nJust two modifications: dropping words with apostrophes, and dropping the " \
            + "\nword bitch, because fuck there's enough misogyny, I don't need it in my game." \
            + "\nAnd dropping proper nouns and adding stuff as I see fit. Though I'll try and" \
            + "\nverify things on dictionary.com or something."
        if print:
            print(citation)
            return None
        else:
            return citation


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
        return [ (i, word[i]) for i in range(self.word_length) if word[i] != '_' ]

    def merge_hint_dicts(self, a, b):
        """ 
        Input: Two dicts where the values are sets (i.e. the dict for a new word, and the existing hint 
            tree branch for the associated word-length)
        Output: One dict with all of the keys, and unions of the sets where the keys overlap
        """
        r = a.copy()
        both_index = a.keys() & b.keys()
        unions = {i : (a[i] | b[i]) for i in both_index}
        r.update(b) ## add b indices to a where they are missing, and overwrite a values with b where they overlap
        r.update(unions) ## overwrite the overlapping values with the unions we ultimately want
        return r

    def _build_hint_tree(self):
        """ 
        Takes the list of words, and transforms it into a hierarchy to use for quickly finding hints.
        The idea is from here: https://wdi.centralesupelec.fr/1CC1000/Hangman

        The hint tree is a dict:
        - key is a tuple of character and position
        - value is a set of words with that character and position

        The hint then is the intersection of all of the words with the known character, position pairs

        It takes time and space to set up this structure. The brute force approach of evaluating 
        every word in the list isn't all that slow. And, not every player will ask for a hint in every game.
        So for a real software package, I would at least save this rather than generating it in memory at the 
        start of every game, and probably just skip it. But it was fun to implement, and would allow the 
        computer to guess letters as an alternate game dynamic.
        """
        assert type(self.word_list) == list
        hint_tree = {}
        for w in self.word_list:
            add_leaves = dict.fromkeys(self.get_hint_index(w), set([w]))
            hint_tree = self.merge_hint_dicts(hint_tree, add_leaves)
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
    print("REGULAR WORDS")
    print("="*80)
    a = all_the_words()
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

