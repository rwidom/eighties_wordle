# this little practice project is an homage to WORDLE
# find the real thing here: https://www.powerlanguage.co.uk/wordle/

# TO DO: 
# more testing, more debugging material, more memory management / scope clarity
# center the guess display
# add a clear screen before each move
# improve the "guesses left" display, add an arrow?

from ew_display import *
from ew_answer import all_the_words
from ew_guesses import all_the_guesses

## initialize the game dictionary and choose a word
# don't have to specify 5 here, but in case I want to change it...
d = all_the_words(word_length=5)
## initialize the object to handle of guesses and feedback
# don't have to specify 6 here, but in case I want to change it...
g = all_the_guesses(d, game_length=6)
## play the game
while not(g.game_over):
    g.next_step()
