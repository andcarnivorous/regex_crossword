import string
import re
import numpy as np


LETTERS = list(string.ascii_uppercase)

SPECIAL_CHARS = [r"+", r"*", r".*"]
SQUARE_BRACKETS = ["[{}]*", "[{}]+"]
REGEXIS = SPECIAL_CHARS + LETTERS

flag = False

SPICES = {1: 0, 2: -1, 3: -2}


class PuzzleGenerator(object):

    def __init__(self, size: int):
        self.letters_matrix = np.random.choice(LETTERS,  size=(size, size))
        self.solution = list(self.letters_matrix.flatten())
        self.empty_matrix = np.empty((size, size), dtype="<U10")
        self.columns = self.columns_to_strings()
        self.rows = self.rows_to_strings()
        self.cols_expressions = self.generate_regexes(self.columns)
        self.cols_expressions = list(map(self.collapse_duplicated_chars, self.cols_expressions))
        self.rows_expressions = self.generate_regexes(self.rows)
        self.rows_expressions = list(map(self.collapse_duplicated_chars, self.rows_expressions))
        self.add_more_spice()

    @staticmethod
    def base_expression(raw_string: str):
        """Generate first round of expressions"""
        candidates = []
        for i in range(1, len(raw_string)-1):
            for j in SPECIAL_CHARS:
                match = re.match(raw_string[:i]+j, raw_string)
                if match and match.span()[1] == len(raw_string):
                    candidates.append(raw_string[:i]+j)
        return candidates

    def add_spice(self, raw_string: str):
        """This adds a square bracket expression to the regex, only to use as deception or SOMETIMES for strings with duplicate letters e.g. HHRGBN"""
        new_candidates = []
        set_raw_string = list(set(list(raw_string)))
        for square_bracket in SQUARE_BRACKETS:
            for i in range(len(set_raw_string)-1):
                for j in range(len(raw_string)+1):
                    pattern = raw_string[:j] + square_bracket.format(set_raw_string[i]) + raw_string[j:]
                    pattern = self.check_remove_next_chars(pattern)
                    match = re.match(pattern, raw_string)
                    if match and match.span()[1] == len(raw_string):
                        new_candidates.append(pattern)
        return new_candidates

    @staticmethod
    def check_remove_next_chars(pattern: str):
        """I don't remember why I have this"""
        try:
            idx = pattern.index("*")
        except ValueError:
            idx = pattern.index("+")
        if idx < len(pattern) - 1:
            flag = False
            letter = pattern[idx-2]
            i = idx + 1
            while not flag:
                try:
                    if pattern[i] == letter:
                        pattern = list(pattern)
                        pattern.pop(i)
                        pattern = "".join(pattern)
                    else:
                        flag = True
                except IndexError:
                    flag = True
        return pattern

    def columns_to_strings(self):
        """Extracts list of strings from matrix cols"""
        size = self.letters_matrix.shape[1]
        columns_strings = [""] * size
        for i in range(size):
            columns_strings[i] = "".join(self.letters_matrix[:, i])
        return columns_strings

    def rows_to_strings(self):
        """Extracts list of strings from matrix rows"""
        size = self.letters_matrix.shape[0]
        columns_strings = [""] * size
        for i in range(size):
            columns_strings[i] = "".join(self.letters_matrix[i, :])
        return columns_strings

    def generate_regexes(self, list_of_strings: list):
        """Generate the base regex expressions for the random strings, choose the shortest expressions since they can have more regex special chars."""
        output_list = []
        for raw_string in list_of_strings:
            candidates = self.base_expression(raw_string)
            candidates = self.add_spice(raw_string)
            shortest = min(candidates, key=lambda x: len(x))
            output_list.append(shortest)
        return output_list

    def add_more_spice(self):
        """Adds a random .* to a col or row in one of the possible idx of constant SPICES"""
        counter = 0
        for row, col in zip(self.rows_expressions, self.cols_expressions):
            if np.random.randint(10) % 2:
                idx = SPICES[np.random.randint(1, 3)]
                to_avoid = (len(row), len(row) - 1)
                special_idx = row.index("*") if "*" in col else row.index("+")
                spice = ".*" if special_idx not in to_avoid else ""
                row = row[:idx] + spice + row[idx:]
            else:
                idx = SPICES[np.random.randint(1, 3)]
                to_avoid = (len(col), len(col) - 1)
                special_idx = col.index("*") if "*" in col else col.index("+")
                spice = ".*" if special_idx not in to_avoid else ""
                col = col[:idx] + spice + col[idx:]
            row, col = self.mess_up_common(row, col)
            self.rows_expressions[counter] = row
            self.cols_expressions[counter] = col
            counter += 1

    @staticmethod
    def mess_up_common(row: str, col: str):
        """If a character is the same in row and col at same point, make it a [AB] in one of the two."""
        shorter = min([col, row], key=lambda x: len(x))
        randlett = np.random.choice(LETTERS)
        for i in range(len(shorter)):
            if col[i].isalpha() and col[i] == row[i] and col[i-1] != "[" and row[i-1] != "[":
                if np.random.randint(10) % 2:
                    col = f"{col[:i]}[{randlett + col[i]}]" if i == len(shorter) else f"{col[:i]}[{randlett + col[i]}]" + col[i+1:]
                    break
                else:
                    row = f"{row[:i]}[{randlett + row[i]}]" if i == len(shorter) else f"{row[:i]}[{randlett + row[i]}]" + row[i+1:]
                    break
        return row, col

    @staticmethod
    def collapse_duplicated_chars(expression: str):
        """if the next character is the same as the current, collapse them into a [A]+"""
        for idx in range(len(expression)-1):
            if expression[idx].isalpha() and expression[idx] == expression[idx+1]:
                expression = f"{expression[:idx]}[{expression[idx]}]+{expression[idx+2:]}"
        return expression
