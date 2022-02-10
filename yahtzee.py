import random
import sys
import time
from prettytable import PrettyTable
import collections

# TODO
# - Make it a multiplayer game
#           -- https://stackoverflow.com/questions/35321722/python-prettytable-add-title-above-the-tables-header
# - Add README
# - Make repo public

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

def roll_dices(times):
    return sorted([random.randint(1,6)for x in range(times)])


def play_round(name, scoreboard):
    print(f"\n-------------------{name} playing----------------------------")
    print_scoreboard(scoreboard, name)


    dices = roll_dices(5)

    print(f"\nYou have rolled {dices}")
    keeping_dices = input(f"Which dices do you wanna keep {name}? (seperated with a comma)\n")

    kept_dices = []
    if keeping_dices == "":
        print("\nYou kept no dices")
        print("\nRerolling all five (second time)...")

        second_dices = roll_dices(5)
    else:
        for val in [int(x) for x in keeping_dices.split(",")]:
            if (val in dices):
                kept_dices.append(val)
                dices.remove(val)

        if len(kept_dices) == 5:
            print("\nYou have kept all dices, so we're skipping next throws")
            return kept_dices
        else:
            print(f"\nYou have kept {kept_dices}")
            print("\nRolling again (second time)...")
            second_dices = sorted(roll_dices(5 - len(kept_dices)) + kept_dices)


    print(f"\nYou have rolled {second_dices}")
    keeping_dices = input(f"Which dices do you wanna keep {name}? (seperated with a comma)\n")

    kept_dices = []
    if keeping_dices == "":
        print("\nYou kept no dices")
        print("\nRerolling all five (third time)...")

        third_dices = roll_dices(5)
    else:
        for val in [int(x) for x in keeping_dices.split(",")]:
            if (val in second_dices):
                kept_dices.append(val)
                second_dices.remove(val)

        if len(kept_dices) == 5:
            print("\nYou have kept all dices, so we're skipping next throw")
            return kept_dices
        else:
            print(f"\nYou have kept {kept_dices}")
            print("\nRolling again (third time)...")
            third_dices = sorted(roll_dices(5 - len(kept_dices)) + kept_dices)

    return third_dices

def print_scoreboard(scoreboard, name):
    scoreboard_table = PrettyTable()
    scoreboard_table.title = f"{name}'s Scoreboard"
    scoreboard_table.field_names = ["Id", "Field", "Score"]
    i = 1
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

def fill_score_in_scoreboard(thrown_dices, scoreboard, name):
    print_scoreboard(scoreboard, name)
    empty_field_chosen = False

    while not empty_field_chosen:
        field_id = input("What field would you like to fill in your scoreboard? (id)\n")
        chosen_key = list(scoreboard)[int(field_id) - 1]
        if scoreboard[chosen_key] == None:
            empty_field_chosen = True
            score = calculate_correct_score(chosen_key, thrown_dices)
            scoreboard[chosen_key] = score
        else:
            print("\nThe field you chose is already filled in, choose another field!")


    return scoreboard

def calculate_total_score(scoreboard):
    # Check if bonus is applicable
    total_upper_part = scoreboard["One's"] + \
        scoreboard["Two's"] + \
        scoreboard["Three's"] + \
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
    player_count = int(input("How many players will be playing?\n"))
    scoreboards = {}
    player_names = []
    for x in range(player_count):
        player_names.append(input(f"Enter name for player {x + 1}\n"))

    for name in player_names:
        scoreboards[name] = {
            "One's": 1,
            "Two's": 1,
            "Three's": 1,
            "Four's": 1,
            "Five's": 1,
            "Six's": 1,
            "Three of a kind": 1,
            "Four of a kind": 1,
            "Full House": 1,
            "Low Straight": 1,
            "High Straight": 1,
            "Yahtzee": 1,
            "Chance": None
        }

    # Player 0 starts
    player_to_play_next = player_names[0]

    scoreboard_contains_none = not_full_scoreboard(scoreboards[player_to_play_next])

    # Only executed before starting
    print("\nEveryone starts with an empty scoreboard")
    # time.sleep(1)
    for name in player_names:
        print_scoreboard(scoreboards[name], name)

    # time.sleep(2)
    print("\nLet's start the first round!")

    while scoreboard_contains_none:
        for name in player_names:
            thrown_dices = play_round(name, scoreboards[name])
            print(f"Congratulations, you have rolled {thrown_dices}")
            print("----------------------------------------------------------")
            # time.sleep(1)

            scoreboard = fill_score_in_scoreboard(thrown_dices, scoreboards[name], name)
            print("\nGreat, now your scoreboard looks like this:")
            print_scoreboard(scoreboards[name], name)
            scoreboard_contains_none = not_full_scoreboard(scoreboards[name])
            print("\nNext round")


    # After all rounds are played, print the final scoreboard and calculate their score!
    print("\nWell played everyone! All rounds have been played")
    print("Let's look at the final scoreboards")
    for name in player_names:
        print_scoreboard(scoreboards[name], name)

    scores = {}
    for name in player_names:
        scores[name] = calculate_total_score(scoreboards[name])

    sorted_scores = {k: v for k, v in sorted(scores.items(), key=lambda item: item[1])}

    # Copied from Stackoverflow
    ordinal = lambda n: "%d%s" % (n,"tsnrhtdd"[(n//10%10!=1)*(n%10<4)*n%10::4])

    i = 0
    for name, score in list(sorted_scores.items()):
        print(f"Congratulations {name}, you are ranked {ordinal(player_count - i)}.")
        i += 1


# Call
print_intro()
play_game()
print_outro()
