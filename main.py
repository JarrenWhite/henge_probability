from itertools import product
from collections import Counter
from tqdm import tqdm

# Static Factors
ROLL_COUNT = 0
DICE_VALUES = range(0, 10)

# Adjusting Factors
DICE_NUMBER = 1
REROLL = True
NUDGE = True


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


def reroll_and_nudge_dice(roll):
    print("Reroll and nudge dice does nothing")
    return [evaluate_roll(roll)]


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


if __name__ == "__main__":
    all_rolls = roll_all_dice()
    if REROLL and NUDGE:
        ROLL_COUNT *= 10
        result_list = []
        for result in tqdm(all_rolls):
            result_list.extend(reroll_and_nudge_dice(result))
    elif NUDGE:
        result_list = [nudge_dice(result) for result in tqdm(all_rolls)]
    elif REROLL:
        ROLL_COUNT *= 10
        result_list = []
        for result in tqdm(all_rolls):
            result_list.extend(reroll_dice(result))
    else:
        result_list = [evaluate_roll(result) for result in tqdm(all_rolls)]

    mean = calculate_mean(result_list)
    print("Mean:")
    print(mean)
    print("Standard Deviation:")
    print(calculate_sd(result_list, mean))
    print("Mode")
    print(calculate_mode(result_list))
    sorted_result_list = sort_data(result_list)
    print("Iq Range")
    print(calculate_lq(sorted_result_list))
    print(calculate_median(sorted_result_list, ROLL_COUNT))
    print(calculate_uq(sorted_result_list))
