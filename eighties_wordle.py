# this little practice project is an homage to WORDLE
# find the real thing here: https://www.powerlanguage.co.uk/wordle/

from os.path import exists

from ew_answer import all_the_equations, all_the_words
from ew_config import ew_configuration
from ew_guesses import all_the_guesses, elimination_guesses
from ew_word_definition import get_first_definition, internet


# import logging
# logging.basicConfig(
#     filename='ew_log.txt',
#     filemode='a',
#     format='%(asctime)s %(levelname)-8s %(message)s',
#     level=logging.INFO,
#     datefmt='%Y-%m-%d %H:%M:%S')

config = ew_configuration()

while True:
    # clear the screen
    config.clear()
    # choose the type of game, length of thing to guess, and number of changes
    config.check_settings()

    # initialize the game dictionary and choose a word / equation
    # initialize the object to handle of guesses and feedback
    if config.get_game_type() == "words":
        d = all_the_words(
            word_length=config.get_value("word_length_words"),
            word_list_file_loc="twl06.txt",
        )
        if config.get_value("absurdle_words") == "Yes":
            g = elimination_guesses(
                d, game_length=config.get_value("game_length_words")
            )
        else:
            g = all_the_guesses(
                d,
                game_length=config.get_value("game_length_words"),
                game_type=config.get_game_type(),
            )
    elif config.get_game_type() == "equations":
        d = all_the_equations(
            word_length=config.get_value("word_length_equations"),
            max_value=config.get_value("max_value_equations"),
        )
        g = all_the_guesses(
            d,
            game_length=config.get_value("game_length_equations"),
            game_type=config.get_game_type(),
        )
    else:
        print("Uh-oh, where did game type", config.get_game_type(), "come from?")
        exit()

    # play the game
    g.print_header()
    g.take_a_guess()
    while not (g.game_over):
        g.next_step()

    # show the word definition
    if (
        config.get_game_type() == "words"
        and exists("dictionary_api.txt")
        and internet()
    ):
        print("-->", g.answer, "means", get_first_definition(g.answer))

    # want to play again?
    p = input(
        "Want to play again? (No, N, and Nope, with any capitalization, will all exit "
        + "the game):"
    )
    if p.lower() in ("no", "n", "nope"):
        print("That's cool, I didn't want to either.")
        exit()
    else:
        continue
