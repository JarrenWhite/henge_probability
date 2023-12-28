from itertools import product
from collections import Counter

# Static Factors
ROLL_COUNT = 0
DICE_VALUES = range(0, 10)

# Adjusting Factors
DICE_NUMBER = 1
MEAN = 27.68827  # Required for Standard Deviation
REROLL = True
NUDGE = False


def roll_all_dice():
    global ROLL_COUNT
    ROLL_COUNT = len(DICE_VALUES) ** DICE_NUMBER
    all_permutations = list(product(DICE_VALUES, repeat=DICE_NUMBER))
    result = [list(perm) for perm in all_permutations]
    return result


def reroll_dice(roll):
    # If only 1 dice, only reroll if under mean
    if DICE_NUMBER == 1:
        if roll[0] <= 4:
            return 14.5
        else:
            return evaluate_roll(roll)

    # If more than 1 dice, count values
    dice_counts = Counter(sort_data(roll, True)).most_common()

    # If all dice are the same, do not re-roll
    if len(dice_counts) == 1:
        return evaluate_roll(roll)

    # Re-roll lowest value with lowest count
    # Get average of all possible re-rolled values
    best_counts = dice_counts[:-1]
    minimum_result = evaluate_roll(roll)
    seen_value_rerolls = [max(pair[0] + ((pair[1]+1) * 10), minimum_result) for pair in best_counts]
    total_of_seen_values = sum(seen_value_rerolls)
    no_of_unseen_values = 10 - len(seen_value_rerolls)
    total_of_unseen_values = no_of_unseen_values * minimum_result
    result_average = (total_of_seen_values + total_of_unseen_values) / 10
    return result_average


def nudge_dice(roll):
    print("Nudge dice does nothing")
    return evaluate_roll(roll)


def reroll_and_nudge_dice(roll):
    print("Reroll and nudge dice does nothing")
    return evaluate_roll(roll)


def evaluate_roll(roll):
    counts = [0] * 10

    for result in roll:
        counts[result] += 1

    max_count = 0
    max_value = 0

    for i in range(len(counts)):
        if counts[i] >= max_count:
            max_count = counts[i]
            max_value = i

    return max_count * 10 + max_value


def calculate_mean(numbers):
    total = sum(numbers)
    return total / len(numbers)


def calculate_sd(numbers, mean):
    squared_diff = sum((x - mean) ** 2 for x in numbers)
    variance = squared_diff / ROLL_COUNT
    return variance ** 0.5


def calculate_mode(numbers):
    data = Counter(numbers)
    print(data.most_common())
    return data.most_common(1)[0][0]


def sort_data(numbers, reverse=False):
    return sorted(numbers, reverse=reverse)


def calculate_median(sorted_data, data_count):
    if data_count % 2 == 0:
        mid1 = sorted_data[data_count // 2 - 1]
        mid2 = sorted_data[data_count // 2]
        median = (mid1 + mid2) / 2
    else:
        median = sorted_data[data_count // 2]
    return median


def calculate_lq(sorted_data):
    data_count = ROLL_COUNT // 2
    lower_half = sorted_data[:data_count]
    return calculate_median(lower_half, data_count)


def calculate_uq(sorted_data):
    data_count = ROLL_COUNT // 2
    upper_half = sorted_data[-data_count:]
    return calculate_median(upper_half, data_count)


all_rolls = roll_all_dice()
if REROLL and NUDGE:
    result_list = [reroll_and_nudge_dice(result) for result in all_rolls]
elif NUDGE:
    result_list = [nudge_dice(result) for result in all_rolls]
elif REROLL:
    result_list = [reroll_dice(result) for result in all_rolls]
else:
    result_list = [evaluate_roll(result) for result in all_rolls]

print(calculate_mean(result_list))
# print(calculate_sd(result_list, MEAN))
# print(calculate_mode(result_list))

# sorted_result_list = sort_data(result_list)
# print(calculate_lq(sorted_result_list))
# print(calculate_median(sorted_result_list, ROLL_COUNT))
# print(calculate_uq(sorted_result_list))
