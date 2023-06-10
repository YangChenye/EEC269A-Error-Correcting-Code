# Copyright (c) 2023 Pranav Kharche, Chenye Yang
# Toolbox for polynomials and CRC

import numpy as np
import logging

# Create a logger in this module
logger = logging.getLogger(__name__)


# find the order of a polynomial in integer form
def order(p):
	p = p >> 1
	order = 0
	while p:
		p = p >> 1
		order += 1
	return order

# find the hamming weight of a polynomial in integer form
def weight(p):
	weight = 0
	while p:
		if p & 1:
			weight += 1
		p = p >> 1
	return weight

# reverse the order of the bits of the polynomial
# this is used becase some tasks work better with the highest order coeffecient as the least significant bit 
# if no order is specified, it is found using order(p) from above
# returns the reversed polynomial
def bitRev(p, pOrder = None):
	if p == 0:
		return 0
	if pOrder == None:
		pOrder = order(p)

	retVal = 0
	for i in range(pOrder+1):
		retVal = (retVal << 1) + (p & 1)
		p = p >>1
	return retVal

# divide two polynomials
# each polynomial must be with the lowest order coeff as the LSB and the highest order as the MSB
# if order is not provided it is found automatically
# returns a tuple of the result and remainder of the division.
def polyDiv(dividend, divisor, dividendOrder = None, divisorOrder = None):
	if dividendOrder == None or divisorOrder == None:
		dividendOrder = order(dividend)
		divisorOrder = order(divisor)

	sizeDiff = dividendOrder - divisorOrder
	rem = dividend
	remOrder = dividendOrder
	result = 0
	for i in range(sizeDiff, -1, -1):
		if(rem >> remOrder):
			rem = rem ^ (divisor << i)
			result = result + (1 << i)
		remOrder -= 1
	
	# if rem:
	# 	print(f'{dividend:b}',' : ',  f'{divisor:b}', ' = ', f'{result:b}',' R', f'{rem:0{divisorOrder}b}', sep='')
	# else:
	# 	print(f'{dividend:b}',':',  f'{divisor:b}', '=', f'{result:b}')
	return result, rem

# find a generator polynomial that can create a cyclic code
# this uses the mathematical rules of a cyclic code and brute force searches for a compatible polynomial
# returns None if polynomial cannot be found.
# n, k: code length and information length of the code
# findN: find the nth solution. function normally stops upon finding the first solution that matches n and k. However, this is not always optimal.
# 		 Callers of this function may find that the 2nd or 3rd solution works better.
def findGen(n,k, initialGen = None):
	target = (1 << n) + 1
	if initialGen:
		gen = initialGen
	else:
		gen = (1 << (n-k)) + 1
	maxGen = (1 << (n-k+1))
	rem = 1
	while rem:
		gen += 2
		if gen >= maxGen:
			return None
		parity, rem = polyDiv(target, gen, n, n-k)
	logger.debug('generator = %s', f'{gen:b}')
	logger.debug('parity    = %s', f'{parity:b}')
	return gen

# build a generator matrix for a systematic cyclic code
# n, k: code length and information length of the code
# genPoly: the generator polynomial to be used
def buildGenMatrix(n, k, genPoly):
	genMatrix = [genPoly]
	# print(f'{genPoly:0{n}b}')
	for i in range(k-1):
		nextLine = genMatrix[i] << 1
		if (nextLine >> (n-k))%2:
			nextLine = nextLine ^ genPoly
		genMatrix.append(nextLine)
		# print(f'{nextLine:0{n}b}')
	logger.debug('Generator matrix')
	for i in range(k):
		genMatrix[i] = bitRev(genMatrix[i], n-1)
		logger.debug(f'{genMatrix[i]:0{n}b}')
	return genMatrix

# build the transpose of the parity matrix using the generator matrix
# n, k: code length and information length of the code
# genMatrix: the generator matrix to be used
def buildParityMatrix(n, k, genMatrix):
	Ht = []
	m = n-k
	logger.debug('Parity Matrix Transpose')
	for i in range(m-1, -1, -1):
		Ht.append(1 << i)
		logger.debug(f'{(Ht[-1]):0{m}b}')
	for row in genMatrix:
		Ht.append(row >> k)
		logger.debug(f'{(Ht[-1]):0{m}b}')
	return Ht


# create a generator matrix for a systematic cyclic code that matches the requirements provided by the input
# returns None if requirements are impossible to meet.
# n, k: code length and information length of the code
# nECC: number of correctable errors the code must have
# 		input of nECC = None means it will search for the best possible code.
def findMatrix(n,k, nECC = 1):
	numErrors = 0
	bestPoly = 0
	genPoly = 0
	bestGen = None
	maxErrors = 0
	while nECC == None or numErrors < nECC:
		genPoly = findGen(n,k,genPoly)
		if genPoly == None:
			genMatrix = None
			break
		genMatrix = buildGenMatrix(n, k, genPoly)
		numErrors = correctableErrors(n, k, genMatrix)
		if numErrors > maxErrors:
			bestGen = genMatrix 
			maxErrors = numErrors 
			bestPoly = genPoly
	if (nECC == None and bestGen == None) or (nECC and genMatrix == None):
		logger.debug('no viable matrix found')
		# print('no viable matrix found')
		return None
	logger.debug('used polynomial %d', bestPoly)
	logger.debug('%d correctable errors', maxErrors)	
	# print('used polynomial', bestPoly)
	# print(maxErrors,'correctable errors')	
	return bestGen

# encode a data word with the provided generator matrix
def encode(data, genMatrix):
	if order(data)+1 > len(genMatrix):
		return None
	result = 0
	data = bitRev(data, len(genMatrix)-1)
	for row in genMatrix:
		result = result ^ ((data & 1)*row)
		data = data >> 1
	return result

# Find the number of errors that a specific code can fix.
# This is based on the minimum distance between code words which
# is eq to the minimum weight of the non-zero codewords
def correctableErrors_old(n, k, genMatrix):
	weightTable = [0] * (n+1)
	minWeight = n
	for i in range(1, 1<<k, 1):
		wordWeight = weight(encode(i, genMatrix))
		if wordWeight < minWeight:
			minWeight = wordWeight
			# print(minWeight)
		weightTable[wordWeight] += 1
	# print(weightTable)
	return ((minWeight-1) // 2)


def nCr_Seq(n, r):
	if r > n:
		return []
	if r == 0:
		return [0]
	if n == r:
		return [((1<<n) - 1)]

	seq = []
	for inc in nCr_Seq(n-1, r-1):
		seq.append((inc<<1) + 1)
	for exc in nCr_Seq(n-1, r):
		seq.append(exc<<1)
	return seq

def correctableErrors(n, k, genMatrix):
	minWeight = n
	for minPossible in range(1, n-k+1, 1):
		if minWeight <= minPossible:
			break
		# print(k, 'choose', minPossible)
		for word in nCr_Seq(k, minPossible):
			if minWeight <= minPossible:
				break
			wordWeight = weight(encode(word, genMatrix))
			if wordWeight < minWeight:
				minWeight = wordWeight
				# print(minWeight, word)
	return (minWeight-1) // 2

def genMatrixDecmial2Ndarray(genMatrix_decimal, n):
	"""
	Convert the generator matrix in decimal form to numpy array form
	
		@type  genMatrix_decimal: list
		@param genMatrix_decimal: generator matrix in decimal form

		@type  n: int
		@param n: number of bits in a codeword
		
		@rtype:   ndarray
		@return:  generator matrix in numpy array form
	"""
	# Convert the generator matrix in decimal form to binary form
	genMatrix_binary = [[int(bit) for bit in f'{num:0{n}b}'] for num in genMatrix_decimal]

	# Convert the binary generator matrix to a numpy array
	G = np.array(genMatrix_binary, dtype=np.uint8)

	return G