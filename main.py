from random import shuffle
from classes import Player, Deck
from user_input import *
import game_logic
from print_statements import *

deck = Deck()
amount_on_table = 0


def get_players_with_money(players):
    players_with_money = []
    for player in players:
        if player.get_money_amount() > 0:
            players_with_money.append(player)
        else:
            print_player_has_no_money_left(player.get_name())

    return players_with_money


def play_next_round(players, bank):
    global deck
    for player in players:
        if player.get_status() and player.hand.check_if_hand_is_not_bust():
            game_logic.deal_card_and_let_player_choose_action(player)
        else:
            print_player_is_bust(player.hand.get_hand_value())

    bank.hand.add_card_to_hand(deck.deal_card())
    game_logic.run_bank_logic(bank)
    highest_hand_players, highest_hand_value = game_logic.get_highest_hand_on_table(players)

    if game_logic.check_for_bust(highest_hand_players, bank, amount_on_table):
        winner = game_logic.check_who_wins(bank, bank.hand.get_hand_value(),
                                           highest_hand_players, highest_hand_value, amount_on_table)
        if isinstance(winner, list):
            print_multiple_winners(winner)
        else:
            print_winner(winner)
    play_another_round(players, bank)


def first_betting_round(players, bank):
    global amount_on_table
    amount_on_table = 0
    for player in players:
        print_hand_value_for_player(player.get_name(), player.hand.get_card_names(), player.hand.get_hand_value())
        amount_on_table += game_logic.place_bet_and_remove_money_from_player(player)
        print_amount_money_for_player(player.get_name(), player.get_money_amount())

    play_next_round(players, bank)


def start_round(players, bank):
    global deck
    shuffle(deck.cards)
    for player in players:
        player.hand.empty_hand()
        player.hand.add_card_to_hand(deck.deal_card())
    bank.hand.add_card_to_hand(deck.deal_card())
    first_betting_round(players, bank)


def reset(players, bank):
    bank.hand.empty_hand()
    bank.set_status(True)
    for player in players:
        player.hand.empty_hand()
        player.set_status(True)


def play_another_round(players, bank):
    reset(players, bank)

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
