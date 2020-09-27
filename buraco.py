"""
Toda vez que o computador tiver que fazer uma decisão, ele vai ter o state:
    - p1 comprou de cima ou baixo
    - descarte do p1
    - how many cards p1 has
    - p2 comprou de cima ou baixo
    - descarte do p2
    - how many cards p2 has
    - p3 comprou de cima ou baixo
    - descarte do p3
    - how many cards p3 has
    - table do proprio time
    - table do oponente
    - own hand
    - if the opponent team has already gotten the dead hand
    - if the own team has gotten the dead hand

Decision
    - To grab from the top or from the bottom

We are making it a "game rule", for simplicity sake (To discuss - up for debate):
    - That everytime you have a way to encaixar uma carta no jogo, voce baixa
    - Everytime you have a way to bater voce bate
    - Voce so usa o coringa se for do mesmo naipe e se for abaixo de 8 a nao ser que vc for bater!

Duvida:
    - Como replicar o "descer jogos sujos porque a gente acha que o oponente ta perto de bater / acabar o jogo"
"""

import random

SUITS = ["Diamonds", "Clubs", "Hearts", "Spades"]
RANKS = ["Ace", "2", "3", "4", "5", "6", "7", "8", "9", "10", "Jack", "Queen", "King"]
NUM_PLAYERS = 4
NUM_DEADS = 2
NUM_STARTING_CARDS = 11
JOKER_INDEX = 1
TOTAL_NUM_CARDS = 104

class Card():
    def __init__(self, rank, suit):
        self.rankIndex = rank
        self.rankName = RANKS[rank]
        self.suitIndex = suit
        self.suitName = SUITS[suit] 

    def print(self):
        print(self.rankName, "of", self.suitName)

    def isJoker(self):
        return self.rankIndex == JOKER_INDEX

    def isNeighbor(self, card):
        if (self.suitIndex == card.suitIndex):
            diff = self.rankIndex - card.rankIndex
            return diff == -1 or diff == 1 or diff == -12 or diff == 12
        return (self.isJoker() or card.isJoker())

class Hand():
    def __init__(self, isDead, deck):
        self.isDead = isDead
        self.cards = []
        self.numJokers = 0
        for i in range(NUM_STARTING_CARDS):
            thisCard = deck.pop()
            if thisCard.isJoker():
                self.numJokers += 1
            self.cards.append(deck.pop())

    def add(self, card):
        self.cards.append(card)
        if card.isJoker():
            self.numJokers += 1

    def remove(self, rankIndex, suitIndex):
        for i, obj in enumerate(self.cards):
            if obj.rankIndex == rankIndex and obj.suitIndex == suitIndex:
                if rankIndex == JOKER_INDEX:
                    self.numJokers -= 1
                del self.cards[i]
                return Card(rankIndex, suitIndex)

    def removeJoker(self, suitIndex):
        index = -1
        suitAtIndex = -1
        for i, obj in enumerate(self.cards):
            if obj.isJoker():
                suitAtIndex = i
                suitAtIndex = obj.suitIndex
                if obj.suitIndex == suitIndex:
                    del self.cards[i]
                    return Card(JOKER_INDEX, suitAtIndex)
        del self.cards[suitAtIndex]
        self.numJokers -= 1
        return Card(JOKER_INDEX, suitAtIndex)

    def print(self):
        for card in self.cards:
            card.print()

    def numCards(self):
        return len(self.cards)
    
    def getGroupsOfSuits(self):
        groupedBySuit = [[], [], [], []]
        for card in self.cards:
            groupedBySuit[card.suitIndex].append(card.rankIndex) # consider adding a 13 in case it's an Ace depending on implementation
        for group in groupedBySuit:
            group.sort()
        return groupedBySuit

class Deck():
    def __init__(self):
        self._deck = []
        for rank in range(len(RANKS)):
            for suit in range(len(SUITS)):
                cardFromDeck1 = Card(rank, suit)
                cardFromDeck2 = Card(rank, suit)
                self._deck.append(cardFromDeck1)
                self._deck.append(cardFromDeck2)
        random.shuffle(self._deck)

    def pop(self):
        return self._deck.pop()

    def length(self):
        return len(self._deck)

class Player():
    def __init__(self, deck):
        self.hand = Hand(False, deck)
        self.ranOutOfHards = 0

    def getDeadPile(self, hand):
        self.hand = hand

    def printHand(self):
        self.hand.print()

    def numCards(self):
        return self.hand.numCards()

class Table():
    def __init__(self):
        self._groups = []

    def addGroup(self, group):
        self._groups.append(group)
        """
        def groupSort(a, b):
            return len(a.cards) < len(b.cards)
        self._groups.sort(groupSort)
        """

    def numCards(self):
        numberOfCards = 0
        for group in self._groups:
            numberOfCards += group.numCards()
        return numberOfCards

    def _checkTable(self, hand):
        hasBeenPlaced = True
        while (hasBeenPlaced == True):
            hasBeenPlaced = False
            for group in self._groups:
                for card in hand.cards:
                    if (group.fits(card)):
                        #hand.remove(card)
                        hasBeenPlaced = True
                        break

    def _countLengthOfSequence(self, group, startingIndex):
        k = startingIndex + 1
        n = len(group)
        while (k < n):
            if ((group[k] - group[startingIndex]) != (k - startingIndex)):
                break
            k += 1
        return k - j

    def place(self, hand):
        self._checkTable(hand)
        groupedBySuit = hand.getGroupsOfSuits(hand)
        for i in range(len(groupedBySuit)):
            for j in range(len(groupedBySuit[i])):
                lengthOfSequence = self._countLengthOfSequence(groupedBySuit[i], j)
                if (lengthOfSequence > 1):
                    new_group_cards = []
                    # add joker first
                    if (lengthOfSequence == 2):
                        if (hand.numJokers > 0):
                            thisCard = hand.removeJoker(i)
                            if thisCard == None:
                                continue
                            new_group_cards.append(thisCard)
                        else:
                            continue
                    alreadyAdded = False
                    for m in range(lengthOfSequence):
                        thisCard = hand.remove(groupedBySuit[i][j + m], i)
                        if thisCard == None:
                            alreadyAdded = True
                            break
                        new_group_cards.append(thisCard)
                    if alreadyAdded:
                        for card in new_group_cards:
                            hand.add(card)
                        continue
                    thisGroup = Group(new_group_cards)
                    self.addGroup(thisGroup)

    def print(self):
        print("Printing groups in this table")
        for group in self._groups:
            group.print()

class Group():
    def __init__(self, cards):
        self.cards = cards

    def fits(self, card):
        # if fits, add card to group, remove from hand return true
        # if not return false
        pass

    def numCards(self):
        return len(self.cards)

    def print(self):
        print("Printing cards in this group:")
        for card in self.cards:
            card.print()

def sanityCheck(deck, a1, b1, a2, b2, dead1, dead2, discardPile, tableA, tableB):
    totalCards = deck.length() + a1.numCards() + b1.numCards() + a2.numCards() + b2.numCards()
    totalCards += dead1.numCards() + dead2.numCards() + len(discardPile)
    totalCards += tableA.numCards() + tableB.numCards()
    if totalCards == TOTAL_NUM_CARDS:
        print("Correct amount of cards out there :)")
    else:
        print("ERROR: number of cards out there =", totalCards)
    print("")

# TODO: consider building a Game class so that sanityCheck runs without parameters
def main():
    deck = Deck()
    a1 = Player(deck)
    b1 = Player(deck)
    a2 = Player(deck)
    b2 = Player(deck)
    dead1 = Hand(True, deck)
    dead2 = Hand(True, deck)
    discardPile = []
    tableA = Table()
    tableB = Table()

    #print("Before a1 placing cards")
    #a1.printHand()
    tableA.place(a1.hand)
    sanityCheck(deck, a1, b1, a2, b2, dead1, dead2, discardPile, tableA, tableB)
    #print("After a1 placed cards and before b1 places cards")
    #a1.printHand()
    #print("")
    #b1.printHand()
    tableB.place(b1.hand)
    sanityCheck(deck, a1, b1, a2, b2, dead1, dead2, discardPile, tableA, tableB)
    #print("After b1 placed cards")
    #b1.printHand()

    print("Printing Table A")
    tableA.print()
    print("Printing Table B")
    tableB.print()

    print("Before a2 placing cards")
    a2.printHand()
    tableA.place(a2.hand)
    sanityCheck(deck, a1, b1, a2, b2, dead1, dead2, discardPile, tableA, tableB)
    print("After a2 placed cards and before b2 places cards")
    a2.printHand()
    print("")
    b2.printHand()
    tableB.place(b2.hand)
    sanityCheck(deck, a1, b1, a2, b2, dead1, dead2, discardPile, tableA, tableB)
    print("After b2 placed cards")
    b2.printHand()
    
main()
