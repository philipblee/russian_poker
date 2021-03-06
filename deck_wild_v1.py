# using Tkinter to display a hand of 13 random card images
# each time you click the canvas
# this program runs in python27 - directory is c:\python27
# program needs c:\python27\Cards_gif to get card images
# program also needs c:\python27\Probability1Wild.csv for winning probability

import time
from Tkinter import *
import sys
from random import shuffle
import csv

#getcontext().prec = 2
f = open ('card_list2.csv', 'w')
prob_file = False
prob_chart = [0,0,0]
prob_chart = 1200 * [prob_chart]
prob_array1 = [0,0,0]
prob_array1 = 600 * [prob_array1]
prob_array2 = [0,0,0]
prob_array2 = 600 * [prob_array2]
prob_array3 = [0,0,0]
prob_array3 = 600 * [prob_array3]

class Hand(list):
  pass

class Deck(object):
  suit = 1*'SHDC'
  rank = 'AKQJT98765432'
  
  def deal(self, n):
    deck = [s+r for s in Deck.suit for r in Deck.rank]
    deck.append("WX")
    for i in range(5):
        shuffle(deck)
    return [Hand(deck[i::n]) for i in xrange(n)]

  @staticmethod
  def cmpkey(card):
    return Deck.suit.index(card[0]), Deck.rank.index(card[1])

def best_13card_hand(card_list2):
    card_list = list(card_list2)
    card_list2_string = ""
    for i in card_list2:
        card_list2_string = card_list2_string + i+ ","
    #print card_list2_string
    suits = "SHDC"
    ranks = "0A23456789TJQKA"        
    suit_rank_array = analyze(card_list2)
    straightflushes = 0 
    flushes = suit_rank_array[4][15]     
    straights = suit_rank_array[5][15]       
    singles_list = suit_rank_array[10]
    pairs_list = suit_rank_array[11]
    trips_list = suit_rank_array[12]
    fourks_list = suit_rank_array[13]
    fiveks_list = suit_rank_array[14]
    singles = len (singles_list)
    pairs = len (pairs_list)
    trips = len (trips_list)
    fourks = len (fourks_list)
    fiveks = len (fiveks_list)     

    hand3 = [[],[],[],[],[],[],[],[],[],[],[],[],[],[],
             [],[],[],[],[],[],[],[],[],[],[],[],[]]

    hand2 = [[],[],[],[],[],[],[],[],[],[],[],[],[],[],
             [],[],[],[],[],[],[],[],[],[],[],[],[]]

    hand1 = [[],[],[],[],[],[],[],[],[],[],[],[],[],[],
             [],[],[],[],[],[],[],[],[],[],[],[],[]]
 
    invalid_hand = [False]
    invalid_hand = 25 * invalid_hand
    
    score_array = [[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                   [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                   [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                   [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                   [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                   [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]]
    
    cards_remaining = [[],[],[],[],[],[],[],[],[],[],[],[],[],[],
             [],[],[],[],[],[],[],[],[],[],[],[],[]]
    
    hand_num = 0
    for j in range(14,1,-1): #fivek
         if suit_rank_array[4][j] == 5:
             for card in card_list2:
                 if ranks[j] in card:
                     hand3[hand_num].append(card)
             score_array[3][hand_num] = score(hand3[hand_num],"3")
             #print "hand3", hand_num, hand3[hand_num],score_array[3][hand_num]
             hand_num = hand_num + 1
                                              
    for i in range (4):  #straight flush
        for j in range (1,11):
            if suit_rank_array[i+6][j] >= 1:              
                for k in range(5):
                    card = suits[i] + ranks[j+k]
                    hand3[hand_num].append(card)               
                score_array[3][hand_num] = score(hand3[hand_num],"3")
                #print "hand3", hand_num, hand3[hand_num], score_array[3][hand_num]
                hand_num = hand_num + 1

    for j in range(14,1,-1):    #fourk
        if suit_rank_array[4][j] == 4:
            for card in card_list2:
                if ranks[j] in card:
                    hand3[hand_num].append(card)           
            score_array[3][hand_num] = score(hand3[hand_num],"3")
            #print "hand3", hand_num, hand3[hand_num], score_array[3][hand_num]
            hand_num = hand_num + 1

    for j in range(14,1,-1):    #full house with trip and pair
        if suit_rank_array[4][j] == 3 and len(pairs_list) > 0:  #find trips
            for pair_card in pairs_list:
                for card in card_list2:
                    if ranks[j] in card or pair_card in card:
                        hand3[hand_num].append(card)
                score_array[3][hand_num] = score(hand3[hand_num],"3")
                #print "hand3", hand_num, hand3[hand_num], score_array[3][hand_num]
                hand_num = hand_num + 1

    
    for j in range(15,1,-1):    #full house with 2 or more trips only
        if suit_rank_array[4][j] == 3 and len(pairs_list) > 1:  #find trips
            pair_card = pairs_list[-1]
            for card in card_list2:
                if ranks[j] in card or pair_card in card:
                    hand3[hand_num].append(card)
            score_array[3][hand_num] = score(hand3[hand_num],"3")
            #print "hand3", hand_num, hand3[hand_num], score_array[3][hand_num]
            hand_num = hand_num + 1
                            
    for i in range(4):    #flush
        if suit_rank_array[i][15] >= 5:
            for card in card_list2:
                if suits[i] in card:
                    hand3[hand_num].append(card)
            #print "flush hand3 before", hand_num, hand3[hand_num]
            if len(hand3[hand_num]) >5:
                hand3[hand_num] = flush_overage(hand3[hand_num], card_list2)
            score_array[3][hand_num] = score(hand3[hand_num],"3")
            #print "hand3", hand_num, hand3[hand_num], score_array[3][hand_num]
            hand_num = hand_num + 1
            
    for j in range (11,0,-1):   #straight
        if suit_rank_array[5][j] >= 1:
            for k in range (5):
                n = 0
                for card in card_list2:
                    if ranks[j+k] in card and n == 0:
                        hand3[hand_num].append(card)
                        n = 1
            score_array[3][hand_num] = score(hand3[hand_num],"3")
            #print "hand3", hand_num, hand3[hand_num], score_array[3][hand_num]
            hand_num = hand_num + 1
            
    for j in range(15,2,-1):    #trips
        if suit_rank_array[4][j] == 3:
            for card in card_list2:
                if ranks[j] in card:
                    hand3[hand_num].append(card)
            score_array[3][hand_num] = score(hand3[hand_num],"3")
            #print "hand3", hand_num, hand3[hand_num], score_array[3][hand_num]
            hand_num = hand_num + 1
            
    if pairs == 6 and len(trips_list) == 0:  #create two pairs from 5 pairs
        for card in card_list2:
           if pairs_list[-2] in card:
               hand3[hand_num].append(card)
           if pairs_list[1] in card:
               hand3[hand_num].append(card)
        score_array[3][hand_num] = score(hand3[hand_num],"3")
        #print "hand3 5 pair", hand_num, hand3[hand_num], score_array[3][hand_num]
        hand_num = hand_num + 1    

    if pairs == 5 and len(trips_list) == 0:  #create two pairs from 5 pairs
        for card in card_list2:
           if pairs_list[-1] in card:
               hand3[hand_num].append(card)
           if pairs_list[1] in card:
               hand3[hand_num].append(card)
        score_array[3][hand_num] = score(hand3[hand_num],"3")
        #print "hand3 5 pair", hand_num, hand3[hand_num], score_array[3][hand_num]
        hand_num = hand_num + 1    

    if pairs == 4 and len(trips_list) == 0:  #create two pairs from 4 pairs
        for card in card_list2:
           if pairs_list[-1] in card:
               hand3[hand_num].append(card)
           if pairs_list[-2] in card:
               hand3[hand_num].append(card)
        score_array[3][hand_num] = score(hand3[hand_num],"3")
        #print "hand3 4 pair", hand_num, hand3[hand_num], score_array[3][hand_num]
        hand_num = hand_num + 1

    if (pairs == 3 or pairs == 2) and len(trips_list) == 0:   #create largest pair
        for card in card_list2:
            if pairs_list[0] in card:
                hand3[hand_num].append(card)
        score_array[3][hand_num] = score(hand3[hand_num],"3")
        #print "hand3", hand_num, hand3[hand_num], score_array[3][hand_num]
        hand_num = hand_num + 1
        
    for hand_x in hand3:
        hand_x = hand_x.sort(cmp = rank_sort, reverse = True)
    for i in range (len(hand3)):
        if hand3[i] != []:
            #print i, hand3[i]
            pass
    # Initialize cards_remaining to card_list
    # if card_ is in hand3[i] then remove card_x

    hand_num = 0
    #print "============ hand3, cards_remaining =========="
    card_z = []
    for hand_x in hand3:
        if len(hand_x) > 0:
            sorted (hand_x, cmp = rank_sort, reverse = True)
            #print "sorted hand_x", hand_x
            score_array[3][hand_num] = score(hand3[hand_num],"3")
            cards_remaining [hand_num] = list(card_list)
            for card_x in hand_x:
                for card_y in cards_remaining[hand_num]:                
                    if card_x == card_y:
                        cards_remaining[hand_num].remove(card_y)
            #print "hand3", hand3[hand_num], score_array[3][hand_num]
            #print "cards_remaining", cards_remaining [hand_num]

            # Now figure out best_hand of cards_remaining[hand_num]
            hand2[hand_num] = best_hand2(cards_remaining[hand_num], score_array[3][hand_num])
            score_array[2][hand_num] = score(hand2[hand_num],"2")
            #print "hand2", hand2[hand_num], score_array[2][hand_num]     
            for card_x in hand2[hand_num]:
                for card_y in cards_remaining[hand_num]:
                    if card_x == card_y:
                        cards_remaining[hand_num].remove(card_x)
                        #print "looping", card_x, cards_remaining[hand_num]
                        
            #print "Calling best_hand1", cards_remaining[hand_num]           
            hand1[hand_num] = best_hand1(cards_remaining[hand_num],score_array[2][hand_num])

            for card_x in hand1[hand_num]:
                for card_y in cards_remaining[hand_num]:
                    if card_x == card_y:
                        cards_remaining[hand_num].remove(card_x)
                        #print "looping", card_x, cards_remaining[hand_num]
            score_array[1][hand_num] = score(hand1[hand_num],"1")
            #print "hand1", hand1[hand_num], score_array[1][hand_num]
            
            #print "hand1 cards remaining", cards_remaining[hand_num]
            while (len(hand3[hand_num]) < 5 and len(cards_remaining[hand_num]) > 0):
               #print "filler3", cards_remaining[hand_num][0]
               card_z = cards_remaining[hand_num][-1]
               hand3[hand_num].append(card_z)
               cards_remaining[hand_num].remove(card_z)
            while (len(hand2[hand_num]) < 5 and len(cards_remaining[hand_num]) > 0):
               card_z = cards_remaining[hand_num][-1]
               hand2[hand_num].append(card_z)
               cards_remaining[hand_num].remove(card_z)
            while (len(hand1[hand_num]) < 3 and len(cards_remaining[hand_num]) > 0):
               card_z = cards_remaining[hand_num][-1]
               hand1[hand_num].append(card_z)
               cards_remaining[hand_num].remove(card_z)
               
            hand3[hand_num] = sorted(hand3[hand_num],cmp = rank_sort, reverse = True)
            hand2[hand_num] = sorted(hand2[hand_num],cmp = rank_sort, reverse = True)
            hand1[hand_num] = sorted(hand1[hand_num],cmp = rank_sort, reverse = True)
            
            #print hand_num, hand3[hand_num], score_array[3][hand_num]
            #print hand_num, hand2[hand_num], score_array[2][hand_num]
            #print hand_num, hand1[hand_num], score_array[1][hand_num],
            total_score = score_array[3][hand_num][1] + score_array[2][hand_num][1] + score_array[1][hand_num][1]
            #print total_score
            hand_num = hand_num + 1

    #print "Searching for Invalid Hands"
    for i in range(hand_num):
        score_array[3][i] = score_final(hand3[i],"3")
        score_array[2][i] = score_final(hand2[i],"2")
        score_array[1][i] = score_final(hand1[i],"1")

    for i in range (hand_num):
        valid_hand = True
        if score_array[1][i][0] > score_array[2][i][0]:
            valid_hand = False
        if score_array[2][i][0] > score_array[3][i][0]:
            valid_hand = False
        if valid_hand == False:
            invalid_hand[i] = True
            
    best_total_score = 0
    best_hand = 0
    for i in range(hand_num):
        total_score = score_array[3][i][1] + score_array[2][i][1] + score_array[1][i][1]
        #print "i, invalid_hand", i, invalid_hand[i]
        if total_score > best_total_score and invalid_hand[i] != True:
             best_total_score = total_score
             best_hand = i
        #print "hand", i, score_array[3][i], score_array[2][i], score_array[1][i], total_score, not(invalid_hand[i])
    #print "best hand", best_hand, score_array[3][best_hand], score_array[2][best_hand], score_array[1][best_hand], best_total_score
    best_hand_score = score_array[3][best_hand], score_array[2][best_hand], score_array[1][best_hand], best_total_score
    #print "best hand", best_hand, score_array[3][best_hand], score_array[2][best_hand], score_array[1][best_hand], best_total_score, not(invalid_hand[i])

    card_list_string = str(best_hand) + ", "
    for i in range (3,0,-1):
         for j in range (2):
             #print "i, j, score_array[i][best_hand]", i, j, score_array[i][best_hand]
             card_list_string += str(score_array[i][best_hand][j]) + ", "
    card_list_string += str(best_total_score) + "\n"
    #print card_list_string
        
    card_listx = hand3[best_hand] + hand2[best_hand] + hand1[best_hand]
    #print "best_hand", card_listx
    return [card_listx, best_hand_score]
  

def rank_sort(a,b):
    suit = "SHDC"
    rank = "23456789TJQKA"
    if rank.index(a[1]) > rank.index(b[1]):
        return 1
    return -1
  
def straightcount (rankcount):
    """ count straights - takes in rankcount(list of ranks), and returns straightct
        array with straights in straightct [1:10] - if 1, it's A2345, if 2 it's23456
        finally straightct [15] = total number of straights
        used mainly by analyze()"""
    straightct = 16 * [0]
    for i in range(1,11):
        straightct [i] = 1
        for j in range (0,5):
            if rankcount[i+j] == 0:
                straightct[i] = 0
    straightct[15] = sum(straightct[1:11])
    return (straightct)

def analyze (card_list):
    """ returns suit_rank_array[i] where i is row
     0 - S           6 - SF S        10 - singles_list    15 - S_list
     1 - H           7 - SF H        11 - pairs_list      16 - H_list
     2 - D           8 - SF D        12 - trips_list      17 - D_list
     3 - C           9 - SF C        13 - fourks_list     18 - C_list
     4 - Frequency                   14 - fiveks_list
     5 - Straights                        
     column 15 is always sum of row - for flushes [5][15]
     """
    suits = "SHDC"
    ranks = "123456789TJQKA"
    
    x = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    suit_rank_array = [[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                       [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                       [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                       [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                       [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                       [],[],[],[],[],[],[],[],[]]
    #print " 0",
    for card in card_list:
        suit_int = suits.index(card[0]) #0:3
        rank_int = ranks.index(card[1]) + 1 #1:14
        suit_rank_array[suit_int][rank_int] += 1 #increment[i][j] by 1

    for i in range (4): # count number of cards per suit
        suit_rank_array[i][1] = suit_rank_array[i][14]  #set up Ace as 1 for straights
        suit_rank_array[i][15] = sum(suit_rank_array[i][0:14]) #put suit freq in 15
        #print suit_rank_array[i], suits[i]
    
    flushes = 0  # count flushes
    for i in range(4):
        if suit_rank_array[i][15] >= 5:
             flushes = flushes + 1
    suit_rank_array[4][15] = flushes #store sum of flushes in [4][15]
    
    for i in range(4):
        for j in range(1,15):
            suit_rank_array[4][j] += suit_rank_array[i][j]

    #print suit_rank_array[4], "rank freq/flush sum"

    # 5 card straights
    suit_rank_array[5] = straightcount(suit_rank_array[4])
    no_straight =  True
    #print suit_rank_array[5], "straights"

    # 5 card straight flush
    for i in range (6,10):
        suit_rank_array[i] = straightcount(suit_rank_array[i-6])
        #print suit_rank_array[i], "SF", suits[i-6]

    ranks = "0123456789TJQKA"
    hand_x = []
    card_id = []
    
    # Go through all 15 ranks and count singles, pairs, trips, etc.
    for j in range(14,1,-1):      
        if suit_rank_array[4][j] == 1:
            suit_rank_array[10].append(ranks[j])
        if suit_rank_array[4][j] == 2:
            suit_rank_array[11].append(ranks[j])
        if suit_rank_array[4][j] == 3: 
            suit_rank_array[12].append(ranks[j])
        if suit_rank_array[4][j] == 4:
            suit_rank_array[13].append(ranks[j])
        if suit_rank_array[4][j] == 5:
            suit_rank_array[14].append(ranks[j])
        for i in range (4):
           if suit_rank_array[i][j] >= 1:
              suit_rank_array[15+i].append(ranks[j])
              
##    for i in range(10,19):
##        print i, suit_rank_array[i], len(suit_rank_array[i])
              
    return (suit_rank_array)

def best_hand2(card_listx, score_prob):
    """ Given card_listx, return hand_x which is best 5 card hand"""
    score = score_prob[0]
    suit_rank_array = analyze(card_listx)
    suits = "SHDC"
    ranks = "0A23456789TJQKA"
    hand_x = []
    card_id = []
    singles_list = suit_rank_array[10]
    pairs_list = suit_rank_array[11]
    trips_list = suit_rank_array[12]
    fourks_list = suit_rank_array[13]
    fiveks_list = suit_rank_array[14]
    flushes = suit_rank_array [4][15]
    straights = suit_rank_array[5][15]
    
    # find best hand2 - best hand less than score_prob[0]


    if len(fiveks_list) > 0:
        if score > 90000:
            card_id.append(fiveks_list[0])
            #print "5K", fiveks_list
        
    elif len(fourks_list) > 0:
        if score > 80000:
            card_id.append(fourks_list[0])
            #print "4K", fourks_list
        
    elif len(trips_list) > 0 and len(pairs_list)>=1:
        if score > 70000:
            card_id.append(trips_list[0])
            card_id.append(pairs_list[-1])
            #print "Full House", trips_list[0], pairs_list[-1]
 
    elif flushes > 0:
        if score > 60000:
            for i in range(4):
               if suit_rank_array[i][15] >= 5:
                   card_id.append(suits[i])
            #print "flush", card_id
        
    elif straights > 0:
        straight_found = False
        if score > 50000:
            for j in range (11,0,-1):   #straight
                if straight_found == False:
                    if suit_rank_array[5][j] >= 1:
                        straight_found = True
                        for k in range (5):
                            n = 0  #looks for 1 per ranks[j+k]
                            for cardx in card_listx:
                                #print "cardx, ranks[j+k]", cardx, ranks[j+k]
                                if ranks[j+k] in cardx:
                                     if n == 0:
                                        card_id.append(cardx)
                                        n = 1
                    
        #print "straight", card_id

    elif len(trips_list)>0 and len(pairs_list) == 0:
        if score > 40000:
            card_id.append(trips_list[0])
            #print "trips", card_id

    elif len(pairs_list) == 5:
         if score >30000:
            card_id.append(pairs_list[-1])
            card_id.append(pairs_list[-2])
            #print "2 pairs of 5 pairs", card_id
        
    elif len(pairs_list) == 4:
        if score >30000:
            card_id.append(pairs_list[-1])
            card_id.append(pairs_list[1])
            #print "2 pairs of 4 pairs", card_id
        
    elif len(pairs_list) == 3:
        if score > 30000:
            card_id.append(pairs_list[-1])
            card_id.append(pairs_list[-2])
            #print "2 pairs of 3 pairs", card_id

    elif (len(pairs_list) == 2 or len(pairs_list) == 1):
        if score > 20000:
            #print "pairs_list", pairs_list
            card_id.append(pairs_list[0])
            
    elif len(singles_list) > 4:
        if score > 10000:
            #print "singles_list", singles_list
            card_id.append(singles_list[0])

    else:
        #print "nothing found"
        pass
        
    #print "card_id", card_id
    only_five = 0
    if flushes > 0:
        for id in card_id:
            for cardx in card_listx:
                if id in cardx:
                    hand_x.append(cardx)
        hand_x = flush_overage(hand_x, card_listx)
    else:
        for id in card_id:
            for cardx in card_listx:
                #print "id", id, "cardx", cardx
                if id in cardx:
                    hand_x.append(cardx)
    # if hand_x is more than 5 cards,                                   
    sorted (hand_x, cmp = rank_sort, reverse= True)
    #print "Sorted in best_hand", hand_x
    return (hand_x)
  
def best_hand1(card_listx, score_prob):
    """ Given card_listx, return hand_x which is best 3-card hand less than score_prob"""
    suit_rank_array = analyze(card_listx)
    score = score_prob[0]
    suits = "SHDC"
    ranks = "0A23456789TJQKA"
    hand_x = []
    card_id = []
    singles_list = suit_rank_array[10]
    pairs_list = suit_rank_array[11]
    trips_list = suit_rank_array[12]
    
    # find best hand 3 card hand (mo, pair or trip only)
    #print "Looking for best_hand1", card_listx
    #print "hand2 cannot be > than", score

    if len(trips_list)>0 and len(pairs_list) == 0 and score > 40000:
        card_id.append(trips_list[0])
        #print "trips", card_id

    elif len(pairs_list) == 2 and score > 20000:
          #print "pairs_list", pairs_list
          card_id.append(pairs_list[0])
            
    elif len(pairs_list) == 1 and score > 20000:
          #print "pairs_list", pairs_list
          card_id.append(pairs_list[0])   
        
    elif len(singles_list) >= 3 and score > 10000:
          #print "singles_list", singles_list
          card_id.append(singles_list[0])
          card_id.append(singles_list[1])
          card_id.append(singles_list[2])
          
    else:
        #print "nothing found", card_id
        pass
        
    #print "card_id", card_id

    for id in card_id:
        for cardx in card_listx:
            #print "id", id, "cardx", cardx
            if id in cardx:
                hand_x.append(cardx)                              
    sorted (hand_x, cmp = rank_sort, reverse= True)
    #print "Sorted in best_hand", hand_x
    return (hand_x)
  
def flush_overage (card_listx, card_list2):
    """ Is there a flush overage?
        If yes, return one card which is useful for cards_remaining hand
        If not, return empty"""
    suits = "SHDC"
    flush_overage_card = ""
    found = False
    #print "flush_overage", "card_listx", card_listx
    #print "flush_overage", "card_list2", card_list2
    suit_rank_array = analyze(card_list2)
    extra_cards = len(card_listx) - 5
    for i in range (extra_cards):
        #print "flush overage i", i
        if len(suit_rank_array[13]) > 0 and found == False: # if there are 4K
             for cardx in card_listx:
                 for y in suit_rank_array[13]:
                      if y in cardx:
                          found = True
                          #print "found 4K", cardx
                          flush_overage_card = cardx
                       
        if len(suit_rank_array[12]) > 0 and found == False: # if there are Trips
             for cardx in card_listx:
                  for y in suit_rank_array[12]:
                      if y in cardx:
                          found = True
                          #print "found Trips", cardx
                          flush_overage_card = cardx
                          
        #print "pairs", suit_rank_array[11]
        if len(suit_rank_array[11]) > 0 and found == False: # if there are Pairs 
             for cardx in card_listx:
                  if found == False:
                      for y in suit_rank_array[11]:
                          #print "y, cardx", y, cardx
                          if y in cardx:
                              found = True
                              flush_overage_card = cardx
        if found == False:
            flush_overage_card = card_listx[0]
            found = True
            
        if found == True:
            card_listx.remove(flush_overage_card)
            flush_overage_card = ""
            found = False
            #print "after removal", card_listx
            
    return card_listx

def score(card_listx, hand):
    """ given 1-5 cards, returns initial score and prob depending on hand 1,2 or 3"""
    suit_rank_array = analyze (card_listx)
    suits = "SHDC"
    ranks = "0123456789TJQKA"
    hand_x = []
    card_id = []
    singles_list = suit_rank_array[10]
    pairs_list = suit_rank_array[11]
    trips_list = suit_rank_array[12]
    fourks_list = suit_rank_array[13]
    fiveks_list = suit_rank_array[14]         
    straightflushes = flushes = 0
    for i in range(4):
        if suit_rank_array[i][15] >= 5:
             flushes = flushes + 1
    straights = suit_rank_array[5][15]
    for i in range(6,10):
        if suit_rank_array[i][15] >=1:
            straightflushes += 1
            straightflushsuit = i
            
    if len(fiveks_list) > 0:
        #print "5K", fiveks_list
        score = 100000
        score += ranks.index(suit_rank_array[14][0]) * 100
        
    # need to add straight flush
    elif straightflushes >=1:
        score = 90000
        score += ranks.index(suit_rank_array[straightflushsuit+9][0]) * 100
        
    elif len(fourks_list) > 0:
        #print "4K", fourks_list
        score = 80000
        score += ranks.index(suit_rank_array[13][0]) * 100
        
    elif len(trips_list) > 0 and len(pairs_list)>=1:
        #print "Full House", trips_list[0], pairs_list[-1]
        score = 70000
        score += ranks.index(trips_list[0]) * 100 + ranks.index(pairs_list[-1])
 
    elif flushes > 0:
        for i in range(4):     #print "flush", card_id
           if suit_rank_array[i][15] >= 5:
               score = 60000
               #print "cards in flush", suit_rank_array[15+i]
               score += ranks.index(suit_rank_array[15+i][0]) * 100       
    
    elif straights > 0:           
        for j in range (11,0,-1):   #straight
            if suit_rank_array[5][j] >= 1:
                score = 50000
                if j == 1:
                    score += 1402
                else:
                    score += (j+4)*100 #Highest card in straight
                    score += j+3 #next highest card in straight
                    
        #print "straight", card_id

    elif len(trips_list)>0 and len(pairs_list) == 0:
        score = 40000
        score += ranks.index(trips_list[0]) * 100
        #print "trips", card_id
                    
    elif len(pairs_list) > 1:
        score = 30000
        score += ranks.index(pairs_list[0]) * 100 + ranks.index(pairs_list[-1])
        #print "2 pairs", card_id

    elif len(pairs_list) == 1:
        score = 20000
        score += ranks.index(pairs_list[0]) * 100

    else:
        #print "nothing found - high/2nd high cards", card_listx
        score = 10000
        if len(card_listx) > 0:
            score += ranks.index(card_listx[0][1]) * 100
            
    prob = win_prob(score, hand)
    
    if hand == "3":
        if score >= 100000:
            prob = prob * 6
        elif score >= 90000:
            prob = prob * 5
        elif score >= 80000:
            prob = prob * 4
    elif hand == "2":
        if score >= 100000:
            prob = prob * 12
        elif score >= 90000:
            prob = prob * 10
        elif score >= 80000:
            prob = prob * 8
        elif score >= 70000:
            prob = prob * 2
    elif hand == "1":
        if score >= 40000:
            prob = prob * 3
        
    #print "debug score 1", score, hand, prob
    #print "score", card_listx, score
    return (score, prob)

def score_final(card_listx, hand):
    
    """ given either 3 or 5 cards, return score and prob depending on hand 1,2 or 3
        """
    suit_rank_array = analyze (card_listx)
    suits = "SHDC"
    ranks = "0123456789TJQKA"
    hand_x = []
    card_id = []
    singles_list = suit_rank_array[10]
    pairs_list = suit_rank_array[11]
    trips_list = suit_rank_array[12]
    fourks_list = suit_rank_array[13]
    fiveks_list = suit_rank_array[14]         
    straightflushes = flushes = 0
    for i in range(4):
        if suit_rank_array[i][15] >= 5:
             flushes = flushes + 1
    straights = suit_rank_array[5][15]
    for i in range(6,10):
        if suit_rank_array[i][15] >=1:
            straightflushes += 1
            straightflushsuit = i
            
    if len(fiveks_list) > 0:
        #print "5K", fiveks_list
        score = 100000
        score += ranks.index(suit_rank_array[14][0]) * 100
        
    # need to add straight flush
    elif straightflushes >=1:
        score = 90000
        score += ranks.index(suit_rank_array[straightflushsuit+9][0]) * 100
        
    elif len(fourks_list) > 0:
        #print "4K", fourks_list
        score = 80000
        score += ranks.index(suit_rank_array[13][0]) * 100
        
    elif len(trips_list) > 0 and len(pairs_list)>=1:
        #print "Full House", trips_list[0], pairs_list[-1]
        score = 70000
        score += ranks.index(trips_list[0]) * 100 + ranks.index(pairs_list[-1])
 
    elif flushes > 0:
        for i in range(4):     #print "flush", card_id
           if suit_rank_array[i][15] >= 5:
               score = 60000
               score += ranks.index(suit_rank_array[15+i][0]) * 100 + ranks.index(suit_rank_array[15+i][1])        

    elif straights > 0:           
        for j in range (11,0,-1):   #straight
            if suit_rank_array[5][j] >= 1:
                score = 50000
                if j == 1:
                    score += 1402
                else:
                    score += (j+4)*100 #Highest card in straight
                    score += j+3 #next highest card in straight

    elif len(trips_list)>0 and len(pairs_list) == 0:
        score = 40000
        score += ranks.index(trips_list[0]) * 100
        #print "trips", card_id
                    
    elif len(pairs_list) > 1:
        score = 30000
        score += ranks.index(pairs_list[0]) * 100 + ranks.index(pairs_list[-1])
        #print "2 pairs", card_id

    elif len(pairs_list) == 1:
        score = 20000
        score += ranks.index(pairs_list[0]) * 100
        if len(singles_list) > 0:
            score += ranks.index(singles_list[0]) 
        #print "singles_list", singles_list
        #print "high card", card_id

    else:
        #print "nothing found - high/2nd high cards", card_listx
        score = 10000
        if len(card_listx) > 0:
            score += ranks.index(card_listx[0][1]) * 100
            score += ranks.index(card_listx[1][1])
        if score == 10000:
            "score_final cannot find hand", card_listx
            for m in range (19):
                print suit_rank_array[m]
            
    prob = win_prob(score, hand)
    # specials scoring
    if hand == "3":
        if  score >= 100000:
            prob = prob * 6
        elif score >= 90000:
            prob = prob * 5
        elif score >= 80000:
            prob = prob * 4
    elif hand == "2":
        if score >= 100000:
            prob = prob * 12
        elif score >= 90000:
            prob = prob * 10
        elif score >= 80000:
            prob = prob * 8
        elif score >= 70000:
            prob = prob * 2
    elif hand == "1":
        if score >= 40000:
            prob = prob * 3
    #print "debug score 1", score, hand, prob
    #print "score", card_listx, score
    return ([score, prob])

def win_prob(score, hand):
    global prob_file
    global prob_chart
    global prob_array
    global prob_hand
    
    if prob_file is False:
        with open("probability1wild.csv","rb") as f:
            reader = csv.reader(f)
            x = list(reader)
        prob_file = True
        inum = 0
        # store probability in b
        prob_hand = [0,0,0,0]
        for a in x:
            a[1], a[2] = int(a[1]), float(a[2])
            #print a
            prob_chart[inum] = a
            inum += 1
        i = j = k = 0   
        for m in range(inum):
            #print prob_chart[m][0]
            if "1" in prob_chart[m][0]:
                prob_array1[i] = list(prob_chart[m])
                #print i, prob_array1[i]
                i += 1
            if "2" in prob_chart[m][0]:
                prob_array2[j] = list(prob_chart[m])
                #print j, prob_array2[j]
                j += 1
            if "3" in prob_chart[m][0]:
                prob_array3[k] = list(prob_chart[m])
                #print k, prob_array[3][k]
                k += 1
                
        prob_hand[1] = i
        prob_hand[2] = j
        prob_hand[3] = k

    index = 0

    if hand in prob_array1[0][0]:
        index = bin_search (prob_array1, prob_hand[1], score)
        prob = prob_array1[index][2]

    if hand in prob_array2[0][0]:
        index = bin_search (prob_array2, prob_hand[2], score)
        prob = prob_array2[index][2]
        
    if hand in prob_array3[0][0]:
        index = bin_search (prob_array3, prob_hand[3], score)
        prob = prob_array3[index][2]
        
    return prob

def bin_search(prob_array, items, score):
    orig_items = items
    for i in range(0, items):      
        if score > prob_array[i][1]:
            answer = i
            break
    low = 0
    high = items
    test = (high + low) / 2
    diff = high - low
    #print "before 1 ", diff
    while (diff > 3):
          #print "abs(score-prob[test]", score, test, prob_array[test][1]
          if score >= prob_array[test][1]:
                high = test
          if score <= prob_array[test][1]:
                low = test
          test = (high + low)/2
          diff = high - low
          #print "after 1 ", score, prob_array[test][1], low, high
                                        
    #print "after2", score, "from", low, "to", high, "iterations", answer-low     
    for i in range(low, high+5):      
        if score > prob_array[i][1]:
            index = i
            break
    #print "after 3", index
    return index


