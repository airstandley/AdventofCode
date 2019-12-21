import math


class Point3D:
    def __init__(self, x=0, y=0, z=0):
        self.x = x
        self.y = y
        self.z = z

    def __repr__(self):
        return "Point({},{},{})".format(self.x, self.y, self.z)

    def __hash__(self):
        return hash((self.x, self.y, self.z))

    def __eq__(self, other):
        if isinstance(other, Point3D):
            return other.x == self.x and other.y == self.y and other.z == self.z
        else:
            return False

    def __add__(self, other):
        if isinstance(other, Vector3D):
            return Point3D(self.x + other.x, self.y + other.y, self.z + other.z)
        else:
            raise ValueError("Cannot add Point and {}".format(type(other)))

    def __sub__(self, other):
        if isinstance(other, Vector3D):
            return Point3D(self.x - other.x, self.y - other.y, self.z - other.z)
        else:
            raise ValueError("Cannot subtract Point and {}".format(type(other)))


class Vector3D:
    def __init__(self, x=0, y=0, z=0):
        self.x = x
        self.y = y
        self.z = z

    @property
    def magnitude(self):
        return math.sqrt(self.x**2 + self.y**2 + self.z**2)

    @property
    def direction(self):
        # Return the unit/directoinal vector for this vector
        return Vector3D(self.x/self.magnitude, self.y/self.magnitude, self.z/self.magnitude)

    def dot_product(self, other):
        # X1*X2+Y1*Y2+Z1*Z2......
        return self.x * other.x + self.y * other.y + self.z * other.z

    # def angle(self, other=None):
    #     # Angle between this vector and (optionally) other
    #     angle = math.degrees(math.atan2(self.y, self.x)) + 180
    #     # atan2 returns -pi/2(-180) to pi/2(180) we want it to return 0 - pi(360)
    #     if other:
    #         angle = angle - other.angle()
    #         if angle < 0:
    #             angle = 360 + angle
    #     return angle
    #
    # def rotate(self, angle):
    #     # Only works for rotation about the Z axis.
    #     theta = math.radians(angle)
    #     x = self.x * math.cos(theta) - self.y * math.sin(theta)
    #     y = self.x * math.sin(theta) + self.y * math.cos(theta)
    #     self.x, self.y = x, y

    def nearest_integer(self):
        # Return the nearest vector with only integer components
        return Vector3D(int(self.x), int(self.y), int(self.z))

    # def reduce(self):
    #     """
    #     Given a vector remove all common divisors so that it's a "integer unit vector"
    #     """
    #     if self.x == 0 and self.y == 0:
    #         x, y = self.x, self.y
    #     elif self.x == 0:
    #         x = self.x
    #         y = self.y / abs(self.y)
    #     elif self.y == 0:
    #         x = self.x / abs(self.x)
    #         y = self.y
    #     else:
    #         x, y = self.x, self.y
    #         while True:
    #             for i in range(1, min(abs(x), abs(y)) + 1):
    #                 if x % i == 0 and y % i == 0 and i != 1:
    #                     x, y = x / i, y / i
    #                     break
    #             else:
    #                 break
    #     return Vector(x, y)

    def __repr__(self):
        return "Vector({},{},{})".format(self.x, self.y, self.z)

    def __hash__(self):
        return hash((self.x, self.y, self.z))

    def __eq__(self, other):
        if isinstance(other, Vector3D):
            return self.x == other.x and self.y == other.y and self.z == other.z
        return False

    def __add__(self, other):
        if isinstance(other, Vector3D):
            return Vector3D(self.x + other.x, self.y + other.y, self.z + other.z)
        else:
            return super().__add__(other)

    def __mul__(self, other):
        if isinstance(other, Vector3D):
            return self.dot_product(other)
        else:
            return super().__mul__(other)


class Body3D:

    def __init__(self, position=None, velocity=None, acceleration=None, label=None):
        self.position = position or Point3D()
        self.velocity = velocity or Vector3D()
        self.acceleration = acceleration or Vector3D()
        self.label = label

    def __repr__(self):
        label = self.label or "Body"
        return "{}({},{},{})".format(label, self.position, self.velocity, self.acceleration)

    def __hash__(self):
        return hash((self.position, self.velocity, self.acceleration))

    def __eq__(self, other):
        if isinstance(other, Body3D):
            return self.position == other.position and \
                   self.velocity == other.velocity and \
                   self.acceleration == other.acceleration
        return False
