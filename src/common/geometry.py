from common.constants import *


def distance(x1, y1, x2, y2):

    """
    Used to find the distance between 2 points ((x1,y1), (x2,y2))

    Args:
            x1 (float) : x-coordinate of first point
            y1 (float) : y-coordinate of first point
            x2 (float) : x-coordinate of second point
            y2 (float) : y-coordinate of second point
    """

    return ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5


def circleIntersection(x1, y1, r1, x2, y2, r2):

    """
    Used to find whether two circles are intersecting

    Args:
            x1 (float) : x-coordinate of center of first circle
            y1 (float) : y-coordinate of center of first circle
            r1 (float) : Radius of first circle
            x2 (float) : x-coordinate of center of second circle
            y2 (float) : y-coordinate of center of second circle
            r2 (float) : Radius of second circle
    """

    return distance(x1, y1, x2, y2) < r1 + r2 + EPSILON


class Circle:

    """
    Used to create circle objects with some center, speed, radius and origin time.
    Circle objects are used to create bullets and balloons.
    """

    def __init__(self, center, speed, width, otime):

        """
        Args:
                center (List<float>) : Center of circle object
                speed (List<float>) : speed vector of Circle object
                width (float) : Radius of Circle object
                otime (float) : origin time of Circle object
        """

        self.center = center
        self.width = width
        self.speed = speed
        for i in self.speed:
            i = round(i, 2)
        self.otime = otime

    def getPosition(self, currTime):

        """
        Used to get the position of a circle object at a specific time

        Args:
                currTime (float) : Time at which a Circle object's position has to be returned

        """

        timediff = currTime - self.otime
        # print(self.center,self.speed,timediff)
        return [
            self.center[0] + self.speed[0] * timediff,
            self.center[1] + self.speed[1] * timediff,
        ]
        # TODO: check:  return [self.center[0]+self.speed[0]*timediff,self.center[1] + self.speed[1]*timediff,self.center[2]]

    def intersects(self, other, currTime):

        """
        Checks whether this object intersects with an "other" object

        Args:
                other (Circle) : The other Circle object that intersection has to be tested with
                currTime (float) : Time at which a Circle object's position has to be returned

        """

        if currTime < self.otime or currTime < other.otime:
            return False
        otherPos = other.getPosition(currTime)
        myPos = self.getPosition(currTime)
        return circleIntersection(*myPos, self.width, *otherPos, other.width)

    def getState(self):

        """
        Used to get state of this object in JSON

        """

        return {
            "center": self.center,
            "width": self.width,
            "speed": self.speed,
            "otime": self.otime,
        }

    def copy(self):

        """
        Returns a copy of this object

        """

        return Circle(**self.getState())
