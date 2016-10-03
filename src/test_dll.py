# -*- coding: utf-8 -*-
"""File tests doubly linked list functionality."""
from __future__ import unicode_literals
from dll import DoublyLinkedList
import pytest


TEST_DLL_PUSH = [
    ("hightower", "hightower"),
    ([1, 2, 3, 4], [1, 2, 3, 4])
]


def test_dll_init(dll_initial_1):
    """Tests that we initialized our list."""
    assert dll_initial_1.head.data == [1, 2, 3]


def test_dll_init_error():
    """Test error is raised when list initialized with non-iterable input."""
    with pytest.raises(TypeError):
        DoublyLinkedList(7)


@pytest.mark.parametrize("value, output", TEST_DLL_PUSH)
def test_dll_push(value, output, dll_initial_2):
    """Test node with value is pushed onto the head."""
    dll_initial_2.push(value)
    assert dll_initial_2.head.data == output


@pytest.mark.parametrize("value, output", TEST_DLL_PUSH)
def test_dll_append(value, output, dll_initial_2):
    """Test node with value is appended to the tail."""
    dll_initial_2.append(value)
    assert dll_initial_2.tail.data == output


def test_dll_pop(dll_initial_2):
    """Test that we pop the head off the list."""
    assert dll_initial_2.pop() == [1, 99, 7]


def test_dll_shift(dll_initial_2):
    """Test that we shift(remove tail) from the list."""
    assert dll_initial_2.shift() == ("booksarecool",)


def test_remove_one(dll_initial_1):
    """Remove value that is in the list."""
    assert dll_initial_1.remove("taco") == "taco"


def test_remove_two(dll_initial_1):
    """Remove value not in the list."""
    with pytest.raises(IndexError):
        dll_initial_1.remove("burrito")


def test_remove_empty_list():
    """Throw an error for attempting to remove from an empty list"""
    empty_list = DoublyLinkedList()
    with pytest.raises(IndexError):
        empty_list.remove("taco")


def test_size_zero():
    """Test the size method of LinkedList class."""
    test_case = DoublyLinkedList()
    assert test_case.size() == 0


def test_size_value():
    """Test the size method of LinkedList class."""
    test_case = DoublyLinkedList()
    test_case.push("one")
    test_case.push("two")
    assert test_case.size() == 2


def test_dunder_len():
    """Test the dunder len method of LinkedList class."""
    test_list = [1, 2, 3, 4, 5, 6, 7]
    test_case = DoublyLinkedList(test_list)
    assert len(test_case) == 7
