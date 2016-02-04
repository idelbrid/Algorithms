import sys
import numpy as np
import random

random.seed(123456789)
def read_input():
    n, m = -1, -1
    dnf = np.zeros((1, 1))
    precision = -1
    error_prob = -1

    for i, line in enumerate(sys.stdin):
        if i == 0:
            n, m = line.split(' ')
            dnf = np.zeros((int(m), int(n)))
        elif i < m - 2:
            for word in line.split(' '):
                j = np.abs(int(word))
                sign = int(word) / j
                dnf[i-1][j-1] = sign
        elif i < m - 1:
            precision = float(line.split(' '))
        else:
            error_prob = float(line.split(' '))
    return dnf, precision, error_prob


def sample(dnf, dummy=0):
    num_vars = len(dnf)
    num_clauses = len(dnf)

    i = random.randint(0, num_clauses - 1)
    clause = dnf[i]
    bound = np.abs(clause).sum()
    free = num_vars - bound
    free_choice = np.random.choice(np.array([-1, 1]), free)

    sat_choice = np.put(clause, clause.where(clause == 0), free_choice)
    for early_clause in dnf[:i]:
        comp = early_clause * sat_choice
        sat_early_clause = np.any(comp < 0)
        if sat_early_clause:
            return 0
    return 1

batch_sample = np.vectorize(sample)

def find_space_size(dnf):
    n = len(dnf[0])
    helper = lambda x : 2^(n - np.abs(x).sum())
    vec_helper = np.vectorize(helper)
    clause_options = vec_helper(dnf)
    return clause_options.sum()

if __name__ == "__main__":
    # F, epsilon, delta = read_input()
    F = np.array([[1, 2, 3], [-1, -2, -3]])  # fake input
    epsilon = 0.1
    delta = 0.01
    n, m = len(F), len(F[0])
    num_samples = int(-m * 1/epsilon * np.log(delta))
    tests = np.zeros(num_samples)
    # tests = batch_sample(tests, F)  # 2ill not work... vectorize goes with F as the array
    for indx in range(len(tests)):
        tests[indx] = sample(F)
    satisfiable_ratio = tests.sum() / float(len(tests))

    print satisfiable_ratio * find_space_size(F)


