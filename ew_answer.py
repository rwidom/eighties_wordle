import random

class all_the_words:
    """
    Gets a list of 5 letter words and picks one for the user to guess
    Also has attributes about where the list comes from and all of that
    """


    def __init__(self, 
        word_length=5,
        word_list_file_loc='../Downloads/wlist_match10.txt'):
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
            print("Uh-oh, where is the word list file?")
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
            + "\nby Keith at https://www.keithv.com/software/wlist/"
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

