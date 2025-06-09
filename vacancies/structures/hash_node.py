from typing import Any

class HashNode():
	'''
	Clase nodo hash

	Attributes:
		value (Any): La información guardada.
	'''

	def __init__(self, key, value: Any):
		self.__key = key
		self.__value = value

	@property
	def value(self) -> Any:
		''' La información guardada '''
		return self.__value

	def __eq__(self, other):
		return isinstance(other, HashNode) and self.__key == other.__key

	def __repr__(self):
		return repr(self.__value)
