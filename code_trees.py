from helpers import get_code
import matplotlib.pyplot as plt

class Node:
    def __init__(self):
        self.left = None
        self.right = None
        self.val = "X"
        self.info = ""


class CodeTree:
    def __init__(self, total_words: int):
        self.root = Node()
        self.word_id = 1
        self.total_words = total_words

        digits = len(str(total_words)) if total_words > 0 else 1
        self.label_width = 1 + digits

    def _format_leaf_label(self, idx: int) -> str:
        digits = self.label_width - 1
        return f"w{idx:0{digits}d}"

    def add_word(self, word: str):
        """
        Adds edges on the current tree based on the input word

        Word-RAM complexities: consider tree_x_min, tree_x_max, tree_max_dept the effective numbers, varibles for a tree
        - Time: O(||word|)
        - Space: O(|word|)
        Real-RAM complexities:
        - Time: O(|word|)
        - Space: O(|word|)

        :param self: the instance of CodeTree
        :param word: the code word as string
        """
        current = self.root

        for bit in word.strip():
            if bit == '0':
                if current.left is None:
                    current.left = Node()
                current = current.left
            elif bit == '1':
                if current.right is None:
                    current.right = Node()
                current = current.right
            else:
                raise ValueError(f"Invalid bit '{bit}' in codeword '{word}'")

        current.val = self._format_leaf_label(self.word_id)
        self.word_id += 1


def plot_tree(root, figsize=(14, 10)):
    """
    Plots the binary tree using matplotlib

    Word-RAM complexities: consider tree_x_min, tree_x_max, tree_max_dept the effective numbers, varibles for a tree
    - Time: O(no_tree_nodes * logmax(tree_x_min, tree_x_max, tree_max_depth))
    - Space: O(no_tree_nodes * logmax(tree_x_min, tree_x_max))
    Real-RAM complexities:
    - Time: O(no_tree_nodes)
    - Space: O(no_tree_nodes)

    :param root: the root of the binary tree as Node
    :param figsize: size of the visualization image in the window
    """
    positions = {}
    max_depth = 0

    def compute_positions(node, depth, x_min, x_max):
        """
        Assigns each node an "aligned" set of coordinates (x, y) based on the leftwise point of the tree,
        rightwise and maximum depth

        Word-RAM complexities: consider tree_x_min, tree_x_max, tree_max_dept the effective numbers, varibles for a tree
        - Time: O(no_tree_nodes * logmax(tree_x_min, tree_x_max, tree_max_depth))
        - Space: O(no_tree_nodes * logmax(tree_x_min, tree_x_max))
        Real-RAM complexities:
        - Time: O(no_tree_nodes)
        - Space: O(no_tree_nodes)

        :param node: Node
        :param depth: current depth (of the <node> param)
        :param x_min: current x_min (identified till this depth)
        :param x_max: current x_max (identified till this depth)
        """
        nonlocal max_depth
        if node is None:
            return

        max_depth = max(max_depth, depth)
        x = (x_min + x_max) / 2
        y = -depth
        positions[node] = (x, y)

        compute_positions(node.left, depth + 1, x_min, x)
        compute_positions(node.right, depth + 1, x, x_max)

    compute_positions(root, 0, 0, 1)

    _, ax = plt.subplots(figsize=figsize)
    ax.set_axis_off()

    for node, (x, y) in positions.items():
        if node.left:
            x2, y2 = positions[node.left]
            ax.plot([x, x2], [y, y2], 'k-', linewidth=1)
        if node.right:
            x2, y2 = positions[node.right]
            ax.plot([x, x2], [y, y2], 'k-', linewidth=1)

    for node, (x, y) in positions.items():
        ax.text(
            x, y, node.val,
            fontsize=10,
            ha='center', va='center',
            bbox=dict(facecolor='white', edgecolor='black', boxstyle='circle')
        )

    plt.tight_layout()
    plt.show()


def prefix_tree_presentation(filename):
    print("Binary tree visualizer")
    print("For huffman tree usages, comment the last call to prefix_tree_presentation for clean module presentation")

    words = get_code(filename)

    # Construct the binary tree
    bintree = CodeTree(len(words))
    for word in words:
        bintree.add_word(word)

    plot_tree(bintree.root)


prefix_tree_presentation("code_words")
