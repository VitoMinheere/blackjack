
def get_players_with_money(players):
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



