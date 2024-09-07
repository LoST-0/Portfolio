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
    
    ## LAB
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

    def _find_index(self, leafs):
        total = sum(leaf.value for leaf in leafs)
        accum = 0
        for i, leaf in enumerate(leafs):
            accum += leaf.value
            if accum >= total / 2:
                return i + 1  # Split point for Shannon-Fano

    def shannon_fano(self):
        # Create the list of leaf nodes
        nodes = [TreeNode(value=prob, symbol=symbol) for symbol, prob in zip(self.symbols, self.probabilities)]
        nodes.sort(reverse=True, key=lambda x: x.value)

        def split(leafs):
            if len(leafs) == 1:
                return leafs[0]
            index = self._find_index(leafs)
            left = split(leafs[:index])
            right = split(leafs[index:])
            parent = TreeNode(value=sum(leaf.value for leaf in leafs))
            parent.left = left
            parent.right = right
            return parent

        def assign_codes(node, code, code_dict):
            if node.symbol is not None:
                code_dict[node.symbol] = code
            else:
                if node.left:
                    assign_codes(node.left, code + '0', code_dict)
                if node.right:
                    assign_codes(node.right, code + '1', code_dict)


        root = split(nodes)


        code_dict = {}
        assign_codes(root, '', code_dict)

        return code_dict


    def shannon_encoding(self, d=2):
        find_li = lambda x: math.ceil(math.log(1/x,d))
        lengths = list(map(find_li,self.probabilities))
        return self.create_prefix_code(lengths,d)
    

def sourcefy(text: str) -> Source:
    #text = text.replace(" ", "")
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
        ########
        source2=Source([0.25,0.25,0.25,0.25])
        print("Source 2: ",source2)
        code1 =  source2.create_prefix_code([2,2,3,3],d=4)
        print(f"Code 1:{code1}\nAverage code length:{round(source1.compute_average_code_length(code1),2)}")
        code1 = source2.shannon_encoding()
        print(f"Code 2 (with shannon encoding):{code1}\nAverage code length:{round(source2.compute_average_code_length(code1), 2)}")
        code1 = source2.shannon_fano()
        code1 = list(code1.values())
        print(
            f"Code 2 (with shannon-fano):{code1}\nAverage code length:{round(source2.compute_average_code_length(code1), 2)}")
        #####
        
    except ValueError as e:
        print("Error:", e)


if __name__ == '__main__':
    main()

