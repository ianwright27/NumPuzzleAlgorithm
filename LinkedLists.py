# Author: Ian Wright

class Node:
    def __init__(self, prev=None, data=None, next=None):
        self.prev = prev
        self.data = data
        self.next = next


class DoubleLinkedList:
    def __init__(self):
        self.head = None
        self.last = None

        # [Additional feature] where moves are stored
        self.full_list = []

    def insert_at_beginning(self, data):
        newNode = Node(None, data, self.head)
        if self.head is not None:  # this block did not exist
            self.head.prev = newNode  # run without it to see what happens when you reverse items
        self.head = newNode
        if newNode.next is None:
            self.last = newNode  # Update Last Element

    def append(self, data):
        newNode = Node(None, data, None)
        if self.last is not None:
            self.last.next = newNode
            newNode.prev = self.last
        else:
            self.head = newNode
        self.last = newNode

    def insert_at_end(self, data):
        newNode = Node(None, data, None)
        if self.last is not None:
            self.last.next = newNode
            newNode.prev = self.last
        else:
            self.head = newNode
        self.last = newNode

    def list_items(self, reverse=None):  # Improved method of traversal "with self.last"
        if reverse:
            itr = self.last
            while itr:
                self.full_list.append(itr.data)  # extract comment only
                itr = itr.prev
        elif reverse is False:
            itr = self.head
            while itr:
                self.full_list.append(itr.data)  # extract comment only
                itr = itr.next

        # [Additional feature]
        self.list_game_moves()  # Will only run if self.full_list is full

    # [Additional feature]
    def list_game_moves(self):
        comment = self.last.data.comment
        prefix = "Just"
        if self.last is self.head:
            new_comment = prefix + " " + comment
            self.last.data.comment = new_comment
        else:
            prefix = "Then"
            new_comment = prefix + " " + comment
            self.last.data.comment = new_comment
        for i in self.full_list:
            print(i.comment)

    # You can add more functionality here
