class Rectangle:
    def __init__(self, width, height):
        self._width = width
        self._height = height

    @property
    def width(self):
        """
        Property to get the width of the rectangle.
        """
        return self._width

    @width.setter
    def width(self, value):
        """
        Property setter to update the width of the rectangle.
        """
        if value < 0:
            raise ValueError("Width cannot be negative")
        self._width = value

    @property
    def height(self):
        """
        Property to get the height of the rectangle.
        """
        return self._height

    @height.setter
    def height(self, value):
        """
        Property setter to update the height of the rectangle.
        """
        if value < 0:
            raise ValueError("Height cannot be negative")
        self._height = value

    @property
    def area(self):
        """
        Property to compute the area of the rectangle.
        """
        return self._width * self._height

    @property
    def perimeter(self):
        """
        Property to compute the perimeter of the rectangle.
        """
        return 2 * (self._width + self._height)

# Creating an instance of Rectangle
rect = Rectangle(5, 10)

# Accessing properties
print("Width:", rect.width)          # Output: Width: 5
print("Height:", rect.height)        # Output: Height: 10
print("Area:", rect.area)            # Output: Area: 50
print("Perimeter:", rect.perimeter)  # Output: Perimeter: 30

# Updating properties
rect.width = 7
rect.height = 12
print("Updated Width:", rect.width)          # Output: Updated Width: 7
print("Updated Height:", rect.height)        # Output: Updated Height: 12
print("Updated Area:", rect.area)            # Output: Updated Area: 84
print("Updated Perimeter:", rect.perimeter)  # Output: Updated Perimeter: 38

# Attempting to set a negative dimension
try:
    rect.width = -5
except ValueError as e:
    print("Error:", e)  # Output: Error: Width cannot be negative
