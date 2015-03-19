"""
Merge function for 2048 game.
"""

def merge(line):
    """
    Function that merges a single row or column in 2048.
    """
    # replace with your code

    if len(line) < 2:
        return line

    result_line = [0] * len(line)
    last_merge = False

    for origin_line_index in range(0, len(line)):
        if line[origin_line_index] != 0:

            for new_line_index in range(0, len(result_line)):
                if result_line[new_line_index] == 0:
                    result_line[new_line_index] = line[origin_line_index]
                    last_merge = False
                    break
                elif result_line[new_line_index+1] == 0:
                    if result_line[new_line_index] == line[origin_line_index] and last_merge == False:
                        result_line[new_line_index] += line[origin_line_index]
                        last_merge = True
                        break

    return result_line

# print merge([2, 0, 2, 4]) == [4, 4, 0, 0]
# print merge([0, 0, 2, 2]) == [4, 0, 0, 0]
# print merge([2, 2, 0, 0]) == [4, 0, 0, 0]
# print merge([2, 2, 2, 2]) == [4, 4, 0, 0]
# print merge([8, 16, 16, 8]) == [8, 32, 8, 0]