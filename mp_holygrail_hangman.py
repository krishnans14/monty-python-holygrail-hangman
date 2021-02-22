"""
This is a fun hangman like game to guess quotes from the Monty Python movie,
The quest for the holy grail. Your aim is to guess the quote by guessing the letters
one at a time. You have 5 chances (or 3 changes if you claim you are an expert)
to guess the quote and if not, as the Black knight loses one limb after another,
your champion will also lose.

The quotes were web scrapped from montypython.net and then modified and added
some extra.
"""
import random
from mp_quotes import mp_quotes_list, correct_answer_quotes, wrong_answer_quotes
import re
import os

mp_quotes_select = [mp_q for mp_q in mp_quotes_list if len(mp_q.split(' ')) < 16]

def get_quote():
    quote = random.choice(mp_quotes_select).upper()
    return quote.upper()

def display_quote(quote, guessed_letters, print_to_screen = True):
    """
    The aim of this function is to reformulate the quote in such a way that it will
    display it appropriately. This means that the only alphabetical symbols that will
    remain are those that have been already correctly guessed by the user. other
    alphabets would be replaced with a '_'. All the non alphabetical symbols
    (including apostrophes, hyphens) will be displayed as is
    """
    quote_to_display = re.sub(r'[A-Z]','_', quote)
    if guessed_letters:
        list_quote_to_display = list(quote_to_display) #converting to list because strings are immutable
        for g_letter in guessed_letters:
            for idx, ch in enumerate(quote):
                if(ch == g_letter):
                    list_quote_to_display[idx] = g_letter
        quote_to_display = ''.join(list_quote_to_display) #converting the list back to a string
    if print_to_screen: print(quote_to_display)
    return quote_to_display

def play_mp_hangman(quote, level):
    guessed = False
    guessed_letters = []
    guessed_quotes = []
    tries = 5
    print(display_black_knight(tries))
    quote_incomplete = display_quote(quote, guessed_letters)
    print("\n")
    while not guessed and tries > 0:
        guess = input("Please guess a letter ").upper()
        os.system('cls' if os.name == 'nt' else 'clear')
        if len(guess) == 1 and guess.isalpha():
            if guess in guessed_letters:
                print("You already guessed the letter", guess)
            elif guess not in quote:
                print(random.choice(wrong_answer_quotes), '\n', guess, "is not in the quote.")
                tries -= level # This would reduce the number of attempts before the user loses (6 or 3)
                if tries < 0:
                    tries = 0
                guessed_letters.append(guess)
                quote_incomplete = display_quote(quote, guessed_letters, False)
            else:
                print(random.choice(correct_answer_quotes), "Yes, ", guess, "is in the quote!")
                guessed_letters.append(guess)
                quote_incomplete = display_quote(quote, guessed_letters, False)
                if "_" not in quote_incomplete:
                    guessed = True
        elif len(guess) > 1 and guess.isalpha():
            print("Just answer 3 three letters at a time. Oops, only 1 letter, sir!!")
        else:
            print("Not a valid guess. Aaaaaaaaaa")
        print(display_black_knight(tries))
        print("Letters already guessed: ", guessed_letters)
        print("\n")
        print(quote_incomplete)
        print("\n")
        print("\n")
    if guessed:
        print("Congrats, you are a true knight of the round table! You win a night in castle Anthrax!")
    else:
        print("You make me sad. \n The quote was " + quote + ". \n Let's go Patsy Maybe next time!")


def display_black_knight(state):
    knight = [
                """
            "You lost. I'm off to cross the bridge"


                  O
                  |



                """,
                """
            "You loose both your legs. I won't call it a draw"
                  _
                 | |
                  O
                  |



                """,
                """
            "A single-legged knight?"
                  _
                 | |
                  O
                  |
                  |
                 /

                """,
                """
            "Now you got no hands"
                  _
                 | |
                  O
                  |
                  |
                 / \\

                """,
                """
            "Ouch! You lose your sword hand"
                  _
                 | |
                  O
                  |\\
                  |
                 / \\

                """,
                """
            "You are the Black knight"
                  _
                 | |
                  O
                \\/|\\
                  |
                 / \\

                """
    ]
    return knight[state]


def main():
    quote = get_quote()
    os.system('cls' if os.name == 'nt' else 'clear')
    print("Let's play Hangman! - Monty Python Holygrail version \n")
    print("Ready to Test if you can cross the bridge of death?\n\n")
    print("Your job is to guess the quote before the Black Knight loses the battle against King Arthur \n\n")
    level_input = input("If you are an expert type 'y' or Enter any other key to continue:  ")
    os.system('cls' if os.name == 'nt' else 'clear')
    if level_input == 'y' or level_input == 'Y':
        level = 2
    else:
        level = 1
    play_mp_hangman(quote, level)
    while input("\n Play Again? (Y/N) ").upper() == "Y":
        os.system('cls' if os.name == 'nt' else 'clear')
        quote = get_quote()
        play_mp_hangman(quote, level)


if __name__ == "__main__":
    main()
