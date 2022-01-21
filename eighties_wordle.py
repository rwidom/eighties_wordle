# this little practice project is an homage to WORDLE
# find the real thing here: https://www.powerlanguage.co.uk/wordle/

# TO DO: more testing, more debugging material, more memory management / scope clarity

from ew_display import guess_display
from ew_answer import all_the_words
from ew_guesses import all_the_guesses

## initialize the game dictionary and choose a word
d = all_the_words()
## initialize the object to handle of guesses and feedback
g = all_the_guesses(d)
## play the game
while not(g.game_over):
    g.next_step()
