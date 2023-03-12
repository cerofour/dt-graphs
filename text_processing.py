"""
Libreria de procesamiento de texto. El objetivo de esta libreria es
convertir una función matemática válida a un objeto que pueda ser
pasado al metodo .plot() de matplotlib.

Stage 1: interpreta funciones matemáticas con operaciones aritméticas básicas
	Gramática:
	```
	Function -> Expression
				| AssignOperation
	AssignOperation -> Identifier "=" Expression
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
	'EqualsSign',
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
		# String con la expresión matemática a analizar, y su longitud (len)
		self.src = None
		self.src_len = 0

		# Offset de lectura. Apunta al siguiente carcacter en self.src
		# que TODAVíA no se ha leído
		self.readoff = 0
		self.tokens = []

	def _reset(self, src: str):
		self.src = src
		self.src_len = len(self.src)
		self.readoff = 0
		self.tokens = []

	def _can_read(self, offset: int = 0) -> bool:
		return (self.readoff + offset < self.src_len)
	
	# "CC" para "current character", regresa el caracter actual que el
	# algoritmo está analizando
	def _cc(self) -> chr :
		assert(self._can_read())
		return self.src[self.readoff]

	# "cpast" para "Character past": Regresa el caracter "offset" posiciones
	# después de self.readoff sin modificar el readoff
	def _cpast(self, offset: int) -> chr:
		assert(self._can_read(offset))
		return self.src[self.readoff + offset]

	def _advance(self, step=1):
		self.readoff = self.readoff + step
	
	# TODO: Esto debe retornar un Token
	def _read_number(self) -> str:
		start = self.readoff
		end = self.readoff
		while (self._can_read() and self._cc().isdigit()):
			self._advance()
			end = end + 1

		return self.src[start:end]

	def _read_identifier(self) -> Token:
		start = self.readoff
		end = self.readoff

		while self._can_read() and (self._cc().isalnum() or self._cc() == '_'):
			self._advance()
			end = end + 1

		return Token(TokenType.Identifier, self.src[start:end])
	
	# TODO: El algoritmo tal vez es un poco ineficiente???
	def get_tokens(self, src: str) -> List[Token]:
		self._reset(src)

		single_char_tokens = {
			'+': (TokenType.PlusSign, '+'),
			'-': (TokenType.PlusSign, '-'),
			'*': (TokenType.PlusSign, '*'),
			'/': (TokenType.PlusSign, '/'),
			'(': (TokenType.PlusSign, '('),
			')': (TokenType.PlusSign, ')'),
			'=': (TokenType.EqualsSign, '='),
			# 'x': (TokenType.IdentifierX, 'x'),
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
			elif c.isalpha():
				# Lee el siguiente caracter para saber si estamos leyendo
				# una variable X o un identificador que empiece con X
				# TODO: Revisar si estas condiciones son completamente
				# eficientes y no hay ningun edge case.
				if c == 'x' and self._can_read(1):
					peekedchr = self._cpast(1)
					# El siguiente caracter no forma parte de un identificador, 
					# así que solo es una X
					if not peekedchr.isalnum() or peekedchr != '_':
						self.tokens.append(Token(TokenType.IdentifierX, 'x'))
						self._advance()

				else:
					t = self._read_identifier()
					self.tokens.append(t)

			else:
				print("Invalid token", file=sys.stderror)

		return self.tokens

"""
Parser LL(1). Crea un árbol de sintáxis que entienda la función ingresada por
el usuario. Luego este árbol se debe compilar a datos que pyplot.plot()
pueda recibir.
"""
class LL1Parser(object):
	pass

class TextProcessor:
    # def __init__(src: str):
    #     self.src = src

	def text_to_npobject(src: str):
		pass

# TextProcessor.text_to_npobject("x + 1")
# k = Lexer()
# x = k.get_tokens("204 * x + (3 - hola)")
# print(x)