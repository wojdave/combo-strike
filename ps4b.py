#!/usr/bin/python

from ps4a import *
from ps4sort import *
import time
import os
from dictionary import define

#
# Problem #6: Computer chooses a word
#
#
def compChooseWord(hand, wordList, n):
    """
    Given a hand and a wordList, find the word that gives 
    the maximum value score, and return it.

    This word should be calculated by considering all the words
    in the wordList.

    If no words in the wordList can be made from the hand, return None.

    hand: dictionary (string -> int)
    wordList: list (string)
    n: integer (HAND_SIZE; i.e., hand size required for additional points)

    returns: string or None
    """
    def canHandConstruct(word,hand):
        h = hand.copy()
        try:                        # try: are letters in hand? No, except.
            for i in word:
                h[i] -= 1           # remove letters used in word
                if h[i] < 0:        # test if using more letters than held 
                    return False
            return True
        except KeyError, e:         # letter not in hand. exception thrown.
            return False

    def bestWord(hand, wordList, n) :
        score = 0
        bestWord = None
        for word in wordList:
            if (len(word) <= n):        # eliminate all words larger than hand ***optimization***
                if canHandConstruct(word, hand):
                    wordScore = getWordScore(word,n)
                    if score < wordScore:            
                        score = wordScore
                        bestWord = word            
        return bestWord

    return bestWord(hand, wordList, n)

#
# Problem #7: Computer plays a hand
#
def compPlayHand(hand, wordList, n):
    """
    Allows the computer to play the given hand, following the same procedure
    as playHand, except instead of the user choosing a word, the computer 
    chooses it.

    1) The hand is displayed.
    2) The computer chooses a word.
    3) After every valid word: the word and the score for that word is 
    displayed, the remaining letters in the hand are displayed, and the 
    computer chooses another word.
    4)  The sum of the word scores is displayed when the hand finishes.
    5)  The hand finishes when the computer has exhausted its possible
    choices (i.e. compChooseWord returns None).
 
    hand: dictionary (string -> int)
    wordList: list (string)
    n: integer (HAND_SIZE; i.e., hand size required for additional points)
    """

    score = 0
    while calculateHandlen(hand):
        print "\nCurrent Hand:",
        displayHand(hand)
        word = compChooseCombo(hand, wordList, n) # Hard Mode
        #word = compChooseWord(hand, wordList, n) # Easy Mode
        if word == None:
            break
        if not isValidWord(word, hand, wordList):
            print "Invalid word, please try again.\n"
        else:
            score += getWordScore(word,n)
            print '\"%s\" earned %s points. Total: %s points.' % (word, str(getWordScore(word, n)), str(score))
            hand = updateHand(hand, word)
            #print "%s" % define(word)
    print "Total score: %s points.\n" % str(score)
    
#
# Problem #8: Playing a game
#
#
def playGame(wordList):
    """
    Allow the user to play an arbitrary number of hands.
 
    1) Asks the user to input 'n' or 'r' or 'e'.
        * If the user inputs 'e', immediately exit the game.
        * If the user inputs anything that's not 'n', 'r', or 'e', keep asking them again.

    2) Asks the user to input a 'u' or a 'c'.
        * If the user inputs anything that's not 'c' or 'u', keep asking them again.

    3) Switch functionality based on the above choices:
        * If the user inputted 'n', play a new (random) hand.
        * Else, if the user inputted 'r', play the last hand again.
      
        * If the user inputted 'u', let the user play the game
          with the selected hand, using playHand.
        * If the user inputted 'c', let the computer play the 
          game with the selected hand, using compPlayHand.

    4) After the computer or user has played the hand, repeat from step 1

    wordList: list (string)
    """
    # two helper functions     
    def uorc(*hand): # polymorphism - do not need to supply argument
        ui = raw_input("Enter u to have yourself play, c to have the computer play: ")
        return ui
    
    def play(ui): # plays player based on user input
        if ui == 'u':
            print
            playHand(hand, wordList, HAND_SIZE)
        elif ui == 'c':
            compPlayHand(hand, wordList, HAND_SIZE)
        else:
            print("Invalid command.\n")
            play(uorc())

    ui = '' # start here
    while ui != 'e':
        ui = raw_input("Enter n to deal a new hand, r to replay the last hand, d for dictionary, or e to end game: ")
        if ui == 'n':
            hand = dealHand(HAND_SIZE)
            #hand = {'e':1, 'g':1, 'i':1, 'l':1, 'v':1, 'x':1, 'z':1}
            #hand = {'a':1 ,'c':1, 'b':1, 'g':1, 'm':1, 'p':1, 'u':1}

            play(uorc()) # ask for player and play(player)
        elif ui == 'r':
            try: # no hand if user's first game 
                play(uorc(hand)) # makes use of polymorphism to throw exception
            except NameError, e:
                print("You have not played a hand yet. Please play a new hand first!\n")
        elif ui == 'e':
            break
        # dictionary module
        elif ui[0] == 'd':
            ui = raw_input("\nWhat word do you want to define? "),
            print "\n" + define(str(ui))
            print ""
        else:
            print("Invalid command.\n")

#
# Build data structures used for entire session and play game
#
if __name__ == '__main__':
    wordList = loadWords()
    playGame(wordList)

