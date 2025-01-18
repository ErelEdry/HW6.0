class Node:
    def __init__(self, val):
        self.val = val
        self.next = None

    def __repr__(self):
        return "[" + str(self.val) + ", nxt:" + str(id(self.next)) + "]"

class MyQueue():
    def __init__(self, seq=None):
        self.head = None
        self.tail = None
        self.len = 0
        if seq != None:
            for x in seq:
                self.enqueue(x)

    def __repr__(self):
        out = "nodes: "
        p = self.head
        while p != None:
            out += str(p) + " "
            p = p.next
        return out

    def enqueue(self, val):
        ''' add node with value val at the list tail '''
        p = self
        n = Node(val)
        if self.len == 0:
            p.head = p.tail = Node(val)
        else:
            p.tail.next = Node(val)
            p.tail = p.tail.next
        self.len += 1

    def dequeue(self):
        ''' add node with value val at the list head '''
        if self.len == 0:
            raise RuntimeError("Queue is empty")

        p = self
        ret_val = p.head.val
        p.head = p.head.next
        self.len -= 1

        return ret_val

    def __len__(self):
        ''' called when using Python's len() '''
        return self.len

    def is_empty(self):
        ''' called when using Python's len() '''
        return self.len == 0



class Stack:
    def __init__(self):
        self.stack = []

    def push(self, item):
        self.stack.append(item)

    def pop(self):
        if self.is_empty():
            raise IndexError("Pop from an empty stack.")
        return self.stack.pop()

    def is_empty(self):
        return len(self.stack) == 0

    def peek(self):
        if self.is_empty():
            raise IndexError("Peek from an empty stack.")
        return self.stack[-1]

    def __len__(self):
        return len(self.stack)
    
    def __repr__(self):
        out = 'top->'
        for item in self.stack[::-1]:
            out += str(item) + ' | \n'
            out += "_" * len(str(item)) + "\n"
        out += '|'
        return out

