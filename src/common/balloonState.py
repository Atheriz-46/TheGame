from common.geometry import *
from common.constants import *


class Balloon(Circle):
    """
    Used to create a Balloon object from using Circle class
    """

    def __init__(self, center, otime, **kwargs):
        """
        Args:
                        center (List<float>) : Coordinates of Center of balloon
                        otime (float) : Origin time of the balloon
        """
        Circle.__init__(self, center, [0, 0], BALLOON_RADIUS, otime)

    def copy(self):
        """
        Used to return a copy of this object
        """
        return Balloon(**self.getState())
