# Eighties Wordle ReadME

## What is this?
I like to play [wordle](https://www.nytimes.com/games/wordle/index.html), and so I'm using it as an opportunity to make my own version. I'm playing with features from other games, and an idea from a kid I know whose teacher has the class play wordle with math. This is really just an exercise for me to learn and have fun.
## Where / how can I run it?
I've tested it on a mac (running MacOS Big Sur 11.6), and on an iPhone via [pythonista](http://omz-software.com/pythonista/).

I've used starting python in a directory called "eighties_wordle" as a standin for having all of the files needed for this program:
- eighties_wordle.py
- ew_answer.py
- ew_display.py
- ew_guesses.py
- ew_config.py 
- ew_options.json
- twl06.txt

That's not the most user-friendly pythonic approach, but MVP and all that. :)

## What is a word?

Here are the things I'm trying to make reserver characters in this game: '*' (for users to ask for hints) and '_' (for the program to indicate unknown characters when collecting hints). And I guess I'm assuming that there won't be any games with more than 99 turns or any valid "words" with fewer than 3 characters, because if you want to ask for a hint for a specific turn, you can still do that even in the equations version of the game. 

Huge thanks to WordGameDictionary.com for the [TWL06 Scrabble Word List](https://www.wordgamedictionary.com/twl06/download/twl06.txt).
## Why Eighties?
I'm calling it Eighties Wordle, because it's all text based, and because working on it has reminded me of when I was a kid in the eighties and I first started to learn computer programming.
