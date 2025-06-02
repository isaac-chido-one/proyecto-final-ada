
class Node():
	''' Clase nodo para implementar las estructuras y guardar los datos manejados. '''

	def __init__(self, data, link):
		self._data = data
		self._link = link

	@property
	def data(self):
		return self._data

	@data.setter
	def data(self, data):
		self._data = data

	@property
	def link(self):
		'''
		Returns
		-------
		Node
		'''
		return self._link

	@link.setter
	def link(self, link):
		self._link = link

	@staticmethod
	def length(node):
		'''
		Contar el número de elementos.

		Returns
		-------
		int
		'''
		return 0 if node is None else 1 + Node.length(node._link)

	@staticmethod
	def contains(node, elemento):
		'''
		Comprobar si un elemento está en la estructura.

		Returns
		-------
		bool
		'''
		return False if node is None else elemento == node._data or Node.contains(node._link, elemento)

	@staticmethod
	def print(node):
		''' Mostrar el contenido de la estructura. '''
		if node is not None:
			print(node._data)
			Node.print(node._link)

	@staticmethod
	def first(node):
		'''
		Returns
		-------
		Node
		'''
		return None if node is None else (node if node._link is None else Node.first(node._link))
