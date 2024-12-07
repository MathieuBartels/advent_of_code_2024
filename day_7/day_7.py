def read_input(file_path):
    with open(file_path, "r") as file:
        return file.read()


def parse_input(input_data):
    for line in input_data.split("\n"):
        yield int(line.split(":")[0]), [
            int(value) for value in line.split(":")[1].strip().split(" ")
        ]


def combine_values(current_values, input_value):
    try:
        return int(str(int(current_values)) + str(int(input_value)))
    except:
        print(current_values, input_value)
        raise ValueError("Invalid values")


def can_be_matched(test_value, input_values):
    first_value = input_values.pop(0)
    current_values = [first_value]
    for input_value in input_values:
        new_values = []
        for current_value in current_values:
            new_values.append(current_value * input_value)

            new_values.append(current_value + input_value)

            new_values.append(combine_values(current_value, input_value))

        current_values = new_values
        # print(current_values)
    if test_value in current_values:
        # print("True ")
        return True
    # print("False")
    return False


if __name__ == "__main__":
    # input_data = read_input("samples/sample.txt")
    input_data = read_input("samples/challange.txt")
    test_values_of_matched = 0
    for test_value, input_values in parse_input(input_data):
        if can_be_matched(test_value, input_values):
            test_values_of_matched += test_value
    print(test_values_of_matched)
