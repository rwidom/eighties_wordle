import re
import subprocess
## requests does not come standard but is how we ping the dictionary api
try:
    import requests
except ImportError:
    print("Trying to Install required module: requests...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", 'requests'])
finally:
    import requests

def get_first_definition(word):
    """ ping dictionary api for an oversimplified definition of a word """
    ## get the api key for https://dictionaryapi.com/ which is run by Merriam-Webster
    with open('dictionary_api.txt') as f:
        API_KEY = f.read()
    ## call the API
    api_call = requests.get('https://dictionaryapi.com/api/v3/references/collegiate/json/'+word+'?key='+API_KEY).json()[0]
    ## parse the results
    if type(api_call) == str:
        return api_call
    elif 'def' not in api_call:
        return '??? no definition available ???'
    else:
        # take the first definition / element on the array called 'def'.
        # verbs generally have two definitions: one for transitive and one for intransitive
        step1 = api_call['def'][0]
        # each definition has a sense sequence, which is a list
        if 'sseq' not in step1:
            return '??? definition has no senses of the meaning ???'
        else:
            # we take the first sense, which is itself a list, which can represent a complex tree
            step2 = step1['sseq'][0]
            # simple case, a single sense, with a dict containing the definition text
            if step2[0] == 'sense' and 'dt' in step2[1]:
                pass
            else:
                # navigate nesting collections within senses (loop down the tree)
                max_iter = 10
                while isinstance(step2, list) and step2[0] != 'sense' and max_iter > 0:
                    # bypass branches that won't contain definition text
                    next_first = next(x for x in step2 if x[0] in ['pseq','sense'])
                    # if it's another list of senses take the first one
                    if next_first[0] == 'pseq': 
                        step2 = next_first[1]
                    # if it's a simple sense, go with that, we're done
                    elif next_first[0] == 'sense':
                        step2 = next_first
                    max_iter -= 1
            ## then the definition text within that simple case sense
            step3 = step2[1]
            if 'dt' in step3:  # definition text, also a list of lists
                definition = ' '.join([i[1] for i in step3['dt'] if i[0]=='text'])
                if 'dx' in definition:
                    definition = re.sub(r"(\{dx).*(\/dx\})", "", definition)
                definition = definition \
                    .replace('{a_link|','') \
                    .replace('{d_link|','') \
                    .replace('{bc}','') \
                    .replace('{sx|','') \
                    .replace('||}','') \
                    .replace('{it}','') \
                    .replace('{/it}','') \
                    .replace('}','')
                return definition
            else:
                return '??? definition for the first sense of the meaning has no text ???'

if __name__ == '__main__':
    import random
    from ew_answer import all_the_words
    game_dictionary = all_the_words()
    ## assume that the game dictionary only has real words that at least have aliases in dictionary.com
    sample_words = ['BLUMED', 'LIERS', 'SERVED', 'POINTS', 'GROSZ', 'SHIRTS', 'TRISTE', 'ARISTA', 'GATES',
         'BIDDER', 'QUARE'] \
        + random.sample(game_dictionary.get_words(), 10)
    for w in sample_words:
        print("#"*80)
        print('----->', w)
        print(get_first_definition(w))