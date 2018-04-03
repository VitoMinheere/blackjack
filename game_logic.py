import main
from print_statements import *
from user_input import *


def check_not_bust_players(players):
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


def run_bank_logic(bank):
    hand_value = bank.hand.get_hand_value()
    action = ""
    if hand_value <= 16:
        bank.hand.add_card_to_hand(main.deck.deal_card())
        action = "hit"
    elif hand_value >= 17:
        action = "stay"

    print_bank_action(action)
    return action


def choose_next_action(player, extra_hand=False):
    player_chosen_action = ask_player_for_next_action(player)

    if player_chosen_action == 'H' and extra_hand is False:
        player.hand.add_card_to_hand(main.deck.deal_card())
        if player.hand.check_if_hand_is_not_bust():
            print_hand_value_for_player(player.get_name(), player.hand.get_card_names(),
                                        player.hand.get_hand_value())
        else:
            print_player_is_bust(player.hand.get_hand_value())

    elif player_chosen_action == 'H' and extra_hand is True:
        player.extra_hand.add_card_to_hand(main.deck.deal_card())
        if player.extra_hand.check_if_hand_is_not_bust():
            print_extra_hand_value_for_player(player.get_name(), player.extra_hand.get_card_names(),
                                        player.extra_hand.get_hand_value())
        else:
            print_player_is_bust(player.extra_hand.get_hand_value())

    elif player_chosen_action == 'S':
        pass
    elif player_chosen_action == 'SP':
        player.hand, player.extra_hand = player.hand.split_hand_when_duplicate_cards()
        deal_card_and_let_player_choose_action(player)


def payout_money_on_table(players, amount_on_table):
    print_amount_money_on_table(amount_on_table)
    if len(players) > 1:
        winners = []
        if amount_on_table > 0:
            part = (amount_on_table / len(players))
            print('Multiple winners, part = ' + str(part))
        else:
            part = 0
        for player in players:
            player.set_money(player.get_money_amount() + part)
            winners.append(player.get_name())
        return winners

    elif len(players) == 1:
        for player in players:
            player.set_money(player.get_money_amount() + amount_on_table)
            return player.get_name()


def check_who_wins(bank, bank_value, players, highest_hand, amount_on_table):
    if highest_hand == bank_value or highest_hand < bank_value:
        bank.set_money(bank.get_money_amount() + amount_on_table)
        return bank.get_name()

    elif highest_hand > bank_value:
        return payout_money_on_table(players, amount_on_table)


def check_bank_is_not_bust(bank):
    bank_value = bank.hand.get_hand_value()
    print_player_hand_value(bank.get_name(), bank_value)
    if bank_value > 21:
        return False
    return True


def check_for_bust(players, bank, amount_on_table):
    if check_not_bust_players(players):
        if check_bank_is_not_bust(bank):
            return True
        else:
            print_bank_has_bust(amount_on_table/(len(players)))
            payout_money_on_table(players, amount_on_table)
            return False
    else:
        print_all_players_are_bust()
        bank.set_money(bank.get_money_amount() + amount_on_table)
        return False


def get_highest_hand_on_table(players):
    highest_hand = 0
    highest_hand_holding_players = []

    for player in players:
        if player.hand.check_if_hand_is_not_bust() and player.extra_hand.check_if_hand_is_not_bust():
            hand_value = player.get_highest_hand_value()
            print_player_hand_value(player.get_name(), hand_value)

            if hand_value == highest_hand:
                highest_hand = hand_value
                highest_hand_holding_players.append(player)
            elif hand_value > highest_hand:
                highest_hand = hand_value
                highest_hand_holding_players = [player]

    return highest_hand_holding_players, highest_hand


def deal_card_for_extra_hand(player):
    if player.extra_hand.get_amount_of_cards() <= 2:
        player.extra_hand.add_card_to_hand(main.deck.deal_card())
        if player.extra_hand.has_ace():
            if ask_player_to_change_ace():
                ace_card = player.extra_hand.get_ace_card()
                ace_card.set_card_value(1)

    if player.hand.check_if_hand_is_not_bust() and player.extra_hand.check_if_hand_is_not_bust():
        print_hand_value_for_player(player.get_name(), player.extra_hand.get_card_names(),
                                    player.extra_hand.get_hand_value())
        choose_next_action(player, True)  # action for extra hand

        print_hand_value_for_player(player.get_name(), player.hand.get_card_names(),
                                    player.hand.get_hand_value())
        choose_next_action(player)  # action for normal hand


def deal_card_and_let_player_choose_action(player):
    if player.has_extra_hand():
        deal_card_for_extra_hand(player)

    if player.hand.get_amount_of_cards() <= 2:
        player.hand.add_card_to_hand(main.deck.deal_card())
        if player.hand.has_ace():
            if ask_player_to_change_ace():
                ace_card = player.hand.get_ace_card()
                ace_card.set_card_value(1)

    if player.hand.check_if_hand_is_not_bust():
        print_hand_value_for_player(player.get_name(), player.hand.get_card_names(), player.hand.get_hand_value())
        choose_next_action(player)

    elif player.hand.check_if_hand_is_not_bust() is False:
        print_player_is_bust(player.hand.get_hand_value())
    elif player.extra_hand.check_if_hand_is_not_bust() is False:
        print_player_is_bust(player.extra_hand.get_hand_value())
