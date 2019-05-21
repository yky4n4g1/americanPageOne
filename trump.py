import random


class Deck:
    def __init__(self):
        self.cards = [Card(index) for index in range(52)]

    def output(self):
        print("Deck:", end="")
        for index in self.cards:
            print(index.suit, index.rank, end=',')
        print()

    def shuffle(self):
        random.shuffle(self.cards)

    def pull(self):
        return self.cards.pop()


class Card:
    def __init__(self, number):
        self.suit = number % 4
        self.rank = number % 13
    __Suit = ["s", "h", "d", "c"]
    __Rank = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]

    #  mutch_card :bool
    def mutch_card(self, card):
        return self.suit == card.suit or self.rank == card.rank or self.rank == 7

    def mutch_rank(self, card):
        return self.rank == card.rank

    def mutch_suit(self, card):
        return self.suit == card.suit

    def get_card(self):
        return (self.__Suit[self.suit] + self.__Rank[self.rank])

    def print_card(self):
        print(self.__Suit[self.suit] + self.__Rank[self.rank])


class FieldCard(Card):
    def __init__(self, card):
        self.suit = card.suit
        self.rank = card.rank
