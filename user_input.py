def ask_player_what_amount_to_bet(player):
    while True:
        try:
            player_bet = int(input("You have " + str(player.get_money_amount()) + ". How much would you like to bet?" + "\n"))
            if player_bet <= player.get_money_amount() and player_bet > 0:
                break
            elif player_bet == 0:
                print("You must be more than 0" + "\n")
            else:
                print("You can only bet up to " + str(player.get_money_amount() + "\n"))
        except ValueError:
            print('Please enter a number' + "\n")
    return player_bet


def ask_player_for_next_action(player):
    matching_cards = False
    question = "What would you like to do? [H]it or [S]tand"
    if player.hand.check_hand_for_matching_cards():
        question = "You have two of the same cards, you can split your hand in 2 separate hands. " \
                   + question + " or [SP]lit" + "\n"
        matching_cards = True
    while True:
        try:
            action = (input(question).upper())
            if action == 'H':
                return action
            elif action == 'S':
                return action
            elif action == 'SP' and matching_cards:
                return action
            elif matching_cards:
                print("Please enter H, S or SP" + "\n")
            else:
                print("Please enter H or S" + "\n")
        except ValueError:
            if matching_cards:
                print("Please enter H, S or SP" + "\n")
            else:
                print("Please enter H or S" + "\n")


def ask_player_for_another_round():
    while True:
        try:
            answer = input("Would you like to play another round? [Y]es or [N]o ?" + "\n").upper()
            if answer == "Y":
                return answer
            elif answer == "N":
                break
        except ValueError:
            print("Please enter Y or N" + "\n")


def ask_for_amount_of_players():
    while True:
        try:
            amount_of_players = int(input("How many players would you like on the table?" + "\n"))
            if amount_of_players >= 1:
                return amount_of_players
            else:
                print("Please enter a number higher then 0" + "\n")
        except ValueError:
            print("Please enter a number" + "\n")


def ask_player_for_name():
    while True:
        try:
            player_name = input("What is your name?" + "\n")
            if len(player_name) > 2:
                break
            else:
                print("Please enter a longer name" + "\n")
        except ValueError:
            pass
    return player_name


def ask_player_to_change_ace():
    while True:
        try:
            answer = input(
                "You have an ace! The value is 11 but you can change it to 1. Do you want to change the value to 1? [Y]es of [N]o" + "\n").upper()
            if answer == "Y":
                return True
            elif answer == "N":
                return False
            else:
                print("Please enter Y or N" + "\n")
        except ValueError:
            print("Please enter Y or N" + "\n")
