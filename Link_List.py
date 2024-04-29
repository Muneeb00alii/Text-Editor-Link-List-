class Node:
    def __init__(self, data, prev=None, next=None):
        self.data = data
        self.prev = prev
        self.next = next

class DLL:
    def __init__(self):
        self.head = None
        self.tail = None

    def __len__(self):
        count = 0
        current = self.head
        while current is not None:
            count += 1
            current = current.next
        return count

    def insert_at_end(self, data):
        new_node = Node(data)
        if self.head is None:
            self.head = new_node
            self.tail = new_node
        else:
            self.tail.next = new_node
            new_node.prev = self.tail
            self.tail = new_node

    def insert_between(self, data, prev_node):
        new_node = Node(data)
        if prev_node is None:
            return
        new_node.next = prev_node.next
        if prev_node.next is not None:
            prev_node.next.prev = new_node
        prev_node.next = new_node
        new_node.prev = prev_node
        if new_node.next is None:
            self.tail = new_node

    def delete_start(self):
        if self.head is None:
            return
        if self.head.next is None:
            self.head = None
            self.tail = None
        else:
            self.head = self.head.next
            self.head.prev = None

    def delete_node(self, node):
        if node is None:
            return
        if node.prev is None:
            self.head = node.next
        else:
            node.prev.next = node.next
        if node.next is None:
            self.tail = node.prev
        else:
            node.next.prev = node.prev
