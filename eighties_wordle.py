# this little practice project is an homage to WORDLE
# find the real thing here: https://www.powerlanguage.co.uk/wordle/

from time import sleep
from ew_display import *
from ew_answer import *
from ew_guesses import *
from ew_config import *
import requests
from pprint import pprint

config = ew_configuration()

while True:
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
            ## get the api key for https://dictionaryapi.com/ which is run by Merriam-Webster
            with open('dictionary_api.txt') as f:
                API_KEY = f.read()
            ## call the API
            definition_url = 'https://dictionaryapi.com/api/v3/references/collegiate/json/'+g.answer+'?key='+API_KEY
            definition = requests.get(definition_url).json()[0]['def']
            ## pretty print isn't 100% pretty, but I don't want to figure out all the details of the formatting
            pprint(definition)
            print()
        except:
            print("Something's up with the dictionary check. Sorry!")

    ## want to play again?
    p = input("Want to play again? (Yes, Y, and You betcha, with any capitalization, will all work):")
    if p.lower() in ('yes','y','you betcha'):
        print("Yay! Me too!")
        sleep(1)
    else:
        print("That's cool, I didn't want to either.")
        exit()
