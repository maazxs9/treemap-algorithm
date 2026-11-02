"""Assignment 2: Modelling CS Education research paper data

=== Module Description ===
This module contains a new class, PaperTree, which is used to model data on
publications in a particular area of Computer Science Education research.
This data is adapted from a dataset presented at SIGCSE 2019.
You can find the full dataset here: https://www.brettbecker.com/sigcse2019/

Although this data is very different from filesystem data, it is still
hierarchical. This means we are able to model it using a TMTree subclass,
and we can then run it through our treemap visualisation tool to get a nice
interactive graphical representation of this data.

TODO: (Task 6) Complete the steps below
Recommended steps:
1. Start by reviewing the provided dataset in cs1_papers.csv. You can assume
   that any data used to generate this tree has this format,
   i.e., a csv file with the same columns (same column names, same order).
   The categories are all in one column, separated by colons (':').
   However, you should not make assumptions about what the categories are, how
   many categories there are, the maximum number of categories a paper can have,
   or the number of lines in the file.

2. Read through all the docstrings in this file once. There is a lot to take in,
   so don't feel like you need to understand it all the first time.
   Draw some pictures!
   We have provided the headers of the initializer as well as of some helper
   functions we suggest you implement. Note that we will not test any
   private top-level functions, so you can choose not to implement these
   functions, and you can add others if you want to for your solution.
   For this task, we will be testing that you are building the correct tree,
   not that you are doing it in a particular way. We will access your class
   in the same way as in the client code in the visualizer.

3. Plan out what you'll need to do to implement the PaperTree initializer.
   In particular, think about how to use the boolean parameters to do different
   things in setting up the tree. You may also find it helpful to review the
   Python documentation about the csv module, which you are permitted and
   encouraged to use. You should have a good plan, including what your subtasks
   are, before you begin writing any code.

4. Write the code for the PaperTree initializer and any helper functions you
   want to use in your design. You should not make any changes to the public
   interface of this module, or of the PaperTree class, but you can add private
   attributes and helpers as needed.

5. Tidy and test your code, and try it with the visualizer client code. Make
   sure you have documented any new private attributes, and that PyTA passes
   on your code.
"""
import csv
from typing import List, Dict
from tm_trees import TMTree

# Filename for the dataset
DATA_FILE = 'cs1_papers.csv'


class PaperTree(TMTree):
    """A tree representation of Computer Science Education research paper data.

    === Private Attributes ===
    TODO: Add any of your new private attributes here.
    These should store information about this paper's <authors> and <doi>.

    === Inherited Attributes ===
    rect:
        The pygame rectangle representing this node in the treemap
        visualization.
    data_size:
        The size of the data represented by this tree.
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
    - All TMTree RIs are inherited.
    """

    # TODO: Add the type contracts for your new attributes here

    def __init__(self, name: str, subtrees: List[TMTree], authors: str = '',
                 doi: str = '', citations: int = 0, by_year: bool = True,
                 all_papers: bool = False) -> None:
        """Initialize a new PaperTree with the given <name> and <subtrees>, 
        <authors> and <doi>, and with <citations> as the size of the data.

        If <all_papers> is True, then this tree is to be the root of the paper
        tree. In that case, load data about papers from DATA_FILE to build the
        tree.

        If <all_papers> is False, Do NOT load new data.

        <by_year> indicates whether or not the first level of subtrees should be
        the years, followed by each category, subcategory, and so on. If
        <by_year> is False, then the year in the dataset is simply ignored.
        """
        # TODO: Complete this initializer. Your implementation must not
        # TODO: duplicate anything done in the superclass initializer.
        self._authors = authors
        self._doi = doi

        if all_papers:
            subtrees = _build_tree_from_dict(_load_papers_to_dict(by_year))
        TMTree.__init__(self, name, subtrees, citations)

    def get_separator(self) -> str:
        """Return the file separator for this OS.
        """
        return ':'

    def get_suffix(self) -> str:
        """Return the final descriptor of this tree.
        """
        if not self._subtrees:
            return ' (Paper)'
        else:
            return ' (Category)'

def _load_papers_to_dict(by_year: bool = True) -> Dict:
    """Return a nested dictionary of the data read from the papers dataset file.

    If <by_year>, then use years as the roots of the subtrees of the root of
    the whole tree. Otherwise, ignore years and use categories only.
    """
    # TODO: Implement this helper, or remove it if you do not plan to use it
    def add_to_dict(acc_temp_dict: Dict, categories: List[str], paper_info: List):
        """Recursively add paper_info into the paper_dict following the categories path."""
        if not categories:
            return

        # Handle the current category
        categ = categories[0]

        if categ not in acc_temp_dict:
            acc_temp_dict[categ] = ([], {}) if len(categories) > 1 else ([paper_info], {})

        if len(categories) == 1:
            # We're at the leaf category, add the paper info here
            if paper_info not in acc_temp_dict[categ][0]:  # Avoid duplicate entries
                acc_temp_dict[categ][0].append(paper_info)
        else:
            # Recurse deeper into the categories
            add_to_dict(acc_temp_dict[categ][1], categories[1:], paper_info)

    new_d = {}
    with open(DATA_FILE, 'r') as file:
        given = csv.reader(file)
        next(given, None)  # Skip header row if present

        for c in given:
            dire, name, date, categ2, link, apa = c
            comb_l = categ2.split(': ')
            if by_year:
                comb_l.insert(0, date)
            new_l = [dire, name, link, int(apa)]

            # Add this paper's info to the dictionary
            add_to_dict(new_d, comb_l, new_l)

    return new_d


def _build_tree_from_dict(nested_dict: Dict) -> List[PaperTree]:
    """Return a list of trees from the nested dictionary <nested_dict>.
    """
    # TODO: Implement this helper, or remove it if you do not plan to use it
    def build_tree(diff_lists, info):
        """Recursively builds the tree from the nested dictionary."""
        new_l = [PaperTree(lst[1], [], lst[0], lst[2], lst[3], False, False)
                 for lst in info[0]]
        if info[1] == {}:
            return PaperTree(diff_lists, new_l, all_papers=False,
                             by_year=False)
        else:
            new_s_t = [build_tree(sub_category, info[1][sub_category]) for
                         sub_category in info[1]]
            new_l.extend(new_s_t)
            return PaperTree(diff_lists, new_l, all_papers=False,
                             by_year=False)

    return [build_tree(category, nested_dict[category]) for category in
            nested_dict]

if __name__ == '__main__':
    import python_ta
    python_ta.check_all(config={
        'allowed-import-modules': ['python_ta', 'typing', 'csv', 'tm_trees'],
        'allowed-io': ['_load_papers_to_dict'],
        'max-args': 8
    })
