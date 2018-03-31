def print_hand_value_for_player(player, card_names, hand_value):
    print(str(player) + ", you have " + str(card_names)
          + " which amounts to a value of " + str(hand_value) + "\n")


def print_player_hand_value(player, hand_value):
    print(str(player) + " has a hand of " + str(hand_value) + "\n")


def print_player_is_bust(hand_value):
    print('Hand value is ' + str(hand_value) + '. You are bust!')


def print_bank_action(action):
    print("The bank chose to " + action + "!" + "\n")


def print_bank_has_bust(split):
    print("Bank has bust. Everybody gets " + str(split))


def print_winner(winner):
    return str(winner) + " is the winner!"


def print_multiple_winners(winners):
    return str(winners) + " are the winners!"


def print_amount_money_player_has(player, amount):
    print(player + " has " + str(amount) + " left")


def print_player_has_no_money_left(player):
    print(player + " has no money left")


def print_all_players_are_bust():
    print("Every player has bust! The bank wins")


def print_amount_money_on_table(amount_on_table):
    print("Amount on table is " + str(amount_on_table))


def print_amount_money_for_player(player, amount):
    print(str(player) + ", you have " + str(amount) + " left" + "\n")
