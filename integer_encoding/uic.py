import matplotlib.pyplot as plt
import random
import math

from compressors import IntegerCompressor,BinaryCompressor,UnaryCompressor,GammaCompressor,DeltaCompressor,FibonacciCompressor,RiceCompressor

def testcase(compressors:list[IntegerCompressor],lower_bound=1,upper_bound=1000,step=1,isRandom=False,distribution=None):
  
  if isRandom:
     if distribution is None:
         raise ValueError(
              "A distribution must be provided if `isRandom` is True.")
     test = distribution
  else:
        test = list(range(lower_bound, upper_bound + 1, step))
        
  results = []
  for compressor in compressors:
    codex = compressor.compress(test)
    results.append(codex)
    
  return results,test


def get_custom_distribution(p,lower_bound=1,upper_bound=1000,step=1):
    probabilities = []
    
    distribution = []
    for j in range(lower_bound, upper_bound + 1, step):
        probabilities.append(p(j))
    
    total_probability = sum(probabilities)
    normalized_probabilities = [prob / total_probability for prob in probabilities]

    for _ in range(lower_bound, upper_bound + 1, step):
        distribution.append(
            random.choices(
                population=range(lower_bound, upper_bound + 1, step), 
                weights=normalized_probabilities, 
                k=1
            )[0]
        )
        
    return distribution

def get_distribution(type=1, lower_bound=1, upper_bound=1000, step=1):
  
  distribution = []
  if type == 0:
      distribution.extend([
        random.randint(lower_bound,upper_bound) 
        for _ in range(lower_bound,upper_bound+1,step)
      ])
      distribution.sort()
      return distribution
  elif type == 1:
    p = lambda x: 1/(2*x**2)
  elif type == 2:
    p = lambda x: 1/(2*x*(math.log(x))**2)
  
  distribution = get_custom_distribution(p,lower_bound=max(2,lower_bound),upper_bound=upper_bound,step=step)
  distribution.sort()
  return distribution
    

def plot_results(results: list[list[int]], test_range: list[int], compressors, title="Compression Results of Different Compressors"):
    num_compressors = len(results)
    plt.figure(figsize=(10, 6))
    for i in range(num_compressors):   
        compressed_lengths = [len(result) for result in results[i]]
        plt.plot(test_range, compressed_lengths, label=f'{compressors[i].__name__}')

    plt.xlabel('Original Data')
    plt.ylabel('Length of Compressed Data')
    plt.title(title)
    plt.tight_layout()
    plt.legend()
    plt.show()
    
    return
 
   
def main():
  test = [1,2,3,4,5,6,7]
  bcompressor = BinaryCompressor()
  bcompressed  = bcompressor.compress(test,optim=True)
  bdecompresed = bcompressor.decompress(bcompressed)
  print(test,bcompressed,bdecompresed)
  
  ucompressor = UnaryCompressor()
  ucompressed = ucompressor.compress(test)
  udecompresed = ucompressor.decompress(ucompressed)
  print(test, ucompressed, udecompresed)
  
  gcompressor = GammaCompressor()
  gcompressed = gcompressor.compress(test)
  gdecompresed = gcompressor.decompress(gcompressed)
  print(test, gcompressed, gdecompresed)
  
  dcompressor = DeltaCompressor()
  dcompressed = dcompressor.compress(test)
  ddecompresed = dcompressor.decompress(dcompressed)
  print(test, dcompressed, ddecompresed)
  
  fcompressor = FibonacciCompressor()
  fcompressed = fcompressor.compress(test)
  fdecompresed = fcompressor.decompress(fcompressed)
  print(test, fcompressed, fdecompresed)
  
  rcompressor = RiceCompressor()
  rcompressed = rcompressor.compress(test)
  rdecompresed = rcompressor.decompress(rcompressed)
  print(test, rcompressed, rdecompresed)
  
  
  print("N=1 up to 1000")
  compressors = [bcompressor,gcompressor,dcompressor,fcompressor,rcompressor,RiceCompressor(k=7)]
  results,xrange = testcase(compressors)
  plot_results(results,xrange,compressors)
  results,xrange = testcase(compressors,lower_bound=1,upper_bound=100_000,step=1_000)
  plot_results(results,xrange,compressors)
  
  ##### Distributions ####
  distribution = get_distribution(type=0)
  results,xrange = testcase(compressors,isRandom=True,distribution=distribution)
  plot_results(results, xrange, compressors,
               title="Compression Results of Different Compressors with uniform distribution")
  
  distribution = get_distribution(type=1)
  results,xrange = testcase(compressors,isRandom=True,distribution=distribution)
  plot_results(results, xrange, compressors,
               title="Compression Results of Different Compressors with distribution p(x)=1/2x^2")
  
  distribution = get_distribution(type=2)
  results, xrange = testcase(compressors, isRandom=True, distribution=distribution)
  plot_results(results, xrange, compressors,
               title="Compression Results of Different Compressors with distribution p(x)=1/(2xlog^2(x))")
  
  
  
  
if __name__ == "__main__":
  main()