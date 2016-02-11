import sys
import numpy as np

# np.random.seed(123456789)


def read_input():
    """
    Subroutine to read the input from stdin
    """
    n, m = -1, -1
    dnf = np.zeros((1, 1))
    precision = -1
    error_prob = -1

    for i, line in enumerate(sys.stdin):
        if i == 0:
            n, m = line.split(' ')
            n = int(n)
            m = int(m)
            dnf = np.zeros((int(m), int(n)), dtype=np.int8)
        elif i <= m:
            for word in line.split(' '):
                j = np.abs(int(word))
                sign = int(word) / j
                dnf[i-1][j-1] = sign
        elif i == m + 1:
            precision = float(line)
        else:
            error_prob = float(line)
    return dnf, precision, error_prob


def sample_choice_helper(dnf, space_size):
    num_vars = len(dnf[0])

    clause_indx = -1
    random_choice = np.random.randint(0, space_size)  # uniformly randomly choose which state
    while random_choice >= 0:  # finding the corresponding clause
        clause_indx += 1
        clause_freedom_size = 2 ** (num_vars - np.abs(dnf[clause_indx]).sum())
        random_choice -= clause_freedom_size

    clause = np.copy(dnf[clause_indx])
    random_choice += 2 ** (num_vars - np.abs(dnf[clause_indx]).sum())  # correcting remainder
    
    bound = np.abs(clause).sum()
    free = num_vars - bound
    
    # interpret remainder as bit to identify choice of free variables
    asbit = bin(random_choice).lstrip('-0b')  
    if len(asbit) < free:
        asbit += '0' * (free - len(asbit))
    choice_as_array = np.array([int(i) for i in asbit])
    choice_as_array[choice_as_array == 0] = -1
    return clause_indx, choice_as_array


def sample(dnf, space_size):
    """
    Pick random sample from sample space
        - a clause i and satisfying assigment sigma... 
    Decide if clause i is the first clause to be satisfied by sigma
    """
    
    # generate a sample from the space with uniform probability
    clause_ind, free_choice = sample_choice_helper(dnf, space_size) 
    clause = np.copy(dnf[clause_ind])
    
    sat_choice = clause
    sat_choice[clause == 0] = free_choice  # filling the free variables with the random choice
    
    for early_clause in dnf[:clause_ind]:  # testing all clauses up to this one
        comp = early_clause * sat_choice
        sat_early_clause = not np.any(comp < 0)
        if sat_early_clause:
            return 0
    return 1


def find_space_size(dnf):
    """
    Subroutine to go sum over each clause the dnf and find the number of
        satisfying assignments calculated by 2^(#free variables in clause)
    """
    n = len(dnf[0])
    helper = lambda x: 2 ** (n - np.abs(x).sum())  # num free

    clause_options = np.apply_along_axis(helper, 1, dnf)
    return clause_options.sum()

if __name__ == "__main__":
    F, epsilon, delta = read_input()  # real input

    # F = np.array([[1, 1, 1], [-1, -1, -1]])  # fake input 1

    # F = np.array([[1, 0, -1], [1, 1, 0]])  # fake input 2

    # F = np.array([[1, 1, 1, 1 , 0, 0, 0, 0, -1], #fake input 4
    #              [-1, 1, 1, 1, -1, 1, 1, 1, 1],
    #              [1, 1, 1, 1, 0, 0, 0, 0, 1]])

    n, m = len(F), len(F[0])
    num_samples = int(-1 * m * 1/epsilon ** 2 * np.log(delta))
    space_size = find_space_size(F)
    
    # tests = np.zeros(num_samples)
    # h = lambda x: sample(F, space_size)    # batch test
    # hvec = np.vectorize(h)                 # slower
    # tests = hvec(tests)
    # s = tests.sum()
    
    cumulative = 0    
    for indx in range(0, num_samples):  # One by one test samples...
        cumulative += sample(F, space_size)
        
    satisfiable_ratio = cumulative / float(num_samples)  # ratio 

    print satisfiable_ratio * space_size  # scale ratio by total sample space size
