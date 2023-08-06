from typing import Generic
from ..edge import TData, TNode
from ..frontier import Frontier
from typed_data_structures import Stack
from ..state import State


class IterativeDeepeningFrontier(Generic[TNode, TData], Frontier[TNode, TData]):
	"""A frontier for a graph search algorithm that performs DFS up to a limited depth, then if no path is found, increases the depth and starts again.

	Args:
		Generic (TNode): The type of the nodes of the graph.
		Generic (TData): The type of the data stored by the edges of the graph.
	"""

	def __init__(self, start: TNode, initial_depth: int = 1, depth_step: int = 1):
		"""Construct a frontier for an interative deepening search algorithm.

		Args:
			start (TNode): The node from which to start the search.
			initial_depth (int, optional): The initial depth limit for the search. Defaults to 1.
			depth_step (int, optional): The amount to increase the depth by each time. Defaults to 1.
		"""
		self.__stack = Stack[State[TNode, TData]]()
		self.__start_state = State[TNode, TData](start)
		self.__stack.push(self.__start_state)
		self.__depth = initial_depth
		self.__can_go_deeper = False
		self.__depth_step = depth_step

	def is_empty(self) -> bool:
		return self.__stack.is_empty() and not self.__can_go_deeper

	def insert(self, state: State[TNode, TData]):
		if len(state.path) <= self.__depth:
			self.__stack.push(state)
			self.__start_state = self.__start_state or state
		else:
			# ignore new state this time because this branch is too deep. But set indicator that there are branches that go deeper than the current depth.
			self.__can_go_deeper = True

	def extract(self):
		if self.__stack.is_empty():
			if self.__can_go_deeper:
				# start over with increased depth
				self.__depth += self.__depth_step
				self.__can_go_deeper = False
				return self.__start_state
			else:
				return None  # There is no path to the target
		return self.__stack.pop()

	def __len__(self) -> int:
		"""Get the number of states in the frontier.

		Returns:
			int: The number of states in the frontier.
		"""
		return len(self.__stack)