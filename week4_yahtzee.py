"""
Planner for Yahtzee
Simplifications:  only allow discard and roll, only score against upper level
"""

# Used to increase the timeout, if necessary
import codeskulptor
codeskulptor.set_timeout(20)

def gen_all_sequences(outcomes, length):
    """
    Iterative function that enumerates the set of all sequences of
    outcomes of given length.
    """

    answer_set = set([()])
    for dummy_idx in range(length):
        temp_set = set()
        for partial_sequence in answer_set:
            for item in outcomes:
                new_sequence = list(partial_sequence)
                new_sequence.append(item)
                temp_set.add(tuple(new_sequence))
        answer_set = temp_set
    return answer_set


def score(hand):
    """
    Compute the maximal score for a Yahtzee hand according to the
    upper section of the Yahtzee score card.

    hand: full yahtzee hand

    Returns an integer score
    """
    score_tuple = ()
    for each_count in hand:
        temp_score = each_count * hand.count(each_count)
        score_tuple = score_tuple + (temp_score, )

    return max(score_tuple)


def expected_value(held_dice, num_die_sides, num_free_dice):
    """
    Compute the expected value based on held_dice given that there
    are num_free_dice to be rolled, each with num_die_sides.

    held_dice: dice that you will hold
    num_die_sides: number of sides on each die
    num_free_dice: number of dice to be rolled

    Returns a floating point expected value
    """
    # As an example, in a standard Yahtzee game using five dice,
    # the length of held_dice + num_free_dice should always be five
    outcomes = [ number+1 for number in range(num_die_sides) ]
    possible_rolls = gen_all_sequences(outcomes, num_free_dice)
    expected_val = 0
    total_score = 0

    for each_roll in possible_rolls:
        total_dice = held_dice + each_roll
        total_score += score(total_dice)

    expected_val += total_score * 1.0 / len(possible_rolls)

    return expected_val


def gen_all_holds(hand):
    """
    Generate all possible choices of dice from hand to hold.

    hand: full yahtzee hand

    Returns a set of tuples, where each tuple is dice to hold
    """
    holds = set([()])

    if len(hand) != 0:
        temp_holds = hand[:-1]
        for each_tuple in gen_all_holds(temp_holds):
            holds.add(each_tuple)
            holds.add( (each_tuple + (hand[-1], )) )

    return holds



def strategy(hand, num_die_sides):
    """
    Compute the hold that maximizes the expected value when the
    discarded dice are rolled.

    hand: full yahtzee hand
    num_die_sides: number of sides on each die

    Returns a tuple where the first element is the expected score and
    the second element is a tuple of the dice to hold
    """
    holds_dict = {}
    possible_hold = gen_all_holds(hand)

    for each_hold in possible_hold:
        expected_val = expected_value(each_hold, num_die_sides, len(hand)-len(each_hold))
        holds_dict[each_hold] = holds_dict.get(each_hold, expected_val)

    temp_list = []
    for key, value in holds_dict.items():
        temp_list.append((value, key))

    return sorted(temp_list, reverse=True)[0]


def run_example():
    """
    Compute the dice to hold and expected score for an example hand
    """
    num_die_sides = 6
    hand = (1, 1, 1, 5, 6)
    hand_score, hold = strategy(hand, num_die_sides)
    print "Best strategy for hand", hand, "is to hold", hold, "with expected score", hand_score



run_example()


#import poc_holds_testsuite
#poc_holds_testsuite.run_suite(gen_all_holds)

