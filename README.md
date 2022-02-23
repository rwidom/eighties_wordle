# Eighties Wordle ReadME

## What is this?
I like to play wordle, and so I'm using it as an opportunity to make my own version. I'm stealing features from other games, and this is really just an exercise for me to learn and have fun.

## Where / how can I run it?
I've tested it on a mac (running MacOS Big Sur 11.6), and on an iPhone via pythonista.

I've used starting python in a directory called "eighties-wordle" as a standin for having all of the files needed for this program:
- ew_answer.py
- ew_config.py (just figures out whether to print things for an iphone or a mac)
- ew_display.py
- ew_guesses.py
- wordlist.txt

That's not the most user-friendly pythonic approach, but MVP and all that. :)

## What is a word?

I'm working on adding a math version, because my 9-year-old friend/G-ddaughter/neice-in-spirit person told me that her teacher had them play wordle with math / equations and that seemed fun to both her and me. But it does raise questions in the program about what counts as a valid character for a guess, and this would come up if anyone wanted to adapt this for a language other than English anyway. So here are the things I'm trying to make reserver characters in this game: '*' (for users to ask for hints) and '_' (for the program to indicate unknown characters when collecting hints). And I guess I'm assuming that there won't be any games with more than 99 turns or any valid "words" with fewer than 3 characters, because if you want to ask for a hint for a specific turn, you can still do that even in the equations version of the game.
## Why Eighties?
I'm calling it Eighties Wordle, because it's all text based.