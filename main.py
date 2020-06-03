all_states = []
all_signs = []
final_state_name = "FINAL"

""" on_status on_sign direction new_sign new_state """


def parse(filename):
    code_file = open(filename, "r")
    lines = code_file.readlines()

    commands = {}

    for line in lines:
        tokens = line.split(" ")
        on_sign = tokens[1]
        on_state = tokens[0]
        direction = tokens[2]
        sign = tokens[3]
        state = tokens[4]

        state = state.replace("\n", "")

        if on_state == final_state_name:
            raise Exception("You are not allowed to define FINAL!")

        append_if_not_in_list(on_state, all_states)
        append_if_not_in_list(on_sign, all_signs)

        if state != final_state_name:
            append_if_not_in_list(state, all_states)
        append_if_not_in_list(sign, all_signs)

        if on_state not in commands.keys():
            commands[on_state] = {}

        if state != final_state_name:
            commands[on_state][on_sign] = [get_direction_bit(direction), all_signs.index(sign), all_states.index(state)]
        else:
            commands[on_state][on_sign] = [get_direction_bit(direction), all_signs.index(sign), 31]

    if len(all_states) > 19:
        print("Too many states!")
    elif len(all_signs) > 4:
        print("Too many signs")
    else:
        return commands


def sort_commands(commands):
    while len(all_signs) < 4:
        all_signs.append(-1)

    out = []
    for state in all_states:
        for sign in all_signs:
            if sign in commands[state].keys():
                out.append(commands[state][sign])
            else:
                out.append([1, 3, 31])
    return out


def get_direction_bit(direction):
    if direction == '<':
        return 0
    if direction == '>':
        return 1


def append_if_not_in_list(obj, lst):
    if obj not in lst:
        lst.append(obj)


def write(sorted_out_list):
    f = open("out.txt", "w")

    counter = 0

    for entry in sorted_out_list:

        out_str = "{}\t".format(counter * 1000)
        out_str += str(entry[0])
        out_str += "{0:02b}".format(entry[1]).replace("", " ")[: -1]
        out_str += "{0:05b}".format(entry[2]).replace("", " ")[:-1]

        print(out_str)
        out_str += '\n'
        f.write(out_str)

        counter += 8


result = parse('code.txt')
sorted_commands = sort_commands(result)
print(all_signs)
print(all_states)
print(len(sorted_commands))
write(sorted_commands)
