# this little practice project is an homage to WORDLE
# find the real thing here: https://www.powerlanguage.co.uk/wordle/

from time import sleep
from ew_display import *
from ew_answer import *
from ew_guesses import *
from ew_config import *

while True:
    clear()
    ## choose the type of game, length of thing to guess, and number of changes
    settings = check_settings()

    ## initialize the game dictionary and choose a word / equation
    ## initialize the object to handle of guesses and feedback
    t = settings['game_type']['value']
    if t == 'words':
        d = all_the_words(word_length = settings['word_length_words']['value'])
        g = all_the_guesses(d, game_length = settings['game_length_words']['value'], game_type = t)
    elif t == 'equations':
        d = all_the_equations(word_length = settings['word_length_equations']['value'])
        g = all_the_guesses(d, game_length = settings['game_length_equations']['value'], game_type = t)
    else:
        print("Uh-oh, where did game type",t,"come from?")
        exit()

    ## play the game
    g.print_header()
    g.take_a_guess()
    while not(g.game_over):
        g.next_step()

    ## want to play again?
    p = input("Want to play again? (Yes, Y, and You betcha, with any capitalization, will all work):")
    if p.lower() in ('yes','y','you betcha'):
        print("Yay! Me too!")
        sleep(2)
    else:
        print("That's cool, I didn't want to either.")
        exit()
