import math

class Circle:
    def __init__(self, radius):
        self._radius = radius  # Use a protected attribute for internal storage

    @property
    def radius(self):
        """
        Property to get the radius of the circle.
        """
        return self._radius

    @radius.setter
    def radius(self, value):
        """
        Property setter to update the radius of the circle.
        """
        if value < 0:
            raise ValueError("Radius cannot be negative")
        self._radius = value

    @property
    def area(self):
        """
        Property to compute the area of the circle.
        """
        return math.pi * (self._radius ** 2)

# Creating an instance of Circle
circle = Circle(5)

# Accessing the radius and area using properties
print("Radius:", circle.radius)  # Output: Radius: 5
print("Area:", circle.area)      # Output: Area: 78.53981633974483

# Updating the radius using the setter
circle.radius = 10
print("Updated Radius:", circle.radius)  # Output: Updated Radius: 10
print("Updated Area:", circle.area)      # Output: Updated Area: 314.1592653589793

# Attempting to set a negative radius
try:
    circle.radius = -1
except ValueError as e:
    print("Error:", e)  # Output: Error: Radius cannot be negative
