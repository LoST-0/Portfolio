
from src.utils import *
from src.integer_encoding.codes import *

def testcase(encoders:list[IntegerEncoder], lower_bound=1, upper_bound=1000, step=1, is_random=False, distribution=None):
  
  if is_random:
     if distribution is None:
         raise ValueError(
              "A distribution must be provided if `isRandom` is True.")
     test = distribution
  else:
        test = list(range(lower_bound, upper_bound + 1, step))
        
  results = []
  for encoder in encoders:
    codex = encoder.encode(test)
    results.append(codex)
    
  return results,test


def main():
  test = [1,2,3,4,5,6,7]
  bEncoder = BinaryEncoder()
  bencodeed  = bEncoder.encode(test,optim=True)
  bdedecoded = bEncoder.decode(bencodeed)
  print(test,bencodeed,bdedecoded)
  
  uEncoder = UnaryEncoder()
  uencodeed = uEncoder.encode(test)
  udedecoded = uEncoder.decode(uencodeed)
  print(test, uencodeed, udedecoded)
  
  gEncoder = GammaEncoder()
  gencodeed = gEncoder.encode(test)
  gdedecoded = gEncoder.decode(gencodeed)
  print(test, gencodeed, gdedecoded)
  
  dEncoder = DeltaEncoder()
  dencodeed = dEncoder.encode(test)
  ddedecoded = dEncoder.decode(dencodeed)
  print(test, dencodeed, ddedecoded)
  
  fEncoder = FibonacciEncoder()
  fencodeed = fEncoder.encode(test)
  fdedecoded = fEncoder.decode(fencodeed)
  print(test, fencodeed, fdedecoded)
  
  rEncoder = RiceEncoder()
  rencodeed = rEncoder.encode(test)
  rdedecoded = rEncoder.decode(rencodeed)
  print(test, rencodeed, rdedecoded)
  
  
  print("N=1 up to 1000")
  Encoders = [bEncoder,gEncoder,dEncoder,fEncoder,rEncoder,RiceEncoder(k=7)]
  results,xrange = testcase(Encoders)
  plot_results(results,xrange,Encoders)
  results,xrange = testcase(Encoders,lower_bound=1,upper_bound=100_000,step=1_000)
  plot_results(results,xrange,Encoders)
  
  ##### Distributions ####
  distribution = get_distribution(distribution_type=0) # Uniform
  results,xrange = testcase(Encoders, is_random=True, distribution=distribution)
  plot_results(results, xrange, Encoders,
               title="Results of Different Encoders with uniform distribution")
  
  distribution = get_distribution(distribution_type=1) # 1/2x^2
  results,xrange = testcase(Encoders, is_random=True, distribution=distribution)
  plot_results(results, xrange, Encoders,
               title="Results of Different Encoders with distribution p(x)=1/2x^2")
  
  distribution = get_distribution(distribution_type=2) # 1/ 2x*(log x)^2
  results, xrange = testcase(Encoders, is_random=True, distribution=distribution)
  plot_results(results, xrange, Encoders,
               title="Results of Different Encoders with distribution p(x)=1/(2xlog^2(x))")
  
  
  
  
if __name__ == "__main__":
  main()