# Jekyll solution

## TL;DR;
Jekyll gives you a hashing function and you're prompted to find a value that hashed with two different seeds gives you two different predefined values.
The round function behind the hash is reversible and the "digest" of the hash function is one of the 3 internal states of the round function.
Because the round function is invertible, it's possible to brute force the missing internal states that lead to the given hash value, revert those to the values that produced them and then run the hashing function forward again with the other seed, expecting to find the other hash value. 
Luckily, a positive result happens pretty fast (why? would be an interesting question to answer) and a solution is found in a few minutes of bruteforce (/exhaustive search of potential missing states).

## The longer version
Now that the solution is somewhat spoiled, the rest of this document is going to explain how I arrived to those conclusions.
This is meant to be a learning opportunity for the reader; more than how to solve it, I'm going to explain how I came to solve it, with the good an bad decisions.
So here we go!

## The mix function 

```python
def mix(a, b, c):
	a &= 0xFFFFFFFF; b &= 0xFFFFFFFF; c &= 0xFFFFFFFF;

	a -= b+c; a &= 0xFFFFFFFF; a ^= c >> 13
	b -= c+a; b &= 0xFFFFFFFF; b ^=(a <<  8)&0xFFFFFFFF
	c -= a+b; c &= 0xFFFFFFFF; c ^= b >> 13
	a -= b+c; a &= 0xFFFFFFFF; a ^= c >> 12
	b -= c+a; b &= 0xFFFFFFFF; b ^=(a << 16)&0xFFFFFFFF
	c -= a+b; c &= 0xFFFFFFFF; c ^= b >>  5
	a -= b+c; a &= 0xFFFFFFFF; a ^= c >>  3
	b -= c+a; b &= 0xFFFFFFFF; b ^=(a << 10)&0xFFFFFFFF
	c -= a+b; c &= 0xFFFFFFFF; c ^= b >> 15

	return a, b, c
```

And the initial state:

```python
  a = 0x9e3779b9
  b = a
  c = seed
```

Looking at the function with all the ands an bit shift, I blindly assumed the function was lossy (ie what we get out doesn't have as much information as the original input). 
Well, it turns out it is invertible (and therefore not lossy at all!)... I'm sure starting at the bits might reveal the hidden truth, but my approach to find it out was a little more pragmatic. 
Something that should be obvious and raise question is the seeding value `0x9e3779b9`. Why, how ? Well, it turns out it's the inverse (ish) of the golden ratio:

From stack overflow: http://stackoverflow.com/questions/4948780/magic-number-in-boosthash-combine
```
phi = (1 + sqrt(5)) / 2
2^32 / phi = 0x9e3779b9
```

The two best reasons for picking this number is, it's not an arbitrary choice, and, (I think) because it's not a rational number it may have better properties for hashing functions (justification for that lays in the hand of hashing experts....)

In any case, looking on google for this number leads to the source code of "lookup2.c" where the mix function was first defined (I think) and explanation of the engineering decisions behind it. 
It turns out jekyll is a modified version of the hashing function used in lookup2, which is the source code of a hash table using a non cryptographic hash function (it's probably good for us).
The authors states the mixing function is reversible, and the reverse is somewhat obvious.... 

## Solving the hash problem

My first approach to the problem, was "meh, looks like something Z3 can handle". Z3 is a SAT solver that helps people prove mathematical things, and usually give you a proper result to your question (assuming there's a solution). 
It turns out asking Z3 to find the solution to the question "what value gives those two hashes" is too complicated (ie it runs for 6h with no result). My rationalization is that the point of the mix function is to mix bits and a simple bit flip is expected to have cascading effect, so for Z3 there's a lot of equations to draw out of all those bits relationships. 
(See the solve.py script file for details about this approach)

My second approach, (after spending a while modelling the problem for Z3) was to ask Z3 to find the inverse of the mix function (because I'm lazzy and wanted to believe in the magic black box that is Z3).
It turns out that Z3 can confirm mix is invertible (well, it says "True" if you asked the question...) but getting an inverse function is not really something I could get from it.

So my third approach was reading more about this mix function. I couldn't find the theory behind it, but it seemed obvious to the author it's reversible. 
So out of desperation (and hopes) I just tried to run in backward (ie from the last instruction to the first). Addition/subtraction and xor are reversible operations, so let's have some faith.
It turns out that was the solution. Testing on some values showed that running mix "backward" was reversing it (I'm still not convinced there is no edge case to that, but well, ...)

## Breaking the hash

From there, we have a way to reverse the mix function, so what do we do next ? 
Assuming the the values are short (ie just the size of a hashing block), the mixing function is run once with its initial state, on the data and then run again (with 0 added to the various states).
If we assume we had exactly an input value that splits in 3 ints (4 bytes each) we're only running one round of the mix function on the actual data, and an extra mix round on the current state of the hash generator. Then the result of the jekyll function is the "c" state of the hash generator. 

The easiest approach to solve this problem (with the knowledge of the inverse of the mix function) is to take for granted the first desired hash as the "c" value of the generator, try all possible values for the "a" and "b" states from the generator, run the inverse mix function to deduce the values that where supposedly entered and compute the second hash using those (with an updated seed value), looking for a match with the second desired hash value.
Writing a c program to run the bruteforce seemed the fastest approach (see the bruteforce folder )

It turns out it's pretty easy to get a collision with the second desired values (takes 5 minutes of bruteforce). Then it's just a matter of setting a cookie accordingly and visit the ctf website.

## Conclusion

This was a humbling experience: instead of running blindly a SAT solver to find the solution for you, thinking a bit about the problem  was way more efficient. 
And as a security perspective, hash function meant for hash tables do not have the same security requirements as cryptographic hash functions (ie problems solved are really not the same), so using them indiscriminately should be avoided.
 



