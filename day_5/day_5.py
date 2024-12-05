from collections import defaultdict


class Rule:
    def __init__(self, line):
        rule_parts = line.split("|")
        self.before = int(rule_parts[0].strip())
        self.after = int(rule_parts[1].strip())

    def __repr__(self):
        return f"{self.before} | {self.after}"


def read_file(file_path):
    with open(file_path, "r") as file:
        return file.read()


def parse_rules(content):
    rules = []
    for line in content.split("\n"):
        if "|" in line:
            rules.append(Rule(line))
    return rules


def parse_print_jobs(content):
    print_jobs = []
    for line in content.split("\n"):
        print_job = []
        if "|" not in line and line != "":
            for number in line.split(","):
                print_job.append(int(number.strip()))
            print_jobs.append(print_job)
    return print_jobs


def is_job_valid(print_job, before_after_map, after_before_map):
    seen_numbers = set()
    unvalid_numbers = set()

    for number in print_job:

        if number in after_before_map:
            for before_number in after_before_map[number]:
                unvalid_numbers.add(before_number)

        if number in before_after_map:
            for after_number in before_after_map[number]:
                if after_number in seen_numbers:
                    return False

        seen_numbers.add(number)

    return True


def get_middle_number_of_job(print_job):
    return print_job[len(print_job) // 2]


# content = read_file('samples/sample_1.txt')
content = read_file("samples/challange.txt")

rules = parse_rules(content)
print_jobs = parse_print_jobs(content)

before_after_map = defaultdict(list)
after_before_map = defaultdict(list)
for rule in rules:
    before_after_map[rule.before].append(rule.after)
    after_before_map[rule.after].append(rule.before)


count = 0
for print_job in print_jobs:
    if is_job_valid(print_job, before_after_map, after_before_map):
        middle_number = get_middle_number_of_job(print_job)
        count += middle_number

print(count)


def make_job_valid_by_switching_numbers(print_job, before_after_map, after_before_map):
    seen_numbers = set()
    unvalid_numbers = set()

    for number in print_job:

        if number in after_before_map:
            for before_number in after_before_map[number]:
                unvalid_numbers.add(before_number)

        if number in before_after_map:
            for after_number in before_after_map[number]:
                if after_number in seen_numbers:
                    before_number_index = print_job.index(after_number)
                    after_number_index = print_job.index(number)
                    print_job[before_number_index] = number
                    print_job[after_number_index] = after_number

        seen_numbers.add(number)

    return print_job


count = 0
for print_job in print_jobs:
    if is_job_valid(print_job, before_after_map, after_before_map):
        continue
    else:
        print_job = make_job_valid_by_switching_numbers(
            print_job, before_after_map, after_before_map
        )
        while not is_job_valid(print_job, before_after_map, after_before_map):
            print_job = make_job_valid_by_switching_numbers(
                print_job, before_after_map, after_before_map
            )
    middle_number = get_middle_number_of_job(print_job)
    count += middle_number

print(count)
