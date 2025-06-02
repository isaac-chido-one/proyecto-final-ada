from node import Node

class Queue():
	''' Clase cola '''

	def __init__(self):
		self.Inicializar()

	def Cima(self):
		''' Mostrar el siguiente elemento que se sacaría (sin sacarlo). '''
		return None if self.Vacia() else self.header.data

	def Contiene(self, elemento):
		'''
		Comprobar si un elemento está en la estructura.

		Returns
		-------
		bool
		'''
		return Node.contains(self.header, elemento)

	def Desencolar(self):
		if self.Vacia():
			return None

		node = self.header
		self.header = self.header.link
		node.link = None

		if self.header is None:
			self.last = None

		return node.data

	def Encolar(self, elemento):
		node = Node(elemento, None)

		if self.Vacia():
			self.header = node
		else:
			self.last.link = node

		self.last = node

	def Inicializar(self):
		self.header = None
		self.last = None

	def Limpiar(self):
		self.Inicializar()

	def Mostrar(self):
		''' Mostrar el contenido de la estructura. '''
		Node.print(self.header)

	def Primero(self):
		node = Node.first(self.header)
		return None if node is None else node.data

	def Tamano(self):
		'''
		Contar el número de elementos.

		Returns
		-------
		int
		'''
		return Node.length(self.header)

	def Vacia(self):
		'''
		Returns
		-------
		bool
		'''
		return self.header is None and self.last is None
