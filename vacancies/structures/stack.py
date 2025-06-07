from vacancies.structures.node import Node

class Stack():
	''' Clase pila '''

	def __init__(self):
		self.Inicializar()

	def Apilar(self, elemento):
		''' Insertar un elemento. '''
		self.node = Node(elemento, self.node)
		return True

	def Cima(self):
		''' Mostrar el siguiente elemento que se sacaría (sin sacarlo). '''
		return None if self.Vacia() else self.node.data

	def Contiene(self, elemento):
		'''
		Comprobar si un elemento está en la estructura.

		Returns
		-------
		bool
		'''
		return Node.contains(self.node, elemento)

	def Desapilar(self):
		''' Sacar un elemento. '''
		if self.Vacia():
			return None
		elemento = self.node.data
		self.node = self.node.link
		return elemento

	def Inicializar(self):
		self.node = None

	def Limpiar(self):
		self.Inicializar()

	def Mostrar(self):
		''' Mostrar el contenido de la estructura. '''
		Node.print(self.node)

	def Primero(self):
		node = Node.first(self.node)
		return None if node is None else node.data

	def Tamano(self):
		'''
		Contar el número de elementos.

		Returns
		-------
		int
		'''
		return Node.length(self.node)

	def Vacia(self):
		'''
		Returns
		-------
		bool
		'''
		return self.node is None

	def each(self, callback, args):
		''' Ejecuta una funcion en cada elemento de cada nodo. '''
		Node.each(self.node, callback, args)

	def find(self, element):
		''' Busca un elemento por comparación y regresa el elemento encontrado '''
		return Node.find(self.node, element)

	def remove(self, element):
		self.node = Node.remove(self.node, element)
