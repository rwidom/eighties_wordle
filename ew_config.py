import platform
import os
import json

class ew_platform():
    """ manages background settings for text display """

    def __init__(self):
        (self.IS_IPHONE, self.python_version, self.start_dir) = self.get_platform()
        self.clear = lambda: os.system('clear')
        if self.IS_IPHONE == True:
            import console
            self.clear = console.clear
            self.iphone_set_color = console.set_color
            console.set_font('courier')
        
    def get_platform(self):
        if 'iPhone' in platform.platform():
            IS_IPHONE = True
        elif 'mac' in platform.platform():
            IS_IPHONE = False
        python_version = platform.python_version()
        start_dir = os.getcwd().split('/')[-1]
        return (IS_IPHONE, python_version, start_dir)

    def is_correct_directory(self):
        if self.start_dir == 'eighties_wordle':
            return True
        else:
            try:
                os.chdir('eighties_wordle')
                return(True)
            except:
                print("Uh-oh, I can't find the eighties_wordle directory.")
                return(False)

class letter_display():
    """ 
    Prints a string with spacing at either end based on one of four statuses:
        OK   -- green background / black text, intended for the character is in the answer in the same location
        MOVE -- yellow background / black text, intended for the character is in the answer, but not in the right place
        NO   -- black background / grey bold text, intended for when we know the character is not in the answer word
        ?    -- default appearance (dark grey background / white text), intended for when the character has not been guessed yet, so we don't know
    """
    def __init__(self, letter=" ", status="?"):
        """ initialize a letter_display with a single letter and status. defaults to a space and unknown status """ 
        self.set_status(status)
        self.set_letter(letter)
        self.p = ew_platform()

    def set_status(self, status):
        """ choose one of four possible statuses for this letter: OK, MOVE, NO, or ? """
        assert status in ['OK', 'MOVE', 'NO', '?']
        self.status = status

    def set_letter(self, letter):
        """ set a single character to be displayed """
        assert type(letter) == str
        self.letter = letter

    def get_letter(self):
        return self.letter

    def get_status(self):
        return self.status

    def get_colors(self):
        """
        This just returns a constant dict with the color codes we'll use for different letter statuses
        """
        if self.p.IS_IPHONE == False: ## running on a laptop
            # ANSI color codes described here https://en.wikipedia.org/wiki/ANSI_escape_code
            # python code reference from https://stackoverflow.com/questions/287871/how-to-print-colored-text-to-the-terminal
            colors = {
                # the right letter in the right position -- green background, black text
                'OK': '\033[42m\033[30m',
                # a letter in the word, but not in the right position -- yellow background, black text
                'MOVE': '\033[43m\033[30m',
                # a letter not in the word -- black background, grey bold text
                'NO': '\033[40m\033[90m\033[1m',
                # at the end of a letter to reset the color, or if the letter status is unknown
                'END': '\033[0m',
                '?': '\033[0m'
                }
        elif self.p.IS_IPHONE == True:
            # http://omz-software.com/pythonista/docs/ios/console.html
            # here, we're returning the (r, g, b) tuple to set the consol color the way we want
            colors = {
                # the right letter in the right position -- green 
                'OK': [0.0, 1.0, 0.0],
                # a letter in the word, but not in the right position -- yellow 
                'MOVE': [1.0, 1.0, 0.0],
                # a letter not in the word -- grey
                'NO': [0.5, 0.5, 0.5],
                # at the end of a letter to reset the color, or if the letter status is unknown
                'END': [1.0, 1.0, 1.0],
                '?': [1.0, 1.0, 1.0]
            }      
        return(colors)

    def get_color(self):
        return self.get_colors()[self.get_status()]

    def __str__(self):
        """ 
        On the mac, where ansi colors work, this works really nicely: 
            Put one space on either side of the character and ansi colors for the status on either side of that
        On the iphone in pythonista:
            You lose the color and just get space + letter + space
        """
        if self.p.IS_IPHONE == False:
            return self.get_color() + ' ' + self.get_letter() + ' ' + self.get_colors()['END']
        elif self.p.IS_IPHONE == True:
            return self.get_letter() + ' '

    def __add__(self, other):
        """ concatenate letters with space in between by adding them in the same way that you can with strings """
        return str(self) + ' ' + str(other) + ' '

    def display(self):
        """ prints the string version of the letter with status coloring, without any new line at the end """
        if self.p.IS_IPHONE == False:
            ## mac lap top can handle the unicode string
            print(self, end='')
        elif self.p.IS_IPHONE == True:
            ## iphone uses a list [r, g, b]
            ## I can't use ** because set_color won't take named parameters :(
            c = self.get_color()
            self.p.iphone_set_color(c[0], c[1], c[2])
            print(self, end='')
            self.p.iphone_set_color()
class ew_configuration(ew_platform):

    def __init__(self, filename='ew_options.json'):
        ## initialize the platform (parent) class
        super(ew_configuration, self).__init__()
        ## get basic info
        self.filename = filename
        ## check and change directory
        assert self.is_correct_directory()
        ## load options dict
        self.settings = self.load_settings()
        self.max_desc_length = max( [ len(i["desc"]) for i in self.settings.values() ] )
        self.column1 = self.settings['game_type']['options'][0]
        self.column2 = self.settings['game_type']['options'][1]

    def get_game_type(self):
        return self.settings['game_type']['value']

    def get_value(self, s):
        assert type(s) == str
        assert s in self.settings
        return self.settings[s]['value']

    def load_settings(self):
        """ reads basic game settings from the json file """
        try:
            with open(self.filename) as f:
                return dict(json.load(f))
        except:
            print("Uh-oh, I'm not able to access your settings file.")

    def column_padding(self, setting_string = None):
        """ 
        Given a game type or setting value, returns the right number of spaces to right 
        justify settings displayed in columns 
        """
        if setting_string == None:
            ## this works as a default before we have settings values or if we don't have
            ## a value, because there is one setting that only applies to equations and 
            ## we have equations in column 2 on the right
            return ' ' * (self.max_desc_length - 3)
        else:
            ## the minus 2 is for padding that happens as part of letter display
            return ' ' * (self.max_desc_length - len(str(setting_string)) - 2)

    def get_settings_display_table(self):
        """
        Returns a list rows (dicts) each containing row title (options desc), words value 
        (if applicable, with letter display object colored with OK if words is the game type, 
        NO if not), equations value (same logic), row number, and padding strings for display. 
        The first row is game type.

        Assumes that there are two possible settings, though it's built for flexibility on the 
        names (e.g. if we want to change capitalization or order of the columns). Also assumes that all 
        settings we want to display (except for game type) will have one or the other game types 
        in their names.
        """
        column1_selected = (self.settings['game_type']['value'] == self.column1)
        rows = { "Game Type": 
            {
                'row_number': 0,
                'column1_pad': self.column_padding(self.column1),
                self.column1: letter_display(self.column1, ('OK'*column1_selected + '?'*(1 - column1_selected))),
                'column2_pad': self.column_padding(self.column2),
                self.column2: letter_display(self.column2, ('?'*column1_selected + 'OK'*(1 - column1_selected)))
            } 
        }
        for (s, info) in self.settings.items():
            ## add the row to start
            if info['desc'] not in rows and (self.column1 in s or self.column2 in s):
                row_number = len(rows)
                rows[info['desc']] = {
                    'row_number': row_number,
                    'column1_pad': self.column_padding(),
                    self.column1: letter_display(), 
                    'column2_pad': self.column_padding(),
                    self.column2: letter_display()
                    }
            ## then add the values as they come up
            if self.column1 in s:
                status = ('OK'*column1_selected + '?'*(1 - column1_selected))
                rows[info['desc']][self.column1] = letter_display(str(info['value']), status)
                rows[info['desc']]['column1_pad'] = self.column_padding(info['value'])
            elif self.column2 in s:
                status = ('?'*column1_selected + 'OK'*(1 - column1_selected))
                rows[info['desc']][self.column2] = letter_display(str(info['value']), status)
                rows[info['desc']]['column2_pad'] = self.column_padding(info['value'])
        list_of_dicts = [dict({'row_title': row_name}, **row_contents) \
            for (row_name, row_contents) in rows.items()]
        return list_of_dicts

    def __str__(self):
        """ 
        Creates a string version of the settings display, including ANSI colors for mac and 
        no coloring for IPHONE 
        """
        row_strings = [
                row['row_title'].rjust(self.max_desc_length) + \
                row['column1_pad'] + str(row[self.column1]) + \
                row['column2_pad'] + str(row[self.column2])
            for row in self.get_settings_display_table() ]
        return('\n'.join(row_strings))

    def display_settings(self):
        table_width = self.max_desc_length * 3
        self.clear()
        print("-" * table_width)
        print("Eighties Wordle!".center(table_width),"\n")
        if self.IS_IPHONE == False:
            print(self)
        elif self.IS_IPHONE == True:
            for row in self.get_settings_display_table():
                print(row['row_title'].rjust(self.max_desc_length), end='')
                print(row['column1_pad'], end='')
                row[self.column1].display()
                print(row['column2_pad'], end='')
                row[self.column2].display()
                print('')
        print("-" * table_width)

    def check_settings(self):
        while True:
            self.display_settings()
            confirm = input("Is this the game you'd like to play? (Y / N) ")
            if confirm.lower() in ('yes','y','you betcha'):
                break
            game_type = input(self.settings['game_type']['question']+' ').lower()
            if game_type in self.settings['game_type']['options']:
                self.settings['game_type']["value"] = game_type
                for (setting, i) in self.settings.items():
                    if (game_type in setting):
                        new_value = input(i['question']+' ')
                        try:
                            self.settings[setting]["value"] = int(new_value)
                        except:
                            print("OK, let's stay with", self.settings[setting]["value"])
                            new_value = None
                            continue
                    ## TO DO: stop hard coding this
                    if self.settings['word_length_words']['value']<2 or self.settings['word_length_words']['value']>15:
                        print("Sorry, I only have words between 2 and 15 letters long. Let's go with 5.")
                        self.settings['word_length_words']['value'] = 5
            else:
                print("Sorry, I don't know that game.")
        with open(self.filename, 'w') as f:
            f.write(json.dumps(self.settings, indent=4)) 
        print("Great!")

if __name__ == '__main__':
    s = ew_configuration()
    s.check_settings()
