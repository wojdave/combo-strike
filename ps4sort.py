from ps4a import SCRABBLE_LETTER_VALUES, HAND_SIZE, loadWords, getWordScore
from ps4b import compChooseWord

def point_alpha(): # function unused
    point_alpha = {v: k for k, v in SCRABBLE_LETTER_VALUES.items()} # create dictionary skeleton

    for k in point_alpha.keys():
        point_alpha[k] = ''                         # clear dictionary for repopulation

    for k in SCRABBLE_LETTER_VALUES.keys():
        p = SCRABBLE_LETTER_VALUES[k]               # get point value of letter for new point_alpha[key]
        point_alpha[p] = point_alpha.get(p,0) + k   # repopulate dictionary as {points : 'letters'}

    return point_alpha                              # returns {points : 'letters'}
    
def word_list_by_hand(hand, wordList, n, *flag):    # polymorphism to flag combo strikes
    
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

    if flag == (1,):                # flag for combination. 
        comboWordList=[]
        combo_dict = {}
        for a in wordList:          # cross matrix of all words.
            for b in wordList:
                if (len(a + b) <= n): 
                    if canHandConstruct(a + b, hand):   # can combo be made?
                        comboWordList.append(a + b)     # build combo dictionary [overwrite duplicates]
                        combo_dict[getWordScore(a, n) + getWordScore(b, n)] = [a, b] # combo_dict = {score:[a,b]} 
        
        if len(combo_dict) >= 1:
            print "%s Viable Combinations from Word List:" % len(combo_dict),
            print combo_dict
            print ""    
        return combo_dict
        
    handWordList =[]                # create word list based on hand only.
    for word in wordList:
        if (len(word) <= n):        # eliminate all words larger than hand ***optimization***
            if canHandConstruct(word, hand):
                handWordList.append(word)   # compile custom word list
    if len(handWordList) >= 1:
        print "\n%s Words in Word List:" % len(handWordList),
        print handWordList
        print ""
    return handWordList

def word_or_combo(combo_dict, bestWord):    # use bestWord or combo strike
    x = getWordScore(bestWord, HAND_SIZE)
    sort_combo_dict = sorted(combo_dict, reverse=True)  # get highest combo score first
    for p in sort_combo_dict:
        if p > x:
            return combo_dict[p]
    return bestWord

# point_alpha = point_alpha()                                             # dict
# sort_alpha_by = sorted(point_alpha, key=point_alpha.get, reverse=True)  # list

def compChooseCombo(hand, wordList, HAND_SIZE):
    handWordList = word_list_by_hand(hand, wordList, HAND_SIZE)         # get all words possible in hand
    combo_dict = word_list_by_hand(hand, handWordList, HAND_SIZE, 1)    # get all combos, score and save

    try:    # best word or best combo
        word = word_or_combo(combo_dict, compChooseWord(hand,wordList,HAND_SIZE))
        print "try",
    except TypeError, e:
        return compChooseWord(hand,wordList,HAND_SIZE)
    if type(word) == type('str'):
        return word
    elif len(word[0])>len(word[-1]):
        return word[0]
    else:
        return word[-1]

