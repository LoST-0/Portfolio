import math
from src.utils import TreeNode



class Source:
    def __init__(self, probabilities, *symbols):
        if not isinstance(probabilities, list):
            raise ValueError("Probabilities must be a non-empty list")
        if not symbols or len(symbols) != len(probabilities):
            self.symbols = [str(i) for i in range(len(probabilities))]
        else:
            self.symbols = symbols     
        if not all(isinstance(p, (int, float)) and 0 <= p <= 1 for p in probabilities):
            raise ValueError("All probabilities must be numbers between 0 and 1")
        if round(sum(probabilities),5) != 1:
            raise ValueError("Probabilities must sum to 1")
        self.probabilities = probabilities
        self.size=len(probabilities)
        #Several alternatives:  #dictionary of probabilities
        self.prob = {self.symbols[i]:self.probabilities[i] for i in range(len(probabilities))} 
        #or
        self.mappa= list(zip(self.symbols,self.probabilities))
        
    def entropy(self, d=2):
        import math
        entropy = 0
        for probability in self.probabilities:
            entropy -= probability * math.log(probability,d)
        return entropy
    
    def __str__(self):
        return self.mappa.__str__()
        
    def compute_average_code_length(self,code):
        if len(code) != self.size:
            raise ValueError("Code and probabilities must have the same length")
        average_length = 0
        for i in range(len(code)):
            average_length += len(code[i]) * self.probabilities[i]
        return average_length

    def efficiency(self,code, d=2):
        entropy = self.entropy(d)
        average_length = self.compute_average_code_length(code)
        return (entropy - average_length) / entropy

    def redudancy(self,code):
        return 1 - self.efficiency(code)
    
    def kraft_mcmillan(self,lengths, d=2):
        return sum([d**(-lengths[i]) for i in range(self.size)])<=1
    

    def create_prefix_code(self, lengths, d=2):
        if not self.kraft_mcmillan(lengths, d):
            print("Failed Kraft-McMillan inequality")
            return []
        else:
            code = []
            tree = [''] 

            level = 0
            max_level = max(lengths)
            length_key = {length: lengths.count(length) for length in set(lengths)}
            available = 1

            while level < max_level:
                next_level = []
                for node in tree:
                    for symbol in self.symbols:
                        if not any(node.startswith(codex) for codex in code):
                            next_level.append(node + symbol)
                tree = next_level

                needed = length_key.get(level + 1, 0)
                code.extend(tree[:needed])
                
                available = len(tree) - needed
                if available <= 0:
                    break  

                level += 1

            print("Generated prefix code:", code)
            return code

    def _find_index(self, leaf):
        
        total = sum(leaf)
        left = 0
        for i in range(len(leaf)):
            left += leaf[i]
            if left >= total/2:
                return i+1
                
    def shannon_fano(self):
       
        def split(leaf):
            if len(leaf) == 1:
                return [leaf]
            index = self._find_index(leaf)
            left = leaf[:index]
            right = leaf[index:]
            return [split(left) + split(right)]
        
        def assing_code(leaf, code):
           
            if isinstance(leaf[0], list):
                assing_code(leaf[0], code + '0')
                assing_code(leaf[1], code + '1')
            else:
                print(leaf, code)
        
        leaf = [int(p*100) for p in self.probabilities]
        
        leaf = split(leaf)
        
        assing_code(leaf[0], '')
        print("Generated Shannon-Fano code:")
          
            

    def shannon_encoding(self, d=2):
        find_li = lambda x: math.ceil(math.log(1/x,d))
        lengths = list(map(find_li,self.probabilities))
        return self.create_prefix_code(lengths,d)
    
    def _huffman_traverse_helper(self, node, symbol):
        if node.symbol == symbol:
            return ''
        if node.left and symbol in node.left.symbol:
            return '0' + self._huffman_traverse_helper(node.left, symbol)
        if node.right and symbol in node.right.symbol:
            return '1' + self._huffman_traverse_helper(node.right, symbol)
        return ''

    def _huffman_traverse(self, node, text):
        
        code = ''
        text.replace(" ", "")
        for symbol in text:
            code += self._huffman_traverse_helper(node, symbol) + ' '
            
        return code
    
    
    def huffman_encoding(self,text):
    
       leafs = [TreeNode(self.probabilities[i],symbol=self.symbols[i]) for i in range(self.size)]
      
       leafs.sort(key=lambda x: x.value,reverse=True)
       
       while len(leafs) > 1:
              left = leafs.pop()
              right = leafs.pop()
              node = TreeNode(left.value + right.value,symbol=left.symbol+right.symbol)
              node.left = left
              node.right = right
              leafs.append(node)
              leafs.sort(key=lambda x: x.value,reverse=True)
              
       root = leafs[0]
       
       return self._huffman_traverse(root,text), root
       
    def huffman_decoding(self, code, root):
        decoded = ''
        node = root

        for bit in code:
            node = node.left if bit == '0' else node.right
            if node.left is None and node.right is None:
                decoded += node.symbol
                node = root  

        return decoded
    

def sourcefy(text: str) -> Source:
    text = text.replace(" ", "")
    mapping = {
        text[i]: text.count(text[i])/len(text) for i in range(len(text))
    }
    return Source(list(mapping.values()), *mapping.keys())
    


def main():
    # Example usage:
    try:
        source1 = Source([0.4, 0.3, 0.2, 0.1], "a", "b", "c", "d")
        print("Source 1: ",source1, "Entropy: ",round(source1.entropy(),2))
        code1=["00","01","10","11"]
        print("Code 1:",code1," Average code length: ",round(source1.compute_average_code_length(code1),2))
        source2=Source([0.25,0.25,0.25,0.25])
        print("Source 2: ",source2)
        print(source2.kraft_mcmillan([1,2,3,3]))
        source2.create_prefix_code([2,2,2,2,3,3,3],d=4)
        source2.shannon_encoding()
        source2.shannon_fano()
        
        ##### 
        test = "ciao a tutti quanti?"
        source3 = sourcefy(test)
        test = test.replace(" ", "")
        print("Pre compression:", ''.join(format(ord(char), '08b') for char in test))
        compressed, root = source3.huffman_encoding(test)
        compressed = compressed.replace(" ", "")    
        print("Post compression:", compressed)
        print("Compression factor:", round(len(test)/len(compressed),2))
        print("Compression ratio:", round((len(compressed)/len(test)), 2))
        decompressed =  source3.huffman_decoding(compressed, root)
        print("Decompressed: ",decompressed)
        
        
    except ValueError as e:
        print("Error:", e)


if __name__ == '__main__':
    main()

