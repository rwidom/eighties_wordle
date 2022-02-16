# Eighties Wordle ReadME

## Eighties Wordle?
I'm calling it Eighties Wordle, because it's all text based.

## Design
Currently there are three objects, but they have multiple jobs and I don't think they are super well designed. So I'm going to try and think more carefully about that here.

Now:
- all_the_guesses (main game dynamic)
- all_the_words (holding the dictionary and ways to evaluate guesses)
- guess_display (this is really set up to display a single guess, with color coded results based on accuracy)

The problem is that the keyboard needs to reflect all guesses, and the color scheme is only in guess display. It's ironic, because I saw related color scheme code in it's own object type, and I thought "that's weird, why not put it with other stuff?"  Aaaaaaand now I know.

Next:
- letter printer -- which will have the colors and statuses
- guess_display -- which will use letter printer, but otherwise be the same as now, printing one word at a time
- keyboard display -- which will also use letter printer, but will print a keyboard with a hierarchy of guess outcomes

TO DO:
- Right now, the keyboard display takes a list of guesses and converts it to a dict, but I don't know if that's best. Better to have it as part of the guesses / game play?