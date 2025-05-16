from node import Node


class LLStack:
    def __init__(self) -> None:
        """
        Constructor for the LLStack class.
        """

        self.__head = None
        self.__size = 0

    @property
    def size(self) -> int:
        """
        Property for the size attribute.

        :return:
            __size (int): The number of elements in the stack.
        """
        return self.__size

    def pop(self) -> tuple:
        """
        Removes the top node on the stack and returns the data (tuple) stored at that node.

        :return:
            data (tuple): The top node in the stack.
        :raises:
            IndexError if the stack is empty.
        """
        if self.__head is None:
            raise IndexError('Cannot pop from an empty stack.')

        data = self.__head.data
        self.__head = self.__head.next
        self.__size -= 1
        return data

    def push(self, data: tuple) -> None:
        """
        Adds a new node to the top of the stack.

        :param data:
            A tuple containing two positive integers.
        :raises:
            TypeError if data is not a tuple containing integers.
        :raises:
            ValueError if the tuple values are not positive integers, or if the tuple doesn't contain two values.
        """

        if not isinstance(data, tuple):
            raise TypeError
        if len(data) != 2 or not isinstance(data[0], int) or not isinstance(data[1], int) or data[0] < 0 or data[1] < 0:
            raise ValueError

        new_node = Node(data)
        new_node.next = self.__head
        self.__head = new_node
        self.__size += 1

    def __str__(self) -> str:
        """
        String override that returns the string representation of the stack, with the entry point node coming first,
        and each node pointing at the following one until the exit point node.

        :return:
            stack_str (str): The string representation of the LLStack.
        """

        stack_str = str(self.__head)
        if self.__head:
            node = self.__head.next
        for _ in range(self.__size - 1):
            stack_str = f'{str(node)} -> ' + stack_str  # Adds the new node to the start (top) of the stack.
            node = node.next

        return stack_str


