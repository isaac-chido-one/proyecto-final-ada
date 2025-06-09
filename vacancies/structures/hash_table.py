from typing import Any, Callable
from vacancies.sorting import mergesort
from vacancies.structures.hash_node import HashNode
from vacancies.structures.node import Node
from vacancies.utils import appendToArray

class HashTable():
	''' Clase tabla hash '''

	def __init__(self):
		self.__table = None

	def contains(self, key: int | str) -> bool:
		''' Comprueba si la estructura contiene la llave hash. '''
		hashNode = HashNode(key, None)

		return Node.contains(self.__table, hashNode)

	def get(self, key: int | str) -> Any:
		''' Obtener un elemento de la tabla a partir de su llave hash. '''
		hashNodeForFind = HashNode(key, None)
		hashNode = Node.find(self.__table, hashNodeForFind)

		return None if hashNode is None else hashNode.value # type: ignore

	def callCallback(self, hash_node: HashNode, args: Any):
		''' Ejecuta una funcion en el elemento de un nodo hash. '''
		self.callback(hash_node.value, args)

	def each(self, callback: Callable[[Any, Any], None], args: Any):
		''' Ejecuta una funcion por cada elemento la tabla hash. '''
		self.callback = callback
		Node.each(self.__table, self.callCallback, args)

	def print(self):
		''' Mostrar el contenido de la estructura. '''
		Node.print(self.__table)

	def set(self, key: int | str, value: Any):
		''' Agrega un elemento a la tabla hash. '''
		hashNode = HashNode(key, value)
		self.__table = Node(hashNode, self.__table)

	def unset(self, key: int | str):
		''' Quita un elemento de la tabla hash a partir de la llave. '''
		hashNode = HashNode(key, None)
		self.__table = Node.remove(self.__table, hashNode)

	def insertSort(self, field: str):
		'''
		Ordena el contenido de la tabla de menor a mayor por el atributo
		especificado con el algoritmo Merge Sort.
		'''
		array = []
		self.each(appendToArray, array)
		mergesort(array, field)
		self.__table = None

		for value in array:
			key = value.hash()
			self.set(key, value)
