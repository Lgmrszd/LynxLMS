import unittest
import managers.doc_manager as doc_manager
import managers.booking_system as booking_system
import managers.user_manager as user_manager
import managers.group_manager as group_manager
import db_connect
import db_config

class tests(unittest.TestCase):

    def test_case_1(self):
        #db init values
        db_connect.custom_db('test1.db')
        db_config.drop_db()
        db_config.initialize_db()
        patron = group_manager.Group.create(name = 'patrons', book_ct = 3, book_bestseller_ct = 2, journal_ct = 2, av_ct = 2)
        user = user_manager.User.add(name = 'user_name', surname = 'user_surname', address = 'user_address', phone = 11111111111, group = patron)
        book = doc_manager.Book.create(title = 'Wonderful book', author = 'Nice Author', cost = 500, keywords = 'key', edition = 1, publisher = 'Good publisher', year = 2018)
        copy2 = doc_manager.Copy.add(book)
        copy1 = doc_manager.Copy.add(book)
        #test operations
        bs = booking_system.Booking_system()
        bs.check_out(user, copy1, 'mr. Librarian')
        #check values
        checked_out_copies = 0
        not_checked_out_copies = 0
        for entry in bs.get_document_copies(book):
            if (entry.checked_out):
                checked_out_copies += 1
            else:
                not_checked_out_copies += 1
        self.assertEqual(checked_out_copies, 1)
        self.assertEqual(not_checked_out_copies, 1)

if __name__ == '__main__':
    unittest.main()