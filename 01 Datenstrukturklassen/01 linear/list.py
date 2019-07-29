from typing import TypeVar, Generic, Optional

ContentType = TypeVar('ContentType')


class List(Generic[ContentType]):

    class ListNode():

        def __init__(self, p_content):
            self.__content = p_content
            self.__next = None

        def get_content(self):
            return self.__content

        def set_content(self, p_content):
            self.__content = p_content

        def get_next_node(self) -> 'List.ListNode':
            return self.__next

        def set_next_node(self, p_next: 'List.ListNode'):
            self.__next = p_next

    def __init__(self):
        self._first = None
        self._last = None
        self._current = None

    def is_empty(self):
        return self._first is None

    def has_access(self):
        return self._current is not None

    def next(self):
        if self.has_access():
            self._current = self._current.get_next_node()

    def to_first(self):
        if not self.is_empty():
            self._current = self._first

    def to_last(self):
        if not self.is_empty():
            self._current = self._last

    def get_content(self) -> Optional[ContentType]:
        if self.has_access():
            return self._current.get_content()
        else:
            return None

    def set_content(self, p_content: ContentType):
        if p_content is not None and self.has_access():
            self._current.set_content(p_content)

    def insert(self, p_content: ContentType):
        if p_content is not None:
            if self.has_access():
                new_node = List.ListNode(p_content)

                if self._current is not self._first:
                    previous = self.get_previous(self._current)
                    if previous is not None:
                        new_node.set_next_node(previous.get_next_node())
                        previous.set_next_node(new_node)
                else:
                    new_node.set_next_node(self._first)
                    self._first = new_node
            else:
                if self.is_empty():
                    new_node = List.ListNode(p_content)

                    self._first = new_node
                    self._last = new_node

    def append(self, p_content: ContentType):
        if p_content is not None:
            if self.is_empty():
                self.insert(p_content)
            else:
                new_node = List.ListNode(p_content)

                self._last.set_next_node(new_node)
                self._last = new_node

    def concat(self, p_list: 'List[ContentType]'):
        if p_list is not self and p_list is not None and not p_list.is_empty():
            if self.is_empty():
                self._first = p_list._first
                self._last = p_list._last
            else:
                self._last.set_next_node(p_list._first)
                self._last = p_list._last

            p_list._first = None
            p_list._last = None
            p_list._current = None

    def remove(self):
        if self.has_access() and not self.is_empty():
            if self._current is self._first:
                self._first = self._first.get_next_node()
            else:
                previous = self.get_previous(self._current)
                if self._current is self._last:
                    self._last = previous
                previous.set_next_node(self._current.get_next_node())

            temp = self._current.get_next_node()
            self._current.set_content(None)
            self._current.set_next_node(None)
            self._current = temp

            if self.is_empty():
                self._last = None

    def get_previous(self, p_node: 'List.ListNode') -> Optional['List.ListNode']:
        if p_node is not None and p_node is not self._first and not self.is_empty():
            temp = self._first
            while temp is not None and temp.next is not p_node:
                temp = temp.get_next_node()
            return temp
        else:
            return None
