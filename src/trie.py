# -*- coding: utf-8 -*-
"""The following code implements a trie tree in python."""


class Trie(object):
    """Implement Trie tree class with supporting methods."""

    def __init__(self):
        """Initializes an empty Trie tree."""
        self.tokens = {}

    def insert(self, token):
        """Inserts a new token into our trie tree."""
        tokens = self.tokens
        if not isinstance(token, str):
            raise TypeError("Input must be a string.")
        if '$' in token:
            raise ValueError("Input must not contain $ character.")
        for char in token:
            tokens = tokens.setdefault(char, {})
        tokens['$'] = True

    def contains(self, token):
        """Returns true if token is in trie, false if not."""
        if not isinstance(token, str):
            raise TypeError("Input must be a string.")
        if '$' in token:
            raise ValueError("Input must not contain $ character.")
        tokens = self.tokens
        for char in token:
            if char not in tokens:
                return False
            tokens = tokens[char]
        return tokens.get('$', False)

    def traversal(self, start):
        """Performs a depth-first traversal of our trie beginning at the
        string we specify as start"""
        if not isinstance(start, str):
            raise TypeError("Input must be a string.")
        if '$' in start:
            raise ValueError("Input must not contain $ character.")
        tokens = self.tokens
        for char in start:
            tokens = tokens[char]
        # step through the trie from here
        # yeild each word as you come to it
        # the type of traversal isn't important, just make one
