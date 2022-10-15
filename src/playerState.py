import math
from tick import *
from constants import *
from bullet import Bullet


class PlayerState:
    """
    Used to create objects to store player information
    """

    def __init__(self, parent, center):
        """
        Args:
                parent (OverallState) : Reference to parent object of class OverallState
                center (List<float>) : Coordinates of player
        """
        self.parent = parent
        self.center = center
        self.orientation = 45
        self.bulletsList = []
        self.points = 0

    def cleanBullets(self, x):
        """
        Used to despawn bullets that originated before time x

        Args:
                x (float) : Time threshold for not despawning bullets
        """
        newBulletList = []
        for i in self.bulletsList:
            if i.otime > x:
                newBulletList.append(i)
        self.bulletsList = newBulletList

    def shoot(self):
        """
        Creates a new bullet object for the player and assigns otime as current time
        """
        newBullet = Bullet(
            self.center,
            [
                math.cos(self.orientation * 0.0174) * BULLET_SPEED,
                math.sin(self.orientation * 0.0174) * BULLET_SPEED,
            ],
            timeFromTick(self.parent.offset),
        )
        self.bulletsList.append(newBullet)

    def turnClock(self):
        """
        Used to turn the player clockwise
        """
        self.orientation += SENSTIVITY

    def turnAntiClock(self):
        """
        Used to turn the player anti-clockwise
        """
        self.orientation -= SENSTIVITY

    def getState(self):
        """
        Used to get state of this object in JSON format
        """
        # @TODO fix this
        return {
            k: getattr(self, k)
            if k != "bulletsList"
            else [getattr(self, k)[i].getState() for i in range(len(getattr(self, k)))]
            for k in ["points", "orientation", "bulletsList", "center"]
        }

    def setState(self, state):
        """
        Used to set attributes of this object from state in JSON format

        Args:
                state (Dict<str, Object>) : Object state to be set in JSON format
        """
        for k, v in state.items():
            if k == "bulletsList":
                newBulletList = []
                for i in v:
                    newBulletList.append(Bullet(**i))

                setattr(self, k, newBulletList)

            else:
                setattr(self, k, v)

    def copy(self):
        """
        Return a copy of this object
        """
        bulletList = [x.copy() for x in self.bulletsList]
        cop = PlayerState(self.parent, self.center.copy())
        for k, v in zip(
            ["points", "orientation", "bulletsList"],
            [self.points, self.orientation, bulletList],
        ):
            setattr(cop, k, v)
        return cop
