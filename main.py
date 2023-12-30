from itertools import product
from collections import Counter
from tqdm import tqdm

# Static Factors
ROLL_COUNT = 0
DICE_VALUES = range(0, 10)

# Adjusting Factors
DICE_NUMBER = 5
REROLL = True
NUDGE = True

# Broken Rolls
# [0, 0, 2, 3, 3, 4]
# [0, 0, 2, 3, 3]
# [0, 0, 2, 3, 3, 5]
test_roll = [0, 0, 2, 3, 3]


def roll_all_dice():
    global ROLL_COUNT
    ROLL_COUNT = len(DICE_VALUES) ** DICE_NUMBER
    all_permutations = list(product(DICE_VALUES, repeat=DICE_NUMBER))
    return [list(perm) for perm in all_permutations]


def reroll_dice(roll):
    # If only 1 dice, only reroll if under mean
    if DICE_NUMBER == 1:
        if roll[0] <= 4:
            return [10, 11, 12, 13, 14, 15, 16, 17, 18, 19]
        else:
            value = evaluate_roll(roll)
            return [value, value, value, value, value, value, value, value, value, value]

    # If more than 1 dice, count values
    dice_counts = Counter(sort_data(roll, True)).most_common()

    # If all dice are the same, do not re-roll
    if len(dice_counts) == 1:
        value = evaluate_roll(roll)
        return [value, value, value, value, value, value, value, value, value, value]

    # Re-roll lowest value with lowest count
    # Get average of all possible re-rolled values
    best_counts = dice_counts[:-1]
    minimum_result = evaluate_roll(roll)
    new_rolls = [max(pair[0] + ((pair[1]+1) * 10), minimum_result) for pair in best_counts]
    while len(new_rolls) < 10:
        new_rolls.append(minimum_result)
    return new_rolls


def nudge_up(number):
    if number == 9:
        return 0
    else:
        return number + 1


def nudge_down(number):
    if number == 0:
        return 9
    else:
        return number - 1


def nudge_dice(roll):
    # If only 1 dice, nudge to best value
    if DICE_NUMBER == 1:
        if roll[0] == 0:
            return 19
        else:
            return min(19, roll[0] + 11)

    # If more than 1 dice, try nudging every value up & down
    all_roll_variants = [[] for _ in range(DICE_NUMBER * 2)]
    i = 0
    for value in roll:
        for j in range(len(all_roll_variants)):
            if j != i and j != i + DICE_NUMBER:
                all_roll_variants[j].append(value)

        all_roll_variants[i].append(nudge_up(value))
        all_roll_variants[i + DICE_NUMBER].append(nudge_down(value))
        i += 1

    # Evaluate all results and return best one
    best_result = 0
    for attempt in all_roll_variants:
        total_value = evaluate_roll(attempt)
        if total_value > best_result:
            best_result = total_value
    return best_result


def brute_force_nudge_and_reroll(roll):
    all_base_rolls = [roll[:i] + roll[i+1:] for i in range(len(roll))]

    # Case if "as is" is best strategy
    best_total_so_far = nudge_dice(roll) * 10
    best_rolls = [nudge_dice(roll) for _ in range(10)]

    for base_roll in all_base_rolls:
        re_rolled = [nudge_dice(base_roll.copy() + [i]) for i in range(10)]
        new_total = sum(re_rolled)
        if new_total > best_total_so_far:
            print(base_roll)
            best_total_so_far = new_total
            best_rolls = re_rolled

    return best_rolls


def reroll_and_nudge_dice(roll):
    # If only 1 dice, only reroll if under mean
    if DICE_NUMBER == 1:
        if roll[0] <= 4:
            return [19, 12, 13, 14, 15, 16, 17, 18, 19, 19]
        else:
            if roll[0] == 0:
                return [19, 19, 19, 19, 19, 19, 19, 19, 19, 19]
            else:
                value = min(19, roll[0] + 11)
                return [value, value, value, value, value, value, value, value, value, value]

    # If more than 1 dice, count values
    base_roll = []
    dice_counts = Counter(sort_data(roll, reverse=True))

    # If all dice are the same, do not re-roll or nudge
    if len(dice_counts) == 1:
        value = evaluate_roll(roll)
        return [value, value, value, value, value, value, value, value, value, value]

    # Find all dice which are not in groups, and all dice that are not nudge candidates
    more_than_once = [num for num, count in dice_counts.items() if count > 1]
    nudge_requirements = set()
    for value in roll:
        nudge_requirements.add(nudge_up(value))
        nudge_requirements.add(nudge_down(value))

    # Find dice which is not grouped, and not a nudge candidate, re-roll lowest (non-zero) dice
    unique_dice = [num for num, count in dice_counts.items() if (count == 1)]
    reroll_candidates = [num for num in unique_dice if (num not in nudge_requirements) and (num not in more_than_once)]
    if len(reroll_candidates) > 0:
        sorted_list = sort_data(reroll_candidates, reverse=True)
        if sorted_list[-1] == 0:
            dice_to_reroll = sorted_list[-2]
        else:
            dice_to_reroll = sorted_list[-1]
        base_roll = [item for item in roll if item != dice_to_reroll]

    # If all grouped, determine smallest value group, re-roll one of its dice
    if base_roll == [] and len(unique_dice) == 0:
        grouped_dice = dice_counts.most_common()
        lowest_value_group = grouped_dice[-1][0]

        for num, count in grouped_dice:
            if num == lowest_value_group:
                for _ in range(count - 1):
                    base_roll.append(num)
            else:
                for _ in range(count):
                    base_roll.append(num)

    # If all nudge candidates, reroll smallest non-zero value
    # (Unless only two dice, then the nudge will correct)
    if base_roll == [] and all(value in nudge_requirements for value in roll):
        # If only two dice, allow the nudge to correct
        if DICE_NUMBER == 2:
            value = nudge_dice(roll)
            return [value for _ in range(10)]

        # Otherwise, re-roll the smallest non-zero value
        sorted_list = sort_data(roll)
        if sorted_list[-1] == 0:
            dice_to_reroll = sorted_list[-2]
        else:
            dice_to_reroll = sorted_list[-1]
        base_roll = [item for item in roll if item != dice_to_reroll]

    # All in group OR nudgeable
    # One group, one outlier - no re-roll, then nudge
    # One group, several outliers - reroll any outlier, then nudge
    # Multiple groups, one outlier - if outlier can make strongest group: reroll from other group, then nudge
    #                              - else reroll it, then nudge
    # Multiple groups, multiple outliers - if an outlier can make strongest group, reroll another outlier, then nudge
    #                                    - else reroll any outlier, then nudge

    # Roll a dice & add to all bases
    new_rolls = [base_roll.copy() for _ in range(10)]
    for reroll in DICE_VALUES:
        new_rolls[reroll].append(reroll)
    # Nudge all versions of re-rolled dice
    return [nudge_dice(new_roll) for new_roll in new_rolls]


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


def calculate_sd(numbers, mean_in):
    squared_diff = sum((x - mean_in) ** 2 for x in numbers)
    variance = squared_diff / ROLL_COUNT
    return variance ** 0.5


def calculate_mode(numbers):
    data = Counter(numbers)
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


print(brute_force_nudge_and_reroll([1, 2, 2, 3, 5]))

# if __name__ == "__main__":
#     all_rolls = roll_all_dice()
#     if REROLL and NUDGE:
#         ROLL_COUNT *= 10
#         result_list = []
#         for result in tqdm(all_rolls):
#             result_list.extend(reroll_and_nudge_dice(result))
#     elif NUDGE:
#         result_list = [nudge_dice(result) for result in tqdm(all_rolls)]
#     elif REROLL:
#         ROLL_COUNT *= 10
#         result_list = []
#         for result in tqdm(all_rolls):
#             result_list.extend(reroll_dice(result))
#     else:
#         result_list = [evaluate_roll(result) for result in tqdm(all_rolls)]

    # mean = calculate_mean(result_list)
    # print("Mean:")
    # print(mean)
    # print("Standard Deviation:")
    # print(calculate_sd(result_list, mean))
    # print("Mode")
    # print(calculate_mode(result_list))
    # sorted_result_list = sort_data(result_list)
    # print("Iq Range")
    # print(calculate_lq(sorted_result_list))
    # print(calculate_median(sorted_result_list, ROLL_COUNT))
    # print(calculate_uq(sorted_result_list))
