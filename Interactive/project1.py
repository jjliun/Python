#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
# Filename      : project1.py
# Author        : Yang Leo (JeremyRobturtle@gmail.com)
# Last Modified : 2014-04-01
'''Demo of rock-paper-scissors-lizard-Spock
'''
# The key idea of this program is to equate the strings
# "rock", "paper", "scissors", "lizard", "Spock" to numbers
# as follows:
#
# 0 - rock
# 1 - Spock
# 2 - paper
# 3 - lizard
# 4 - scissors

# Exceptions
class NotDefinedError(Exception):
    pass

# Global variables
_NAME_LIST = ['rock', 'Spock', 'paper', 'lizard', 'scissors']
_DICT_NAME_TO_NUM = dict([name, idx] for idx, name in enumerate(_NAME_LIST))


# Helper functions
def name_to_number(name):
    '''Convert name of choice into relative number'''
    # The if/elif/else statements are ugly!
    try:
        return _DICT_NAME_TO_NUM[name]
    except KeyError:
        raise KeyError, "Valid inputs are: %s" % _NAME_LIST


def number_to_name(number):
    '''Convert integer number into relative choice string'''
    # Use the built-in list exceptions to handle wrong inputs
    return _NAME_LIST[number]


def rpsls(player_choice):
    '''Main implementation of rock-paper-scissors-lizard-Spock
Player's choice is passed via parameter and computer's
choice is random.

Para:
    player_choice : string
Returns:
    None. Results will be printed
Raises:
    KeyError if player_choice is not valid
    NotDefinedError if the determine process didn't cover the situation
    '''
    # Print player's choice and convert it into integer
    print
    print 'player chooses %s' % player_choice
    player_number = name_to_number(player_choice)

    # Generate random guess and print computer's choice
    import random
      # use len() expression instead of hard code 5 for flexibility
      # Change the _NAME_LIST and change the determine process then
      # you will get your own variant version.
    comp_number = random.randrange(0, len(_NAME_LIST))
    comp_choice = number_to_name(comp_number)
    print 'Computer chooses %s' % comp_choice

    # Determine process
    diff = (player_number - comp_number) % len(_NAME_LIST)
    if diff in [1, 2]:
        print 'Player wins!'
    elif diff in [3, 4]:
        print 'Computer wins!'
    elif diff is 0:
        print 'Player and computer tie!'
    else:
        raise NotDefinedError, diff # in case of variant version


def main():
    '''Tests'''
    rpsls("rock")
    rpsls("Spock")
    rpsls("paper")
    rpsls("lizard")
    rpsls("scissors")


if __name__ == '__main__':
    main()

