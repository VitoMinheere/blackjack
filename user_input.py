

def ask_player_what_amount_to_bet(player):
    while True:
        try:
            player_bet = int(input("You have " + str(player.get_money_amount()) + ". How much would you like to bet?"))
            if player_bet <= player.get_money_amount():
                break
            else:
                print("You can only bet up to " + str(player.get_money_amount()))
        except ValueError:
            print('Please enter a number')
    return player_bet


def ask_player_for_next_action(player):
    matching_cards = False
    question = "What would you like to do? [H]it or [S]tand"
    if player.check_hand_for_matching_cards():
        question = "You have two of the same cards, you can split your hand in 2 separate hands. " \
                   + question + " or [SP]lit"
        matching_cards = True
    try:
        action = (input(question).upper())
        if action == 'H':
            return action
        elif action == 'S':
            return action
        elif action == 'SP' and matching_cards:
            return action
    except ValueError:
        if matching_cards:
            print("Please enter H, S or SP")
        else:
            print("Please enter H or S")


def ask_player_for_another_round():
    while True:
        try:
            answer = input("Would you like to play another round? [Y]es or [N]o ?").upper()
            if answer == "Y":
                return answer
            elif answer == "N":
                break
        except ValueError:
            print("Please enter Y or N")


def ask_for_amount_of_players():
    while True:
        try:
            amount_of_players = int(input("How many players would you like on the table?"))
            if amount_of_players >= 1:
                return amount_of_players
            else:
                print("Please enter a number higher then 0")
        except ValueError:
            print('Please enter a number')