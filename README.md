# Eighties Wordle ReadME

## What is this?
I like to play [wordle](https://www.nytimes.com/games/wordle/index.html), and so I'm using it as an opportunity to make my own version. I'm playing with features from other games, and an idea from a kid I know whose teacher has the class play wordle with math. This is really just an exercise for me to learn and have fun.

Today, when I was faffing about with this, I also discovered [nerdle](https://nerdlegame.com/). Theirs is different from mine, in its approach to which equations to include as valid "words". They also don't give hints. The approach to hints that I use for the word version depends on a finite dictionary, and of course math is infinite. OK, and even limiting it to a range of integers, there are still way more possible combinations than words in the scrabble dictionary. Still noodling on different options there... Another I had considered in done by [mathler](https://www.mathler.com/), where they give you the answer to start, so your guesses don't include the equal sign. To be continued!

Having played [absurdle](https://qntm.org/absurdle) a little bit, I couldn't resist making my own non-deterministic version. Here, you don't make the first guess, the computer makes a random first guess for you. It's not terribly well-integrated with the config stuff at this point, but it's an MVP.

And some other variations that I will not be working on, but might play (with thanks to [Tom's guide](https://www.tomsguide.com/news/wordle-alternatives)):
- [worldle](https://worldle.teuteuf.fr/) geography shapes and vectors
- [chessle](https://jackli.gg/chessle/)
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
## Can I get a hint?
Yes. If you have at least one character in the right place, you can get a list of all of the words in the dictionary that also have that character or those characters in the same place. The list will include the right answer, and a bunch of wrong answers, some of which you should be able to rule out by taking into account your greyed out letters. 

I think it makes more sense for words than equations, but that's another to do.
## Why Eighties?
I'm calling it Eighties Wordle, because it's all text based, and because working on it has reminded me of when I was a kid in the eighties and I first started to learn computer programming.
