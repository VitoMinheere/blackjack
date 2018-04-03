# blackjack
Python blackjack game with unit tests

Game is written in Python 3.5

Unit tests are written in unittest library from Python

You can run the tests via this command in the root

```
python3 -m unittest discover
```

## Twenty one

This game is a Dutch variant on blackjack, named "eenentwintigen"
In this game the max hand score is 21, if you have a hand above that you are bust.

### game start
By running the Python code the game will start in the terminal or console in Pycharm

You will first be asked the amount of players on the table, this excludes the bank which is always added and will be controlled by the code. The amount of players will determine the amount of decks used. For each 3 players another deck is added.

After dealing a card the first betting round starts. Here you can place your bets between 1 and the amount of money you have.
When betting is finished another card will be dealt and you can either choose to [H]it and get another card or [S]tay and keep the 2 cards.

## cards

The number of points for the cards is as follows:
King 3 points, queen 2 points, jack 1 point.
Ace is 1 or 11 points of your choice.
Cards 2 to 10 have their normal point value.
The ‘suit’ of the card is not important.
The Joker does not play

When you have 2 matching cards you can split you hand and play 2 games at once with 2 hands. If you have an Ace you will be asked if you want it to have an 11 or 1 value.

## Example game
```
How many players would you like on the table?2
What is your name?Player 1
What is your name?Player 2
Player 1, you have ['3'] which amounts to a value of 3

You have 1000. How much would you like to bet?100
Player 1, you have 900 left

Player 2, you have ['11'] which amounts to a value of 11

You have 1000. How much would you like to bet?100
Player 2, you have 900 left

Player 1, you have ['3', 'Jack'] which amounts to a value of 4

What would you like to do? [H]it or [S]tandH
Player 1, you have ['3', 'Jack', 'Queen'] which amounts to a value of 6

Player 2, you have ['11', 'King'] which amounts to a value of 14

What would you like to do? [H]it or [S]tandS
The bank chose to hit!

Player 1 has a hand of 6

Player 2 has a hand of 14

bank has a hand of 24

Amount on table is 200
Bank has bust. Everybody gets 100.0
```

