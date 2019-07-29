from typing import List


class QueryResult():

    def __init__(self, p_data: List[List[str]], p_column_names: List[str], p_column_types: List[str]):
        self.__data = p_data
        self.__column_names = p_column_names
        self.__column_types = p_column_types

    def get_data(self) -> List[List[str]]:
        return self.__data

    def get_column_names(self) -> List[str]:
        return self.__column_names

    def get_column_types(self) -> List[str]:
        return self.__column_types

    def get_row_count(self) -> int:
        if self.__data is not None:
            return len(self.__data)
        else:
            return 0

    def get_column_count(self) -> int:
        if self.__data is not None and len(self.__data) > 0 and self.__data[0] is not None:
            return len(self.__data[0])
        else:
            return 0

