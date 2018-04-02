import unittest
import managers.doc_manager as doc_manager
import managers.booking_system as booking_system
import managers.user_manager as user_manager
import managers.group_manager as group_manager
import db_config
import datetime


class TestCases2(unittest.TestCase):
    def prepare_database(self):
        db_fname = "test_database.db"
        db_config.init_db(db_fname)
        db_config.drop_tables()
        db_config.create_tables()

    def test_case_1(self):
        self.prepare_database()


if __name__ == '__main__':
    unittest.main()
