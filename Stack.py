class Node:

    def __init__(self, data) -> None:
        self.data = data
        self.next_node = None

    def view(self):
        if self.next_node == None:
            return self.data
        else:
            return self.data + " -> " + self.next_node.view()


class Stack:

    def __init__(self) -> None:
        self.items_count = 0
        self.head = None

    def push(self, data) -> None:
        item = Node(data)
        self.items_count += 1
        if self.head is None:
            self.head = item
        else:
            item.next_node = self.head
            self.head = item

    def pop(self) -> any:
        if self.isEmpty():
            raise IndexError
        removed_node = self.head
        self.head = self.head.next_node
        self.items_count -= 1
        removed_node.next_node = None
        return removed_node

    def top(self) -> any:
        return self.head.data

    def isEmpty(self) -> bool:
        return self.items_count == 0
