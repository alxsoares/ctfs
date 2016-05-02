from z3 import *
#from jekyll import * #doesnt work with bitvec :()

import struct
import base64

def mix2(a, b, c):
    #a &= 0xFFFFFFFF; b &= 0xFFFFFFFF; c &= 0xFFFFFFFF;
    #a = swapbytes(a)
    #b = swapbytes(b)
    #c = swapbytes(c)
    a = ZeroExt(32,a)
    b = ZeroExt(32,b)
    c = ZeroExt(32,c)

    a &= 0xFFFFFFFF; b &= 0xFFFFFFFF; c &= 0xFFFFFFFF;

    a -= b+c; a &= 0xFFFFFFFF;

    a ^= c >> 13
    b -= c+a; b &= 0xFFFFFFFF;
    b ^=(a <<  8)&0xFFFFFFFF
    c -= a+b; c &= 0xFFFFFFFF; c ^= b >> 13
    a -= b+c; a &= 0xFFFFFFFF; a ^= c >> 12
    b -= c+a; b &= 0xFFFFFFFF; b ^=(a << 16)&0xFFFFFFFF
    c -= a+b; c &= 0xFFFFFFFF; c ^= b >>  5
    a -= b+c; a &= 0xFFFFFFFF; a ^= c >>  3
    b -= c+a; b &= 0xFFFFFFFF; b ^=(a << 10)&0xFFFFFFFF
    c -= a+b; c &= 0xFFFFFFFF; c ^= b >> 15
    #a = swapbytes(a)
    #b = swapbytes(b)
    #c = swapbytes(c)

    a = Extract(31,0,a)
    b = Extract(31,0,b)
    c = Extract(31,0,c)

    #print "mix {} {} {}".format(hex(simplify(a).as_long()),hex(simplify(b).as_long()),hex(simplify(c).as_long()))
    return a, b, c

def unmix(a, b, c):
    #a &= 0xFFFFFFFF; b &= 0xFFFFFFFF; c &= 0xFFFFFFFF;
    #a = swapbytes(a)
    #b = swapbytes(b)
    #c = swapbytes(c)
    a = ZeroExt(32,a)
    b = ZeroExt(32,b)
    c = ZeroExt(32,c)

    c ^= b >> 15
    c += a+b; c &= 0xFFFFFFFF;
    b ^=(a << 10)&0xFFFFFFFF
    b += c+a; b &= 0xFFFFFFFF;
    a ^= c >>  3
    a += b+c; a &= 0xFFFFFFFF;
    c ^= b >>  5
    c += a+b; c &= 0xFFFFFFFF;
    b ^=(a << 16)&0xFFFFFFFF
    b += c+a; b &= 0xFFFFFFFF;
    a ^= c >> 12
    a += b+c; a &= 0xFFFFFFFF;
    c ^= b >> 13
    c += a+b; c &= 0xFFFFFFFF;
    b ^=(a <<  8)&0xFFFFFFFF
    b += c+a; b &= 0xFFFFFFFF;
    a ^= c >> 13
    a += b+c; a &= 0xFFFFFFFF;

    a = Extract(31,0,a)
    b = Extract(31,0,b)
    c = Extract(31,0,c)

    #print "mix {} {} {}".format(hex(simplify(a).as_long()),hex(simplify(b).as_long()),hex(simplify(c).as_long()))
    return a, b, c

def swapbytes(n): #swap bytes function.
    a = Extract(31,24,n)
    b = Extract(23,16,n)
    c = Extract(15,8,n)
    d = Extract(7,0,n)
    return Concat((d,c,b,a))

def jekyll32(data, seed):
    def mix(a, b, c):
        #a &= 0xFFFFFFFF; b &= 0xFFFFFFFF; c &= 0xFFFFFFFF;
        #a = swapbytes(a)
        #b = swapbytes(b)
        #c = swapbytes(c)
        a = ZeroExt(32,a)
        b = ZeroExt(32,b)
        c = ZeroExt(32,c)

        a &= 0xFFFFFFFF; b &= 0xFFFFFFFF; c &= 0xFFFFFFFF;

        a -= b+c; a &= 0xFFFFFFFF;

        a ^= c >> 13
        b -= c+a; b &= 0xFFFFFFFF;
        b ^=(a <<  8)&0xFFFFFFFF
        c -= a+b; c &= 0xFFFFFFFF; c ^= b >> 13
        a -= b+c; a &= 0xFFFFFFFF; a ^= c >> 12
        b -= c+a; b &= 0xFFFFFFFF; b ^=(a << 16)&0xFFFFFFFF
        c -= a+b; c &= 0xFFFFFFFF; c ^= b >>  5
        a -= b+c; a &= 0xFFFFFFFF; a ^= c >>  3
        b -= c+a; b &= 0xFFFFFFFF; b ^=(a << 10)&0xFFFFFFFF
        c -= a+b; c &= 0xFFFFFFFF; c ^= b >> 15
        #a = swapbytes(a)
        #b = swapbytes(b)
        #c = swapbytes(c)

        a = Extract(31,0,a)
        b = Extract(31,0,b)
        c = Extract(31,0,c)

        #print "mix {} {} {}".format(hex(simplify(a).as_long()),hex(simplify(b).as_long()),hex(simplify(c).as_long()))
        return a, b, c

    a = BitVecVal(0x9e3779b9,32)
    b = a
    c = seed

    print data.size()
    print "hello"
    length =  data.size()

    keylen = length
    values = data


    while keylen >= 12*8:

        #values = struct.unpack('<3I', data[:12])
        values  = data
        a += Extract(4*8-1,0,data)
        b += Extract(8*8-1,4*8,data)
        c += Extract(12*8-1,8*8,data)

        print 'loop'
        #print hex(simplify(a).as_long()),hex(simplify(b).as_long()),hex(simplify(c).as_long())

        a, b, c = mix(a, b, c)
        keylen -= 12*8
        if (keylen is 0):
            data = None
            continue
        data = Extract(data.size()-1,12*8, data)


    c += BitVecVal(length/8,32)
    #print c


    print "bla"


    if (data is not None):
        print "Not none"
        data = Concat(data, BitVecVal(0x0, (32*3 -  data.size())) )
        #values = struct.unpack('<3I', data)

        a += Extract(4*8-1,0,data)
        b += Extract(8*8-1,4*8,data)
        c += Extract(12*8-1,8*8,data)

    a, b, c = mix(a, b, c)

    print "done"
    return c


def cheapJekyllSolver(seed1,seed2,c1,c2):

    length = 12

    values = list(BitVecs("v1 v2 v3",32))
    a1 = BitVec("a1",32)
    a2 = BitVec("a2",32)
    b1 = BitVec("b1",32)
    b2 = BitVec("b2",32)

    c1 = BitVecVal(c1,32)
    c2 = BitVecVal(c2,32)

    print "Computing unmix"
    x1,y1,z1 = unmix(a1,b1,c1)
    x2,y2,z2 = unmix(a2,b2,c2)

    x1 -= values[0]
    y1 -= values[1]
    z1 -= values[2]

    x2 -= values[0]
    y2 -= values[1]
    z2 -= values[2]

    z1 -= BitVecVal(length,32)
    z2 -= BitVecVal(length,32)


    print "Setting up constraints"
    s = Solver()
    s.add(x1 == 0x9e3779b9)
    s.add(x2 == 0x9e3779b9)
    s.add(y1 == 0x9e3779b9)
    s.add(y2 == 0x9e3779b9)

    s.add(z1 == seed1)
    s.add(z2 == seed2)

    print "Checking"
    print s.check()
    print s.model()





    return c

def jekyll(data):
    #return Concat( jekyll32(data, BitVecVal(0x900913,32)), jekyll32(data, BitVecVal(0x60061e,32)))
    return jekyll32(data, BitVecVal(0x900913,32))

cheapJekyllSolver(0x900913,0x60061e,0x203b1b70,0xcb122e29)
