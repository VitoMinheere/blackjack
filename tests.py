import unittest
from main import *
from game_logic import *
from classes import Player, Deck, Card, Hand


class TestGameFunctions(unittest.TestCase):
    def setUp(self):
        self.blackjack_hand = Hand([Card('7', 7), Card('7', 7), Card('7', 7)])
        self.losing_hand = Hand([Card('1', 1), Card('1', 1), Card('1', 1)])
        self.winning_hand = Hand([Card('7', 7), Card('7', 7), Card('6', 6)])
        self.bust_hand = Hand([Card('7', 7), Card('7', 7), Card('8', 8)])

        self.matching_hand = Hand([Card('7', 7), Card('7', 7)])
        self.non_matching_hand = Hand([Card('7', 7), Card('3', 3)])

        self.ace_hand = Hand([Card('Ace', 11), Card('7', 7)])
        self.non_ace_hand = Hand([Card('4', 4), Card('7', 7)])

        self.low_hand = Hand([Card('4', 4), Card('7', 7)])
        self.high_hand = Hand([Card('9', 9), Card('9', 9)])

        self.player = Player('player')
        self.player2 = Player('player2')
        self.bank = Player('bank')
        self.amount_on_table = 500

    def test_asses_cards_in_hand(self):
        self.player.hand = self.bust_hand
        self.assertFalse(self.player.hand.check_if_hand_is_not_bust())

        self.player.hand = self.blackjack_hand
        self.assertTrue(self.player.hand.check_if_hand_is_not_bust())

    def test_check_matching_cards_in_hand(self):
        self.player.hand = self.matching_hand
        self.assertTrue(self.player.hand.check_hand_for_matching_cards())

        self.player.hand = self.non_matching_hand
        self.assertFalse(self.player.hand.check_hand_for_matching_cards())

    def test_player_wins(self):
        self.bank.hand = self.losing_hand
        self.player.hand = self.winning_hand
        winner = check_who_wins(self.bank, self.bank.hand.get_hand_value(),
                                [self.player],  self.player.hand.get_hand_value(), self.amount_on_table)
        self.assertEqual(self.player.name, winner)

    def test_bank_wins(self):
        self.bank.hand = self.winning_hand
        self.player.hand = self.losing_hand
        winner = check_who_wins(self.bank, self.bank.hand.get_hand_value(),
                                [self.player], self.player.hand.get_hand_value(), self.amount_on_table)
        self.assertEqual(self.bank.name, winner)

    def test_bank_wins_with_same_score(self):
        self.bank.hand = self.winning_hand
        self.player.hand = self.winning_hand
        winner = check_who_wins(self.bank, self.bank.hand.get_hand_value(),
                                self.player, self.player.hand.get_hand_value(), self.amount_on_table)
        self.assertEqual(self.bank.name, winner)

    def test_bank_logic(self):
        self.bank.hand = self.low_hand
        self.assertEqual("hit", run_bank_logic(self.bank))

        self.bank.hand = self.high_hand
        self.assertEqual("stay", run_bank_logic(self.bank))

    def test_bank_is_bust(self):
        self.bank.hand = self.bust_hand
        self.assertFalse(check_bank_is_not_bust(self.bank))

        self.bank.hand = self.blackjack_hand
        self.assertTrue(check_bank_is_not_bust(self.bank))

    def test_players_win_with_same_hand(self):
        self.player.hand = self.winning_hand
        self.player2.hand = self.winning_hand
        self.bank.hand = self.losing_hand
        winner = check_who_wins(self.bank, self.bank.hand.get_hand_value(),
                                [self.player, self.player2], self.player.hand.get_hand_value(), self.amount_on_table)
        self.assertEqual(2, len(winner))

    def test_get_players_with_money(self):
        self.player.money = 0
        self.player2.money = 100
        players = get_players_with_money([self.player, self.player2])
        self.assertEqual(1, len(players))

        self.player2.money = 0
        players = get_players_with_money([self.player, self.player2])
        self.assertEqual(0, len(players))

    def test_split_hand_duplicate_cards(self):
        self.player.hand = self.matching_hand
        self.player.hand, self.player.extra_hand = self.player.hand.split_hand_when_duplicate_cards()
        self.assertEqual(self.player.hand.get_hand_value(), self.player.extra_hand.get_hand_value())


class TestDeckFunctions(unittest.TestCase):

    def test_deck_is_complete(self):
        test_deck = Deck()
        self.assertEqual(len(test_deck.cards), 56)

    def test_draw_card(self):
        test_deck = Deck()
        test_deck.deal_card()
        self.assertEqual(len(test_deck.cards), 55)


class TestCardFunctions(unittest.TestCase):

    def setUp(self):
        self.ace = Card('Ace', 11)
        self.card = Card('1', 1)

    def test_card_has_value(self):
        card_value = self.card.get_card_value()
        self.assertEqual(1, card_value)

    def test_set_card_value(self):
        self.card.set_card_value(2)
        self.assertEqual(2, self.card.get_card_value())

    def test_get_card_name(self):
        card_name = self.ace.get_card_name()
        self.assertEqual('Ace', card_name)

    def test_card_is_ace(self):
        self.assertTrue(self.ace.is_ace())
        self.assertFalse(self.card.is_ace())


class TestHandFunctions(unittest.TestCase):

    def setUp(self):
        self.one_card_hand = Hand([Card('7', 7)])
        self.matching_hand = Hand([Card('7', 7), Card('7', 7)])
        self.non_matching_hand = Hand([Card('6', 6), Card('7', 7)])
        self.bust_hand = Hand([Card('7', 7), Card('7', 7), Card('8', 8)])
        self.ace_hand = Hand([Card('Ace', 11), Card('7', 7)])

    def test_get_hand_value(self):
        self.assertEqual(14, self.matching_hand.get_hand_value())

    def test_get_amount_of_cards(self):
        self.assertEqual(2, self.matching_hand.get_amount_of_cards())

    def test_get_card_names(self):
        self.assertEqual(['7', '7'], self.matching_hand.get_card_names())

    def test_add_Card_to_hand(self):
        self.card = Card('7', 7)
        self.one_card_hand.add_card_to_hand(self.card)
        self.assertEqual(2, self.one_card_hand.get_amount_of_cards())

    def test_check_if_hand_not_bust(self):
        self.assertTrue(self.matching_hand.check_if_hand_is_not_bust())
        self.assertFalse(self.bust_hand.check_if_hand_is_not_bust())

    def test_hand_for_duplicate_cards(self):
        self.assertTrue(self.matching_hand.check_hand_for_matching_cards())
        self.assertFalse(self.non_matching_hand.check_hand_for_matching_cards())

    def test_hand_has_ace(self):
        self.assertTrue(self.ace_hand.has_ace())
        self.assertFalse(self.matching_hand.has_ace())

    def test_get_ace_card(self):
        ace_card = self.ace_hand.get_ace_card()
        self.assertTrue(ace_card.is_ace())

    def test_empty_hand(self):
        self.matching_hand.empty_hand()
        self.assertEqual(0, self.matching_hand.get_amount_of_cards())


if __name__ == '__main__':
    unittest.main()