from random import shuffle
from classes import Player, Deck

deck = Deck()
amount_on_table = 0


def get_players_with_money(players):
    print(players)
    players_with_money = []
    for player in players:
        if player.get_money_amount() > 0:
            print(player.name + " has " + str(player.get_money_amount()) + " left")
            players_with_money.append(player)
        else:
            print(player.name + " has no money left")

    return players_with_money


def check_players_status(players):
    still_playing = []
    for player in players:
        status = player.get_status()
        if status:
            still_playing.append(player)

    if len(still_playing) > 0:
        return True
    else:
        return False


def place_bet(player):
    while True:
        try:
            player_bet = int(input("You have " + str(player.get_money_amount()) + ". How much would you like to bet?"))
            if player_bet <= player.get_money_amount():
                break
            else:
                print("You can only bet up to " + str(player.get_money_amount()))
        except ValueError:
            print('Please enter a number')
    player.set_money(player.get_money_amount()-player_bet)
    return player_bet


def run_bank_logic(bank):
    global deck
    hand_value = bank.get_hand_value()
    action = ""
    if hand_value <= 16:
        bank.hit(deck)
        action = "hit"
    elif hand_value >= 17:
        action = "stay"

    print("The bank chose to " + action + "!" + "\n")
    return action


def bank_is_bust(players):
    global amount_on_table
    split = int(amount_on_table / len(players))
    print("Bank has bust. Everybody gets " + str(split))
    for player in players:
        player.set_money(player.get_money_amount()+split)


def choose_next_action(player):
    global deck
    matching_cards = False
    question = "What would you like to do? [H]it or [S]tand"
    if player.check_hand_for_matching_cards():
        question = "You have two of the same cards, you can split your hand in 2 separate hands. " \
                   + question + " or [SP]lit"
        matching_cards = True
    try:
        action = (input(question).upper())
        if action == 'H':
            player.hit(deck)
            if player.get_hand_value() < 21:
                print(str(player.get_name()) + ", you have " + str(player.get_card_names())
                      + " which amounts to a value of " + str(player.get_hand_value()) + "\n")
            else:
                print('Hand value is ' + str(player.get_hand_value()) + '. You are bust!')
        elif action == 'S':
            pass
        elif action == 'SP' and matching_cards:
            player_extra_hand = player.split_hand_when_duplicate_cards()
            return player_extra_hand
    except ValueError:
        if matching_cards:
            print("Please enter H, S or SP")
        else:
            print("Please enter H or S")


def print_winner(winner):
    if type(winner) is not list:
        winner = [winner]

    if len(winner) == 1:
        return str(winner) + " is the winner!"
    elif len(winner) > 1:
        return str(winner) + " are the winners!"


def check_who_wins(bank, bank_value, players, highest_hand):
    winner = []
    if highest_hand == bank_value:
        winner = bank.get_name()
        bank.set_money(bank.get_money_amount()+amount_on_table)
    elif highest_hand < bank_value:
        winner = bank.get_name()
        bank.set_money(bank.get_money_amount()+amount_on_table)
    elif highest_hand > bank_value:

        if len(players) > 1:
            part = amount_on_table / len(players)
            for player in players:
                player.set_money(player.get_money_amount()+part)
                winner.append(player.get_name())
                print_winner(winner)
        elif len(players) == 1:
            for player in players:
                winner = player.get_name()
                print_winner([winner])
                player.set_money(player.get_money_amount()+amount_on_table)

    return winner


def get_highest_card_on_table(players, bank):
    global amount_on_table
    highest_hand = 0
    highest_hand_holding_players = []
    for player in players:
        if player.get_status():
            hand_value = player.get_hand_value()
            print(player.name + " has a hand of " + str(hand_value))
            if hand_value == highest_hand:
                highest_hand = hand_value
                highest_hand_holding_players.append(player)
            elif hand_value > highest_hand:
                highest_hand = hand_value
                highest_hand_holding_players = [player]

    if check_players_status(players):
        bank_value = bank.get_hand_value()
        if bank_value == 0:
            bank_is_bust(players)
            return
        else:
            print("The bank has a hand of " + str(bank_value) + "\n")
            check_who_wins(bank, bank_value, highest_hand_holding_players, highest_hand)
    else:
        print("Every player has bust! The bank wins")
        bank.add_money(amount_on_table)
    players = get_players_with_money(players)
    play_another_round(players, bank)


def play_next_round(players, bank):
    global deck
    for player in players:
        if player.get_status() and player.assess_hand_value():
            player.add_card_to_hand(deck.deal_card())
            if player.assess_hand_value():
                print(str(player.get_name()) + ", you have " + str(player.get_card_names())
                      + " which amounts to a value of " + str(player.get_hand_value()) + "\n")
                player_extra_hand = choose_next_action(player)
                if player_extra_hand:
                    players += player_extra_hand
            else:
                print('Hand value is ' + str(player.get_hand_value()) + '. You are bust!')
        else:
            print('Hand value is ' + str(player.get_hand_value()) + '. You are bust!')

    bank.add_card_to_hand(deck.deal_card())
    run_bank_logic(bank)
    get_highest_card_on_table(players, bank)


def first_betting_round(players, bank):
    global amount_on_table
    amount_on_table = 0
    for player in players:
        print(str(player.get_name()) + ", you have " + str(player.get_card_names())
              + " which amounts to a value of " + str(player.get_hand_value()) + "\n")
        player_bet = place_bet(player)
        amount_on_table += player_bet
        print(str(player.name) + ", you have " + str(player.get_money_amount()) + " left" + "\n")
        print("Amount on the table is " + str(amount_on_table))
    play_next_round(players, bank)


def start_round(players, bank):
    global deck
    shuffle(deck.cards)
    for player in players:
        player.hand = []
        player.add_card_to_hand(deck.deal_card())
    bank.add_card_to_hand(deck.deal_card())
    first_betting_round(players, bank)


def play_another_round(players, bank):
    players_for_next_round = get_players_with_money(players)
    if len(players_for_next_round) > 0:
        while True:
            try:
                answer = input("Would you like to play another round? [Y]es or [N]o ?").upper()
                if answer == "Y":
                    start_round(players_for_next_round, bank)
                elif answer == "N":
                    break
            except ValueError:
                print("Please enter Y or N")

    else:
        print("No players left. Game has ended")


def set_up_game():
    players = []
    while True:
        try:
            amount_of_players = int(input("How many players would you like on the table?"))
            if amount_of_players >= 1:
                break
            else:
                print("Please enter a number higher then 0")
        except ValueError:
            print('Please enter a number')

    for x in range(0, amount_of_players):
        # player_name = input('Enter your name')
        player = Player("test")
        players.append(player)

    global deck
    if amount_of_players > 3:
        amount_of_decks = int(amount_of_players / 3)
        deck = Deck(amount_of_decks)

    bank = Player('bank')
    start_round(players, bank)


if __name__ == "__main__":
    set_up_game()
