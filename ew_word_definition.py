import requests

def get_first_definition(word):
    """ ping dictionary api for the definition of a word """
    ## get the api key for https://dictionaryapi.com/ which is run by Merriam-Webster
    with open('dictionary_api.txt') as f:
        API_KEY = f.read()
    ## call the API
    api_call = requests.get('https://dictionaryapi.com/api/v3/references/collegiate/json/'+word+'?key='+API_KEY).json()[0]
    if type(api_call) == str:
        return api_call
    elif 'def' in api_call:
        step1 = api_call['def'][0] # first definition collection
        if 'sseq' in step1:
            step2 = step1['sseq'][0] # first item in sense sequence array
            ## then first sense or subsense
            if type(step2) == list and step2[0] == 'sense':
                step3 = step2[1] # dict containing sense data
            elif type(step2[0]) == list and step2[0][0] == 'sense':
                step3 = step2[0][1] # dict containing subsense data
            elif type(step2[0]) == list and step2[0][0] == 'pseq':
                step3 = step2[0][1][1][1] # dict containing sense data in the context of a parenthesized seq of senses
            elif type(step2[0]) == list and step2[0][0] == 'bs':
                step3 = step2[0][1]['sense'] # dict within a sense within a binding substitute
            else:
                return '-----> step2\n'+str(step2)
            ## then the definition text within that first sense
            if 'dt' in step3:  # definition text, also a list of lists
                definition = '\n'.join([str(i[1]) for i in step3['dt'] if i[0]=='text']) \
                    .replace('{bc}','') \
                    .replace('{sx','') \
                    .replace('{a_link','') \
                    .replace('{d_link','') \
                    .replace('{it}','') \
                    .replace('{/it}','') \
                    .replace('|','') \
                    .replace('}','')
                return definition
            else:
                return '-----> step3\n'+str(step3)
        else:
            return '-----> step1\n'+str(step1)
    else:
        return '-----> api_call\n'+api_call

if __name__ == '__main__':
    import random
    from ew_answer import all_the_words
    game_dictionary = all_the_words()
    sample_words = ['BLUMED', 'REAVED', 'SERVED', 'POINTS', 'SQUIRT', 'SHIRTS', 'TRISTE', 'ARISTA', 'GATES'] \
        + random.sample(game_dictionary.get_words(), 10)
    for w in sample_words:
        print("#"*80)
        print('----->', w)
        print(get_first_definition(w))