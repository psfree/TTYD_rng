#Author: Calypso
#Python implementation of paper mario RNG
#All credit to trivial171 for the original algorithm

import math

#Linear Congruential Generator constants for TTYD
# X[n+1] = (a*X[n] +b) % m

a=0x41c64e6d
b=0x3039

#32 bit maximum/ modulus
m = 1<<32


powers = []
for i in range(0,31):
    powers += [1<<i]

#recurrence relation for newtons method, see below
def recur(x,y):
    return int(y*(2-y*x))%m

#find the  multiplicative inverse (modulo m), using Newtons method
#Many thanks to Brian Kessler for improving the initial guess to 5 bits
#This provably converges to the inverse in only 3 recurrences.
def inv(x):
    y= (3*x)^2
    y=int(recur(x,y))
    y=int(recur(x,y))
    y=int(recur(x,y))
    return y

#This implements a calculation that finds the state of the LCG for a given index
def rngAtIndex(i):
    return (b* math.floor((pow(a,i,4*m)-1)/4))* inv((a-1)//4) %m

#returns the largest power of 2 that divides the input integer
def v2(n):
    if n==0:
        return 1000000
    i=n
    v=0
    while i%2 ==0:
        i = i>>1
        v+=1
    return v


def rngInverse(r):
    inv2 = 0x55d4be09
    xpow = (r*4*math.floor((a-1)/4) * inv2 +1) % (4*m)
    xguess = 0
    for p in powers:
        if v2(pow(a,xguess+p, 4*m)-xpow) > v2(pow(a,xguess, 4*m)-xpow):
            xguess+=p
    return xguess
    

i=0
while i < m:
    assert(rngInverse(rngAtIndex(i))==i)
    i+=1
    if(i % 100000==0):
        print("All good up to " + str(i))
assert(rngInverse(rngAtIndex(956))==956)
print(rngAtIndex(2))
print(rngAtIndex(3))

print(rngInverse(rngAtIndex(3)))
