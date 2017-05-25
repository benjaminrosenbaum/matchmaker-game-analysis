from random import shuffle
from copy import deepcopy

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
def is_free(money):
    return money["shem"] == 0 and money["gelt"] == 0


def flip(money):
    return {"shem": money["gelt"], "gelt": money["shem"]}


def kind(money):
    return "gelt" if (money["shem"] == 0) else "shem"


#AI
def match_cost(client, visitor):
    if client['sex'] == visitor['sex']:
        return None
    marrying_down = client['rank'] - visitor['rank']
    return { "shem": max(0, marrying_down), "gelt": max(0, -marrying_down)}


def expected_match_reward(client, visitor):
    cost = match_cost(client, visitor)
    if cost == None:
        return None 
    if is_free(cost):
        return {"shem": 0, "gelt": 2.5}
    cost[kind(cost)] += visitor["rank"]
    return flip(cost)


client_cards = get_deck()
visitor_cards = get_deck()

handsize = 4
num_visitors = 2

my_hand = deal_from(client_cards, handsize)
your_hand = deal_from(client_cards, handsize)
visitors = deal_from(visitor_cards, num_visitors)



print "My hand: %s \nYour hand: %s \n Visitors: %s" % (my_hand, your_hand, visitors)
print "%s remain in client cards, %s in visitor_cards" % (len(client_cards), len(visitor_cards))

def print_cost_and_reward(client, visitor):
    m = match_cost(client, visitor)
    r = expected_match_reward(client, visitor)
    vals = (client['rank'], visitor['rank'], m, r)
    print "match cost & reward of a %s client to marry a %s visitor: %s, %s" % vals

print_cost_and_reward(boy(4), girl(6))
print_cost_and_reward(boy(6), girl(6))
print_cost_and_reward(boy(6), girl(4))
print "queer match:"
print_cost_and_reward(boy(4), boy(6)) 




