
from src.utils import *
from src.integer_encoding.compressors import IntegerCompressor,BinaryCompressor,UnaryCompressor,GammaCompressor,DeltaCompressor,FibonacciCompressor,RiceCompressor

def testcase(compressors:list[IntegerCompressor], lower_bound=1, upper_bound=1000, step=1, is_random=False, distribution=None):
  
  if is_random:
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
  distribution = get_distribution(distribution_type=0)
  results,xrange = testcase(compressors, is_random=True, distribution=distribution)
  plot_results(results, xrange, compressors,
               title="Compression Results of Different Compressors with uniform distribution")
  
  distribution = get_distribution(distribution_type=1)
  results,xrange = testcase(compressors, is_random=True, distribution=distribution)
  plot_results(results, xrange, compressors,
               title="Compression Results of Different Compressors with distribution p(x)=1/2x^2")
  
  distribution = get_distribution(distribution_type=2)
  results, xrange = testcase(compressors, is_random=True, distribution=distribution)
  plot_results(results, xrange, compressors,
               title="Compression Results of Different Compressors with distribution p(x)=1/(2xlog^2(x))")
  
  
  
  
if __name__ == "__main__":
  main()