import sys
import numpy as np
from Queue import Queue

# class set todo for speed improvement?
def read_input():  # read input to array from file(stdin)
    m, n = -1, -1
    rv_data = np.zeros((1,1))

    for i, line in enumerate(sys.stdin):
        if i == 0:
            m, n = line.split(' ')
            rv_data = np.zeros((int(n), int(m)))
        else:
            rv_data[i-1][:] = line.split(' ')
    return rv_data

class event:  # represents, e.g., the event where X=1
    next_id = 0
    cached_ints = dict()
    ind_events = dict()
    
    def __init__(self, atomic_events=None, intersected_events=None, 
                 intersected_events_ids=None):
        """
        atomic_events = elements of the set that the event describes
        intersected_events = events intersected to get this event
        intersected_events_ids = their ids
        self.size = number of atomic events
        self.id = serialized identification integer for the events
        self.ind = are the intersected events independent?
        """
        self.atomic_events = atomic_events
        self.size = len(atomic_events)
        self.id = event.next_id
        event.next_id += 1        
        if intersected_events is None:
            self.intersected_events = frozenset([self])
        else:
            self.intersected_events = intersected_events
        if intersected_events_ids is None:
            self.intersected_events_ids = frozenset([self.id])
        else:
            self.intersected_events_ids = intersected_events_ids
            
    def cached_intersect(e1, e2):
        """
        look in cache for events e1 and e2 being intersected before, 
            return their intersection
        the key is the set of event ids for events that were intersected to
            get the intersection you want... 
        the value is an event (the intersection of e1 and e2)
        """
        total_intersections = e1.intersected_events_ids.union(
                                    e2.intersected_events_ids)
        if total_intersections in event.cached_ints:
            return event.cached_ints[total_intersections]
        else:
            int_at_evts = e1.atomic_events.intersection(e2.atomic_events)
            total_events = e1.intersected_events.intersection(e2.intersected_events)            
            e3 = event(int_at_evts, total_events, total_intersections)
            return e3
            
    def intersect(self, other):
        """
        calls cached_intersection for a member event
        """
        intersection = event.cached_intersect(self, other)
        return intersection
        

def print_input(rv_data):
    """
    My helper function to print the input nicely
    """
    print len(rv_data[1]), len(rv_data)
    for row in rv_data:
        print row
    
def find_rv_inverses(rv_data):
    """
    'find random variable inverses'
    INPUT matrix of random variable data
    OUTPUT list of dictionaries, rv_inverse, where rv_inverse[X][1]
        returns the event where X = 1
    """
    rv_inverse = [None] * len(rv_data)
    
    for rv_index, X in enumerate(rv_data):
       d = dict()
       for i, value in enumerate(X):
           if d.has_key(value):
               d[value].add(i)
           else:
               d[value] = set([i])
       for key in d:
           d[key] = event(frozenset(d[key]))
       rv_inverse[rv_index] = d
    return rv_inverse


class state:
    """
    as a state search algorithm, represents the states
    k = number of rv being considered at one time (generation in the tree)
    parent = previously computed state
    children = next states computed
    prior_event = intersection of independent events
    posterior = event testing to be independent of the prior
    joint = prior intersect posterior
    rv_used = the random variables being considered in this branch
    """
    space_size = -1
    def __init__(self, original=None, new_event=None, rv_of_new=None):
        self.parent = original
        if original is not None:
            original.children.append(self)
            self.prior = original.joint
            self.rv_used = original.rv_used + [rv_of_new]
            self.joint = None  # to be filled in later if explored
            self.k = original.k + 1
        else:
            self.prior = None
            self.rv_used = [rv_of_new]
            self.joint = new_event
            self.k = 1
        self.posterior = new_event
        self.children = list()

    def check_independence(self):
        """
        computes the joint event (intersection) and checks if the event 
            posterior is independent given prior
        """
        if self.parent is None:
            self.joint.ind = True  # serves as a flag to not generate (identitcal) succs
            return True
        self.joint = self.prior.intersect(self.posterior)
        ind = self.joint.size * state.space_size == self.prior.size * self.posterior.size
        self.joint.ind = ind  # serves as a flag to not generate (identitcal) succs
        return ind
        
    def successors(self):
        """
        if an identical state has been computed already, don't generate succs
        otherwise, choose all of the possible events to add on to it (not from same RV)
        """
        suc = list()
        if self.joint.intersected_events_ids in event.ind_events:
            return suc # don't move forward if you'd already explored this state
        event.ind_events[self.joint.intersected_events_ids] = self.joint.ind

        for rv_index, rv in enumerate(rv_inverse):
            if rv_index not in self.rv_used:  # can't say X=1 ind? X=2
                for value in rv:
                    suc.append(state(self, rv[value], rv_index))
        return suc

if __name__ == '__main__':
    rv_data = read_input()
# rv_data = np.array([[1,1,1,1,0,0,0,0], # another testing set
#                   [1,1,0,0,1,1,0,0],
#                   [1,0,1,0,1,0,1,0]])


    state.space_size = len(rv_data[0])        
    # print_input(rv_data)

    rv_inverse = find_rv_inverses(rv_data)

    q = Queue()
    for rv_index, rv in enumerate(rv_inverse):  #initialize the queue
        for val in rv:
            q.put(state(new_event=rv[val], rv_of_new=rv_index))
        
    max_k = len(rv_data)  # maximium k for which rv are k-wise independent
    while not q.empty():  
        s = q.get()       # queue => breadth first search
        if not s.check_independence():  #stop here if not independent
            max_k = s.k-1
            break
        else:                           # else put its successors in queue
            succ = s.successors()
            for t in succ:
                q.put(t)

print max_k