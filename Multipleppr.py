class Triangle:
    def __init__(self, a, b, c):
        self._a = a
        self._b = b
        self._c = c
        self._update_area_and_perimeter()

    def _update_area_and_perimeter(self):
        """
        Helper method to calculate area and perimeter.
        """
        # Perimeter
        self._perimeter = self._a + self._b + self._c
        # Area using Heron's formula
        s = self._perimeter / 2
        self._area = (s * (s - self._a) * (s - self._b) * (s - self._c)) ** 0.5

    @property
    def sides(self):
        """
        Property to get the sides of the triangle.
        """
        return (self._a, self._b, self._c)

    @sides.setter
    def sides(self, values):
        """
        Property setter to update all three sides and recompute area and perimeter.
        """
        if len(values) != 3:
            raise ValueError("A triangle must have exactly three sides")
        a, b, c = values
        if a <= 0 or b <= 0 or c <= 0:
            raise ValueError("Sides must be positive numbers")
        if a + b <= c or a + c <= b or b + c <= a:
            raise ValueError("The given sides do not form a valid triangle")
        
        self._a, self._b, self._c = a, b, c
        self._update_area_and_perimeter()

    @property
    def area(self):
        """
        Property to get the area of the triangle.
        """
        return self._area

    @property
    def perimeter(self):
        """
        Property to get the perimeter of the triangle.
        """
        return self._perimeter

    def get_updated_values(self):
        """
        Method to return updated side lengths, area, and perimeter.
        """
        return {
            'sides': self.sides,
            'area': self.area,
            'perimeter': self.perimeter
        }

# Creating an instance of Triangle
triangle = Triangle(3, 4, 5)

# Accessing properties and updated values
print("Initial Values:", triangle.get_updated_values())  
# Output: Initial Values: {'sides': (3, 4, 5), 'area': 6.0, 'perimeter': 12}

# Updating sides using the property setter
triangle.sides = (6, 8, 10)
print("Updated Values:", triangle.get_updated_values())
# Output: Updated Values: {'sides': (6, 8, 10), 'area': 24.0, 'perimeter': 24}

# Attempting to set invalid sides
try:
    triangle.sides = (1, 1, 3)
except ValueError as e:
    print("Error:", e)  
# Output: Error: The given sides do not form a valid triangle
