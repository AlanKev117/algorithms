'''
# ciclos para unir subarreglos no ascendentes de un arreglo
[3,7,7,8,7,7,5,4,6,5,2]
[3,7,7,7,5,4,5,2]
[3,7,7,5,4,2]
[3,7,5,4,2]
[3,5,4,2]
[3,4,2]
[3,2]

[[3],[7,7],[8,7,7,5,4],[6,5,2]] ### [4,5,7,7,8], [2,5,6]
[[3],[7],[7,7,5,4],[5,2]] -> [[3],[7,7,7,5,4],[5,2]]
[[3],[7,7,5,4],[2]] -> [[3],[7,7,5,4,2]]
[[3],[7,5,4,2]]
[[3],[5,4,2]]
[[3],[4,2]]
[[3],[2]] -> [[3,2]]
'''
from collections import deque
class SinglyLinkedListNode:
    def __init__(self, value):
        self.next = None
        self.value = value
    def insert(self, value):
        new_node = SinglyLinkedListNode(value)
        self.next = new_node
        return new_node
    def print_values(self):
        aux_node = self
        values = []
        while aux_node:
            values.append(aux_node.value)
            aux_node = aux_node.next
        print(*values, sep=", ")

def poisonous_plants(p):
    decks = [] # Array of stacks
    i = 0
    while i < len(p): # Create array of deques (stacks)
        deck = deque()
        while i < len(p) and (len(deck) == 0 or p[i] <= deck[0]):
            deck.appendleft(p[i])
            i += 1
        decks.append(deck)
    
    # Transform array of deques into a singly linked list of deques
    head = SinglyLinkedListNode(decks[0])
    aux_node = head
    for i in range(1, len(decks)):
        aux_node = aux_node.insert(decks[i])
    
    # Reduce list to one node as deques pop
    days = 0
    while head.next:
        days += 1
        aux_node = head
        while aux_node.next:
            aux_node.next.value.pop()
            if len(aux_node.next.value) == 0:
                aux_node.next = aux_node.next.next
            elif aux_node.value[0] >= aux_node.next.value[-1]:
                aux_node.next.value.extend(aux_node.value)
                aux_node.value = aux_node.next.value
                aux_node.next = aux_node.next.next
            else:
                aux_node = aux_node.next
    return days
        



print(poisonous_plants([3,2,5,4]))