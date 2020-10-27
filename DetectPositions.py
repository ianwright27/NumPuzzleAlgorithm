# This file powers the whole game's logic


# an algorithm to return the elements in the center
def determine_center(_shape, _puzzle):
    if _shape < 3:
        return _puzzle
    else:
        rem = 0
        limit = _shape * _shape
        center_elements = []
        sample_list = [i for i in range(_shape)]

        for i in range(_shape):
            if rem == 2:
                center_elements = sample_list
            else:
                sample_list.remove(sample_list[i])
                sample_list.remove(sample_list[len(sample_list) - 1])
                rem += 2

        full_center_elements = center_elements

        i = 1
        while i < limit:
            i += 3
            if i < limit:
                full_center_elements.append(i)
            else:
                break

        elements = [_puzzle[i] for i in full_center_elements]
        return elements


# an algorithm to return the elements in the sides and corners
def determine_sides(_shape, _puzzle, _corner):
    # Only by finding the sides
    # can we find the corner values as well
    left = []
    right = []
    i, j = 0, _shape - 1
    while i < len(_puzzle):
        if i > len(_puzzle):
            break
        else:
            left.append(_puzzle[i])
            right.append(_puzzle[j])
            i += _shape
            j += _shape
    # Append corners to global "corner"
    _corner.append(left[0])
    _corner.append(left[len(left) - 1])
    _corner.append(right[0])
    _corner.append(right[len(right) - 1])
    all_sides = left + right
    return all_sides


#  Detecting the position of the space / blank space (in center, sides or corner)

def DetectElementsFromCenter(shape, puzzle):
    space = (shape * shape) + 1
    space_index = puzzle.index(space)
    swap_list = []
    deviation_val_one = -shape
    deviation_val_two = -1
    for i in range(4):
        deviation = 0  # can be by 3 or 1
        if i + 1 < 3:
            deviation_val_one = -deviation_val_one
            deviation = deviation_val_one
        else:
            deviation_val_two = -deviation_val_two
            deviation = deviation_val_two
        element = space_index + deviation
        try:
            if puzzle[element] is not None and element > -1:
                swap_list.append(puzzle[element])
        except IndexError:
            pass
    return swap_list


def DetectElementsFromCorner(shape, puzzle):
    # detect elements in corner again
    corner = []
    sides = determine_sides(shape, puzzle, corner)

    # assign to two types
    left_corner = corner[:len(corner)-2]
    right_corner = corner[len(corner)-2:]

    space = (shape * shape) + 1
    space_index = puzzle.index(space)
    swap_list = []
    belongsToTop = False

    if space_index < shape:
        belongsToTop = True

    element_indices= []
    # deal with each accordingly
    if space in left_corner:
        e1 = puzzle.index(left_corner[0])
        e2 = puzzle.index(left_corner[-1])
        element_indices.append(e1+shape)
        element_indices.append(e1+1)
        element_indices.append(e2-shape)
        element_indices.append(e2+1)
    else:
        e1 = puzzle.index(right_corner[0])
        e2 = puzzle.index(right_corner[-1])
        element_indices.append(e1+shape)
        element_indices.append(e1-1)
        element_indices.append(e2-shape)
        element_indices.append(e2-1)

    if belongsToTop:
        elements = element_indices[:len(element_indices)-2]
    else:
        elements = element_indices[len(element_indices)-2:]
    for element in elements:
        try:
            if puzzle[element] is not None or puzzle[element] > 0:
                swap_list.append(puzzle[element])
        except IndexError:
            pass
    return swap_list


def DetectElementsFromSides(shape, puzzle):
    # detect elements in sides again
    sides = determine_sides(shape, puzzle, [])
    # split them to two lists
    left_side = sides[:len(sides)-shape]
    right_side = sides[len(sides)-shape:]
    element_indices = []
    left_elements = left_side[1:-1]
    right_elements = right_side[1:-1]
    space = (shape * shape) + 1
    swap_list = []

    belongsToLeft = False
    if space in left_side:
        belongsToLeft = True

    if belongsToLeft:
        for i in left_elements:
            i_pos = puzzle.index(i)
            element_indices.append(i_pos-shape)
            element_indices.append(i_pos+1)
            element_indices.append(i_pos+shape)
    else:
        for i in right_elements:
            i_pos = puzzle.index(i)
            element_indices.append(i_pos-shape)
            element_indices.append(i_pos-1)
            element_indices.append(i_pos+shape)

    for element in element_indices:
        try:
            if puzzle[element] is not None:
                swap_list.append(puzzle[element])
        except IndexError:
            pass
    return swap_list


# Algorithm to check whether the list is sorted
def check_order(_puzzle):
    _sorting_score = 0
    for i in range(len(_puzzle) - 1):
        current = _puzzle[i]
        next = _puzzle[i + 1]
        if next == (current + 1):
            _sorting_score += 1
    return _sorting_score


def determine_best_outcome(swappable_list, shape, puzzle):
    space = (shape * shape) + 1
    element_scores = []
    for i in swappable_list:
        _puzzle = []
        _puzzle = [i for i in puzzle]

        i_pos = _puzzle.index(i)
        space_pos = _puzzle.index(space)

        _puzzle[i_pos] = space
        _puzzle[space_pos] = i

        score = check_order(_puzzle)
        element_scores.append({
            'value': i, 'init_pos': i_pos,
            'current_pos': space_pos,
            'score': score,
            'list': _puzzle
        })
        _puzzle = []
    scores = [int(i['score']) for i in element_scores]
    winner = None
    for i in element_scores:
        if int(i['score']) == max(scores):
            winner = i
            break
    # we have our winner
    return winner
