import math


class Point:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def __repr__(self):
        return "Point({},{})".format(self.x, self.y)

    def __hash__(self):
        return hash((self.x, self.y))

    def __eq__(self, other):
        if isinstance(other, Point):
            return other.x == self.x and other.y == self.y
        else:
            return False

    def __add__(self, other):
        if isinstance(other, Vector):
            return Point(self.x + other.x, self.y + other.y)
        else:
            raise ValueError("Cannot add Point and {}".format(type(other)))

    def __sub__(self, other):
        if isinstance(other, Vector):
            return Point(self.x - other.x, self.y - other.y)
        else:
            raise ValueError("Cannot subtract Point and {}".format(type(other)))


class Vector:
    def __init__(self, x=0.0, y=0.0):
        self.x = x
        self.y = y

    @property
    def magnitude(self):
        return math.sqrt(self.x**2 + self.y**2)

    @property
    def direction(self):
        # Return the unit/directoinal vector for this vector
        return Vector(self.x/self.magnitude, self.y/self.magnitude)

    def dot_product(self, other):
        # X1*X2+Y1*Y2+Z1*Z2......
        return self.x * other.x + self.y * other.y

    def angle(self, other=None):
        # Angle between this vector and (optionally) other
        angle = math.degrees(math.atan2(self.y, self.x)) + 180
        # atan2 returns -pi/2(-180) to pi/2(180) we want it to return 0 - pi(360)
        if other:
            angle = angle - other.angle()
            if angle < 0:
                angle = 360 + angle
        return angle

    def rotate(self, angle):
        theta = math.radians(angle)
        x = self.x * math.cos(theta) - self.y * math.sin(theta)
        y = self.x * math.sin(theta) + self.y * math.cos(theta)
        self.x, self.y = x, y

    # def alt_angle(self, other):
    #     angle = math.acos(
    #         self.dot_product(other)/(self.magnitude * other.magnitude)
    #     )
    #     return math.degrees(angle)

    def nearest_integer(self):
        # Return the nearest vector with only integer components
        return Vector(int(self.x), int(self.y))

    def reduce(self):
        """
        Given a vector remove all common divisors so that it's a "integer unit vector"
        """
        if self.x == 0 and self.y == 0:
            x, y = self.x, self.y
        elif self.x == 0:
            x = self.x
            y = self.y / abs(self.y)
        elif self.y == 0:
            x = self.x / abs(self.x)
            y = self.y
        else:
            x, y = self.x, self.y
            while True:
                for i in range(1, min(abs(x), abs(y)) + 1):
                    if x % i == 0 and y % i == 0 and i != 1:
                        x, y = x / i, y / i
                        break
                else:
                    break
        return Vector(x, y)

    def __repr__(self):
        return "Vector({},{})".format(self.x, self.y)

    def __hash__(self):
        return hash((self.x, self.y))

    def __eq__(self, other):
        if isinstance(other, Vector):
            return self.x == other.x and self.y == other.y
        return False

    def __add__(self, other):
        if isinstance(other, Vector):
            return Vector(self.x + other.x, self.y + other.y)
        else:
            return super().__add__(other)

    def __mul__(self, other):
        if isinstance(other, Vector):
            return self.dot_product(other)
        else:
            return super().__mul__(other)