from random import shuffle
from classes import Player, Deck
from user_input import *
from game_logic import *

deck = Deck()
amount_on_table = 0


def place_bet_and_remove_money_from_player(player):
    player_bet = ask_player_what_amount_to_bet(player)
    player.set_money(player.get_money_amount() - player_bet)
    return player_bet


def bank_is_bust(players):
    global amount_on_table
    split = int(amount_on_table / len(players))
    print("Bank has bust. Everybody gets " + str(split))
    for player in players:
        player.set_money(player.get_money_amount() + split)


def print_winner(winner):
    if type(winner) is not list:
        winner = [winner]

    if len(winner) == 1:
        return str(winner) + " is the winner!"
    elif len(winner) > 1:
        return str(winner) + " are the winners!"


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


def choose_next_action(player):
    global deck
    player_chosen_action = ask_player_for_next_action(player)

    if player_chosen_action == 'H':
        player.hit(deck)
        if player.get_hand_value() < 21:
            print(str(player.get_name()) + ", you have " + str(player.get_card_names())
                  + " which amounts to a value of " + str(player.get_hand_value()) + "\n")
        else:
            print('Hand value is ' + str(player.get_hand_value()) + '. You are bust!')

    elif player_chosen_action == 'S':
        pass
    elif player_chosen_action == 'SP':
        player_extra_hand = player.split_hand_when_duplicate_cards()
        return player_extra_hand


def check_who_wins(bank, bank_value, players, highest_hand):
    winner = []
    if highest_hand == bank_value:
        winner = bank.get_name()
        bank.set_money(bank.get_money_amount() + amount_on_table)
    elif highest_hand < bank_value:
        winner = bank.get_name()
        bank.set_money(bank.get_money_amount() + amount_on_table)
    elif highest_hand > bank_value:

        if len(players) > 1:
            part = amount_on_table / len(players)
            for player in players:
                player.set_money(player.get_money_amount() + part)
                winner.append(player.get_name())
                print_winner(winner)
        elif len(players) == 1:
            for player in players:
                winner = player.get_name()
                print_winner([winner])
                player.set_money(player.get_money_amount() + amount_on_table)

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
        player_bet = place_bet_and_remove_money_from_player(player)
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
        player_answer = ask_player_for_another_round()
        if player_answer == 'Y':
            start_round(players_for_next_round, bank)
    else:
        print("No players left. Game has ended")


def set_up_game():
    players = []
    amount_of_players = ask_for_amount_of_players()

    for x in range(0, amount_of_players):
        # player_name = input('Enter your name')
        player = Player("test")
        players.append(player)

    global deck
    if amount_of_players > 3:
        amount_of_decks = int(amount_of_players / 3)  # max 3 players per deck
        deck = Deck(amount_of_decks)

    bank = Player('bank')
    start_round(players, bank)


if __name__ == "__main__":
    set_up_game()
