from collections import Counter


def read_file(file_path):
    with open(file_path, "r") as file:
        return file.read()


def parse_content(content):
    left_numbers = []
    right_numbers = []
    for line in content.split("\n"):
        line_list = line.split("   ")
        left_numbers.append(int(line_list[0].strip()))
        right_numbers.append(int(line_list[1].strip()))
    return left_numbers, right_numbers


content = read_file("challange.txt")
left_numbers, right_numbers = parse_content(content)

left_numbers.sort()
right_numbers.sort()


total_distance = 0
for left, right in zip(left_numbers, right_numbers):
    total_distance += abs(left - right)

print(total_distance)

left_counter = Counter(left_numbers)
right_counter = Counter(right_numbers)

sim_score = 0
for number, count in left_counter.items():
    if number not in right_counter:
        continue
    sim_score += number * right_counter[number]

print(sim_score)
