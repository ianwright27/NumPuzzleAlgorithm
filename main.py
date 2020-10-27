# Author: Ian Wright
import random
import DetectPositions  # This module contains the game's AI
from LinkedLists import DoubleLinkedList as DLL
import Debug


class BestOutcome:
    def __init__(self, value, initial_pos, current_pos, array, score):
        self.list = array
        self.value = value
        self.score = score
        self.initial_pos = initial_pos
        self.current_pos = current_pos
        self.steps_jumped = current_pos - initial_pos
        self.comment = f"Move {self.list[current_pos]}"


class DiscoveryLimit:
    def __init__(self):
        self.swap_value = 0
        self.swap_list = []
        self.limit = 0
        self.sorting_score = 0

    def add_limit(self):
        self.limit += 1

    def choose_new_outcome(self):
        while True:
            new_val = random.choice(self.swap_list)
            if random.choice(self.swap_list) != self.swap_value:
                self.swap_value = new_val
                break

    def swap_elements(self, shape, puzzle):
        space = (shape*shape)+1
        space_pos = puzzle.index(space)
        elem_pos = puzzle.index(self.swap_value)
        puzzle[space_pos] = self.swap_value
        puzzle[elem_pos] = space
        self.sorting_score = DetectPositions.check_order(puzzle)
        return puzzle


debug_value = Debug.DebugValue()
discovery = DiscoveryLimit()


def PlayGame(shape, puzzle):
    global debug_value
    if debug_value.value > 50000:
        return
    else:
        debug_value.add_value()
        Debug.WriteToFile(str(puzzle))
        # Debug.DrawPuzzle(shape, puzzle)
        # print("\n")
        global moves
        space = (shape * shape) + 1

        corner = []
        sides = DetectPositions.determine_sides(shape, puzzle, corner)
        center = DetectPositions.determine_center(shape, puzzle)

        Debug.WriteToFile("DebugLog 1 [Already detected all elements in corners and sides]")
        # detecting swappable elements
        swappable_elements = []
        if space in sides:
            if space in corner:
                swappable_elements = DetectPositions.DetectElementsFromCorner(shape, puzzle)
            else:
                swappable_elements = DetectPositions.DetectElementsFromSides(shape, puzzle)
        else:
            swappable_elements = DetectPositions.DetectElementsFromCenter(shape, puzzle)

        Debug.WriteToFile("DebugLog 2 [Already found position of center and swappable elements]")
        Debug.WriteToFile("\t Swappable elements: " + str(swappable_elements))
        # And now lets determine which element in the list brings the best outcome
        best_outcome = DetectPositions.determine_best_outcome(swappable_elements, shape, puzzle)
        best_move = BestOutcome(best_outcome['value'],
                                best_outcome['init_pos'], best_outcome['current_pos'],
                                best_outcome['list'], best_outcome['score'])

        # Invoke DiscoveryLimit object in case of repetitive best outcomes
        discovery.swap_value = best_outcome['value']
        discovery.swap_list = swappable_elements
        discovery.add_limit()
        if discovery.limit > 3:
            discovery.choose_new_outcome()
            best_move = BestOutcome(discovery.swap_value,
                                    puzzle.index(discovery.swap_value),
                                    puzzle.index((shape*shape)+1),
                                    discovery.swap_elements(shape,puzzle),
                                    discovery.sorting_score)
            discovery.limit = 0

        # Continue debugging
        Debug.WriteToFile("DebugLog 3 [Found the best outcome]")
        Debug.WriteToFile(f"\tBest Outcome: {best_move.value}")
        moves.insert_at_end(best_move)

        # Time to play the move
        latest_node = moves.last  # Get best outcome
        new_puzzle = latest_node.data.list  # Restructure puzzle

        Debug.WriteToFile("DebugLog 4 [New puzzle comes from the one created in the best outcome]")
        Debug.WriteToFile(f"\tNew puzzle: {str(latest_node.data.list)}")
        # Find out whether we won
        if int(latest_node.data.score) == highest_score:
            print("Game Analysis Complete")
            print("--------------------------")
            print("Solution: ")
            print("==========")
            moves.list_items(reverse=False)  # List instructions
            print(f"\n\n\n steps: {debug_value.value}\n")
        else:
            Debug.WriteToFile("DebugLog 5 [Another Function Call]")
            PlayGame(shape, new_puzzle)

        # Debug.DeleteDebugFile()


if __name__ == "__main__":
    moves = DLL()
    shape = 3  # 3x3 puzzle
    space = (shape * shape) + 1
    # variable "space" marks the space
    puzzle = [1, 2, 3, 4, 8, 5, 7, space, 6]
    puzzle = [1, 2, 3, 4, 5, 6, 7, space, 8]
    puzzle = [2, space,3,1,4,6,7,5,8]
    # puzzle = [1, 3, 2, 5, space, 6, 7, 4, 8]
    # puzzle = [2, 3, space, 5, 1, 6, 7, 4, 8]
    # puzzle = [3,5,space,7,6,4,8,1,2]
    # puzzle = [5,2,1,8,7,4,6, space, 3]
    # sorting score
    sorting_score = DetectPositions.check_order(puzzle)
    # highest possible score for complete game
    highest_score = (shape * shape) - 2
    # play the game
    try:
        PlayGame(shape, puzzle)
    except RecursionError:
        pass
