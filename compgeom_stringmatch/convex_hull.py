import sys
import numpy as np
from Queue import Queue
# np.random.seed(123456789)


def read_input():
    """
    Subroutine to read the input from stdin
    """
    n = int(sys.stdin.next())
    points = np.zeros((n, 2), dtype=float)
    
    for i, value in  enumerate(sys.stdin.next().split(', ')):
        points[i/2, i%2] = value    
    return n, points

def norm(vec):
    return np.sqrt(np.abs(vec**2).sum())
    
def angle(pta, elbow, ptc):
    """
    INPUT: three 2-dimensional points
    OUTPUT: angle between the ray from pta to elbow and the ray from elbow to ptc
        (in radians)
    """
    vec1 = pta - elbow
    vec2 = ptc - elbow
    try:
        dot_prod = np.dot(vec1, vec2)
        angle = np.arccos(dot_prod / (norm(vec1) * norm(vec2)))  # inefficient?
    except ArithmeticError:
        sys.exit("No angle between a vector and a length-zero vector")
        
    return angle

def which_side(pta, elbow, ptc):
    pass    
    
def brute_force_convex_hull(points):
    pass    

def jarvis_march(points):
    # ch = list()    
    # leftmost = points[np.argmin(points[:,0])]  
    # ch.append(leftmost)
    # points = (points - leftmost)[1:]  # center remaining around leftmost
    # slopes = points[:,1] - points[:,0]  # numpy handles "infinity" cases
    pass
    

def graham_scan(points):
    ch = Queue()
    leftmost = points[np.argmin(points[:,0])]
    print(leftmost)
    dtype = [('x', np.float64), ('y', np.float64), ('slope', np.float64)]
    cpts = np.zeros(len(points) - 1, dtype=dtype)
    cpts[:]['x'] = (points[1:,0] - leftmost[0]) # centering points around new origin
    cpts[:]['y'] = (points[1:,1] - leftmost[1])
    cpts[:]['slope'] = cpts[:]['y'] - cpts[:]['x']
    
    sorted_pts = np.sort(cpts, order=['slope', 'x'])  # sort by angle, then distancefrom origin
    print sorted_pts
        
    return list(ch)
    
if __name__ == "__main__":

    n, points = read_input()  # real input
    # print n
    # for pt in points:
    #     print "({}, {})".format(pt[0], pt[1])
    import matplotlib.pyplot as plt
    plt.scatter(points[:,0], points[:,1])
    
    graham_scan(points)
    
    
    plt.show()

    # print convex_hull