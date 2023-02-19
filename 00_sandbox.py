import random


def scramble_sentence(sentence):
    words = sentence.split()  # split the sentence into a list of words
    result = []
    for word in words:
        letters = list(word)  # convert the word into a list of letters
        random.shuffle(letters)  # shuffle the letters randomly
        scrambled_word = ''.join(letters)  # join the letters back into a string
        result.append(scrambled_word)
    return ' '.join(result)  # join the scrambled words back into a sentence


while 1==1:
    new_sentence = input("Say anything! ")

    scramble = scramble_sentence(new_sentence)
    print(scramble)
