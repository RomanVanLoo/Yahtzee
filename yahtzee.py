import random
import sys
import time
from prettytable import PrettyTable
import collections

# TODO
# - Make a shortcut and don't roll again when you decide to keep all dices
# - Make it a multiplayer game

def print_intro():
    print("----------------------------------------------------------")
    print("Yahtzee!")
    print("----------------------------------------------------------")
    input("Are you super exited and ready to play? (y/n)\n")

def print_outro():
    print("----------------------------------------------------------")
    print("Thanks for playing, we've had some fun didn't we?!")
    print("Coded by Roman, checkout other projects at github.com/RomanVanLoo")
    print("----------------------------------------------------------")

def play_round():
    print("----------------------------------------------------------")

    def roll_dices(times):
        return sorted([random.randint(1,6)for x in range(times)])

    dices = roll_dices(5)

    print(f"You have rolled {dices}")
    keeping_dices = input("Which dices do you wanna keep? (seperated with a comma)\n")

    kept_dices = []
    if keeping_dices == "":
        print("You kept no dices")
        print("Rerolling all five (second time)...")

        second_dices = roll_dices(5)
    else:
        for val in [int(x) for x in keeping_dices.split(",")]:
            if (val in dices):
                kept_dices.append(val)

        print(f"You have kept {kept_dices}")
        print("Rolling again (second time)...")

        second_dices = sorted(roll_dices(5 - len(kept_dices)) + kept_dices)

    print(f"You have rolled {second_dices}")
    keeping_dices = input("Which dices do you wanna keep? (seperated with a comma)\n")

    kept_dices = []
    if keeping_dices == "":
        print("You kept no dices")
        print("Rerolling all five (third time)...")

        third_dices = roll_dices(5)
    else:
        for val in [int(x) for x in keeping_dices.split(",")]:
            if (val in second_dices):
                kept_dices.append(val)

        print(f"You have kept {kept_dices}")
        print("Rolling again (third time)...")

    third_dices = sorted(roll_dices(5 - len(kept_dices)) + kept_dices)

    print(f"Congratulations, you have rolled {third_dices}")
    print("----------------------------------------------------------")
    # time.sleep(2)

    return third_dices

def print_scoreboard(scoreboard):
    scoreboard_table = PrettyTable()
    scoreboard_table.field_names = ["Id", "Field", "Score"]
    i = 0
    for key,score in scoreboard.items():
        scoreboard_table.add_row([i, key, score])
        i += 1

    print(scoreboard_table)

def calculate_correct_score(chosen_key, thrown_dices):
    if chosen_key ==  "One's":
        score = sum([x for x in thrown_dices if x == 1])
    elif chosen_key ==  "Two's":
        score = sum([x for x in thrown_dices if x == 2])
    elif chosen_key == "Three's":
        score = sum([x for x in thrown_dices if x == 3])
    elif chosen_key == "Four's":
        score = sum([x for x in thrown_dices if x == 4])
    elif chosen_key == "Five's":
        score = sum([x for x in thrown_dices if x == 5])
    elif chosen_key == "Six's":
        score = sum([x for x in thrown_dices if x == 6])
    elif chosen_key == "Three of a kind":
        if collections.Counter(thrown_dices).most_common()[0][1] >= 3:
            score = sum(thrown_dices)
        else:
            score = 0

    elif chosen_key == "Four of a kind":
        if collections.Counter(thrown_dices).most_common()[0][1] >= 4:
            score = sum(thrown_dices)
        else:
            score = 0

    elif chosen_key == "Full House":
        # Score 25
        if (collections.Counter(thrown_dices).most_common()[0][1] == 3 and
                collections.Counter(thrown_dices).most_common()[1][1] == 2):
            score = 25
        else:
            score = 0

    elif chosen_key == "Low Straight":
        if (
            1 in thrown_dices and
            2 in thrown_dices and
            3 in thrown_dices and
            4 in thrown_dices
        ) or (
            2 in thrown_dices and
            3 in thrown_dices and
            4 in thrown_dices and
            5 in thrown_dices
        ) or (
            3 in thrown_dices and
            4 in thrown_dices and
            5 in thrown_dices and
            6 in thrown_dices
            ):
            score = 30

        else:
            score = 0
    elif chosen_key == "High Straight":
        if (
            1 in thrown_dices and
            2 in thrown_dices and
            3 in thrown_dices and
            4 in thrown_dices and
            5 in thrown_dices
        ) or (
            6 in thrown_dices and
            5 in thrown_dices and
            4 in thrown_dices and
            3 in thrown_dices and
            2 in thrown_dices
            ):
            score = 40

        else:
            score = 0

    elif chosen_key == "Yahtzee":
        if len(set(thrown_dices)) == 1:
            score = 50
        else:
            score = 0
    elif chosen_key == "Chance":
        score = sum(thrown_dices)

    return score

def fill_score_in_scoreboard(thrown_dices, scoreboard):
    print_scoreboard(scoreboard)
    empty_field_chosen = False

    while not empty_field_chosen:
        field_id = input("What field would you like to fill in the scoreboard? (id)\n")
        chosen_key = list(scoreboard)[int(field_id)]
        if scoreboard[chosen_key] == None:
            empty_field_chosen = True
            score = calculate_correct_score(chosen_key, thrown_dices)
            scoreboard[chosen_key] = score
        else:
            print("The field you chose is already filled in, choose another field!")


    return scoreboard

def calculate_total_score(scoreboard):
    # Check if bonus is applicable
    total_upper_part = scoreboard["One's"] + \
        scoreboard["Two's"] + \
        scoreboard["Third's"] + \
        scoreboard["Four's"] + \
        scoreboard["Five's"] + \
        scoreboard["Six's"]

    if total_upper_part >= 63:
        bonus = 35
    else:
        bonus = 0

    return bonus + sum(scoreboard.values())

def not_full_scoreboard(scoreboard):
    return any(v == None for k,v in scoreboard.items())

def play_game():
    scoreboard = {
        "One's": None,
        "Two's": None,
        "Three's": None,
        "Four's": None,
        "Five's": None,
        "Six's": None,
        "Three of a kind": None,
        "Four of a kind": None,
        "Full House": None,
        "Low Straight": None,
        "High Straight": None,
        "Yahtzee": None,
        "Chance": None
    }
    # Set all_scores_filled_in variable
    scoreboard_contains_none = not_full_scoreboard(scoreboard)

    # Only executed before starting
    print("You start with an empty scoreboard")
    # time.sleep(2)
    print_scoreboard(scoreboard)
    # time.sleep(2)
    print("Let's start the first round!")

    while scoreboard_contains_none:
        thrown_dices = play_round()
        scoreboard = fill_score_in_scoreboard(thrown_dices, scoreboard)
        print("Great, now scoreboard looks like this:")
        print_scoreboard(scoreboard)
        scoreboard_contains_none = not_full_scoreboard(scoreboard)
        print("Next round")


    # After all rounds are played, print the final scoreboard and calculate their score!
    print_scoreboard(scoreboard)
    # This score calculation is wrong, the bonus from the top part is not taken care of.
    # Extract this calculation to a method

    score  = calculate_total_score(scoreboard)
    print("Well played, you've finished the game.")
    time.sleep(3)
    print(f"You have a final score of: {score}")

# Call
print_intro()
play_game()
print_outro()
