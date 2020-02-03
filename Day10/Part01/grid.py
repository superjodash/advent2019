class Grid:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.points = [0 for x in range(width * height)]
 
    def coordinateToIndex(self, x, y):
        return y * self.height + x

    def indexToCoordinate(self, ix):
        return (ix % self.width, ix // self.width)

    def add(self, x, y, value):
        self.points[self.coordinateToIndex(x, y)] = value

    def get(self, x, y):
        return self.points[self.coordinateToIndex(x,y)]

    def length(self):
        return self.width * self.height

