# Grupo 3

class BinarySearchTree(BinarySearchTreeADT):
    def __init__(self) -> None:
        self._root: Node = None

    def clear(self) -> None:
        self._root = None

    def is_empty(self) -> bool:
        return self._root is None

    def _get_parent(self, key: object) -> Node:
        parent: Node = None
        current: Node = self._root
        while current and key != current.key:
            parent = current
            current = current.next(key)
        return parent, current

    def insert(self, key: object, value: object) -> None:
        def insert(current: Node, key: object, value: object) -> Node:
            if current is None:
                return Node(key, value)
            elif key > current.key:
                current.right = insert(current.right, key, value)
            elif key < current.key:
                current.left = insert(current.left, key, value)
            return current

        self._root = insert(self._root, key, value)

    def search(self, key: object) -> object:
        def search(current: Node, key: object) -> object:
            if current is None:
                return None
            elif key == current.key:
                return current.value
            return search(current.next(key), key)

        return search(self._root, key)

    def __str__(self) -> str:
        return '[empty]' if self.is_empty() else self._str_tree()

    def _str_tree(self) -> str:
        def _str_tree(current: Node, is_right: bool, tree: str, ident: str) -> str:
                if current.right:
                    tree = _str_tree(current.right, True, tree, ident + (' ' * 8 if is_right else ' |' + ' ' * 6))
                tree += ident + (' /' if is_right else ' \\') + "----- " + str(current) + '\n'
                if current.left:
                    tree = _str_tree(current.left, False, tree, ident + (' |' + ' ' * 6 if is_right else ' ' * 8))
                return tree

        tree: str = ''
        if self._root.right:
            tree = _str_tree(self._root.right, True, tree, '')
        tree += str(self._root) + '\n'
        if self._root.left:
            tree = _str_tree(self._root.left, False, tree, '')

        return tree

    def _delete_by_copying(self, key: object) -> bool:
        parent: Node; current: Node
        parent, current = self._get_parent(key)
        if current is None:
            return False
        # Case 3
        elif current.left and current.right:
            at_the_right: Node = current.left
            while at_the_right.right:
                at_the_right = at_the_right.right
            self._delete_by_copying(at_the_right.key)
            current.key, current.value = at_the_right.key, at_the_right.value
        # Case 1/2
        else:
            next_node: Node = current.left or current.right
            if current == self._root:
                self._root = next_node
            elif current == parent.left:
                parent.left = next_node
            else:
                parent.right = next_node
        return True

    def delete(self, key: object) -> bool:
        return self._delete_by_copying(key)
        # return self._delete_by_merging(key)

    def _delete_by_merging(self, key: object) -> bool:
        parent: Node; current: Node
        parent, current = self._get_parent(key)
        if current is None:
            return False
        # Case 3
        elif current.left and current.right:
            at_the_right: Node = current.left
            while at_the_right.right:
                at_the_right = at_the_right.right
            at_the_right.right = current.right
            if current == self._root:
                self._root = current.left
            elif parent.left == current:
                parent.left = current.left
            else:
                parent.right = current.left
        # Case 1/2
        else:
            next_node: Node = current.left or current.right
            if current == self._root:
                self._root = next_node
            elif current == parent.left:
                parent.left = next_node
            else:
                parent.right = next_node
        return True

    def pre_order_traversal(self) -> None:
        def pre_order_traversal(current: Node) -> None:
            if current:
                print(current.key, end=' ')
                pre_order_traversal(current.left)
                pre_order_traversal(current.right)
        pre_order_traversal(self._root)

    def in_order_traversal(self) -> None:
        def in_order_traversal(current: Node) -> None:
            if current:
                in_order_traversal(current.left)
                print(current.key, end=' ')
                in_order_traversal(current.right)
        in_order_traversal(self._root)

    def post_order_traversal(self) -> None:
        def post_order_traversal(current: Node) -> None:
            if current:
                post_order_traversal(current.left)
                post_order_traversal(current.right)
                print(current.key, end=' ')
        post_order_traversal(self._root)

    def level_order_traversal(self) -> None:
        if self._root:
            queue = [self._root]
            while queue:
                current: Node = queue.pop(0)
                print(current.key, end=' ')
                if current.left: queue.append(current.left)
                if current.right: queue.append(current.right)

    # IMPLEMENTACAO !!!

    def count_internal(self) -> int:
        def count_internal(current: Node, root: bool = False) -> int:
            if current:
                if current.left or current.right:
                    if root:
                        return count_internal(current.left) + count_internal(current.right)
                    return 1 + count_internal(current.left) + count_internal(current.right)
                return 0
            return 0

        return count_internal(self._root, True)

    def degree(self, key: object) -> int:
        def degree(current: Node, key: object) -> int:
            if current is None:
                return -1
            elif key == current.key:
                if current.left and current.right:
                    return 2
                elif current.left or current.right:
                    return 1
                return 0
            return degree(current.next(key), key)

        return degree(self._root, key)

    def height(self, key: object) -> int:
            def height(node, key, depth):
                if node is None:
                    return -1
                if node.key == key:
                    return depth
                elif key < node.key:
                    return height(node.left, key, depth + 1)
                else:
                    return height(node.right, key, depth + 1)

            return height(self._root, key, 0)


    def level(self, key: object) -> int:
        def level(current: Node, key: object) -> int:
            if current is None:
                return -1
            elif key == current.key:
                return 0
            elif level(current.next(key), key) == -1:
                return -1
            return level(current.next(key), key) + 1

        return level(self._root, key)

    def ancestor(self, key: object) -> str:
        def ancestor(current: Node, key: object) -> str:
            if current is None:
                return "None"
            elif key == current.key:
                return str(current.key)
            elif ancestor(current.next(key), key) == "None":
                return "None"
            return str(current.key) + " " + str(ancestor(current.next(key), key))

        return ancestor(self._root, key)

    # IMPLEMENTACAO !!!
