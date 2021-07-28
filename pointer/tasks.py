import logging
import math

from pointer.models import ClosestPointCompute
from project import app

logger = logging.getLogger(__file__)


def processor(points: list):
    """“(2, 3), (1, 1), (5, 4), ...”"""
    new_points = []
    for x, point in enumerate(points):
        clean_list = []
        for y in point:
            clean_list.append(float(y))
        new_points.append(tuple(clean_list))
    ax = sorted(new_points, key=lambda x: x[0])  # Presorting x-wise
    ay = sorted(new_points, key=lambda x: x[1])  # Presorting y-wise
    p1, p2, mi = closest_pair(ax, ay)  # Recursive D&C function
    return p1, p2, mi


def closest_pair(ax, ay):
    ln_ax = len(ax)  # It's quicker to assign variable
    if ln_ax <= 3:
        return brute(ax)  # A call to bruteforce comparison
    mid = ln_ax // 2  # Division without remainder, need int
    Qx = ax[:mid]  # Two-part split
    Rx = ax[mid:]  # Determine midpoint on x-axis
    qx = set(Qx)
    Qy = list()
    Ry = list()
    for x in ay:  # split ay into 2 arrays using midpoint
        if x in qx:
            Qy.append(x)
        else:
            Ry.append(x)
            # Call recursively both arrays after split

    (p1, q1, mi1) = closest_pair(Qx, Qy)
    (p2, q2, mi2) = closest_pair(Rx, Ry)

    # Determine smaller distance between points of 2 arrays
    if mi1 <= mi2:
        d = mi1
        mn = (p1, q1)
    else:
        d = mi2
        mn = (p2, q2)

    # Call function to account for points on the boundary

    (p3, q3, mi3) = closest_split_pair(ax, ay, d, mn)

    # Determine smallest distance for the array

    if d <= mi3:
        return mn[0], mn[1], d
    else:
        return p3, q3, mi3


def brute(ax):
    mi = dist(ax[0], ax[1])
    p1 = ax[0]
    p2 = ax[1]
    ln_ax = len(ax)
    if ln_ax == 2:
        return p1, p2, mi
    for i in range(ln_ax - 1):
        for j in range(i + 1, ln_ax):
            if i != 0 and j != 1:
                d = dist(ax[i], ax[j])
                if d < mi:  # Update min_dist and points
                    mi = d
                    p1, p2 = ax[i], ax[j]
    return p1, p2, mi


def dist(p1, p2):
    return math.sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)


def closest_split_pair(p_x, p_y, delta, best_pair):
    ln_x = len(p_x)  # store length - quicker
    mx_x = p_x[ln_x // 2][0]  # select midpoint on x-sorted array

    # Create a subarray of points not further than delta from
    # midpoint on x-sorted array

    s_y = [x for x in p_y if mx_x - delta <= x[0] <= mx_x + delta]
    best = delta  # assign best value to delta
    ln_y = len(s_y)  # store length of subarray for quickness
    for i in range(ln_y - 1):
        for j in range(i + 1, min(i + 7, ln_y)):
            p, q = s_y[i], s_y[j]
            dst = dist(p, q)
            if dst < best:
                best_pair = p, q
                best = dst
    return best_pair[0], best_pair[1], best


@app.task()
def close_point_calculator(points, id):
    try:
        p1, p2, mi = processor(points=points)
        payload = {"point A": p1, "point B": p2, "distance between": mi}
        ClosestPointCompute.objects.filter(pk=id).update(
            result=payload, is_done=True, is_processing=False
        )
    except Exception as e:
        logger.error("Error sending email {}", e.args)
