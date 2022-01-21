## structure notes
# the actual characters of a guess (word length is part of the answer object), using upper and ignoring non-alpha
# the formatted version of a guess, which refers to the actual word, and includes strikethrough or 
#   something to indicate not a word, but doesn't count the guess
# the ability to count down 6 guesses?
# classes: right answer, guess list, 

from ew_display import guess_display
from ew_answer import all_the_words
import random

## initialize the game dictionary / list of words and get the answer
game_dictionary = all_the_words()
a = game_dictionary.answer

## make a random guess from the game dictionary
g = random.choice(game_dictionary.word_list) 

## initialize the display printer, and print this combination
printer = guess_display(g, a)
print('answer =',a,'; guess =',g)
printer.display()

