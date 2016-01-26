import sys
import numpy as np
from Queue import Queue

# class set todo for speed improvement?
def read_input():
    m, n = -1, -1
    rv_data = np.zeros((1,1))

    for i, line in enumerate(sys.stdin):
        if i == 0:
            m, n = line.split(' ')
            rv_data = np.zeros((int(n), int(m)))
        else:
            rv_data[i-1][:] = line.split(' ')
    return rv_data

def print_input(rv_data):
    print len(rv_data[1]), len(rv_data)
    for row in rv_data:
        print row
    
def find_rv_inverses(rv_data):
    rv_inverse = [None] * len(rv_data)
    
    for rv_index, X in enumerate(rv_data):
       d = dict()
       for i, value in enumerate(X):
           if d.has_key(value):
               d[value].add(i)
           else:
               d[value] = set([i])
       for key in d:
           d[key] = frozenset(d[key])
       rv_inverse[rv_index] = d
    return rv_inverse
    
huge_intersection_cache = dict()
def intersect(sets, new_set):
    S = sets.union(frozenset([new_set])) # set of sets being intersected
    if S in huge_intersection_cache:
        return huge_intersection_cache[S]
    else:
        huge_intersection_cache[S] = huge_intersection_cache[sets].intersection(new_set)
        return huge_intersection_cache[S]
        
class state:
    """
    k = number of rv being considered at one time
    parent = previously computed state
    children = next states computed
    prior = set of sets known to be independent
    posterior = set testing to be independent of the prior
    rv_used = the random variables being considered in this branch
    """
    space_size = -1
    def __init__(self, original=None, new_set=None, rv_of_new=None):
        self.parent = original
        if original is not None:
            original.children.append(self)
            if original.k == 1:
                self.prior = frozenset([original.posterior])  #a hack... should fix better
            else:
                self.prior = original.prior.union(frozenset([original.posterior]))
            self.rv_used = original.rv_used + [rv_of_new]
            self.cur_intersection = None
            self.k = original.k + 1
        else:
            self.prior = frozenset([])
            self.rv_used = [rv_of_new]
            self.cur_intersection = new_set
            huge_intersection_cache[frozenset([new_set])] = new_set
            self.k = 1
        self.posterior = new_set
        self.children = list()

    def check_independence(self):
        if self.parent is None:
            return True
        self.cur_intersection = intersect(self.prior, self.posterior)
        return len(self.cur_intersection) * state.space_size == len(self.parent.cur_intersection) * len(self.posterior)
        
    def successors(self):
        suc = list()
        for rv_index, rv in enumerate(rv_inverse):
            if rv_index not in self.rv_used:  # can't compare X=1 ind? X=2
                for value in rv:
                    suc.append(state(self, rv[value], rv_index))
        return suc

# rv_data = read_input()
rv_data = np.array([[1,1,1,1,0,0,0,0],
                    [1,1,0,0,1,1,0,0],
                    [1,0,1,0,1,0,1,0]])
state.space_size = len(rv_data[0])        
print_input(rv_data)

rv_inverse = find_rv_inverses(rv_data)

q = Queue()
for rv_index, rv in enumerate(rv_inverse):
    for val in rv:
        q.put(state(new_set=rv[val], rv_of_new=rv_index))
        
max_k = len(rv_data)
while not q.empty():
    s = q.get()
    if not s.check_independence():
        max_k = s.k-1
        break
    else:
        succ = s.successors()
        for t in succ:
            q.put(t)

print max_k