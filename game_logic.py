from main import *
from print_statements import *
from user_input import *

import main as main


def check_players_status(players):
    still_playing = []
    for player in players:
        status = player.get_status()
        if status:
            still_playing.append(player)

    if len(still_playing) > 0:
        return True
    return False


def place_bet_and_remove_money_from_player(player):
    player_bet = ask_player_what_amount_to_bet(player)
    player.set_money(player.get_money_amount() - player_bet)
    return player_bet


def bank_is_bust(players):
    split = int(main.amount_on_table / len(players))
    print_bank_has_bust(split)
    for player in players:
        player.set_money(player.get_money_amount() + split)


def run_bank_logic(bank):
    hand_value = bank.get_hand_value()
    action = ""
    if hand_value <= 16:
        bank.hit(main.deck)
        action = "hit"
    elif hand_value >= 17:
        action = "stay"

    print_bank_action(action)
    return action


def choose_next_action(player, extra_hand=False):
    player_chosen_action = ask_player_for_next_action(player)

    if player_chosen_action == 'H' and extra_hand is False:
        player.hit(main.deck)
        if player.assess_hand_value():
            print_hand_value_for_player(player.get_name(), player.get_card_names(), player.get_hand_value())
        else:
            print_player_is_bust(player.get_hand_value())

    elif player_chosen_action == 'H' and extra_hand is True:
        player.hit_extra_hand(main.deck)
        if player.assess_extra_hand_value():
            print_hand_value_for_player(player.get_name(), player.get_extra_hand_card_names(),
                                        player.get_extra_hand_value())
        else:
            print_player_is_bust(player.get_extra_hand_value())

    elif player_chosen_action == 'S':
        pass
    elif player_chosen_action == 'SP':
        player.split_hand_when_duplicate_cards()


def payout_money_on_table(players):

    if len(players) > 1:
        winners = []
        if main.amount_on_table > 0:
            part = main.amount_on_table / len(players)
        else:
            part = 0
        for player in players:
            player.set_money(player.get_money_amount() + part)
            winners.append(player.get_name())
            print_multiple_winners(winners)
        return winners

    elif len(players) == 1:
        for player in players:
            print_winner(player.get_name())
            player.set_money(player.get_money_amount() + main.amount_on_table)
            return player.get_name()


def check_who_wins(bank, bank_value, players, highest_hand):
    if highest_hand == bank_value or highest_hand < bank_value:
        print_winner(bank.get_name())
        bank.set_money(bank.get_money_amount() + main.amount_on_table)
        return bank.get_name()

    elif highest_hand > bank_value:
        return payout_money_on_table(players)


def check_bank_cards(bank):
    bank_value = bank.get_hand_value()
    print_player_hand_value(bank.get_name(), bank_value)
    if bank_value > 21:
        return False
    return True


def get_highest_card_on_table(players, bank):
    highest_hand = 0
    highest_hand_holding_players = []

    for player in players:
        if player.get_status():
            hand_value = player.get_highest_hand_value()
            print_player_hand_value(player.get_name(), hand_value)

            if hand_value == highest_hand:
                highest_hand = hand_value
                highest_hand_holding_players.append(player)
            elif hand_value > highest_hand:
                highest_hand = hand_value
                highest_hand_holding_players = [player]

    if check_players_status(players):
        if check_bank_cards(bank):
            check_who_wins(bank, bank.get_hand_value(), highest_hand_holding_players, highest_hand)
        else:
            bank_is_bust(players)
    else:
        print_all_players_are_bust()
        bank.set_money(bank.get_money_amount() + main.amount_on_table)
    players = get_players_with_money(players)
    play_another_round(players, bank)


def deal_card_and_let_player_choose_action(player, extra_hand=False):
    player.add_card_to_hand(main.deck.deal_card())

    if player.assess_hand_value() and extra_hand is False:
        print_hand_value_for_player(player.get_name(), player.get_card_names(), player.get_hand_value())
        choose_next_action(player)

        if player.check_for_extra_hand() and extra_hand is False:  # Check for extra hand and give player extra turn
            deal_card_and_let_player_choose_action(player, True)

    elif player.assess_extra_hand_value() and extra_hand is True:
        print_hand_value_for_player(player.get_name(), player.get_extra_hand_card_names(), player.assess_extra_hand_value())
        choose_next_action(player)

    elif player.assess_hand_value() is False:
        print_player_is_bust(player.get_hand_value())
    elif player.assess_extra_hand_value() is False:
        print_player_is_bust(player.get_extra_hand_value())
