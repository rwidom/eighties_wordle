# this little practice project is an homage to WORDLE
# find the real thing here: https://www.powerlanguage.co.uk/wordle/

# TO DO: 
# more testing, more debugging material, more memory management / scope clarity

from ew_display import *
from ew_answer import all_the_words
from ew_guesses import all_the_guesses
from time import sleep

## initialize the game dictionary and choose a word
w = input("I'm going to pick a word for you to guess, how many letters should it have? Choose a number between 3 and 7:")
try:
    assert int(w) >= 3 and int(w) <= 7
    d = all_the_words(word_length = int(w))
except:
    print("OK, let's just go with 5 letters this time.")
    d = all_the_words(word_length = 5)

## initialize the object to handle of guesses and feedback
c = input("And how many chances do you want to guess the right word? Choose a number between 3 and 20:")
try:
    assert int(c) >= 3 and int(c) <= 20
    g = all_the_guesses(d, game_length = int(c))
except:
    print("OK, let's just go with 6 guesses this time.")
    g = all_the_guesses(d, game_length = 6)
sleep(2)

## play the game
g.print_header()
g.take_a_guess()
while not(g.game_over):
    g.next_step()
