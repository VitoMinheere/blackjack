class Player:
    def __init__(self, name):
        self.name = name
        self.money = 1000
        self.hand = []
        self.playing = True

    def add_card_to_hand(self, card):
        self.hand += [card]

    def set_money(self, amount):
        self.money = amount

    def get_money_amount(self):
        return self.money

    def get_status(self):
        return self.playing

    def get_name(self):
        return self.name

    def get_card_names(self):
        return [card['card'] for card in self.hand]

    def get_hand_value(self):
        return sum(card['value'] for card in self.hand)

    def assess_hand_value(self):
        hand_value = self.get_hand_value()
        if hand_value > 21:
            self.playing = False
            return False
        elif hand_value <= 21:
            return True

    def hit(self, deck):
        self.add_card_to_hand(deck.deal_card())
        self.assess_hand_value()

    def check_hand_for_aces(self):
        cards_in_hand = self.get_card_names()
        for name in cards_in_hand:
            if name == 'Ace':
                return True

    def check_hand_for_matching_cards(self):
        if self.hand[0] == self.hand[1]:
            return True
        return False

    def split_hand_when_duplicate_cards(self):
        player_extra_hand = Player(self.name + "_extra_hand")
        player_extra_hand.money = self.money
        player_extra_hand.hand = self.hand[1]
        self.hand = self.hand[0]
        return player_extra_hand


class Deck:
    def __init__(self, amount=1):
        self.cards = ([{'card': str(x), 'value': x} for x in range(2, 12)])
        self.cards += [{'card': 'Ace', 'value': 11},
                       {'card': 'King', 'value': 3},
                       {'card': 'Queen', 'value': 2},
                       {'card': 'Jack', 'value': 1}]
        self.cards *= (4*amount)

    def deal_card(self):
        return self.cards.pop()
