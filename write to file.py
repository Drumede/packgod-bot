from nltk.corpus import wordnet as wn
import re

def fix_word(word : str):
    return re.sub("_"," ",word)

words = []
for synset in list(wn.all_synsets(wn.NOUN)):
    for word in synset.lemma_names():
        words.append(fix_word(word))
for synset in list(wn.all_synsets(wn.ADJ)):
    for word in synset.lemma_names():
        words.append(fix_word(word))
for synset in list(wn.all_synsets(wn.VERB)):
    for word in synset.lemma_names():
        words.append(fix_word(word))

with open("words.txt","w") as file:
    file.write("\n".join(words))