from typing import Any, Callable
from vacancies.sorting import mergesort
from vacancies.structures.hash_node import HashNode
from vacancies.structures.node import Node
from vacancies.utils import appendToArray

class HashTable():

	def __init__(self):
		self.__table = None

	def contains(self, key: int | str) -> bool:
		hashNode = HashNode(key, None)

		return Node.contains(self.__table, hashNode)

	def get(self, key: int | str) -> Any:
		hashNodeForFind = HashNode(key, None)
		hashNode = Node.find(self.__table, hashNodeForFind)

		return None if hashNode is None else hashNode.value # type: ignore

	def callCallback(self, hash_node: HashNode, args: Any):
		self.callback(hash_node.value, args)

	def each(self, callback: Callable[[Any, Any], None], args: Any):
		''' Ejecuta una funcion en cada elemento la tabla. '''
		self.callback = callback
		Node.each(self.__table, self.callCallback, args)

	def print(self):
		''' Mostrar el contenido de la estructura. '''
		Node.print(self.__table)

	def set(self, key: int | str, value: Any):
		hashNode = HashNode(key, value)
		self.__table = Node(hashNode, self.__table)

	def unset(self, key: int | str):
		hashNode = HashNode(key, None)
		self.__table = Node.remove(self.__table, hashNode)

	def insertSort(self, field: str):
		array = []
		self.each(appendToArray, array)
		mergesort(array, field)
		self.__table = None

		for value in array:
			key = value.hash()
			self.set(key, value)
