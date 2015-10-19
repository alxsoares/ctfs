#Utils for crypto stuff... from personal cryptopals
#proablay 80% is dumb or useless :)

import base64
import string
from Crypto.Cipher import AES

def hexToRaw(hexString):
	hexString = hexString.upper()
	return base64.b16decode(hexString)
	

def hexToB64(hexString):
	return base64.b64encode(hexToRaw(hexString))


def XOR(c1, c2):
	return chr(ord(c1) ^ ord(c2)) 

def fixedXORRaw(rawA, rawB):
	

	assert (len(rawA) == len(rawB))

	res = ""
	for i in range(0,len(rawA)):
			res = res + XOR(rawA[i],rawB[i])
	return res

def fixedXOR(hexA, hexB):
	rawA = hexToRaw(hexA)
	rawB = hexToRaw(hexB)

	assert (len(rawA) == len(rawB))

	res = ""
	for i in range(0,len(rawA)):
			res = res + XOR(rawA[i],rawB[i])
	return res


def singleByteXor(hexInput, c):
	res = ""
	raw = hexToRaw(hexInput)
	for c1 in raw: res = res + XOR(c1,c)
	return res

def singleByteXorRaw(raw, c):
	res = ""
	for c1 in raw: res = res + XOR(c1,c)
	return res



def isPrintableString(input_str):
	#from stack overflow http://stackoverflow.com/questions/3636928/test-if-a-python-string-is-printable (let a few things go though)
	return all(ord(c) < 127 and c in string.printable for c in input_str)

def freqSBXor(input, isHex=True):
	#Let's do the classic counting the E see if it gets us somewhere

	eCountMax = 0
	bestString = ""
	bestKey= 0
	for i in range(0,256):
		if (isHex): bla = singleByteXor(input,chr(i))
		else: 
			bla = singleByteXorRaw(input,chr(i))
			#print bla
		if not isPrintableString(bla): continue
		#print bla  #haha cheater
		eCount = 0
		for c in bla: 
			if ((c == 'e') | (c == 'E')): eCount = eCount + 1 #doesn't work
			if ((c == 'a') | (c == 'A')): eCount = eCount + 1 #doesn't work
			if ((c == ' ') | (c == ' ')): eCount = eCount + 1 #the three together work....  #i'm a total hack on this
		if (eCount > eCountMax):
			eCountMax = eCount
			bestString = bla
			bestKey = i
	return {'res':bestString, 'key':chr(bestKey), 'score':eCountMax}


def xorCipher(input_str, key_str):
	res = ""
	i_key = 0
	for c in input_str:
		res += XOR(c,key_str[i_key])
		i_key +=1
		if (i_key >= len(key_str)): i_key = 0
	return res


def guessXorKeySize(input_str):
	best_keysize = 0
	avg = 666.0 #float version of the demon number111111!!!
	for i in range(1,40): #get a shitty result for i =3 so let's skip the early ones....
		current_avg = 0.0
		j_max = 20
		for j in range(0,j_max): #average hamming distance on 2*j_max blocks ie (0,1) (2,3) ... (2*(j_max-1) -1, 2*(j_max -1))
			assert(2*j_max*i < len(input_str)) #lol I could do that better I guess.....
			current_avg += hammingDistance(input_str[2*j*i:(2*j+1)*i],input_str[(2*j+1)*i:2*(j+1)*i])
		
			#current_avg += hammingDistance(input_str[2*i:3*i],input_str[3*i:4*i]) 
			#current_avg += hammingDistance(input_str[4*i:5*i],input_str[5*i:6*i]) 
			#current_avg += hammingDistance(input_str[6*i:7*i],input_str[7*i:8*i]) 
		current_avg /= (float(j_max*i)) #i >0
		print current_avg
		if (current_avg < avg):
			avg = current_avg
			best_keysize = i
	return best_keysize


def getRandomnessScore(input_str):
	bin = [0]*256
	for c in input_str:
		bin[ord(c)] += 1
	res = 0
	for i in range(0,len(bin)): #we compute the L1-norm of distance from ideal average of (1/256,1/256,...)
		bin[i] = abs (float(bin[i])/float(len(input_str)) - 1/256.0)
		res += bin[i]
	return 1-res

def hammingDistance(input_str1, input_str2):
		assert(len(input_str1) == len(input_str2))
		res = 0
		for j in range(0,len(input_str1)):
			for i in range(0,8):
				if (( (ord(input_str1[j]) >> i) & 1) != ((ord(input_str2[j]) >> i) & 1)): res += 1
		return res