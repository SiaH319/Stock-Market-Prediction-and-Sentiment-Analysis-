'''
Sia Ham, 1730812
Rhina Kim,1731848
R. Vincent, instructor
420-LCW-MS 
Programming Techniques and Applications
Final Project
'''


from nltk.corpus import wordnet
import re


def unicode_decode(text):
    RE_EMOJI = re.compile('[\U00010000-\U0010ffff]', flags=re.UNICODE)
    text = RE_EMOJI.sub(r'', text)
    return text

# Only extract Alphabets from contents
def clean(word):
    return ''.join(letter for letter in word.lower() if 'a' <= letter <= 'z')


# Check if word is english word or not
def spelling(words):
    for word in words:
        if not word:
            continue
        elif not wordnet.synsets(word): #Not an English Word
            continue
        else: #English Word
            words = [str(word) for word in words if wordnet.synsets(word)]
    return words


### Process of filtering out strings other than alphabets, and checking if english word or not ###
def separate(text):
    words = [word for word in map(clean, text.split())] # so filter out empty strings and get the final list of clean words
    words = spelling(words)
    words = " ".join(str(item) for item in words)
    return words




### SAMPLE TEST HERE ###
if __name__ == "__main__":
    text = '''
    こんにちは。私は　誰でしょう
    @I_am_not_whoIam
    @Ford
    @NiceHero
    @cherrypiedelicious
    #Ford #OneOkRock #concert I wanna go
    #resultsWhat is life, where is laughter? "Hahaha"
    What's my name
    #ohilovemuscle
    fanclub #fordinstagram #FordInstagram
    Keep Support Our Page : (@musclemanmanman )✅✔
    and (secret...) .
    loveyou love love like unlike un like muchlove much love much_love
    FOLLOW FOR MORE UPDATE'S:✅✔ .
    #3x3x3
    Follow Us ✅ Complete detail below link
    '''

    def sample():
        print(clean(text))
        print("==========↓==========")
        words = separate(text)
        print(separate(text))
        
    sample()




# https://codereview.stackexchange.com/questions/191279/filter-out-non-alphabetic-characters-from-a-list-of-words
# https://stackoverflow.com/questions/3788870/how-to-check-if-a-word-is-an-english-word-with-python
