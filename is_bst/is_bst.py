def ino(root):
    return [*ino(root.left), root, *ino(root.right)] if root else []

def checkBST(root):
    inorder_values = list(map(lambda node: node.data, ino(root)))
    count = {}
    for value in inorder_values:
        count[value] = count.get(value, 0) + 1
    return inorder_values == sorted(inorder_values) and sum(count.values()) == len(count.values())