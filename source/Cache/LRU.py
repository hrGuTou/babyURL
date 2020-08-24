class ListNode:
    # Double linked list
    def __init__(self, key=None, val=None):
        self.key = key
        self.val = val
        self.prev = None
        self.next = None


class LRU:
    def __init__(self, capacity):
        self.capacity = capacity
        self.hashMap={}
        self.head = ListNode()
        self.tail = ListNode()
        # initialize
        self.head.next = self.tail
        self.tail.prev = self.head

    def move_to_tail(self, key):
        # Tail: most recently used
        # Get from hash table
        node = self.hashMap[key]
        # remove current node
        node.prev.next = node.next
        node.next.prev = node.prev
        # move node to last, [node] <-> tail
        node.prev = self.tail.prev
        node.next = self.tail
        # tail node connect to current node
        self.tail.prev.next = node
        self.tail.prev = node

    def get(self, key):
        if key in self.hashMap:
            self.move_to_tail(key)
        res = self.hashMap.get(key, -1)
        if res == -1:
            return res
        else:
            return res.val

    def put(self, key, val):
        if key in self.hashMap:
            self.hashMap[key].val = val
            self.move_to_tail(key)

        else:
            if len(self.hashMap) == self.capacity:
                # Reach the capacity
                # Delete least use, head
                self.head.next = self.head.next.next
                self.head.next.prev = self.head

            # if key not exist
            newNode = ListNode(key, val)
            self.hashMap[key] = newNode
            newNode.prev = self.tail.prev
            newNode.next = self.tail
            self.tail.prev.next = newNode
            self.tail.prev = newNode


