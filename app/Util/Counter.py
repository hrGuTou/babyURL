
class Counter:
    def __init__(self):
        self.lastestID = 1000

    def nextID(self):
        self.lastestID += 1
        return self.lastestID



if __name__ == "__main__":

    c = Counter()
    print(c.nextID())
    print(c.nextID())
    print(c.nextID())
    print(c.nextID())
    print(c.nextID())