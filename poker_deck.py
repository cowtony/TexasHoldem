from typing import List, Tuple
import random


class PokerDeck:
    def __init__(self):
        # Standard Deck
        self.kSuitColor = ['\u001b[37;1m', '\u001b[31m', '\u001b[32;1m', '\u001b[34;1m']
        self.kSuits = ['♤', '♡', '♧', '♢']
        self.kRanks = ['2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A']

        # Leduc Deck (COmment out to use the standard deck)
        self.kSuitColor = ['\u001b[37;1m']
        self.kSuits = ['♤']
        self.kRanks = ['Q', 'K', 'A']

        self.deck = list(range(len(self.kSuits) * len(self.kRanks)))
        random.shuffle(self.deck)


    # Util function to print a card nicely.
    def printCard(self, card_index: int) -> str:
        return f'{self.kSuitColor[card_index // len(self.kRanks)]}{self.kSuits[card_index // len(self.kRanks)]} {self.kRanks[card_index % len(self.kRanks)]}\u001b[0m'


    # Util function to print a list of card. Normally used for printing player's hand.
    def printCards(self, cards: List[int]) -> str:
        return ' '.join([self.printCard(card) for card in cards])

    
    def dealCard(self) -> int:
        return self.deck.pop()