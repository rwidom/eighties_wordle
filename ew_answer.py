import random

class all_the_words:
    """
    Gets a list of 5 letter words and picks one for the user to guess
    Also has attributes about where the list comes from and all of that
    """


    def __init__(self, 
        word_length=5,
        word_list_file_loc='../Downloads/wordlist.txt'):
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
            + "\nword bitch, because fuck there's enough misogyny, I don't need it in my game."
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
        with open(self.file_location,'r') as f:
            all_words = f.read().split('\n')
            word_list = [w.upper() for w in all_words if len(w)==self.word_length]
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
        Generates an index -- nested tuple -- including a list of position / letter tuples for 
        navigating the hint tree
        """
        l1_key = len(word)
        l2_keys = [ (i, word[i]) for i in range(l1_key) if word[i].isalpha() ]
        return (l1_key, l2_keys)

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

        The hint tree is a dict of dicts:
        - first layer key is the number of characters in the word
        - first layer value is the second layer dict
        - second layer key is a tuple of character and position
        - second layer value is a set of words with that character and position

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
            (l1_key, l2_keys) = self.get_hint_index(w)
            add_leaves = dict.fromkeys(l2_keys, set([w]))
            if l1_key in hint_tree:
                hint_tree[l1_key] = self.merge_hint_dicts(hint_tree[l1_key], add_leaves)
            else:
                hint_tree[l1_key] = add_leaves
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
        assert type(self.hint_tree) == dict ## the hint tree has been defined and built globally
        assert type(my_word) == str
        (l1_key, l2_keys) = self.get_hint_index( my_word )
        hints = self.hint_tree[l1_key][l2_keys[0]]
        for l2 in l2_keys[1:]:
            hints = set.intersection(hints, self.hint_tree[l1_key][l2])
        hints = list(hints)
        hints.sort()
        return(hints)