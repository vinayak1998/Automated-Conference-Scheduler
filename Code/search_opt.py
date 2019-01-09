from random import randint
import sys
import time
import math

start_time=time.time()
input_file=sys.argv[1]
output_file=sys.argv[2]

f = open(input_file)

program_time=float(f.readline())
k=int(f.readline())
p=int(f.readline())
t=int(f.readline())
c=int(f.readline())
tnp=p*k*t # total number of paper

dim=k*p*t
dis=[]  #Distance array

sim=[]  #Similarity array

for i in range(dim):
  m=[]
  l=f.readline().strip().split(' ')
  for i in range(len(l)):
    l[i]=float(l[i])
    m+=[round(1.0-float(l[i]),2)]
  dis+=[l]
  sim+=[m]


#compute random neighbor with random swaps
def swappy(arr,score):
  new_arr=arr[:]
  a = randint(0,tnp-1)
  a=1
  b = randint(0,tnp-1)
  b=3
  if b!=a:
    new_arr[a],new_arr[b] = new_arr[b],new_arr[a]
  elif b!=tnp-1:
    new_arr[a], new_arr[b+1] = new_arr[b+1], new_arr[a]
  else:
    new_arr[a], new_arr[b - 1] = new_arr[b - 1], new_arr[a]
  block1 = int(math.floor(a / k))
  block2 = int(math.floor(b / k))
  if (block2==block1):return (new_arr,score)
  if (math.floor(a/(k*p))==math.floor(b/(k*p))):

    # print(block1)
    # print(block2)
    sim1=0
    sim2=0
    sim3=0
    sim4=0
    for i in range(block1*k,block1*k+k):
      if i != a:
        sim1+=sim[arr[a]][arr[i]]
        sim2+=sim[arr[b]][arr[i]]
    for i in range(block2*k,block2*k+k):
      if i!=b:
        sim4 += sim[arr[a]][arr[i]]
        sim3 += sim[arr[b]][arr[i]]

    print(sim1)
    print(sim2)
    print(sim3)
    print(sim4)
    return (new_arr,score-sim1+sim2-sim3+sim4)
  else:
    # print("1")
    block1 = int(math.floor(a / k))
    block2 = int(math.floor(b / k))
    part1=int(math.floor(a / (k*p)))
    part2 = int(math.floor(b / (k*p)))
    sim1 = 0
    sim2 = 0
    sim3 = 0
    sim4 = 0
    diff1 = 0
    diff2 = 0
    diff3 = 0
    diff4 = 0
    for i in range(block1 * k, block1 * k + k):
      sim1 += sim[arr[a]][arr[i]]
      if i!=a:
        sim2+=sim[arr[b]][arr[i]]
    for i in range(block2 * k, block2 * k + k):
      sim3 += sim[arr[b]][arr[i]]
      if i!=b:
        sim4 += sim[arr[a]][arr[i]]
    for i in range(part1*k*p,block1 * k):
      diff1 += dis[arr[a]][arr[i]]
      diff2 += dis[arr[b]][arr[i]]
    if ((block1+1)%p!=0):
      for i in range(block1 * k + k,(part1+1)*k*p):
        diff1 += dis[arr[a]][arr[i]]
        diff2 += dis[arr[b]][arr[i]]
    for i in range(part2*k*p,block2 * k):
      diff3 += dis[arr[b]][arr[i]]
      diff4 += dis[arr[a]][arr[i]]
    if ((block2+1) % p != 0):
      for i in range(block2 * k + k,(part2+1)*k*p):
        diff3 += dis[arr[b]][arr[i]]
        diff4 += dis[arr[a]][arr[i]]

    return (new_arr, score - sim1 + sim2 - sim3 + sim4+c*(-diff1+diff2-diff3+diff4))


#repeat swappy n times
def neighbor(arr , n):
  for i in range(0,n):
    swappy(arr)

# To compute the goodness of the confrence schedule
def goodness(arr):
  g=0
  for i in range(p*t):
    for j in range(k-1):
      for x in range(j+1,k):
        g+=sim[arr[j+k*i]][arr[x+k*i]]

  for a in range(t):
    for j in range(p):
      for i in range(a*p*k+k*j,a*p*k+k*(j+1)):
        for x in range(a*p*k+k*(j+1),(a+1)*p*k):
          g+=dis[arr[i]][arr[x]]

  return round(c*g,2)

arr=[]
for i in range(tnp):
  arr+=[i]

# start_time=time.time()
# # code to check time
# for i in range(2500):
#   arr2=swappy(arr)
#   goodness(arr2)
#
# time_taken=time.time()-start_time
# print(time_taken)


def local_search(arr):
  count=0
  c=0
  goodness_arr=goodness(arr)
  while(count<=tnp**2-tnp):
    arr_new,goodness_new = swappy(arr,goodness_arr)
    count+=1
    c+=1
    if goodness_new>goodness_arr:
      arr=arr_new
      goodness_arr = goodness_new
      count=0
    if c==7500:
      break
  return arr




# final_arr=local_search(arr)
# file=open(output_file,'w')
# for i in range(t):
#   for j in range(p):
#     for x in range(k):
#       file.write(str(final_arr[x+j*k+p*k*i]))
#       file.write(" ")
#     if j!=p-1:
#       file.write("|")
#       file.write(" ")
#   file.write("\n")

s=goodness(arr)
arr3,s1=swappy(arr,s)
# print(s1)
# print(arr3)
# print(goodness(arr3))
print(sim[1][0])
print(sim[3][0])
print(sim[3][2])
print(sim[2][1])


# print(goodness(arr))
# print(final_arr)
# print(goodness(final_arr))

time_taken=time.time()-start_time
# print(time_taken)