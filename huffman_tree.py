import heapq
import matplotlib.pyplot as plt


class Node:
    def __init__(self, symbol=None, prob=None, code=None):
        self.left = None
        self.right = None
        self.symbol = symbol
        self.prob = prob
        self.code = code


class CodeTree:
    def __init__(self, total_words: int):
        self.root = Node()
        self.total_words = total_words

    def add_word(self, word: str, symbol: str, prob: float = None):
        """
        Adds edges to the binary tree based on the word bits

        Word-RAM complexities:
        - Time: O(|word|)
        - Space: O(|word|)
        Real-RAM complexities:
        - Time: O(|word|)
        - Space: O(|word|)

        :param self: the instance of CodeTree
        :param word: the code word as string
        :param symbol: a string
        :param prob: The probability of the word as float in [0, 1]
        """
        current = self.root
        for bit in word.strip():
            if bit == "0":
                if current.left is None:
                    current.left = Node()
                current = current.left
            elif bit == "1":
                if current.right is None:
                    current.right = Node()
                current = current.right
            else:
                raise ValueError(f"Invalid bit '{bit}' in codeword '{word}'")
        current.symbol = symbol
        current.prob = prob
        current.code = word


def propagate_probs(node: Node):
    """
    The probability of the current node is calculated as sum of its first-level children
    Word-RAM complexities:
    - Time: O(|no_subtree_nodes_of_current_node|)
    - Space: O(1)
    Real-RAM complexities:
    - Time: O(|no_subtree_nodes_of_current_node|)
    - Space: O(1)

    :param node: Node
    """
    if node is None:
        return 0.0
    if node.left is None and node.right is None:
        return 0.0 if node.prob is None else node.prob
    lp = propagate_probs(node.left)
    rp = propagate_probs(node.right)
    node.prob = lp + rp
    return node.prob


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
            ax.plot([x, x2], [y, y2])
        if node.right:
            x2, y2 = positions[node.right]
            ax.plot([x, x2], [y, y2])

    for node, (x, y) in positions.items():
        if node.symbol is None:
            if node.prob is not None:
                label = f"p={node.prob:.3f}"
            else:
                label = "•"
        else:
            if node.prob is not None:
                label = f"{node.symbol}\np={node.prob:.3f}"
            else:
                label = str(node.symbol)
        ax.text(
            x,
            y,
            label,
            fontsize=10,
            ha="center",
            va="center",
            bbox=dict(facecolor="white", edgecolor="black", boxstyle="circle"),
        )

    plt.tight_layout()
    plt.show()


class HuffmanNode:
    def __init__(self, prob, symbol=None, left=None, right=None, idx=0):
        self.prob = prob
        self.symbol = symbol
        self.left = left
        self.right = right
        self.idx = idx

    def __lt__(self, other):
        if self.prob != other.prob:
            return self.prob < other.prob
        return self.idx < other.idx


def build_huffman_tree(symbols, probs):
    """
    Creates a Huffman tree from the set of pairs (symbols[i], probs[i])

    Word-RAM complexities: Let K be the maximum number of digits a probability can have
    - Time: O(len(symbols) * log(len(symbols)) * K)     // K appears from comparison between floats or adding
    - Space: O(len(symbols))
    Real-RAM complexities:
    - Time: O(len(symbols) * log(len(symbols)))
    - Space: O(len(symbols))

    :param symbols: list of symbols
    :param probs: list of probabilities
    """
    if len(symbols) != len(probs):
        raise ValueError("Number of symbols and probabilities must match")
    heap = []

    # Making len(symbols) roots
    for i, (s, p) in enumerate(zip(symbols, probs)):
        heap.append(HuffmanNode(p, s, None, None, i))

    # Makes so that every time heap[0] has the smallest probability
    heapq.heapify(heap)
    if len(heap) == 1:
        return heap[0]

    while len(heap) > 1:
        # Select top 2 with smallest probability
        n1 = heapq.heappop(heap)
        n2 = heapq.heappop(heap)

        # Combines those trees
        merged = HuffmanNode(n1.prob + n2.prob, None, n1, n2, min(n1.idx, n2.idx))
        heapq.heappush(heap, merged)

    return heap[0]


def build_huffman_codes(root):
    """
    Provides the actual binary encoding, done by just traversing the tree with DFS

    Word-RAM complexities:
    - Time: O(no_tree_nodes)
    - Space: O(1)
    Real-RAM complexities:
    - Time: O(no_tree_nodes)
    - Space: O(1)

    :param root: HuffmanNode
    """
    codes = {}

    def dfs(node, prefix):
        if node is None:
            return
        if node.symbol is not None:
            codes[node.symbol] = prefix or "0"
            return
        dfs(node.left, prefix + "0")
        dfs(node.right, prefix + "1")

    dfs(root, "")
    return codes


def read_source_from_file(path):
    """
    Reads the code words on the first row and their probabilities in the second row
    Word-RAM complexities:
    - Time: O(len(file))
    - Space: O(len(file))
    Real-RAM complexities:
    - Time: O(len(file))
    - Space: O(len(file))
    :param path: the FS path of the file
    """
    with open(path, "r", encoding="utf-8") as f:
        symbols_line = f.readline()
        probs_line = f.readline()
    symbols = symbols_line.split()
    probs = [float(x) for x in probs_line.split()]
    if len(symbols) != len(probs):
        raise ValueError("Error: symbols and probabilities must have same length")
    return symbols, probs


def huffman_tree_visualization(file_path="huffman_input"):
    symbols, probs = read_source_from_file(file_path)
    print("Alphabet A:", symbols)
    print("Probabilities P:", probs)

    if len(symbols) == 0 or len(probs) == 0 or len(symbols) != len(probs):
        print("Invalid input!")
        return
    h_root = build_huffman_tree(symbols, probs)
    codes = build_huffman_codes(h_root)
    print("\nHuffman code C (symbol -> codeword):")
    for s in symbols:
        print(f"{s} : {codes[s]}")
    codewords = [codes[s] for s in symbols]
    bintree = CodeTree(total_words=len(codewords))
    for word, symbol, prob in zip(codewords, symbols, probs):
        bintree.add_word(word, symbol=symbol, prob=prob)
    propagate_probs(bintree.root)
    plot_tree(bintree.root)

huffman_tree_visualization("huffman_input")
