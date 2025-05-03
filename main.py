import re
import random

def fix_word(word : str):
    return re.sub("_"," ",word)

def random_from_array(array:list):
    return array[random.randint(0,len(array)-1)]

words = []
with open("words.txt","r") as file:
    for word in file.readlines():
        words.append(word.replace("\n",""))

new_words = []
for i in range(random.randint(2,10)):
    new_words.append(random_from_array(words).upper())
new_words = " ".join(new_words)

sentence = re.sub("{w}",new_words,"SHUT YO {w} AHH")

print(sentence)

