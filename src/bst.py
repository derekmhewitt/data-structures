# -*- coding: utf-8 -*-
"""File implements a binary search tree data structure."""
from __future__ import unicode_literals


class Node(object):
    """Example node class with example @property decorators

    pieces of this code are significantly wrong (parent deletion for
    instance) and you should test your implementation throughly"""

    def __init__(self, val, data=None, left=None, right=None,
                 parent=None):
        """sets self.whatever values for instantiating instances of
        the class"""
        self.val = val
        self._left = left
        self._right = right
        self._parent = parent
        self.data = data
        self.depth = 1

    @property
    def left(self):
        """value getter for _left
        syntax: node.left returns _left's value"""
        return self._left

    @left.setter
    def left(self, node):
        """value setter for _left, allows us to say 'set node.left = X'
        elsewhere in our code and not have it throw wrenches at us"""
        self._left = node
        if node is not None:
            node._parent = self

    @left.deleter
    def left(self):
        """allows us to say 'del node.left' elsewhere in our code and
        thereby set it to none"""
        try:
            self._left._parent = None
        except AttributeError:
            pass
        self._left = None

    @property
    def right(self):
        """returns value of _right"""
        return self._right

    @right.setter
    def right(self, node):
        """sets value of _right and right's parent"""
        self._right = node
        if node is not None:
            node._parent = self

    @right.deleter
    def right(self):
        """allows us to say 'del node.right' elsewhere in our code and
        thereby set it to none"""
        try:
            self._right._parent = None
        except AttributeError:
            pass
        self._right = None

    @property
    def parent(self):
        """returns the parent node of self"""
        return self._parent

    @parent.setter
    def parent(self, node):
        """sets the parent node and the parent's left or right,
        as appropriate"""
        self._parent = node
        try:
            if node.val > self.val:
                node._left = self
            else:
                node._right = self
        except AttributeError:
            pass

    def has_left_child(self):
        """Returns true if there is a left child."""
        return self.left

    def has_right_child(self):
        """Returns true if there is a right child."""
        return self.right

    def _insert(self, val, data=None):
        """Helper method to BST.insert method."""
        try:
            if val < self.val:
                if self.has_left_child():
                    self.left._insert(val)
                else:
                    self.left = Node(val, data)
            else:
                if self.has_right_child():
                    self.right._insert(val, data)
                else:
                    self.right = Node(val)
        except TypeError:
            raise(TypeError('Insert values must be the same type'))

    def _in_order(self):
        """
        This internal method is a generator that will output in order traversal
        of a binary tree(left child, parent, right child), one value at a time.
        """
        try:
            for node in self.left._in_order():
                if node is None:
                    pass
                else:
                    yield node
        except AttributeError:
            pass
        yield self.val
        try:
            for node in self.right._in_order():
                if node is None:
                    pass
                else:
                    yield node
        except AttributeError:
            pass

    def _pre_order(self):
        """
        Returns a generator that will output preorder traversalof a binary
        tree(parent, left child, right child), one value at a time.
        """
        yield self.val
        try:
            for node in self.left._pre_order():
                if node is None:
                    pass
                else:
                    yield node
        except AttributeError:
            pass
        try:
            for node in self.right._pre_order():
                if node is None:
                    pass
                else:
                    yield node
        except AttributeError:
            pass

    def _post_order(self):
        """
        Returns a generator that will output postorder traversalof a binary
        tree(left child, right child, parent), one value at a time.
        """
        try:
            for node in self.left._post_order():
                if node is None:
                    pass
                else:
                    yield node
        except AttributeError:
            pass
        try:
            for node in self.right._post_order():
                if node is None:
                    pass
                else:
                    yield node
        except AttributeError:
            pass
        yield self.val


class BinarySearchTree(object):
    """BinarySearchTree implements a Binary Search Tree data structure
    and associated methods."""

    def __init__(self, root=None):
        """Create an instance of our Binary Search Tree w/ supplied
        input, or an emptry tree."""
        self.length = 0
        if root:
            self.root = Node(root)
            self.length = 1
        else:
            self.root = root

    def insert(self, val, data=None):
        """Inserts a value into the BST.  If the value is already in
        the BST it will be ingored."""
        if not self.contains(val):
            if self.root:
                self.root._insert(val, data)
            else:
                self.root = Node(val, data)
            self.length += 1
        self._update_balance(self.root)
        new_node = self.find_node(val)
        self._check_balance_and_call(new_node)
        self._update_balance(self.root)

    def contains(self, val):
        """Will return True if val is in the BST, or False if it's not."""
        try:
            return self._contains(val, self.root)
        except AttributeError:
            pass

    def _contains(self, val, current_node):
        """Helper method to contains, recursively called and returns True
        if we find the node we're looking for, False if not."""
        try:
            if val == current_node.val:
                return True
            elif current_node.right and val > current_node.val:
                return self._contains(val, current_node.right)
            elif current_node.left and val < current_node.val:
                return self._contains(val, current_node.left)
            else:
                return False
        except TypeError:
            raise(TypeError('Node values must be the same type'))

    def size(self):
        """Will return the integer size of the BST, zero if BST is empty."""
        return self.length

    def __len__(self):
        """Returns size of tree using builtin length method."""
        return self.length

    def depth(self, starting_point=None):
        """Will return the depth of the tree by counting "levels".  An empty
        BST will return 0, a BST with 1 value will return 1, a BST with 2
        values will return 2, and the value will fluctuate from then on
        depending on the branch layout."""
        if starting_point is None:
            starting_point = self.root
        try:
            ld = starting_point.left.depth
        except AttributeError:
            ld = 0
        try:
            rd = starting_point.right.depth
        except AttributeError:
            rd = 0
        try:
            md = starting_point.depth
        except AttributeError:
            md = 0
        return max(ld, rd, md)

    def balance(self, starting_point=None):
        """Will return an integer that's positive or negative that represents
        the difference between depth on both sides from the starting point."""
        if starting_point is None:
            if self.root is not None:
                starting_point = self.root
            else:
                return 0
        left_depth = starting_point.left.depth if starting_point.left else 0
        right_depth = starting_point.right.depth if starting_point.right else 0
        return left_depth - right_depth

    def in_order(self, starting_point=None):
        """
        This function will return a generator that will return the values
        of the tree using in-order traversal, one value at a time.
        """
        if starting_point is None:
            starting_point = self.root
        if self.length == 0:
            raise IndexError("You can't in-order traverse an empty Tree.")
        return starting_point._in_order()

    def pre_order(self, starting_point=None):
        """
        This function will return a generator that will return the values
        of the tree using pre_order traversal, one value at a time.
        """
        if self.length == 0:
            raise IndexError("You can't pre-order traverse an empty Tree.")
        if starting_point is None:
            starting_point = self.root
        return starting_point._pre_order()

    def post_order(self, starting_point=None):
        """
        This function will return a generator that will return the values
        of the tree using post_order traversal, one value at a time.
        """
        if self.length == 0:
            raise IndexError("You can't post-order traverse an empty Tree.")
        if starting_point is None:
            starting_point = self.root
        return starting_point._post_order()

    def breadth_first(self, starting_point=None):
        """
        This internal method is a generator that will output breadth first
        traversal of a binary tree(left child, right child, parent),
        one value at a time.
        """
        if self.length == 0:
            raise IndexError("You can't breadth-first traverse an empty Tree.")
        from dll import DoublyLinkedList
        unvisited = DoublyLinkedList()
        if starting_point is None:
            starting_point = self.root
        elif self.contains(starting_point) is False:
            raise IndexError('Starting point is not in the Tree.')
        unvisited.push(starting_point)
        visited = []
        while unvisited.size() > 0:
            current = unvisited.shift()
            if current not in visited:
                visited.append(current)
                if current.left:
                    unvisited.push(current.left)
                if current.right:
                    unvisited.push(current.right)
                yield current.val

    def delete(self, val):
        """Removes a node with val from the Tree, returns None."""
        delete_me = self.find_node(val)
        if not delete_me:
            return
        if delete_me.left is not None:
            try:
                left_childs = list(self.in_order(delete_me.left))
            except AttributeError:
                left_childs = []
        else:
            left_childs = []
        if delete_me.right is not None:
            try:
                right_childs = list(self.in_order(delete_me.right))
            except AttributeError:
                right_childs = []
        else:
            right_childs = []
        try:
            left_choice = left_childs[-1]
        except IndexError:
            left_choice = None
        try:
            right_choice = right_childs[0]
        except IndexError:
            right_choice = None
        try:
            a = abs(right_choice - val)
        except TypeError:
            a = 0
        try:
            b = abs(val - left_choice)
        except TypeError:
            b = 0
        if a > b:
            if left_choice is not None:
                left_choice = self.find_node(left_choice)
                left_choice.parent.right = None
                if self.root == delete_me:
                    self.root = left_choice
                if left_choice.left is not None:
                    left_choice.left.parent = left_choice.parent
                left_choice.parent = None
                delete_me.val = left_choice.val
            else:
                if delete_me.parent.right is not None:
                    delete_me.parent.right = None
                    delete_me.parent.left = None
                delete_me.parent = None
        else:
            if right_choice is not None:
                right_choice = self.find_node(right_choice)
                right_choice.parent.left = None
                if self.root == delete_me:
                    self.root = right_choice
                if right_choice.right is not None:
                    right_choice.right.parent = right_choice.parent
                right_choice.parent = None
                delete_me.val = right_choice.val
            else:
                if delete_me.parent is not None:
                    delete_me.parent.right = None
                    delete_me.parent.left = None
                delete_me.parent = None
        self._check_balance_and_call(delete_me)
        self._update_balance(self.root)
        self.length -= 1

    def find_node(self, val):
        """Will return the node with the val we asked for or False if it
        isn't in the BST."""
        return self._find_node(val, self.root)

    def _find_node(self, val, current_node):
        """Helper method to find_node, recursively called and returns the node
        or False if it isn't in the BST."""
        if self.length > 0:
            try:
                if val == current_node.val:
                    return current_node
                elif current_node.right and val > current_node.val:
                    return self._find_node(val, current_node.right)
                elif current_node.left and val < current_node.val:
                    return self._find_node(val, current_node.left)
                else:
                    return False
            except TypeError:
                raise(TypeError('Node values must be the same type'))

    def _left_rotation(self, pivot_parent):
        """Performs a left rotation on a given section of our BST."""
        a = pivot_parent
        b = pivot_parent.right
        if pivot_parent.parent is None:
            z = None
            self.root = b
        else:
            z = pivot_parent.parent
        try:
            w = pivot_parent.right.left
        except AttributeError:
            w = None
        b.left = a
        a.right = w
        b.parent = z

    def _right_rotation(self, pivot_parent):
        """Performs a right rotation on a given section of our BST."""
        a = pivot_parent
        b = pivot_parent.left
        if pivot_parent.parent is None:
            z = None
            self.root = b
        else:
            z = pivot_parent.parent
        try:
            w = pivot_parent.left.right
        except AttributeError:
            w = None
        a.left = w
        b.right = a
        b.parent = z

    def _check_balance_and_call(self, starting_point, previous=None):
        """Checks the balance of parents of a given node up to the root, calls
        _determine_rotations_and_call if rotations needed."""
        if starting_point is None:
            return
        bal = self.balance(starting_point)
        if previous is None:
            if bal > 0:
                previous = starting_point.left
            elif bal < 0:
                previous = starting_point.right
        if bal > 1:
            self._determine_rotations_and_call(starting_point, previous)
            return
        if bal < -1:
            self._determine_rotations_and_call(starting_point, previous)
            return
        if starting_point.parent is None:
            return
        self._check_balance_and_call(starting_point.parent, starting_point)
        return

    def _determine_rotations_and_call(self, starting_point, previous):
        """Determine which rotations are needed and make them."""
        start_bal = self.balance(starting_point)
        if previous is not None:
            prev_bal = self.balance(previous)
        else:
            prev_bal = 0
        if start_bal < -1:
            if prev_bal > 0:
                self._right_rotation(starting_point.right)
            self._left_rotation(starting_point)
        elif start_bal > 1:
            if prev_bal < 0:
                self._left_rotation(starting_point.left)
            self._right_rotation(starting_point)

    def _update_balance(self, starting_point):
        """Updates the balance of the BST, it's intended this will be called
        on self.root. Recursively calls itself until there are no more
        children to update, then resets the depth value of all nodes."""
        if starting_point.left:
            left_depth = self._update_balance(starting_point.left)
        else:
            left_depth = 0
        if starting_point.right:
            right_depth = self._update_balance(starting_point.right)
        else:
            right_depth = 0
        starting_point.depth = max(left_depth, right_depth) + 1
        return starting_point.depth
