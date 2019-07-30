import unittest
from database_connector import DatabaseConnector


class TestDatabaseConnector(unittest.TestCase):
    def test(self):
        database = DatabaseConnector(
            "localhost", "3306", "d_test", "u_test", "p_test")
        database.execute_statement("DROP TABLE test;")
        database.execute_statement("CREATE TABLE test (c1 Int, c2 Text);")
        database.execute_statement("INSERT INTO test VALUES (1, 'hallo');")
        database.execute_statement("SELECT * FROM test;")

        column_names = ["c1", "c2"]
        column_type = [int, str]
        data = [(1, 'hallo')]
        result = database.get_current_query_result()
        self.assertEqual(result.get_column_names(), column_names)
        self.assertEqual(result.get_column_types(), column_type)
        self.assertSequenceEqual(result.get_data()[0], data[0])

        self.assertIsNone(database.get_error_message())


if __name__ == '__main__':
    unittest.main()
