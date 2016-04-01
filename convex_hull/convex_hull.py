import sys
import numpy as np
from Queue import LifoQueue


def read_input(file=None):
    """
    :arg file: file object from which to read the input. If none, the it's assumed std
    """
    if file is None:
        file = sys.stdin
    n = int(file.next())
    points = np.zeros((n, 2), dtype=float)

    for i, value in enumerate(file.next().split(', ')):
        points[i / 2, i % 2] = value

    pthash = dict()
    mask = np.zeros(len(points))
    mask = np.logical_not(mask)
    for i, point in enumerate(points):
        pttuple = tuple(point)

        if pttuple in pthash:
            mask[i] = False
        pthash[pttuple] = True

    points = points[mask]
    return len(points), points
#
#
# def norm(vec):
#     return np.sqrt(np.abs(vec ** 2).sum())
#
#
# def angle(pta, elbow, ptc):
#     """
#     INPUT: three 2-dimensional points
#     OUTPUT: angle between the ray from pta to elbow and the ray from elbow to ptc
#         (in radians)
#     """
#     vec1 = pta - elbow
#     vec2 = ptc - elbow
#     try:
#         dot_prod = np.dot(vec1, vec2)
#         angle = np.arccos(dot_prod / (norm(vec1) * norm(vec2)))  # inefficient?
#     except ArithmeticError:
#         sys.exit("No angle between a vector and a length-zero vector")
#
#     return angle


def which_side(pta, ptb, test_pt):
    v1 = ptb - pta
    v2 = test_pt - pta
    return - np.cross(v1, v2)


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
    """

    :param points: numpy array of 2-dimensional points
    :return: Convex hull as another numpy array of points
    """
    ch = LifoQueue()
    leftmost = points[np.argmin(points[:, 0])]  # finding the leftmost point... definitely in CH

    dtype = [('x', np.float64), ('y', np.float64), ('slope', np.float64)]  # preparing a nicer object for sorting
    cpts = np.zeros(len(points) - 1, dtype=dtype)
    cpts[:]['x'] = points[1:, 0]
    cpts[:]['y'] = points[1:, 1]
    cpts[:]['slope'] = (cpts[:]['y'] - leftmost[1]) / (cpts[:]['x'] - leftmost[0])  # angle <-> slope from leftmost

    sorted_pts = np.sort(cpts, order=['slope', 'x'])  # sort by angle (slope), then distance from leftmost
                                                      # shows which points are colinear

    mask = np.zeros(len(sorted_pts), dtype=bool)  # getting rid of points with same angle from leftmost
    mask = np.logical_not(mask)
    for i in range(len(sorted_pts[1:])):
        mask[i - 1] = not sorted_pts[i - 1]['slope'] == sorted_pts[i]['slope']  # only keep farthest away
    sorted_pts = sorted_pts[mask]

    sorted_pts[:] = sorted_pts[::-1]  # sort greatest slope to lowest (move clockwise)

    pts = np.zeros((len(sorted_pts) + 1, 2))  # putting leftmost back into a new array object
    pts[1:, 0] = sorted_pts[:]['x']
    pts[1:, 1] = sorted_pts[:]['y']
    pts[0] = leftmost

    ch.put(pts[0])  # leftmost and the point with the highest slope are in the CH for sure
    ch.put(pts[1])
    for i, pt in enumerate(pts):
        if i < 2:
            continue
        else:
            last = ch.get()
            second_to_last = ch.get()
            side = which_side(second_to_last, pts[i], last)  # Less than 0 => on the left, o/w on the right
            while side > 0:  # if last point put in on right side, it must have been wrong to be in CH
                last = second_to_last
                second_to_last = ch.get()
                side = which_side(second_to_last, pts[i], last)
            ch.put(second_to_last)
            ch.put(last)
            ch.put(pt)

    return np.array([ch.get() for i in range(ch.qsize())])  # Put the queue into an array


if __name__ == "__main__":
    if len(sys.argv) > 1:  # if you input a filename, will read from that file
        filename = sys.argv[1]
        with open(filename, 'r') as f:
            n, points = read_input(f)
    else:
        n, points = read_input()  # If no filename, will look at stdin

    convex_hull = graham_scan(points)
    print convex_hull
    import matplotlib.pyplot as plt

    plt.scatter(points[:, 0], points[:, 1])
    convex_hull = np.vstack((convex_hull, convex_hull[0]))
    plt.plot(convex_hull[:, 0], convex_hull[:, 1])
    plt.show()

