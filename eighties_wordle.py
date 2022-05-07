# this little practice project is an homage to WORDLE
# find the real thing here: https://www.powerlanguage.co.uk/wordle/

from ew_display import *
from ew_answer import *
from ew_guesses import *
from ew_config import *
from ew_word_definition import *

config = ew_configuration()

while True:
    ## clear the screen
    config.clear()
    ## choose the type of game, length of thing to guess, and number of changes
    config.check_settings()

    ## initialize the game dictionary and choose a word / equation
    ## initialize the object to handle of guesses and feedback
    if config.get_game_type() == 'words':
        d = all_the_words(word_length = config.get_value('word_length_words'),
            word_list_file_loc='twl06.txt')
        if config.get_value("absurdle_words"):
            g = elimination_guesses(d, \
                game_length = config.get_value('game_length_words'))
        else:
            g = all_the_guesses(d, \
                game_length = config.get_value('game_length_words'), \
                game_type = config.get_game_type())
    elif config.get_game_type() == 'equations':
        d = all_the_equations(word_length = config.get_value('word_length_equations'), \
            max_value = config.get_value('max_value_equations'))
        g = all_the_guesses(d, \
            game_length = config.get_value('game_length_equations'), \
            game_type = config.get_game_type())
    else:
        print("Uh-oh, where did game type",config.get_game_type(),"come from?")
        exit()

    ## play the game
    g.print_header()
    g.take_a_guess()
    while not(g.game_over):
        g.next_step()

    ## show the word definition
    if config.get_game_type() == 'words':
        try:
            print('-->',g.answer,'means',get_first_definition(g.answer))
        except:
            pass

    ## want to play again?
    p = input("Want to play again? (Yes, Y, and You betcha, with any capitalization, will all work):")
    if p.lower() in ('yes','y','you betcha'):
        continue
    else:
        print("That's cool, I didn't want to either.")
        exit()
