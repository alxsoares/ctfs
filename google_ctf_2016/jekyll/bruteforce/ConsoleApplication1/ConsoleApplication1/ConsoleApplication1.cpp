// ConsoleApplication1.cpp : Defines the entry point for the console application.
//

#include "stdafx.h"
#include <stdlib.h>
#include <iostream> 
#include <iomanip>


typedef unsigned int u32;

void unmix(u32 a, u32 b, u32 c, u32 &x, u32 &y, u32 &z)
{
	
	a &= 0xFFFFFFFF; b &= 0xFFFFFFFF; c &= 0xFFFFFFFF;

	c ^= b >> 15;
	c += a + b; c &= 0xFFFFFFFF;
	b ^= (a << 10) & 0xFFFFFFFF;
	b += c + a; b &= 0xFFFFFFFF;
	a ^= c >> 3;
	a += b + c; a &= 0xFFFFFFFF;
	c ^= b >> 5;
	c += a + b; c &= 0xFFFFFFFF;
	b ^= (a << 16) & 0xFFFFFFFF;
	b += c + a; b &= 0xFFFFFFFF;
	a ^= c >> 12;
	a += b + c; a &= 0xFFFFFFFF;
	c ^= b >> 13;
	c += a + b; c &= 0xFFFFFFFF;
	b ^= (a << 8) & 0xFFFFFFFF;
	b += c + a; b &= 0xFFFFFFFF;
	a ^= c >> 13;
	a += b + c; a &= 0xFFFFFFFF;

	x = a;
	y = b;
	z = c;

}

void mix(u32 a, u32 b, u32 c, u32 &x, u32 &y, u32 &z)
{


	a &= 0xFFFFFFFF; b &= 0xFFFFFFFF; c &= 0xFFFFFFFF;

	a -= b + c; a &= 0xFFFFFFFF;

	a ^= c >> 13;
	b -= c + a; b &= 0xFFFFFFFF;
	b ^= (a << 8) & 0xFFFFFFFF;
		
	c -= a + b; c &= 0xFFFFFFFF; c ^= b >> 13;
	a -= b + c; a &= 0xFFFFFFFF; a ^= c >> 12;
	b -= c + a; b &= 0xFFFFFFFF; b ^= (a << 16) & 0xFFFFFFFF;
	c -= a + b; c &= 0xFFFFFFFF; c ^= b >> 5;
	a -= b + c; a &= 0xFFFFFFFF; a ^= c >> 3;
	b -= c + a; b &= 0xFFFFFFFF; b ^= (a << 10) & 0xFFFFFFFF;
	c -= a + b; c &= 0xFFFFFFFF; c ^= b >> 15;

	x = a;
	y = b;
	z = c;

}

using namespace std;

u32 jekyll(u32 seed, u32 v1, u32 v2, u32 v3)
{
	u32 	a = 0x9e3779b9;
	u32 	b = a;
	u32 	c = seed;
	u32 	length = 12;

	c += length;

	a += v1;
	b += v2;
	c += v3;

	u32 dummy1, dummy2, res;
	mix(a, b, c, dummy1, dummy2, res);
	return res;

}


int _tmain(int argc, _TCHAR* argv[])
{
	u32 a, b, c;
	u32 dummy1, dummy2, res;
	//http://burtleburtle.net/bob/c/lookup2.c


		cout << hex << jekyll(0x60061e, 1077336674, 3127917015, 1973153610) << endl;
	cout << hex << jekyll(0x900913, 1077336674, 3127917015, 1973153610) << endl;
	

	int keyLen = 12;
	std::cout << sizeof(long long) << std::endl;


		for (unsigned long j = 0; j < 0xFFFFFFFF; j++)
		{
			for (unsigned  long i = 0; i < 0xFFFFFFFF; i++)
			{
				unmix(i, j, 0xcb122e29, a, b, c);
				unmix(a, b, c - keyLen, a, b, c);
				mix(a, b, c + 0x900913 - 0x60061e, dummy1, dummy2, res);
				mix(dummy1, dummy2, res + keyLen, dummy1, dummy2, res);
				
				if (res == 0x203b1b70)
				{
					cout << "a: " << a << endl;
					cout << "b: " << b << endl;
					cout << "c: " <<c << endl;
					cout << "  " << endl;

					u32 v1 = a - 0x9e3779b9;
					u32 v2 = b - 0x9e3779b9;
					u32 v3 = c - 0x60061e; //assuming it's supposed to be 12 length

					cout << "v1=0x" << hex << v1 << endl;
					cout << "v2=0x" << hex << v2 << endl;
					cout << "v3=0x" << hex << v3 << endl;
					cout << "  " << endl;

					cout << "SUCCESS" << endl;
					system("pause");




				}
			}
			if (j % 0xFF) std::cout << j << " ";
		
		
	}
	std::cout << "done" << std::endl;
}

