import math


class Vec:
    '''
    Implements a 2-dimensional vector class, using rectangular coordinates for
    the data model.
    '''
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return 'Vec(%s, %s)' % (self.x, self.y)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __ne__(self, other):
        return not self.__eq__(other)

    def __add__(self, other):
        return Vec(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Vec(self.x - other.x, self.y - other.y)

    def __mul__(self, number):
        return Vec(self.x * number, self.y * number)

    def __rmul__(self, number):
        return Vec(number * self.x, number * self.y)

    def __truediv__(self, number):
        return Vec(self.x / number, self.y / number)

    def __neg__(self):
        return Vec(-self.x, -self.y)

    def __pos__(self):
        return Vec(self.x, self.y)

    def __abs__(self):
        return self.norm()

    @staticmethod
    def from_rect(x, y):
        '''
        Create a Vec from (x, y) coordinates.
        '''
        return Vec(x, y)

    @staticmethod
    def from_polar(r, theta):
        '''
        Create a Vec from (r, theta) coordinates.
        '''
        return Vec(r * math.cos(theta), r * math.sin(theta))

    def arg(self):
        '''
        Returns the argument (angle) of the vector.
        '''
        return math.atan2(self.y, self.x)

    def norm_squared(self):
        '''
        Returns the square of the norm (length) of the vector.
        '''
        return self.x**2 + self.y**2

    def norm(self):
        '''
        Returns the norm (length) of the vector.
        '''
        return math.sqrt(self.norm_squared())

    def dot(self, other):
        '''
        Returns the dot product of self and other.  This is defined as:

            a . b = |a| |b| cos(theta)
                  = a.x * b.x + a.y * b.y
        '''
        return self.x * other.x + self.y * other.y

    def perpendicular(self):
        '''
        Returns a vector perpendicular to self.
        '''
        return Vec(-self.y, self.x)

    def is_collinear(self, other):
        '''
        Returns True iff self and other are collinear (have the same angle).
        The 0 vector is defined as collinear with everything.
        '''
        return self.x * other.y == other.x * self.y

    def is_perpendicular(self, other):
        '''
        Returns True iff self and other are perpendicular.  The 0 vector is
        defined as perpendicular to everything.
        '''
        return self.x * other.x == -self.y * other.y
