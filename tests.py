import unittest
from main import *
from classes import Player, Deck


class TestGameFunctions(unittest.TestCase):
    def setUp(self):
        self.blackjack_hand = [{'card': '7', 'value': 7}, {'card': '7', 'value': 7}, {'card': '7', 'value': 7}]
        self.losing_hand = [{'card': '1', 'value': 1}, {'card': '1', 'value': 1}, {'card': '1', 'value': 1}]
        self.winning_hand = [{'card': '7', 'value': 7}, {'card': '7', 'value': 7}, {'card': '6', 'value': 6}]
        self.bust_hand = [{'card': '7', 'value': 7}, {'card': '7', 'value': 7}, {'card': '8', 'value': 8}]

        self.matching_hand = [{'card': '7', 'value': 7}, {'card': '7', 'value': 7}]
        self.non_matching_hand = [{'card': '3', 'value': 3}, {'card': '7', 'value': 7}]

        self.ace_hand = [{'card': 'Ace', 'value': 11}, {'card': '7', 'value': 7}]
        self.non_ace_hand = [{'card': '4', 'value': 4}, {'card': '7', 'value': 7}]

        self.low_hand = [{'card': '4', 'value': 4}, {'card': '7', 'value': 7}]
        self.high_hand = [{'card': '9', 'value': 9}, {'card': '9', 'value': 9}]

        self.player = Player('player')
        self.player2 = Player('player2')
        self.bank = Player('bank')

    def test_create_player(self):
        self.assertEqual(len(self.player.hand), 0)
        self.assertGreater(self.player.money, 0)

    def test_asses_cards_in_hand(self):
        self.player.hand = self.bust_hand
        self.assertFalse(self.player.assess_hand_value())

        self.player.hand = self.blackjack_hand
        self.assertTrue(self.player.assess_hand_value())

    def test_check_matching_cards_in_hand(self):
        self.player.hand = self.matching_hand
        self.assertTrue(self.player.check_hand_for_matching_cards())

        self.player.hand = self.non_matching_hand
        self.assertFalse(self.player.check_hand_for_matching_cards())

    def test_check_for_ace_in_hand(self):
        self.player.hand = self.ace_hand
        self.assertTrue(self.player.check_hand_for_aces())

        self.player.hand = self.non_ace_hand
        self.assertFalse(self.player.check_hand_for_aces())

    def test_player_wins(self):
        self.bank.hand = self.losing_hand
        self.player.hand = self.winning_hand
        winner = check_who_wins(self.bank, self.bank.get_hand_value(), [self.player],  self.player.get_hand_value())
        self.assertEqual(self.player.name, winner)

    def test_bank_wins(self):
        self.bank.hand = self.winning_hand
        self.player.hand = self.losing_hand
        winner = check_who_wins(self.bank, self.bank.get_hand_value(),
                                [self.player], self.player.get_hand_value())
        self.assertEqual(self.bank.name, winner)

    def test_bank_wins_with_same_score(self):
        self.bank.hand = self.winning_hand
        self.player.hand = self.winning_hand
        winner = check_who_wins(self.bank, self.bank.get_hand_value(),
                                self.player, self.player.get_hand_value())
        self.assertEqual(self.bank.name, winner)

    def test_bank_logic(self):
        self.bank.hand = self.low_hand
        self.assertEqual("hit", run_bank_logic(self.bank))

        self.bank.hand = self.high_hand
        self.assertEqual("stay", run_bank_logic(self.bank))

    def test_players_win_with_same_hand(self):
        self.player.hand = self.winning_hand
        self.player2.hand = self.winning_hand
        self.bank.hand = self.losing_hand
        winner = check_who_wins(self.bank, self.bank.get_hand_value(),
                                [self.player, self.player2], self.player.get_hand_value())
        self.assertEqual(2, len(winner))

    def test_get_players_with_money(self):
        self.player.money = 0
        self.player2.money = 100
        players = get_players_with_money([self.player, self.player2])
        self.assertEqual(1, len(players))

        self.player2.money = 0
        players = get_players_with_money([self.player, self.player2])
        self.assertEqual(0, len(players))

    def test_print_winner(self):
        win_statement = print_winner(self.player)
        self.assertEqual("r!", win_statement[-2:])

        win_statement = print_winner([self.player, self.player2])
        self.assertEqual("s!", win_statement[-2:])  # Check last 2 characters to check if there are multiple winners

    def test_split_hand_duplicate_cards(self):
        self.player.hand = self.matching_hand
        print(self.player.split_hand_when_duplicate_cards())


class TestDeckFunctions(unittest.TestCase):

    def test_deck_is_complete(self):
        test_deck = Deck()
        self.assertEqual(len(test_deck.cards), 56)

    def test_draw_card(self):
        test_deck = Deck()
        test_deck.deal_card()
        self.assertEqual(len(test_deck.cards), 55)


if __name__ == '__main__':
    unittest.main()
