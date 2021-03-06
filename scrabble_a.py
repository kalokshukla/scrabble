import random
import string

SCRABBLE_DICTIONARY = { 'a': 9, 'b': 2, 'c': 2, 'd': 4, 'e': 12, 'f': 2, 'g': 3, 'h': 2, 'i': 9, 'j': 1, 'k': 1, 'l': 4, 'm': 2, 'n': 6, 'o': 8, 'p': 2, 'q': 1, 'r': 6, 's': 4, 't': 6, 'u': 4, 'v': 2, 'w': 2, 'x': 1, 'y': 2, 'z': 1}

def dictionaryToString(dictionary):
    dictionaryScrabble = ''
    for letter in dictionary.keys():
        for j in range(dictionary[letter]):
             dictionaryScrabble += letter
    return dictionaryScrabble

SCRABBLE_LETTERS = dictionaryToString(SCRABBLE_DICTIONARY)
HAND_SIZE = 7

SCRABBLE_LETTER_VALUES = {
    'a': 1, 'b': 3, 'c': 3, 'd': 2, 'e': 1, 'f': 4, 'g': 2, 'h': 4, 'i': 1, 'j': 8, 'k': 5, 'l': 1, 'm': 3, 'n': 1, 'o': 1, 'p': 3, 'q': 10, 'r': 1, 's': 1, 't': 1, 'u': 1, 'v': 4, 'w': 4, 'x': 8, 'y': 4, 'z': 10
}

WORDLIST_FILENAME = "words.txt"

def loadWords():
    """
    Returns a list of valid words. Words are strings of lowercase letters.

    Depending on the size of the word list, this function may
    take a while to finish.
    """
    print "Loading word list from file..."
    inFile = open(WORDLIST_FILENAME, 'r', 0)
    wordList = []
    for line in inFile:
        wordList.append(line.strip().lower())
    print "  ", len(wordList), "words loaded."
    return wordList

def getFrequencyDict(sequence):
    """
    Returns a dictionary where the keys are elements of the sequence
    and the values are integer counts, for the number of times that
    an element is repeated in the sequence.

    sequence: string or list
    return: dictionary
    """
    freq = {}
    for x in sequence:
        freq[x] = freq.get(x,0) + 1
    return freq


def getWordScore(word, n):
    """
    Returns the score for a word. Assumes the word is a valid word.

    The score for a word is the sum of the points for letters in the
    word, multiplied by the length of the word, PLUS 50 points if all n
    letters are used on the first turn.

    Letters are scored as in Scrabble; A is worth 1, B is worth 3, C is
    worth 3, D is worth 2, E is worth 1, and so on (see SCRABBLE_LETTER_VALUES)

    word: string (lowercase letters)
    n: integer (HAND_SIZE; i.e., hand size required for additional points)
    returns: int >= 0
    """
    #return sum([SCRABBLE_LETTER_VALUES[w] for w in word]) + 50 if len(word) == n else 0
    score = sum([SCRABBLE_LETTER_VALUES[w] for w in word]) * len(word)
    if len(word) == n:
        return score + 50
    else:
        return score


def displayHand(hand):
    """
    Displays the letters currently in the hand.

    For example:
    >>> displayHand({'a':1, 'x':2, 'l':3, 'e':1})
    Should print out something like:
       a x x l l l e
    The order of the letters is unimportant.

    hand: dictionary (string -> int)
    """
    displayedHand = ''
    for letter in hand.keys():
        for j in range(hand[letter]):
            displayedHand += letter + ' '
    return displayedHand


def dictionaryToString(dictionary):
    dictionaryScrabble = ''
    for letter in dictionary.keys():
        for j in range(dictionary[letter]):
             dictionaryScrabble += letter
    return dictionaryScrabble

def dealHand(n):
    """
    Returns a random hand containing n lowercase letters.
    At least n/3 the letters in the hand should be VOWELS.

    Hands are represented as dictionaries. The keys are
    letters and the values are the number of times the
    particular letter is repeated in that hand.

    n: int >= 0
    returns: dictionary (string -> int)
    """
    hand={}

    for i in range(n):
        x = SCRABBLE_LETTERS[random.randrange(0,len(SCRABBLE_LETTERS))]
        hand[x] = hand.get(x, 0) + 1

    return hand


def updateHand(hand, word):
    """
    Assumes that 'hand' has all the letters in word.
    In other words, this assumes that however many times
    a letter appears in 'word', 'hand' has at least as
    many of that letter in it.

    Updates the hand: uses up the letters in the given word
    and returns the new hand, without those letters in it.

    Has no side effects: does not modify hand.

    word: string
    hand: dictionary (string -> int)
    returns: dictionary (string -> int)
    """
    hand_try = hand.copy()
    for w in word:
        hand_try[w] -= 1
    return hand_try

def isInHand(word, dictionary):
    wordDict = getFrequencyDict(word)
    number = 0
    for w in word:
      if dictionary.get(w, 0) >= wordDict[w]:
        number += 1
    return number == len(word)

def isInWordList(word, wordList):
    return word in wordList

def isValidWord(word, hand, wordList):
    """
    Returns True if word is in the wordList and is entirely
    composed of letters in the hand. Otherwise, returns False.

    Does not mutate hand or wordList.

    word: string
    hand: dictionary (string -> int)
    wordList: list of lowercase strings
    """
    return isInHand(word, hand) and isInWordList(word, wordList)

def calculateHandlen(hand):
    """
    Returns the length (number of letters) in the current hand.

    hand: dictionary (string-> int)
    returns: integer
    """
    letterLength = 0
    for i in hand:
        letterLength += hand[i]
    return letterLength



def playHand(hand, wordList, n):
    """
    Allows the user to play the given hand, as follows:

    * The hand is displayed.
    * The user may input a word or a single period (the string ".")
      to indicate they're done playing
    * Invalid words are rejected, and a message is displayed asking
      the user to choose another word until they enter a valid word or "."
    * When a valid word is entered, it uses up letters from the hand.
    * After every valid word: the score for that word is displayed,
      the remaining letters in the hand are displayed, and the user
      is asked to input another word.
    * The sum of the word scores is displayed when the hand finishes.
    * The hand finishes when there are no more unused letters or the user
      inputs a "."

      hand: dictionary (string -> int)
      wordList: list of lowercase strings
      n: integer (HAND_SIZE; i.e., hand size required for additional points)

    """
    def isHandEmpty(hand):
        return sum(hand.values()) == 0

    totalScore = 0
    handed = hand.copy()
    while True:
        if calculateHandlen(handed) == 0:
            print "Run out of letters. Total score: " + str(totalScore) + " points."
            break
        print "Current Hand:  " + displayHand(handed)

        askInput = raw_input('Enter word, or a "." to indicate that you are finished: ')

        if askInput == ".":

            print "Goodbye! Total score: " + str(totalScore) + " points."
            break

        else:

            if not isValidWord(askInput, hand, wordList):

                print "Invalid word, please try again.\n"

            else:

                scored = getWordScore(askInput, HAND_SIZE)
                totalScore += scored
                print '"'+ askInput + '" ' + "earned " + str(scored) + " points. Total: " + str(totalScore) + " points\n"

                handed = updateHand(handed, askInput)


def playGame(wordList):
    """
    Allow the user to play an arbitrary number of hands.

    1) Asks the user to input 'n' or 'r' or 'e'.
      * If the user inputs 'n', let the user play a new (random) hand.
      * If the user inputs 'r', let the user play the last hand again.
      * If the user inputs 'e', exit the game.
      * If the user inputs anything else, tell them their input was invalid.

    2) When done playing the hand, repeat from step 1
    """

    hand = False
    ans = ''
    while not ans == "e":
        ans = raw_input("Enter n to deal a new hand, r to replay the last hand, or e to end game: ")
        if ans == "n":
            hand = dealHand(HAND_SIZE)
            playHand(hand, wordList, HAND_SIZE)
        elif ans == "r":
            if hand:
                playHand(hand, wordList, HAND_SIZE)
            else:
                print "You have not played a hand yet. Please play a new hand first!"
        elif ans == "e":
            print "Goodbye :)"
        else:
            print "Invalid command."

if __name__ == '__main__':
    wordList = loadWords()
    playGame(wordList)
