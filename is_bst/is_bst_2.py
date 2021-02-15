def checkBST(root):
    return check(root, float("-inf"), float("inf"))

def check(n, min_val, max_val):
    if not n:
        return True
    if n.data <= min_val or n.data >= max_val:
        return False
    return check(n.left, min_val, n.data) and check(n.right, n.data, max_val)

