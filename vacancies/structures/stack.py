from typing import Any, Callable
from vacancies.sorting import insertsort
from vacancies.structures.node import Node
from vacancies.utils import appendToArray

class Stack():
	''' Clase pila '''

	def __init__(self):
		self.Inicializar()

	def Apilar(self, element: Any):
		''' Insertar un elemento. '''
		self.__node = Node(element, self.__node)
		return True

	def Inicializar(self):
		''' Establece el nodo cabecera como None. '''
		self.__node = None

	def Limpiar(self):
		''' Quita toda la información de la pila y la deja vacía. '''
		self.Inicializar()

	def Mostrar(self):
		''' Mostrar el contenido de la estructura. '''
		Node.print(self.__node)

	def Tamano(self) -> int:
		''' Contar el número de elementos. '''
		return Node.length(self.__node)

	def each(self, callback: Callable[[Any, Any], None], args: Any):
		''' Ejecuta una funcion en cada elemento de cada nodo. '''
		Node.each(self.__node, callback, args)

	def find(self, element: Any) -> Any:
		''' Busca un elemento por comparación y regresa el elemento encontrado. '''
		return Node.find(self.__node, element)

	def remove(self, element: Any):
		''' Busca un elemento por comparación y lo quita de la pila. '''
		self.__node = Node.remove(self.__node, element)

	def insertSort(self, field: str):
		''' Ordena la pila de menor a mayor con el algoritmo Insertion Sort. '''
		array = []
		Node.each(self.__node, appendToArray, array)
		insertsort(array, field)
		self.Limpiar()

		for element in array:
			self.Apilar(element)
