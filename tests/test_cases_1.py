import unittest
import managers.doc_manager as doc_manager
import managers.booking_system as booking_system
import managers.user_manager as user_manager
import managers.group_manager as group_manager
import db_config
import datetime


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

    def test_case_2(self):
        prepare_database()
        # Sample group
        group1 = group_manager.Group.add(
            {
                "name": "Group",
                "book_ct": 2,
                "book_bestseller_ct": 1,
                "journal_ct": 2,
                "av_ct": 2
            }
        )
        # Sample user
        user1 = user_manager.User.add(
            {
                "name": "User",
                "surname": "Userovich",
                "address": "Pushkin street, Kolotushkin building",
                "phone": 88005553535,
                "group": group1
            }
        )
        # Sample books
        book1 = doc_manager.Book.add(
            {
                "title": "Book 1",
                "author": "Not interesting author",
                "cost": 300,
                "keywords": "keywords",
                "edition": "edition",
                "publisher": "publisher",
                "year": 2000
            }
        )
        book2 = doc_manager.Book.add(
            {
                "title": "Book 2",
                "author": "Another not interesting author",
                "cost": 300,
                "keywords": "keywords",
                "edition": "edition",
                "publisher": "publisher",
                "year": 2000
            }
        )

        # Find the book with author "Totally good author"
        books = doc_manager.Book.get_list(10, 1)[0]
        author = "Totally good author"
        books_by_author = []
        for book in books:
            if book.author == author:
                books_by_author.append(book)

        # There is no such group by this author
        self.assertTrue(len(books_by_author) == 0)

    def test_case_3(self):
        prepare_database()
        faculty = group_manager.Group.add(
            {
                "name": "Faculty",
                "book_ct": 4,
                "book_bestseller_ct": 4,
                "journal_ct": 2,
                "av_ct": 2
            }
        )
        students = group_manager.Group.add(
            {
                "name": "Students",
                "book_ct": 3,
                "book_bestseller_ct": 2,
                "journal_ct": 2,
                "av_ct": 2
            }
        )
        f = user_manager.User.add(
            {
                "name": "Faculty",
                "surname": "Member",
                "address": "Moscow, MSU",
                "phone": 84959391000,
                "group": faculty
            }
        )
        s = user_manager.User.add(
            {
                "name": "Faculty",
                "surname": "Member",
                "address": "Moscow, MSU, ",
                "phone": 88005553535,
                "group": students
            }
        )
        b = doc_manager.Book.add(
            {
                "title": "Book",
                "author": "author",
                "cost": 300,
                "keywords": "keywords",
                "edition": "edition",
                "publisher": "publisher",
                "year": 2000
            }
        )
        bc = doc_manager.Copy.add(b)

        bsystem = booking_system.Booking_system()
        bsystem.check_out(f, bc, "Librarian")
        fh = bsystem.get_user_history(f)
        self.assertTrue(len(fh) == 1)
        fh = fh[0]
        return_time = datetime.datetime.strptime(bsystem.get_max_return_time(fh), "%Y-%m-%d").date()
        self.assertTrue((return_time - datetime.date.today()).days >= 7*4)

    def test_case_4(self):
        prepare_database()
        faculty = group_manager.Group.add(
            {
                "name": "Faculty",
                "book_ct": 4,
                "book_bestseller_ct": 4,
                "journal_ct": 2,
                "av_ct": 2
            }
        )
        students = group_manager.Group.add(
            {
                "name": "Students",
                "book_ct": 3,
                "book_bestseller_ct": 2,
                "journal_ct": 2,
                "av_ct": 2
            }
        )
        f = user_manager.User.add(
            {
                "name": "Faculty",
                "surname": "Member",
                "address": "Moscow, MSU",
                "phone": 84959391000,
                "group": faculty
            }
        )
        s = user_manager.User.add(
            {
                "name": "Faculty",
                "surname": "Member",
                "address": "Moscow, MSU, ",
                "phone": 88005553535,
                "group": students
            }
        )
        b = doc_manager.Book.add(
            {
                "title": "Book",
                "author": "author",
                "cost": 300,
                "keywords": "keywords",
                "edition": "edition",
                "publisher": "publisher",
                "year": 2000
            }
        )
        bc = doc_manager.Copy.add(b)

        bsystem = booking_system.Booking_system()
        bsystem.check_out(f, bc, "Librarian")
        fh = bsystem.get_user_history(f)
        self.assertTrue(len(fh) == 1)
        fh = fh[0]
        return_time = datetime.datetime.strptime(bsystem.get_max_return_time(fh), "%Y-%m-%d").date()
        self.assertTrue((return_time - datetime.date.today()).days >= 7*2)

    


if __name__ == '__main__':
    unittest.main()
