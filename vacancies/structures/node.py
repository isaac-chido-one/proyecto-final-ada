from typing import Any, Callable

class Node():
	'''
	Clase nodo para implementar las estructuras y guardar los datos manejados.

	Attributes:
		data (Any): La información guardada.
		link (Node): Enlace al siguente nodo.
	'''

	def __init__(self, data: Any, link):
		self.__data = data
		self.__link = link

	@property
	def data(self) -> Any:
		''' La información guardada '''
		return self.__data

	@data.setter
	def data(self, data: Any):
		''' La información guardada '''
		self.__data = data

	@property
	def link(self):
		'''
		Enlace al siguente nodo

		Returns
		-------
		Node
		'''
		return self.__link

	@link.setter
	def link(self, link):
		''' Enlace al siguente nodo '''
		self.__link = link

	@staticmethod
	def length(node) -> int:
		''' Contar el número de elementos. '''
		return 0 if node is None else 1 + Node.length(node.__link)

	@staticmethod
	def contains(node, element: Any) -> bool:
		''' Comprueba si la estructura contiene el elemento a buscar. '''
		return False if node is None else element == node.__data or Node.contains(node.__link, element)

	@staticmethod
	def print(node):
		''' Mostrar el contenido de la estructura. '''
		if node is not None:
			print(node.__data)
			Node.print(node.__link)

	@staticmethod
	def each(node, callback: Callable[[Any, Any], None], args: Any):
		''' Ejecuta una funcion en cada elemento de cada nodo. '''
		if node is not None:
			callback(node.__data, args)
			Node.each(node.__link, callback, args)

	@staticmethod
	def find(node, element: Any):
		''' Busca un elemento por comparación y regresa el elemento encontrado '''
		return None if node is None else (node.__data if element == node.__data else Node.find(node.__link, element))

	@staticmethod
	def remove(node, element: Any):
		''' Busca un elemento por comparación y lo quita de la lista. '''
		if node is None:
			return None

		if element == node.__data:
			return node.__link

		node.__link = Node.remove(node.__link, element)

		return node

	@staticmethod
	def bubleSort(node, field: str):
		''' Ordena la lista de menor a mayor con el algoritmo Bubble Sort. '''
		i = node
		while i is not None:
			j = node

			while i is not j:
				result = i.__data.compare(j.__data, field)

				if result < 0:
					pivot = i.__data
					i.__data = j.__data
					j.__data = pivot

				j = j.__link

			i = i.__link
