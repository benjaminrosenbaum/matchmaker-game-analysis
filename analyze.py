from random import shuffle
from random import random
from random import randint
from copy import deepcopy
from functools import reduce

#MATH
def flatten(l):
    return [item for sublist in l for item in sublist]


#PROSPECTS
def boy(rank):
    return {'rank': rank, 'sex': 'm'}

def girl(rank):
    return {'rank': rank, 'sex': 'f'}

def suits(value):
    return [{'rank': value, 'sex': 'm'}, {'rank': value, 'sex': 'f'}] * 2


#CARDS
def get_deck():
    d = flatten([suits(a + 1) for a in range(7)])
    shuffle(d)
    return deepcopy(d)


def deal_from(deck, how_many):
    if len(deck) < how_many:
        return []
    popped = deck[0:how_many]
    del deck[0:how_many]
    return popped


#MONEY
def money(shem, gelt):
    return {"shem": shem, "gelt": gelt}

def is_free(money):
    return money["shem"] == 0 and money["gelt"] == 0

def flip(money):
    return {"shem": money["gelt"], "gelt": money["shem"]}

def kind(money):
    return "gelt" if (money["shem"] == 0) else "shem"

def add_money(m1, m2):
    return money(m1["shem"] + m2["shem"], m1["gelt"] + m2["gelt"])

def subtract_money(m1, m2):
    return {"shem": m1["shem"] - m2["shem"], "gelt": m1["gelt"] - m2["gelt"]}

def multiply_money(m, factor):
    return {"shem": m["shem"] * factor, "gelt": m["gelt"] * factor}


#BUDGET
def starting_budget():
    return {'liquid': money(2, 2), 'escrow': [] }


def cash_in(budget):
    for e in budget['escrow']:
        budget['liquid'] = add_money(budget['liquid'], e)
    budget['escrow'] = []
    
def liquid_resource_count(budget):
    money = budget['liquid']
    return money['shem'] + money['gelt']


#AI


def match_cost(client, visitor):
    if client['sex'] == visitor['sex']:
        return None
    marrying_down = client['rank'] - visitor['rank']
    return {"shem": max(0, marrying_down), "gelt": max(0, -marrying_down)}


def chance_of_match(client, visitor):
    if client['sex'] == visitor['sex']:
        return None
    difference = abs(client["rank"] - visitor["rank"])
    if difference == 0:
        return 1
    return max(0, float(5 - max(2, difference))/4)


def expected_match_reward(client, visitor):
    cost = actual_match_reward(client, visitor)
    if cost is None:
        return None
    return multiply_money(flip(cost), chance_of_match(client, visitor))


def actual_match_reward(client, visitor):
    cost = match_cost(client, visitor)
    if cost is None:
        return None
    if is_free(cost):
        return {"shem": 0, "gelt": 2.5} 
    cost[kind(cost)] += visitor["rank"]
    return cost


client_cards = get_deck()
visitor_cards = get_deck()

handsize = 4
num_visitors = 2

my_hand = deal_from(client_cards, handsize)
my_budget = starting_budget()
your_hand = deal_from(client_cards, handsize)
your_budget = starting_budget()
visitors = deal_from(visitor_cards, num_visitors)

def print_cost_and_reward(client, visitor):
    m = match_cost(client, visitor)
    r = expected_match_reward(client, visitor)
    vals = (client['rank'], visitor['rank'], m, chance_of_match(client, visitor), r)
    print "%s client to marry a %s visitor: cost %s, chance %s, expected rwd %s" % vals

#print_cost_and_reward(boy(4.0), girl(6.0))

    
#ETHAN WORK HERE
### TK for v2: 
###     stealing a match
###     blocking a choice 

def card_match(player_idx, vis_idx, reward):
    return {'player_idx': player_idx, 'vis_idx': vis_idx, 'reward':reward}

def find_best_play(player_hand):
    best_play = None
    for player_idx, player_card in enumerate(player_hand):
        for vis_idx, visitor_card in enumerate(visitors):
            reward = expected_match_reward(player_card, visitor_card)
            if reward != None:
                if best_play == None or reward > best_play['reward']:
                    best_play = card_match(player_idx, vis_idx, reward)
    return best_play

def take_turn(hand, budget):
    play = find_best_play(hand)
    if play is None:
        return
    p_card = hand[play['player_idx']]
    v_card = visitors[play['vis_idx']]
    subtract_money(budget['liquid'], match_cost(p_card,v_card))
    if random() <= chance_of_match(p_card,v_card):
        budget['escrow'].append(actual_match_reward(p_card,v_card))
        del visitors[play['vis_idx']] 
    del hand[play['player_idx']]      

def play_round(first_player):    
    print "\n\tTURN START:\n\tMy hand:\t%s \n\tYour hand:\t%s \n\tVisitors:\t%s" % (my_hand, your_hand, visitors)
    if first_player == 1:
        take_turn(my_hand, my_budget)  
        take_turn(your_hand, your_budget) 
    else: 
        take_turn(your_hand, your_budget)
        take_turn(my_hand, my_budget) 
    # print "\n\tTURN END:\n\tMy hand:\t%s \n\tYour hand:\t%s \n\tVisitors:\t%s" % (my_hand, your_hand, visitors)
    if find_best_play(my_hand) is not None or find_best_play(your_hand) is not None:
        play_round(first_player)    
    
def end_round_bookkeeping():
    ### deal cards
    global visitors
    visitors.extend(deal_from(visitor_cards, num_visitors))
    my_hand.extend(deal_from(client_cards, handsize - len(my_hand)))
    your_hand.extend(deal_from(client_cards, handsize - len(your_hand)))
    ### update player resources
    cash_in(my_budget)
    cash_in(your_budget)
    print "\n\tBUDGET:\n\tMy budget:\t%s\n\tYour budget:\t%s" % (my_budget, your_budget)

# the winner is whoever has the most total resources (i.e. shem + gelt)
def determine_leader(budget1, budget2):
    player1_res = liquid_resource_count(budget1) 
    player2_res = liquid_resource_count(budget2) 
    if player1_res == player2_res:
        return 0
    elif player1_res > player2_res:
        return 1
    else:
        return 2
    
def determine_first_player(budget1, budget2):
    leader = determine_leader(budget1, budget2)
    if leader == 0:
        return randint(1,2)
    elif leader == 1:
        return 2
    else:
        return 1
        
    
def play_game():  
    print "STARTING GAME"
    count = 1
    while len(client_cards) > 0 and len(visitor_cards) > 0 and len(my_hand) == handsize and len(your_hand) == handsize: 
        print "\nRound %s:" % (count)
        print "\t\t%s remain in client cards, %s in visitor_cards" % (len(client_cards), len(visitor_cards))
        play_round(determine_first_player(my_budget, your_budget))
        end_round_bookkeeping()
        count += 1
    print "\nGAME OVER: Player %s won (0 indicates tie)\n" % (determine_leader(my_budget, your_budget))

def reset_game():
    global client_cards, visitor_cards, my_hand, my_budget,your_hand,your_budget,visitors;
    client_cards = get_deck()
    visitor_cards = get_deck()
    my_hand = deal_from(client_cards, handsize)
    my_budget = starting_budget()
    your_hand = deal_from(client_cards, handsize)
    your_budget = starting_budget()
    visitors = deal_from(visitor_cards, num_visitors)
    
def game_result():
    return { 'tie':0,'player1':0,'player2':0 }

def add_game_result(result, outcome):
    if outcome == 0:
        result['tie'] += 1
    elif outcome == 1:
        result['player1'] += 1
    else:
        result['player2'] += 1
    return result    

def run_analysis():
    total_results = game_result()
    for x in range(0, 1000):
        play_game()
        add_game_result(total_results, determine_leader(my_budget, your_budget))
        reset_game()
    print total_results
    
run_analysis()


#BEN WORK HERE







