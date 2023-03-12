"""
Libreria de procesamiento de texto. El objetivo de esta libreria es
convertir una función matemática válida a un objeto que pueda ser
pasado al metodo .plot() de matplotlib.

Stage 1: interpreta funciones matemáticas con operaciones aritméticas básicas
	Gramática:
	```
	Function -> Expression
	Expression -> Term Expression'
	Expression' -> + Term Expression'
				| - Term Expression'
				| <Empty>
	Term -> Factor Term'
	Term' -> * Factor Term'
		   | / Factor Term'
		   | <Empty>
	Factor -> ( Expression )
			| number
			| identifier
	```
"""

import typing
import sys

from enum import Enum
from typing import List

TokenType = Enum('TokenType',
	['EoF',
	'Identifier',
	'IdentifierX',
	'Number',
	'PlusSign',
	'MinusSign',
	'ProductSign',
	'DivisionSign',
	'LParen',
	'RParen',])

class Token:
	"""
	Clase Token. Debe contener como mínimo la información para representar textualmente
	al Token y su tipo.
	TODO: debe tener la información sobre la localización del Token en la
	string de donde fue extraído, para lograr mejores mensajes de error.
	"""
	def __init__(self, type: TokenType, _repr: str):
		self.type = type
		self.repr = _repr

	def __repr__(self):
		return f'Token<{self.type}, "{self.repr}">'
	
	def __str__(self):
		return f'Token<{self.type}, "{self.repr}">'

class Lexer:
	def __init__(self):
		self.src = None
		self.src_len = 0
		self.readoff = 0
		self.tokens = []

	def _reset(self, src: str):
		self.src = src
		self.src_len = len(self.src)
		self.readoff = 0
		self.tokens = []

	def _can_read(self) -> bool:
		return (self.readoff < self.src_len)
	
	def _cc(self) -> chr :
		assert(self._can_read())
		return self.src[self.readoff]

	def _advance(self, step=1):
		self.readoff = self.readoff + step
	
	def _read_number(self) -> str:
		start = self.readoff
		end = self.readoff
		while (self._can_read() and self._cc().isdigit()):
			self._advance()
			end = end + 1

		return self.src[start:end]
	
	def get_tokens(self, src: str) -> List[Token]:
		self._reset(src)

		single_char_tokens = {
			'+': (TokenType.PlusSign, '+'),
			'-': (TokenType.PlusSign, '-'),
			'*': (TokenType.PlusSign, '*'),
			'/': (TokenType.PlusSign, '/'),
			'(': (TokenType.PlusSign, '('),
			')': (TokenType.PlusSign, ')'),
			'x': (TokenType.IdentifierX, 'x'),
		}

		while (self._can_read()):
			c = self._cc()

			if c == ' ' or c == '\n' or c == '\t':
				self._advance()
			elif c in single_char_tokens:
				self.tokens.append(Token(
					single_char_tokens[c][0],
					single_char_tokens[c][1],))
				self._advance()
			elif c.isdigit():
				num = self._read_number()
				self.tokens.append(Token(TokenType.Number, num))
			else:
				print("Invalid token", file=sys.stderror)

		return self.tokens

class TextProcessor:
    # def __init__(src: str):
    #     self.src = src

	def text_to_npobject(src: str):
		pass

# TextProcessor.text_to_npobject("x + 1")
# k = Lexer()
# x = k.get_tokens("4 + 1 * (3 + 2)")
# print(x)