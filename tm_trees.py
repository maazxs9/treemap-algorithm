"""
Assignment 2: Trees for Treemap

=== Module Description ===
This module contains the basic tree interface required by the treemap
visualiser. You will both add to the abstract class, and complete a
concrete implementation of a subclass to represent files and folders on your
computer's file system.
"""
from __future__ import annotations

import math
import os
from random import randint
from typing import List, Tuple, Optional

def get_colour() -> Tuple[int, int, int]:
    """This function picks a random colour selectively such that it is not on
    the grey scale. The colour is close to the grey scale if the r g b values
    have a small variance. This function checks if all the numbers are close
    to the mean, if so, it shifts the last digit by 150.

    This way you can't confuse the leaf rectangles with folder rectangles,
    because the leaves will always be a colour, never close to black / white.
    """
    rgb = [randint(0, 255), randint(0, 255), randint(0, 255)]
    avg = sum(rgb) // 3
    count = 0
    for item in rgb:
        if abs(item - avg) < 20:
            count += 1
    if count == 3:
        rgb[2] = (rgb[2] + 150) % 255
    return tuple(rgb)
class TMTree:
    """A TreeMappableTree: a tree that is compatible with the treemap
    visualiser.

    This is an abstract class that should not be instantiated directly.

    You may NOT add any attributes, public or private, to this class.
    However, part of this assignment will involve you implementing new public
    *methods* for this interface.
    You should not add any new public methods other than those required by
    the client code.
    You can, however, freely add private methods as needed.

    === Public Attributes ===
    rect:
        The pygame rectangle representing this node in the treemap
        visualization.
    data_size:
        The size of the data represented by this tree.

    === Private Attributes ===
    _colour:
        The RGB colour value of the root of this tree.
    _name:
        The root value of this tree, or None if this tree is empty.
    _subtrees:
        The subtrees of this tree.
    _parent_tree:
        The parent tree of this tree; i.e., the tree that contains this tree
        as a subtree, or None if this tree is not part of a larger tree.
    _expanded:
        Whether or not this tree is considered expanded for visualization.

    === Representation Invariants ===
    - data_size >= 0
    - If _subtrees is not empty, then data_size is equal to the sum of the
      data_size of each subtree.

    - _colour's elements are each in the range 0-255.

    - If _name is None, then _subtrees is empty, _parent_tree is None, and
      data_size is 0.
      This setting of attributes represents an empty tree.

    - if _parent_tree is not None, then self is in _parent_tree._subtrees

    - if _expanded is True, then _parent_tree._expanded is True
    - if _expanded is False, then _expanded is False for every tree
      in _subtrees
    - if _subtrees is empty, then _expanded is False
    """

    rect: Tuple[int, int, int, int]
    data_size: int
    _colour: Tuple[int, int, int]
    _name: str
    _subtrees: List[TMTree]
    _parent_tree: Optional[TMTree]
    _expanded: bool

    def __init__(self, name: str, subtrees: List[TMTree],
                 data_size: int = 0) -> None:
        """Initialize a new TMTree with a random colour and the provided <name>.

        If <subtrees> is empty, use <data_size> to initialize this tree's
        data_size.

        If <subtrees> is not empty, ignore the parameter <data_size>,
        and calculate this tree's data_size instead.

        Set this tree as the parent for each of its subtrees.

        Precondition: if <name> is None, then <subtrees> is empty.
        """
        self.rect = (0, 0, 0, 0)
        self._name = name
        self._subtrees = subtrees[:]
        self._parent_tree = None

        # You will change this in Task 5
        self._expanded = False

        # TODO: (Task 1) Complete this initializer by doing two things:
        # 1. Initialize self._colour and self.data_size, according to the
        # docstring.
        # 2. Set this tree as the parent for each of its subtrees.
        self._name = name
        self._colour = get_colour()
        self._subtrees = subtrees[:]
        if not subtrees:
            self.data_size = data_size
        else:
            self.data_size = sum(sub_tree.data_size for sub_tree in subtrees if
                                 not sub_tree.is_empty())

        for subtree in subtrees:
            if not subtree.is_empty():
                subtree._parent_tree = self
    def is_empty(self) -> bool:
        """Return True iff this tree is empty.
        """
        return self._name is None

    def get_parent(self) -> Optional[TMTree]:
        """Returns the parent of this tree.
        """
        return self._parent_tree

    def update_rectangles(self, rect: Tuple[int, int, int, int]) -> None:
        """Update the rectangles in this tree and its descendents using the
        treemap algorithm to fill the area defined by pygame rectangle <rect>.
        """
        # TODO: (Task 2) Complete the body of this method.
        # Read the handout carefully to help get started identifying base cases,
        # then write the outline of a recursive step.
        #
        # Programming tip: use "tuple unpacking assignment" to easily extract
        # elements of a rectangle, as follows.
        # x, y, width, height = rect
        x, y, w, h = rect

        if self.data_size == 0:
            self.rect = (0, 0, 0, 0)
        else:
            self.rect = rect
            horizon = w > h
            check = x if horizon else y
            dimen = w if horizon else h

            for ith, subtree in enumerate(self._subtrees):
                if len(self._subtrees) - 1 != ith:
                    tot_perc = subtree.data_size / self.data_size
                    sec_dimen = math.floor(tot_perc * dimen)
                else:
                    sec_dimen = dimen + (x - check) if horizon else dimen \
                        + (y - check)
                rect_made = (check, y, sec_dimen, h) if horizon else (
                    x, check, w, sec_dimen)
                subtree.update_rectangles(rect_made)
                check += sec_dimen
    def get_rectangles(self) -> List[Tuple[Tuple[int, int, int, int],
                                           Tuple[int, int, int]]]:
        """Return a list with tuples for every leaf in the displayed-tree
        rooted at this tree. Each tuple consists of a tuple that defines the
        appropriate pygame rectangle to display for a leaf, and the colour
        to fill it with.
        """
        # TODO: (Task 2) Complete the body of this method.
        comb_r = []
        if self.data_size != 0 and not self.is_empty():
            if self._expanded:
                for subtree in self._subtrees:
                    comb_r.extend(subtree.get_rectangles())
            else:
                comb_r.append((self.rect, self._colour))
        return comb_r
    def get_tree_at_position(self, pos: Tuple[int, int]) -> Optional[TMTree]:
        """
        Return the leaf in the displayed-tree rooted at this tree whose
        rectangle contains position <pos>, or None if <pos> is outside of this
        tree's rectangle.
        """
        # TODO: (Task 3) Complete the body of this method
        x, y = pos
        rect = self.rect  # Assuming self.rect is (x_len, y_len, side_x, side_y)

        if self.is_empty() or (self._subtrees == [] or not self._expanded):
            return self._get_tree_at_position_helping(x, y, rect)
        else:
            return self._get_tree_at_position_helpingtwo(pos)

    def _get_tree_at_position_helping(self, x: int, y: int,
                                      rect: Tuple[int, int, int, int]) -> \
            Optional['TMTree']:
        x_len, y_len, side_x, side_y = rect
        if x_len <= x <= x_len + side_x and y_len <= y <= y_len + side_y:
            return self
        else:
            return None

    def _get_tree_at_position_helpingtwo(self, pos: Tuple[int, int]) -> \
            Optional['TMTree']:
        touch = None

        for subtree in self._subtrees:
            getting_pos = subtree.get_tree_at_position(pos)
            if getting_pos is not None:
                if touch is None or getting_pos.rect[0] < touch.rect[0] or \
                    (getting_pos.rect[0] == touch.rect[0]
                     and getting_pos.rect[1] < touch.rect[1]):
                    touch = getting_pos
        return touch
    def update_data_sizes(self) -> int:
        """Update the data_size for this tree and its subtrees, based on the
        size of their leaves, and return the new size.

        If this tree is a leaf, return its size unchanged.
        """
        # TODO: (Task 4) Complete the body of this method.
        if self._subtrees:
            c = 0
            for subtree in self._subtrees:
                c += subtree.update_data_sizes()
            self.data_size = c
        return self.data_size if self._subtrees else self.data_size
    def move(self, destination: TMTree) -> None:
        """If this tree is a leaf, and <destination> is not a leaf, move this
        tree to be the last subtree of <destination>. Otherwise, do nothing.
        """
        # TODO: (Task 4) Complete the body of this method.
        des_check = bool(destination._subtrees)
        if not self._subtrees and des_check:
            if self._parent_tree:
                self._parent_tree._subtrees.remove(self)
                self._parent_tree.data_size -= self.data_size
            self._parent_tree = destination
            destination._subtrees.append(self)
    def change_size(self, factor: float) -> None:
        """Change the value of this tree's data_size attribute by <factor>.

        Always round up the amount to change, so that it's an int, and
        some change is made.

        Do nothing if this tree is not a leaf.
        """
        # TODO: (Task 4) Complete the body of this method
        if not self._subtrees:
            if factor > 0:
                form_s = math.ceil(self.data_size * factor)
                self.data_size += form_s
            else:
                form_s = math.floor(self.data_size * factor)
                if self.data_size != 0:
                    new_s = self.data_size + form_s
                    self.data_size = max(new_s, 1)
    def delete_self(self) -> bool:
        """Removes the current node from the visualization and
        returns whether the deletion was successful.

        Only do this if this node has a parent tree.
        """
        # TODO: (Task 4) Complete the body of this method

        if self._parent_tree is None:
            return False
        self._parent_tree._subtrees.remove(self)
        if len(self._parent_tree._subtrees) == 0 and self._parent_tree:
            return self._parent_tree.delete_self()

        self._parent_tree.data_size -= self.data_size
        return True

    # TODO: (Task 5) Write the methods expand, expand_all, collapse, and
    # TODO: collapse_all, and add the displayed-tree functionality to the
    # TODO: methods from Tasks 2 and 3
    def expand(self) -> None:
        """Sets this tree to be expanded. But not if it is a leaf.
        """
        if self._subtrees:
            self._expanded = True
        if self._parent_tree and self._expanded:
            self._parent_tree.expand()

    def expand_all(self) -> None:
        """Sets this tree and all its descendants to be expanded, apart from the
        leaf nodes.
        """
        if self._subtrees:
            self.expand()
            for subtree in self._subtrees:
                subtree.expand_all()

    def collapse(self) -> None:
        """Collapses the parent tree of the given tree node and also collapse
        all of its descendants.
        """
        #
        # NOTES: - This method could be called with any node on the tree.
        #        - After this method is called, the parent of the given node
        #          should not be expanded, and any node underneath this tree
        #          should not be expanded.
        #
        if not self.is_empty():
            self.help_collapse()
        if self._parent_tree:
            self._parent_tree._expanded = False
            for subtree in self._parent_tree._subtrees:
                subtree.help_collapse()

    def help_collapse(self) -> None:
        """Helper function
        """
        self._expanded = False
        for subtree in self._subtrees:
            subtree.collapse()

    def collapse_all(self) -> None:
        """ Collapses ALL nodes in the tree.
        """
        #
        # NOTES - This should work if it is called on any node in the tree.
        #       - After this method is called, _expanded should be set to false
        #         for all nodes in the tree.
        self.collapse()
        if self._parent_tree:
            self._parent_tree.collapse_all()
    # Methods for the string representation
    def get_path_string(self) -> str:
        """
        Return a string representing the path containing this tree
        and its ancestors, using the separator for this OS between each
        tree's name.
        """
        if self._parent_tree is None:
            return self._name
        else:
            return self._parent_tree.get_path_string() + \
                self.get_separator() + self._name

    def get_separator(self) -> str:
        """Return the string used to separate names in the string
        representation of a path from the tree root to this tree.
        """
        raise NotImplementedError

    def get_suffix(self) -> str:
        """Return the string used at the end of the string representation of
        a path from the tree root to this tree.
        """
        raise NotImplementedError


class FileSystemTree(TMTree):
    """A tree representation of files and folders in a file system.

    The internal nodes represent folders, and the leaves represent regular
    files (e.g., PDF documents, movie files, Python source code files, etc.).

    The _name attribute stores the *name* of the folder or file, not its full
    path. E.g., store 'assignments', not '/Users/user/projects/assignments'

    The data_size attribute for regular files is simply the size of the file,
    as reported by os.path.getsize.
    """

    def __init__(self, path: str) -> None:
        """Store the file tree structure contained in the given file or folder.

        Precondition: <path> is a valid path for this computer.
        """
        # Remember that you should recursively go through the file system
        # and create new FileSystemTree objects for each file and folder
        # encountered.
        #
        # Also remember to make good use of the superclass constructor!
        # TODO: (Task 1) Implement the initializer
        self._path = path
        if os.path.isfile(path):
            super().__init__(os.path.basename(path), [],
                             os.path.getsize(path))
        else:
            path_names = [os.path.join(path, name)
                          for name in os.listdir(path)]
            subtrees = [FileSystemTree(pathsss) for pathsss in path_names]
            super().__init__(os.path.basename(path), subtrees, 0)

    def get_separator(self) -> str:
        """Return the file separator for this OS.
        """
        return os.sep

    def get_suffix(self) -> str:
        """Return the final descriptor of this tree.
        """

        def convert_size(data_size: float, suffix: str = 'B') -> str:
            suffixes = {'B': 'kB', 'kB': 'MB', 'MB': 'GB', 'GB': 'TB'}
            if data_size < 1024 or suffix == 'TB':
                return f'{data_size:.2f}{suffix}'
            return convert_size(data_size / 1024, suffixes[suffix])

        components = []
        if len(self._subtrees) == 0:
            components.append('file')
        else:
            components.append('folder')
            components.append(f'{len(self._subtrees)} items')
        components.append(convert_size(self.data_size))
        return f' ({", ".join(components)})'


if __name__ == '__main__':
    import python_ta

    python_ta.check_all(config={
        'allowed-import-modules': [
            'python_ta', 'typing', 'math', 'random', 'os', '__future__'
        ]
    })
