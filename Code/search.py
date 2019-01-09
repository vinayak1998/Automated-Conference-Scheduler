from random import randint
import sys
import time

start_time=time.time()
input_file=sys.argv[1]
output_file=sys.argv[2]

f = open(input_file)

program_time=float(f.readline())*60
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
def swappy(arr):
  new_arr=arr[:]
  a = randint(0,tnp-1)
  b = randint(0,tnp-1)
  if b!=a:
    new_arr[a],new_arr[b] = new_arr[b],new_arr[a]
  if b!=tnp-1:
    new_arr[a], new_arr[b+1] = new_arr[b+1], new_arr[a]
  else:
    new_arr[a], new_arr[b - 1] = new_arr[b - 1], new_arr[a]
  return new_arr

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
    arr_new = swappy(arr)
    count+=1
    c+=1
    goodness_new=goodness(arr_new)
    if goodness_new>goodness_arr:
      arr=arr_new
      goodness_arr = goodness_new
      count=0
    if time.time()-start_time>=program_time*0.9:
      break
  return arr




final_arr=local_search(arr)
file=open(output_file,'w')
for i in range(t):
  for j in range(p):
    for x in range(k):
      file.write(str(final_arr[x+j*k+p*k*i]))
      file.write(" ")
    if j!=p-1:
      file.write("|")
      file.write(" ")
  file.write("\n")





# print(goodness(arr))
# print(final_arr)
# print(goodness(final_arr))
#
# time_taken=time.time()-start_time
# print(time_taken)