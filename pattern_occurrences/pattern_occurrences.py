import sys
import numpy as np


def read_input(file=None):
    """
    :arg file: file object from which to read the input. If none, the it's assumed stdin
    :return list of patterns and list of strings
    """
    if file is None:
        file = sys.stdin
    n = int(file.next())  # num tests
    patterns = list()
    texts = list()
    for i, string in enumerate(file):
        if i % 2 == 0:
            patterns.append(string[:-1])  # don't include the newline
        else:
            texts.append(string[:-1])  # don't include the newline

    return patterns, texts


def get_zvalues(T):
    """

    :param P: pattern (string)
    :param T: text (string)
    :return: indices of pattern occurrences in the text
    """
    n = len(T)
    l = 0
    r = 0
    Z = np.zeros(n)
    for i in range(1, n):
        curchar = T[i]
        j = i - l  # j is "i prime"
        if i >= r:  # Little information about this region... set records
            k = 0
            while T[k] == T[i + k]:
                k += 1
                if len(T) <= i + k:
                    break
            # k -= 1
            Z[i] = k
            r = i + k
            l = i
        else:
            if Z[j] < r - i:  # not the best so far... use previous information
                Z[i] = Z[j]
            else:  # best in range -> calculate more, and set records!!
                k = r - i
                if len(T) > i + k:
                    while T[k] == T[i + k]:
                        k += 1
                        if len(T) <= i + k:
                            break
                # k -= 1
                Z[i] = k
                r = i + k
                l = i
    return Z


def find_occurrences(P, T):
    S = P + '\n' + T
    Z = get_zvalues(S)
    occurrences = list()
    for i in range(len(Z)):
        if i >= len(P)+1 and Z[i] >= len(P):
            occurrences.append(i - len(P) - 1)
    return occurrences


if __name__ == '__main__':
    if len(sys.argv) > 1:
        with open(sys.argv[1], 'r') as f:
            patterns, texts = read_input(f)
    else:
        patterns, texts = read_input()

    for pattern, text in zip(patterns, texts):
        occurrences = find_occurrences(pattern, text)
        print occurrences
        for occurrence in occurrences:
            snippet = ''
            for i in range(occurrence-15, occurrence + 15):
                snippet += text[i]
            print snippet
