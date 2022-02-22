import platform
import os

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


