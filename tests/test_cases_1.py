import unittest
from os.path import exists
from os import remove
import managers.doc_manager as doc_manager
import managers.booking_system as booking_system
import managers.user_manager as user_manager
import managers.group_manager as group_manager
import db_config


def prepare_database():
    db_fname = "test_database.db"
    db_config.init_db(db_fname)
    db_config.drop_tables()
    db_config.create_tables()


class TestCases1(unittest.TestCase):
    def test_case_1(self):
        prepare_database()
        # Sample group
        group_1 = group_manager.Group.add(
            {
                "name":"Group",
                "book_ct":2,
                "book_bestseller_ct":1,
                "journal_ct":2,
                "av_ct":2
            }
        )
        # Sample user
        user_1 = user_manager.User.add(
            {
                "name":"User",
                "surname":"Userovich",
                "address":"Pushkin street, Kolotushkin building",
                "phone":88005553535,
                "group":group_1
            }
        )
        # Sample book
        book_1 = doc_manager.Book.add(
            {
                "title":"title",
                "author":"author",
                "cost":300,
                "keywords":"keywords",
                "edition":"edition",
                "publisher":"publisher",
                "year":2000
            }
        )
        # Book's copies
        b1_copy1 = doc_manager.Copy.add(book_1)
        b1_copy2 = doc_manager.Copy.add(book_1)

        # Checkout first copy to a user
        bsystem = booking_system.Booking_system()
        bsystem.check_out(user_1, b1_copy1, "Librarian")

        # Get copies and make sure there are only two of them
        b1_copies = book_1.get_document_copies()
        self.assertTrue(len(b1_copies) == 2)

        b1_copy1_after = b1_copies[0]
        b1_copy2_after = b1_copies[1]

        # Make sure that user's story contains only one entry
        user1_history = bsystem.get_user_history(user_1)
        self.assertTrue(len(user1_history) == 1)

        # Make sure that copy given to user and this is one of the existing copies
        uh = user1_history[0]
        self.assertTrue(uh.user.card_id == user_1.card_id)
        self.assertTrue((b1_copy1_after.CopyID == uh.copy.CopyID) or (b1_copy2_after.CopyID == uh.copy.CopyID))
        self.assertTrue((b1_copy1_after.CopyID != uh.copy.CopyID) or (b1_copy2_after.CopyID != uh.copy.CopyID))


if __name__ == '__main__':
    unittest.main()
