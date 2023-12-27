from itertools import product
import statistics

# Static Factors
ROLL_COUNT = 0
DICE_VALUES = range(0, 10)

# Adjusting Factors
DICE_NUMBER = 7
MEAN = 27.68827
# Required for Standard Deviation


def roll_all_dice():
    global ROLL_COUNT
    ROLL_COUNT = len(DICE_VALUES) ** DICE_NUMBER
    all_permutations = list(product(DICE_VALUES, repeat=DICE_NUMBER))
    result = [list(perm) for perm in all_permutations]
    return result


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
    return statistics.mode(numbers)


def sort_data(numbers):
    return sorted(numbers)


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


result_list = [evaluate_roll(result) for result in roll_all_dice()]

print(calculate_sd(result_list, MEAN))
