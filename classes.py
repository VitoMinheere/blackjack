class Player:
    def __init__(self, name):
        self.name = name
        self.money = 1000
        self.hand = []
        self.playing = True

    def add_card_to_hand(self, card):
        self.hand += [card]

    def get_money_amount(self):
        return self.money

    def get_status(self):
        return self.playing

    def get_card_names(self):
        return [card['card'] for card in self.hand]

    def get_hand_value(self):
        return sum(card['value'] for card in self.hand)

    def show_cards_to_player(self):
        print(str(self.name) + ", you have " + str(self.get_card_names()) + " which amounts to a value of " +
              str(self.get_hand_value()))

    def assess_hand_value(self):
        hand_value = self.get_hand_value()
        if hand_value > 21:
            print('Hand value is ' + str(hand_value) + '. You are bust!')
            self.playing = False
            return False
        elif hand_value <= 21:
            return True

    def place_bet(self):
        while True:
            try:
                player_bet = int(input("You have " + str(self.money) + ". How much would you like to bet?"))
                if player_bet <= self.money:
                    break
                else:
                    print("You can only bet up to " + str(self.money))
            except ValueError:
                print('Please enter a number')
        self.money -= player_bet
        return player_bet

    def hit(self, deck):
        self.add_card_to_hand(deck.deal_card())
        if self.name != 'bank':
            self.show_cards_to_player()
        self.assess_hand_value()

    def check_hand_for_aces(self):
        cards_in_hand = self.get_card_names()
        for name in cards_in_hand:
            if name == 'Ace':
                return True

    def check_hand_for_matching_cards(self):
        if self.hand[0] == self.hand[1]:
            return True
        else:
            return False

    def choose_next_action(self, deck):
        question = "What would you like to do? [H]it or [S]tand"
        if self.check_hand_for_matching_cards():
            question = "You have two of the same cards, you can split your hand in 2 separate hands. " \
                       + question + " or [SP]lit"
        try:
            action = (input(question).upper())
            if action == 'H':
                self.hit(deck)
            elif action == 'S':
                pass
            elif action == 'SP':
                pass
        except ValueError:
            print("Please enter H or S")


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
