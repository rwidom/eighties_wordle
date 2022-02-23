# this little practice project is an homage to WORDLE
# find the real thing here: https://www.powerlanguage.co.uk/wordle/

from time import sleep
from ew_display import *
from ew_answer import *
from ew_guesses import *
from ew_config import clear

while True:
    clear()
    ## choose the type of game
    t = input("Do you want to play wordle with words or equations?")
    try:
        assert t in ('words','equations')
    except:
        t = 'equations'
        print("OK, let's try math since it's newer.")

    ## initialize the game dictionary and choose a word / equation
    if t == 'words':
        w = input("I'm going to pick a word for you to guess, how many letters should it have? Choose a number between 3 and 7:")
        try:
            assert int(w) >= 3 and int(w) <= 7
            d = all_the_words(word_length = int(w))
        except:
            print("OK, let's just go with 5 letters this time.")
            d = all_the_words(word_length = 5)
    elif t == 'equations':
        w = input("I'm going to pick an equation for you to guess, how many characters should it have? Choose a number between 5 and 9:")
        try:
            assert int(w) >= 5 and int(w) <= 9
            d = all_the_equations(word_length = int(w))
        except:
            print("OK, let's just go with 5 digits and 1 operator this time.")
            d = all_the_equations(word_length = 7)            

    ## initialize the object to handle of guesses and feedback
    c = input("And how many chances do you want to guess the right word? Choose a number between 3 and 20:")
    try:
        assert int(c) >= 3 and int(c) <= 20
        g = all_the_guesses(d, game_length = int(c), game_type = t)
    except:
        print("OK, let's just go with 6 guesses this time.")
        g = all_the_guesses(d, game_length = 6, game_type = t)
    sleep(2)
    print("If you'd like a hint, type * instead of a word as your regular turn. Don't worry, I won't count it.")

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
        clear()
    else:
        print("That's cool, I didn't want to either.")
        exit()
