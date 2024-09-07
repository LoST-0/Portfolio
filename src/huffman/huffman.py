from numpy.ma.core import compressed

from src.source.source_draft import Source,sourcefy
from src.utils import TreeNode

class HuffmanCompressor(Source):
    """
    A class for Huffman compression and decompression.

    This class extends the Source class to perform Huffman encoding and decoding on a given source of symbols
    with associated probabilities. Huffman coding is a lossless data compression algorithm that assigns variable-length
    codes to input characters, with shorter codes assigned to more frequent characters.

    Attributes:
        symbols (list): A list of symbols to be encoded.
        size (int): The number of unique symbols.
    """

    def __init__(self,source:Source):
        """
        Initialize the HuffmanCompressor with a source.

        :param source: The source object containing symbols and their associated probabilities.
        :type source: Source
        """
        super().__init__(source.probabilities)
        self.symbols = source.symbols
        self.size = len(self.symbols)


    def _huffman_traverse_helper(self, node, symbol):
        """
        A helper method for traversing the Huffman tree to find the code for a given symbol.

        :param node: The current node in the Huffman tree.
        :type node: TreeNode
        :param symbol: The symbol to find the code for.
        :type symbol: str
        :return: The binary code for the given symbol.
        :rtype: str
        """
        if node.symbol == symbol:
            return ''
        if node.left and symbol in node.left.symbol:
            return '0' + self._huffman_traverse_helper(node.left, symbol)
        if node.right and symbol in node.right.symbol:
            return '1' + self._huffman_traverse_helper(node.right, symbol)
        return ''

    def _huffman_traverse(self, node, text):
        """
        Traverse the Huffman tree to encode a given text.

        :param node: The root node of the Huffman tree.
        :type node: TreeNode
        :param text: The text to encode.
        :type text: str
        :return: The Huffman-encoded binary string of the text.
        :rtype: str
        """
        code = ''
        for symbol in text:
            code += self._huffman_traverse_helper(node, symbol) + ''
        return code

    def huffman_encoding(self, text):
        """
        Perform Huffman encoding on a given text.

        :param text: The text to encode.
        :type text: str
        :return: A tuple containing the Huffman-encoded string and the root of the Huffman tree.
        :rtype: tuple
        """
        leafs = [TreeNode(self.probabilities[i], symbol=self.symbols[i]) for i in range(self.size)]

        leafs.sort(key=lambda x: x.value, reverse=True)

        while len(leafs) > 1:
            left = leafs.pop()
            right = leafs.pop()
            node = TreeNode(left.value + right.value, symbol=left.symbol + right.symbol)
            node.left = left
            node.right = right
            leafs.append(node)
            leafs.sort(key=lambda x: x.value, reverse=True)

        root = leafs[0]

        return self._huffman_traverse(root, text), root

    @staticmethod
    def huffman_decoding(code, root):
        """
        Perform Huffman decoding on a given encoded string using the Huffman tree.

        :param code: The Huffman-encoded binary string.
        :type code: str
        :param root: The root of the Huffman tree.
        :type root: TreeNode
        :return: The decoded string (original text).
        :rtype: str
        """
        decoded = ''
        node = root

        for bit in code:
            node = node.left if bit == '0' else node.right
            if node.left is None and node.right is None:
                decoded += node.symbol
                node = root

        return decoded


if __name__ == '__main__':

    text = "LA BELLA LILLI BALLA"
    source = sourcefy(text)
    H = HuffmanCompressor(source)
    compressed, root = H.huffman_encoding(text)
    decoded = H.huffman_decoding(compressed, root)

    binary_text = ' '.join(format(ord(char), '08b') for char in text)

    assert decoded == text, "Ops!"
    print("Compression ratio:", len(compressed) / len(binary_text))