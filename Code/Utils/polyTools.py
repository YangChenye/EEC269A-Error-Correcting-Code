# Copyright (c) 2023 Pranav Kharche, Chenye Yang
# Toolbox for polynomials and CRC

import numpy as np
import logging

# Create a logger in this module
logger = logging.getLogger(__name__)


def order(p):
	p = p >> 1
	order = 0
	while p:
		p = p >> 1
		order += 1
	return order

def bitRev(p, pOrder = None):
	if p == 0:
		return 0
	if pOrder == None:
		pOrder = order(p)

	retVal = 0
	for i in range(pOrder+1):
		retVal = (retVal << 1) + (p %2)
		p = p >>1
	return retVal

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

def findGen(n,k):
	target = (1 << n) + 1
	gen = (1 << (n-k)) + 3
	parity, rem = polyDiv(target, gen, n, n-k)
	while rem:
		gen += 2
		if gen >= target:
			return None, None
		parity, rem = polyDiv(target, gen, n, n-k)
	logger.debug('generator =', f'{gen:b}')
	logger.debug('parity    =', f'{parity:b}')
	return gen, parity

def buildMatrix(n, k, gen, parity):
	genMatrix = [gen]
	# print(f'{gen:0{n}b}')
	for i in range(k-1):
		nextLine = genMatrix[i] << 1
		if (nextLine >> (n-k))%2:
			nextLine = nextLine ^ gen
		genMatrix.append(nextLine)
		# print(f'{nextLine:0{n}b}')
	logger.debug('Generator matrix')
	for i in range(k):
		genMatrix[i] = bitRev(genMatrix[i], n-1)
		logger.debug(f'{genMatrix[i]:0{n}b}')
	return genMatrix

def findMatrix(n,k):
	gen, parity = findGen(n,k)
	if gen == None:
		return None
	return buildMatrix(n, k, gen, parity)

def encode(data, gen):
	if order(data)+1 > len(gen):
		return None
	result = 0
	data = bitRev(data, len(gen)-1)
	for row in gen:
		result = result ^ ((data & 1)*row)
		data = data >> 1
	return result


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