from random import shuffle
from classes import Player, Deck
from user_input import *
import game_logic
from print_statements import *

deck = Deck()
amount_on_table = 0


def get_players_with_money(players):
    players_with_money = []
    print('player amount is ' + str(len(players)))
    for player in players:
        if player.get_money_amount() > 0:
            print('dit print 2x')
            print_amount_money_player_has(player.get_name(), player.get_money_amount())
            players_with_money.append(player)
        else:
            print_player_has_no_money_left(player.get_name())

    return players_with_money


def play_next_round(players, bank):
    global deck
    bank.empty_hand()
    for player in players:
        player.empty_hand()
        if player.get_status() and player.assess_hand_value():
            game_logic.deal_card_and_let_player_choose_action(player)
        else:
            print_player_is_bust(player.get_hand_value())

    bank.add_card_to_hand(deck.deal_card())
    game_logic.run_bank_logic(bank)
    game_logic.get_highest_card_on_table(players, bank)


def first_betting_round(players, bank):
    global amount_on_table
    amount_on_table = 0
    for player in players:
        print_hand_value_for_player(player.get_name(), player.get_card_names(), player.get_hand_value())
        player_bet = game_logic.place_bet_and_remove_money_from_player(player)
        amount_on_table += player_bet
        print_amount_money_for_player(player.get_name(), player.get_money_amount())
        print_amount_money_on_table(amount_on_table)
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
        player_name = ask_player_for_name()
        player = Player(player_name)
        players.append(player)

    global deck
    if amount_of_players > 3:
        amount_of_decks = int(amount_of_players / 3)  # max 3 players per deck
        deck = Deck(amount_of_decks)

    bank = Player('bank')
    start_round(players, bank)


if __name__ == "__main__":
    set_up_game()
