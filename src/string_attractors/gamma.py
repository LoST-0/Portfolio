
class StringAttractor:
  
  def __init__(self,positions=None):
    self.positions = positions
    pass
  
  def is_string_attractor_for(self,text:str) -> bool:
    positions = self.positions
    for k in range(0,len(positions)-2):
      i = positions[k]
      j = positions[k+1]
      wij = text[i:j]
      if any( (text[t] in wij and (t != i and t!=j )) for t in positions ):
        continue
      else:
        return False
    return True
  
  
def main():
  positions = [3,6,10,11]
  text = "CDABCCDABCCA"
  s = StringAttractor(positions=positions)
  print(s.is_string_attractor_for(text=text))
  text = "adcbaadcbadc"
  positions = [0,1,2,3]
  s.positions = positions
  print(s.is_string_attractor_for(text=text))
  return

if __name__ == "__main__":
  main()