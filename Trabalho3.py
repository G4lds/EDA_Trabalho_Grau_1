
from abc import ABC, abstractmethod
from typing import List
from typing import Optional

class TrieADT(ABC):
    @abstractmethod
    def clear(self) -> None: ...
    @abstractmethod
    def is_empty(self) -> bool: ...
    @abstractmethod
    def search(self, key: object) -> object: ...
    @abstractmethod
    def insert(self, key: object, value: object) -> None: ...
    @abstractmethod
    def delete(self, key: object) -> None: ...
    @abstractmethod
    def keys_with_prefix(self, prefix: str) -> List[str]: ...
    @abstractmethod
    def count_keys_with_prefix(self, prefix: str) -> int: ...
    @abstractmethod
    def longest_key_of(self, query: str) -> str: ...
    @abstractmethod
    def keys_by_pattern(self, pattern: str) -> List[str]: ...


class Node:
    def __init__(self) -> None:
        self.value = None
        self.next = [None] * WayTrie.R

class WayTrie(TrieADT):
    R: int = 256
    def __init__(self) -> None:
        self._root = None

    def clear(self) -> None:
        self._root = None

    def is_empty(self) -> bool:
        return self._root is None

    def search(self, key: object) -> object:
        node: Node = self._search(self._root, key, 0)
        return node.value if node is not None else None

    def _search(self, current: Node, key: object, index: int) -> Node:
        if current is None:
            return None
        elif index == len(key):
            return current
        return self._search(current.next[ord(key[index])], key, index + 1)

    def insert(self, key: object, value: object) -> None:
        def insert(current: Optional[Node], key: object, value: object, index: int) -> None:
            if current is None:
                current = Node()
            if index == len(key):
                current.value = value
                return current
            c: int = ord(key[index])
            current.next[c] = insert(current.next[c], key, value, index + 1)
            return current
        self._root = insert(self._root, key, value, 0)

    def delete(self, key: object) -> None:
        def delete(current: Node, key: object, index: int) -> Node:
            if current is None:
                return None
            if index == len(key):
                current.value = None
            else:
                c: int = ord(key[index])
                current.next[c] = delete(current.next[c], key, index + 1)
            if current.value is not None:
                return current
            for i in range(WayTrie.R):
                if current.next[i] is not None:
                    return current
            return None
        self._root = delete(self._root, key, 0)

    def keys_with_prefix(self, prefix: str) -> List[str]:
        def keys_with_prefix(current: Node, prefix: str, results: List[str]) -> None:
            if current is None:
                return
            if current.value is not None:
                results.append(prefix)
            for i in range(WayTrie.R):
                prefix += chr(i)
                keys_with_prefix(current.next[i], prefix, results)
                prefix = prefix[:-1]
        results: List[str] = []
        node: Node = self._search(self._root, prefix, 0)
        keys_with_prefix(node, prefix, results)
        return results

    def count_keys_with_prefix(self, prefix: str) -> int:
        def count_keys_with_prefix(current: Node, prefix: str, result: int = 0) -> int:
            if current is None:
                return 0

            for i in range(WayTrie.R):
                prefix += chr(i)
                result += count_keys_with_prefix(current.next[i], prefix)
                prefix = prefix[:-1]

            if current.value is not None:
                return 1 + result
            return 0 + result


        node: Node = self._search(self._root, prefix, 0)
        return count_keys_with_prefix(node, prefix)

    def longest_key_of(self, query:str) -> str:
        def longest_key_of(current: Node, query: str, list: List[str] = []):
            if current is None:
                return query

            for i in range(WayTrie.R):
                query += chr(i)
                list.append(count_keys_with_prefix(current.next[i], query))
                query = query[:-1]
            return


        node: Node = self._search(self._root, query, 0)
        #return longest_key_of(node, query)

        return "nao"

    def keys_by_pattern(self, pattern: str)  -> List[str]:
        return ["0"]

a = WayTrie()
a.insert("aa","aaaa1")
a.insert("aaaaa","aaaa2")
a.insert("aaaaaa","aaaa4")
a.insert("aaaaaaa","aaaa3")


print(a.count_keys_with_prefix("a"))

a.delete("aaaaa")

print(a.longest_key_of("a"))
