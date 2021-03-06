#!/usr/bin/env python

import numpy as np

#penalty box
match    = 3
mismatch = -3
gap      = -2

#sequences. seq2 should always be larger than seq1
seq1 = 'TGTTACGG'
seq2 = 'GGTTGACTA'

#scoring matrix size
rows = len(seq1) + 1
cols = len(seq2) + 1

def create_score_matrix(rows, cols):
    '''
    Create a matrix of scores representing trial alignments of the two sequences.
    Sequence alignment can be treated as a graph search problem. This function
    creates a graph (2D matrix) of scores, which are based on trial alignments
    of different base pairs. The path with the highest cummulative score is the
    best alignment.
    '''
    score_matrix = [[0 for col in range(cols)] for row in range(rows)]
    # Fill the scoring matrix.
    max_score = 0
    max_pos   = None    # The row and columbn of the highest score in matrix.
    for i in range(1, rows):
        for j in range(1, cols):
            score = calc_score(score_matrix, i, j)
            if score > max_score:
                max_score = score
                max_pos   = (i, j)
            score_matrix[i][j] = score
    assert max_pos is not None, 'the x, y position with the highest score was not found'
    return score_matrix, max_pos

def calc_score(matrix, x, y):
    #Calculate score for a given x, y position in the scoring matrix.
    #The score is based on the up, left, and upper-left diagnol neighbors
    similarity = match if seq1[x - 1] == seq2[y - 1] else mismatch
    diag_score = matrix[x - 1][y - 1] + similarity
    up_score   = matrix[x - 1][y] + gap
    left_score = matrix[x][y - 1] + gap
    return max(0, diag_score, up_score, left_score)

def print_matrix(matrix):
    '''
    Print the scoring matrix.
    ex:
    0   0   0   0   0   0
    0   2   1   2   1   2
    0   1   1   1   1   1
    0   0   3   2   3   2
    0   2   2   5   4   5
    0   1   4   4   7   6
    '''
    print(np.matrix(matrix).T)

#add your function(s) to find a solution here.

def track_path(score_matrix, start_pos):
    cur_i, cur_j = start_pos
    result = []
    while not score_matrix[cur_i][cur_j] == 0:
        result.append([cur_i, cur_j])
        # Diagonal
        if seq1[cur_i - 1] == seq2[cur_j - 1] and \
        score_matrix[cur_i][cur_j] - score_matrix[cur_i - 1][cur_j - 1] == 3 or \
        not seq1[cur_i - 1] == seq2[cur_j - 1] and \
        score_matrix[cur_i][cur_j] - score_matrix[cur_i - 1][cur_j - 1] == -3:
            cur_i -= 1
            cur_j -= 1
        # Up
        elif score_matrix[cur_i][cur_j] + 2 == score_matrix[cur_i - 1][cur_j]:
            cur_i -= 1
        # Left
        else:
            cur_j -= 1
    result.append([cur_i, cur_j])
    return result

def print_path(path):
    s = ""
    for p in path:
        s += str(p) + " -> ";
    if not s == "": print(s[:-4])
    else: print("No matches.")

#end of your function(s)

if __name__ == '__main__':
    #my main
    score_matrix, start_pos = create_score_matrix(rows, cols)
    print_matrix(score_matrix)
    path = track_path(score_matrix, start_pos)
    print_path(path)
