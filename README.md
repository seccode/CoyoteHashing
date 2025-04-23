# Coyote Hashing
Truly scalable dynamic hashing

Coyote Hashing allows truly O(1) worst-case performance for insertion and lookups (amoritized for resizing). It works by extending the hash length (with just one hash function) of an element in the table by first hashing the element, then - when a collision occurs - appending the hash of the element plus a special character. Each time a collision occurs, another special character is added. So after the 2nd resizing of the hash length, the hash length is 3x as long as original. This allows the use of only one hash function - differing from cucko hashing.
