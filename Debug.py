# This file contains additional functionalities
# for debugging purposes only
import os


class DebugValue:
    def __init__(self):
        self.value = 0

    def add_value(self):
        self.value += 1


def WriteToFile(data):
    with open("Debug.txt", "a") as f:
        f.write("\n"+data)


def DeleteDebugFile():
    os.system("del Debug.txt")


def DrawPuzzle(shape, puzzle):
    counter = 0
    additional = []
    new_list = additional+puzzle
    print("_________________________")
    for i in range(shape):
        for j in range(shape):
            print("\t", end="")
            if new_list[j+counter] != 0 and new_list[j+counter] != 10:
                print(new_list[j+counter], end="\t")
            else:
                print("[X]", end="\t")
        counter += shape
        print("")
        print("_________________________")


def DrawPuzzleToFile(shape, puzzle):
    counter = 0
    additional = []
    new_list = additional+puzzle
    with open("Debug.txt", "a") as f:
        f.write("_________________________")
        for i in range(shape):
            for j in range(shape):
                f.write("\t")
                if new_list[j+counter] != 0 and new_list[j+counter] != 10:
                    f.write(f"{new_list[j+counter]}\t")
                else:
                    f.write("[X]\t")
            counter += shape
            f.write("")
            f.write("_________________________")
