import hashlib

class CoyoteHashMap:
    def __init__(self):
        self.depth = 0
        self.special_char = '*'
        self.items = {}  # maps full hash (bytes) -> (key, value)

    def _sha256_bytes(self, data):
        return hashlib.sha256(data.encode()).digest()

    def _extended_hash(self, key):
        # Build cascaded hash as per current global depth
        hashes = []
        base = key
        for _ in range(self.depth + 1):
            h = self._sha256_bytes(base)
            hashes.append(h)
            base += self.special_char
        return b''.join(hashes)  # Full extended hash

    def _find_collision(self, hash_bytes):
        return hash_bytes in self.items

    def _extend_and_rehash(self):
        self.depth += 1
        new_items = {}
        for key, (_, value) in self.items.items():
            new_hash = self._extended_hash(key)
            new_items[new_hash] = (key, value)
        self.items = new_items

    def insert(self, key, value):
        while True:
            h = self._extended_hash(key)
            if not self._find_collision(h) or self.items[h][0] == key:
                self.items[h] = (key, value)
                return
            else:
                self._extend_and_rehash()

    def get(self, key):
        h = self._extended_hash(key)
        return self.items[h][1] if h in self.items and self.items[h][0] == key else None

    def delete(self, key):
        h = self._extended_hash(key)
        if h in self.items and self.items[h][0] == key:
            del self.items[h]
            return True
        return False

    def get_raw_extended_hash(self, key):
        return self._extended_hash(key)

    def __repr__(self):
        return f"CoyoteHashMap(depth={self.depth}, keys={list(self.items.keys())})"

