
def index_to_assignment(index, variable_names):
    assignment = {}
    bit_count = len(variable_names)
    for offset, name in enumerate(variable_names):
        shift = bit_count - 1 - offset
        assignment[name] = (index >> shift) & 1
    return assignment


def assignment_to_index(assignment, variable_names):
    value = 0
    for name in variable_names:
        value = (value << 1) | assignment[name]
    return value


def bit_mask_for_variable(variable, variable_names):
    position = variable_names.index(variable)
    shift = len(variable_names) - 1 - position
    return 1 << shift
