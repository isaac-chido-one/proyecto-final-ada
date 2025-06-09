from typing import Any, Callable
from vacancies.structures.hash_node import HashNode
from vacancies.structures.node import Node

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
