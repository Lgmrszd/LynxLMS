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
        # Sample book
        book1 = doc_manager.Book.add(
            {
                "title": "title",
                "author": "author",
                "cost": 300,
                "keywords": "keywords",
                "edition": "edition",
                "publisher": "publisher",
                "year": 2000
            }
        )
        # Book's copies
        b1_copy1 = doc_manager.Copy.add(book1)
        b1_copy2 = doc_manager.Copy.add(book1)

        # Checkout first copy to a user
        bsystem = booking_system.Booking_system()
        bsystem.check_out(user1, b1_copy1, "Librarian")

        # Get copies and make sure there are only two of them
        b1_copies = book1.get_document_copies()
        self.assertTrue(len(b1_copies) == 2)

        b1_copy1_after = b1_copies[0]
        b1_copy2_after = b1_copies[1]

        # Make sure that user's story contains only one entry
        user1_history = bsystem.get_user_history(user1)
        self.assertTrue(len(user1_history) == 1)

        # Make sure that copy given to user and this is one of the existing copies
        uh = user1_history[0]
        self.assertTrue(uh.user.card_id == user1.card_id)
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

    def test_case_5(self):
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
        # Sample users
        users = []
        users.append(user_manager.User.add(
            {
                "name": "User1",
                "surname": "Userovich",
                "address": "Pushkin street, Kolotushkin building",
                "phone": 88005553535,
                "group": group1
            }
        ))
        users.append(user_manager.User.add(
            {
                "name": "User2",
                "surname": "Userovich",
                "address": "Pushkin street, Kolotushkin building",
                "phone": 88005553535,
                "group": group1
            }
        ))
        users.append(user_manager.User.add(
            {
                "name": "User3",
                "surname": "Userovich",
                "address": "Pushkin street, Kolotushkin building",
                "phone": 88005553535,
                "group": group1
            }
        ))
        book = doc_manager.Book.add(
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

        doc_manager.Copy.add(book)
        doc_manager.Copy.add(book)
        b_copies = book.get_document_copies()
        bsystem = booking_system.Booking_system()
        for i, user in enumerate(users):
            b_not_checked_copies = [x for x in b_copies if not x.checked_out]
            print(b_not_checked_copies)
            if i != 2:
                # still have copies
                self.assertTrue(len(b_not_checked_copies) != 0)
                # checkout one of the copies to a user
                copy = b_not_checked_copies[0]
                bsystem.check_out(user, copy, "Librarian")
            else:
                # there is no free copies
                self.assertTrue(len(b_not_checked_copies) == 0)

    def test_case_6(self):
        prepare_database()
        # Sample group
        group = group_manager.Group.add(
            {
                "name": "Group",
                "book_ct": 2,
                "book_bestseller_ct": 1,
                "journal_ct": 2,
                "av_ct": 2
            }
        )
        # Sample user
        user = user_manager.User.add(
            {
                "name": "User1",
                "surname": "Userovich",
                "address": "Pushkin street, Kolotushkin building",
                "phone": 88005553535,
                "group": group
            }
        )
        book = doc_manager.Book.add(
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

        copy1 = doc_manager.Copy.add(book)
        copy2 = doc_manager.Copy.add(book)

        bsystem = booking_system.Booking_system()

        # Copy successfuly checked out
        res, history = bsystem.check_out(user, copy1, "Librarian")
        self.assertEqual(res, 0)

        # Cannot check out another copy
        res, history = bsystem.check_out(user, copy2, "Librarian")
        self.assertEqual(res, 6)

    def test_case_7(self):
        group1 = group_manager.Group.add(
            {
                "name": "Group",
                "book_ct": 2,
                "book_bestseller_ct": 1,
                "journal_ct": 2,
                "av_ct": 2
            }
        )
        # Sample users
        p1 = user_manager.User.add(
            {
                "name": "User1",
                "surname": "Userovich",
                "address": "Pushkin street, Kolotushkin building",
                "phone": 88005553535,
                "group": group1
            }
        )
        p2 = user_manager.User.add(
            {
                "name": "User2",
                "surname": "Userovich",
                "address": "Pushkin street, Kolotushkin building",
                "phone": 88005553535,
                "group": group1
            }
        )
        # Sample book
        b1 = doc_manager.Book.add(
            {
                "title": "title",
                "author": "author",
                "cost": 300,
                "keywords": "keywords",
                "edition": "edition",
                "publisher": "publisher",
                "year": 2000
            }
        )
        b1_copy1 = doc_manager.Copy.add(b1)
        b1_copy2 = doc_manager.Copy.add(b1)

        bsystem = booking_system.Booking_system()
        res1, history1 = bsystem.check_out(p1, b1_copy1, "Librarian")
        res2, history2 = bsystem.check_out(p2, b1_copy2, "Librarian")

        self.assertEqual(res1, 0)
        self.assertEqual(res2, 0)
        self.assertNotEqual(history1, None)
        self.assertNotEqual(history2, None)

    def test_case_8(self):
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
        bsystem.check_out(s, bc, "Librarian")
        fh = bsystem.get_user_history(s)
        self.assertTrue(len(fh) == 1)
        fh = fh[0]
        return_time = datetime.datetime.strptime(bsystem.get_max_return_time(fh), "%Y-%m-%d").date()
        print((return_time - datetime.date.today()).days)
        self.assertTrue((return_time - datetime.date.today()).days >= 7*3)

    def test_case_9(self):
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
                "keywords": "keywords, best seller",
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
        print((return_time - datetime.date.today()).days)
        self.assertTrue((return_time - datetime.date.today()).days >= 7*2)

    def test_case_10(self):
        prepare_database()
        # Sample group
        group = group_manager.Group.add(
            {
                "name": "Group",
                "book_ct": 2,
                "book_bestseller_ct": 1,
                "journal_ct": 2,
                "av_ct": 2
            }
        )
        # Sample user
        user = user_manager.User.add(
            {
                "name": "User1",
                "surname": "Userovich",
                "address": "Pushkin street, Kolotushkin building",
                "phone": 88005553535,
                "group": group
            }
        )
        a = doc_manager.Book.add(
            {
                "title": "BookA",
                "author": "author",
                "cost": 300,
                "keywords": "keywords",
                "edition": "edition",
                "publisher": "publisher",
                "year": 2000
            }
        )
        a_copy = doc_manager.Copy.add(a)
        b = doc_manager.Book.add(
            {
                "title": "BookB",
                "author": "author",
                "cost": 300,
                "keywords": "keywords, reference",
                "edition": "edition",
                "publisher": "publisher",
                "year": 2000
            }
        )
        b_copy = doc_manager.Copy.add(b)

        bsystem = booking_system.Booking_system()
        res1, history1 = bsystem.check_out(user, a_copy, "Librarian")
        res2, history2 = bsystem.check_out(user, b_copy, "Librarian")

        self.assertEqual(res1, 0)
        self.assertEqual(res2, 2)
        self.assertNotEqual(history1, None)
        self.assertEqual(history2, None)


if __name__ == '__main__':
    unittest.main()
