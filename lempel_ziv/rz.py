

def set_Tk(k,i):
  i = max(1,i)
  Tk = []
  for j in range(1,i):
    Tk.append("a"+"b"**(j**k))  
  return Tk

'''
Given an integer k>5, the set of the word 𝑤𝑘defined as (Π𝑖=2
𝑘−1𝑠𝑖𝑒𝑖)𝑞𝑘, where 𝑠𝑖
= 𝑎𝑏𝑖𝑎𝑎, 𝑒𝑖 = 𝑎𝑏𝑖𝑎𝑏𝑎𝑖−2 and 𝑞𝑘 = 𝑎𝑏𝑘𝑎
'''

def set_Wk(k=5):
  k = max(k,5)
  qk = "a"+"b"**k +"a"
  si = lambda x: "a"+"b"**(x)+"aa"
  ei = lambda x: "a"+"b"**(x)+"ab"+"a"**(x-2)
  Wk = []
  for i in range(2,k):
    Wk.append(si(i)+ei(i))
    
  Wk.append(qk)
  return Wk
    
  