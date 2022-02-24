import platform
import os
import json

## running environment basics, these are implemented as GLOBALs, and
## they are really important to the display working correctly, because
## pythonista on the iphone doesn't do ansi color displays the way that
## regular python on the mac does.
def ew_config():
    global IS_IPHONE
    environment = {}
    if 'iPhone' in platform.platform():
        environment['machine'] = 'iPhone'
        IS_IPHONE = True
        from console import set_font
        set_font('courier')
    elif 'mac' in platform.platform():
        environment['machine'] = 'Mac'
        IS_IPHONE = False
    else:
        environment['machine'] = 'unkown'
    environment['python_version'] = platform.python_version()
    environment['start_path'] = os.getcwd()
    environment['start_dir'] = environment['start_path'].split('/')[-1]
    ## this matters for file access, b/c I don't want to deal with path vars
    assert environment['start_dir'] == 'eighties_wordle' 
    ## this matters for display colors
    assert environment['machine'] != 'unknown' 
    return (IS_IPHONE, environment)

def clear():
    """ clears the terminal screen for MacOS (phone and computer) """
    (IS_IPHONE, environment) = ew_config()
    if IS_IPHONE == True:
        import console
        console.clear()
    elif IS_IPHONE == False:
        os.system('clear')
    else:
        print("Uh-oh, this isn't a supported platform.")

def load_settings(filename='ew_options.json'):
    """ reads basic game settings from the json file """
    with open(filename) as f:
        return dict(json.load(f))

def display_settings(filename='ew_options.json', settings_dict=dict()):
    if settings_dict==dict():
        s = load_settings(filename)
    elif type(settings_dict) == dict:
        s = settings_dict
    assert set(s.keys()) == set(['game_type', 'word_length_equations', 'game_length_equations', 'word_length_words', 'game_length_words'])
    max_desc_length = max( [ len(i["desc"]) for i in s.values() ] )
    clear()
    print("-" * max_desc_length * 2)
    print("Eighties Wordle!".center(max_desc_length * 2),"\n")
    for (setting, i) in s.items():
        print(i['desc'].rjust(max_desc_length), ":", i['value'])
    print("-" * max_desc_length * 2)
    return s.copy()

def check_settings(filename='ew_options.json'):
    s = display_settings()
    while 1==1:
        s = display_settings(settings_dict = s)
        confirm = input("Is this the game you'd like to play? (Y / N) ")
        if confirm.upper() in ('Y', 'YES', 'YOU BETCHA'):
            print("Great!")
            break
        else:
            for (setting, i) in s.items():
                new_value = None
                print('\n' + i['desc'] + ", options:", ', '.join([str(o) for o in i['options']]))
                while new_value not in i["options"]:
                    new_value = input(i['question']+' ')
                    if new_value == '':
                        new_value = i["value"]
                    elif type(i['options'][0])==int:
                        try:
                            new_value = int(new_value)
                        except:
                            continue
                s[setting]["value"] = new_value
            with open(filename, 'w') as f:
                f.write(json.dumps(s, indent=4)) 
    return s

if __name__ == '__main__':
    check_settings()
