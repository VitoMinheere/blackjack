from cards import blackjack_cards


class Deck:
    def __init__(self, amount=1):
        self.cards = []
        for card in blackjack_cards:
            self.cards.append(Card(card['name'], card['value']))
        self.cards *= (4 * amount)

    def deal_card(self):
        return self.cards.pop()


class Card:
    def __init__(self, name, value):
        self.name = name
        self.value = value

    def get_card_value(self):
        return self.value

    def get_card_name(self):
        return self.name

    def set_card_value(self, value):
        self.value = value

    def is_ace(self):
        if self.get_card_name() == 'Ace':
            return True
        return False


class Hand:
    def __init__(self, cards=None):
        if cards:
            self.cards = cards
        else:
            self.cards = []

    def get_hand_value(self):
        value = 0
        for card in self.cards:
            value += card.get_card_value()
        return value

    def get_amount_of_cards(self):
        return len(self.cards)

    def get_card_names(self):
        names = []
        for card in self.cards:
            names.append(card.get_card_name())
        return names

    def add_card_to_hand(self, card):
        self.cards += [card]

    def empty_hand(self):
        self.cards = []

    def check_if_hand_is_not_bust(self):
        if self.get_hand_value() > 21:
            return False
        return True

    def check_hand_for_matching_cards(self):
        if len(self.cards) > 1 and self.cards[0].get_card_name() == self.cards[1].get_card_name():
            return True
        return False

    def split_hand_when_duplicate_cards(self):
        return Hand([self.cards[0]]), Hand([self.cards[1]])

    def has_ace(self):
        if 'Ace' in self.get_card_names():
            return True
        return False

    def get_ace_card(self):
        for card in self.cards:
            if card.get_card_name() == 'Ace':
                return card


class Player:
    def __init__(self, name):
        self.name = name
        self.money = 1000
        self.hand = Hand()
        self.extra_hand = Hand()  # used when player splits hand in case of matching cards
        self.playing = True

    def set_money(self, amount):
        self.money = amount

    def get_money_amount(self):
        return self.money

    def get_status(self):
        return self.playing

    def set_status(self, status):
        self.playing = status

    def get_name(self):
        return self.name

    def get_highest_hand_value(self):
        hand_value = self.hand.get_hand_value()
        extra_hand_value = self.extra_hand.get_hand_value()
        if hand_value > extra_hand_value:
            return hand_value
        return extra_hand_value

    def has_extra_hand(self):
        if self.extra_hand.get_card_names():
            return True

