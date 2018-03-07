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

        self.g_f = group_manager.Group.add(
            {
                "name": "Faculty",
                "book_ct": 4,
                "book_bestseller_ct": 4,
                "journal_ct": 2,
                "av_ct": 2
            }
        )
        self.g_s = group_manager.Group.add(
            {
                "name": "Students",
                "book_ct": 3,
                "book_bestseller_ct": 2,
                "journal_ct": 2,
                "av_ct": 2
            }
        )

    def test_case_1(self):
        self.prepare_database()

        self.b1 = doc_manager.Book.add(
            {
                "title": "Introduction to Algorithms",
                "author": "Thomas H. Cormen, Charles E. Leiserson, Ronald L. Rivest and Clifford Stein",
                "cost": 3000,
                "keywords": "",
                "edition": "Third edition",
                "publisher": "MIT Press",
                "year": 2009
            }
        )
        self.b2 = doc_manager.Book.add(
            {
                "title": "Design Patterns: Elements of Reusable Object-Oriented Software",
                "author": "Erich Gamma, Ralph Johnson, John Vlissides, Richard Helm",
                "cost": 3000,
                "keywords": "best seller",
                "edition": "First edition",
                "publisher": "Addison-Wesley Professional",
                "year": 2003
            }
        )
        self.b3 = doc_manager.Book.add(
            {
                "title": "The Mythical Man-month",
                "author": "Brooks,Jr., Frederick P.",
                "cost": 3000,
                "keywords": "reference",
                "edition": "Second edition",
                "publisher": "Addison-Wesley Professional",
                "year": 1995
            }
        )

        self.b1c1 = doc_manager.Copy.add(self.b1)
        self.b1c2 = doc_manager.Copy.add(self.b1)
        self.b1c3 = doc_manager.Copy.add(self.b1)
        self.b2c1 = doc_manager.Copy.add(self.b2)
        self.b2c2 = doc_manager.Copy.add(self.b2)
        self.b3c1 = doc_manager.Copy.add(self.b3)

        self.av1 = doc_manager.AVMaterial.add(
            {
                "title": "Null References: The Billion Dollar Mistake",
                "author": "Tony Hoare",
                "cost": 1000000000,
                "keywords": "",
            }
        )

        self.av2 = doc_manager.AVMaterial.add(
            {
                "title": "Information Entropy",
                "author": "Claude Shannon",
                "cost": 100,
                "keywords": "",
            }
        )

        self.av1c1 = doc_manager.Copy.add(self.av1)
        self.av2c1 = doc_manager.Copy.add(self.av2)

        self.p1 = user_manager.User.add(
            {
                "name": "Sergey",
                "surname": "Afonso",
                "address": "Via Margutta, 3",
                "phone": 30001,
                "group": self.g_f
            }
        )
        self.p2 = user_manager.User.add(
            {
                "name": "Nadia",
                "surname": "Teixeira",
                "address": "Via Sacra, 13",
                "phone": 30002,
                "group": self.g_s
            }
        )
        self.p3 = user_manager.User.add(
            {
                "name": "Elvira",
                "surname": "Espindola",
                "address": "Via del Corso, 22",
                "phone": 30003,
                "group": self.g_s
            }
        )

        copies = doc_manager.Copy.select()
        active_copies = [x for x in copies if x.active]
        self.assertEqual(len(active_copies), 8)
        users = user_manager.User.get_list(100, 1)
        # Librarian is no a patron, only 1 librarian
        self.assertEqual(len(users) + 1, 4)

    def test_case_2(self):
        self.test_case_1()
        b1_c = self.b1.get_document_copies()
        b1_ac = [x for x in b1_c if x.active]
        doc_manager.Copy.remove(b1_ac[0].CopyID)
        doc_manager.Copy.remove(b1_ac[1].CopyID)

        b3_c = self.b3.get_document_copies()
        b3_ac = [x for x in b3_c if x.active]
        doc_manager.Copy.remove(b3_ac[0].CopyID)

        user_manager.User.remove(self.p2.card_id)

        copies = doc_manager.Copy.select()
        active_copies = [x for x in copies if x.active]
        self.assertEqual(len(active_copies), 5)
        users = user_manager.User.get_list(100, 1)
        # Librarian is no a patron, only 1 librarian
        self.assertEqual(len(users) + 1, 3)

    def test_case_3(self):
        self.test_case_1()

        p1 = user_manager.User.get_by_id(1000)
        self.assertEqual(p1.name + " " + self.p1.surname, "Sergey Afonso")
        self.assertEqual(p1.address, "Via Margutta, 3")
        self.assertEqual(p1.phone, 30001)
        self.assertEqual(p1.card_id, 1000)
        self.assertEqual(p1.group, self.g_f)

        p3 = user_manager.User.get_by_id(1002)
        self.assertEqual(p3.name + " " + self.p3.surname, "Elvira Espindola")
        self.assertEqual(p3.address, "Via del Corso, 22")
        self.assertEqual(p3.phone, 30003)
        self.assertEqual(p3.card_id, 1002)
        self.assertEqual(p3.group, self.g_s)

    def test_case_4(self):
        self.test_case_2()

        p3 = user_manager.User.get_by_id(1002)
        self.assertEqual(p3.name + " " + self.p3.surname, "Elvira Espindola")
        self.assertEqual(p3.address, "Via del Corso, 22")
        self.assertEqual(p3.phone, 30003)
        self.assertEqual(p3.card_id, 1002)
        self.assertEqual(p3.group, self.g_s)

        p2 = user_manager.User.get_by_id(1001)
        self.assertEqual(p2.group.id, 1)

    def test_case_5(self):
        self.test_case_2()
        bsystem = booking_system.Booking_system()
        p2 = user_manager.User.get_by_id(1001)
        res = bsystem.check_out(p2, self.b1c1, "Librarian")
        self.assertEqual(res, (4, None))

    def test_case_6(self):
        self.test_case_2()
        bsystem = booking_system.Booking_system()
        p1 = user_manager.User.get_by_id(1000)
        p3 = user_manager.User.get_by_id(1002)
        b1_not_checked_copies = [x for x in doc_manager.Book.get_document_copies(self.b1) if x.active and not x.checked_out]
        res = bsystem.check_out(p1, b1_not_checked_copies[0], "Librarian")
        # successfully checked out b1 to p1
        self.assertEqual(res[0], 0)
        b1_not_checked_copies = [x for x in doc_manager.Book.get_document_copies(self.b1) if not x.checked_out]
        b2_not_checked_copies = [x for x in doc_manager.Book.get_document_copies(self.b2) if not x.checked_out]
        res = bsystem.check_out(p3, b1_not_checked_copies[0], "Librarian")
        # error while checking out b1 to p3
        self.assertEqual(res[0], 3)
        res = bsystem.check_out(p3, b2_not_checked_copies[0], "Librarian")
        # successfully checked out b2 to p3
        self.assertEqual(res[0], 0)

        self.assertEqual(p1.name + " " + self.p1.surname, "Sergey Afonso")
        self.assertEqual(p1.address, "Via Margutta, 3")
        self.assertEqual(p1.phone, 30001)
        self.assertEqual(p1.card_id, 1000)
        self.assertEqual(p1.group, self.g_f)

        self.assertEqual(len(p1.operations), 1)
        p1_h = p1.operations[0]
        p1_d = p1_h.copy.get_doc()
        self.assertEqual(p1_d.DocumentID, self.b1.DocumentID)
        ret_time = bsystem.get_max_return_time(p1_h)
        delay = (datetime.datetime.strptime(ret_time, "%Y-%m-%d").date() - datetime.date.today()).days
        self.assertEqual(delay, 28)

        p3 = user_manager.User.get_by_id(1002)
        self.assertEqual(p3.name + " " + self.p3.surname, "Elvira Espindola")
        self.assertEqual(p3.address, "Via del Corso, 22")
        self.assertEqual(p3.phone, 30003)
        self.assertEqual(p3.card_id, 1002)
        self.assertEqual(p3.group, self.g_s)

        self.assertEqual(len(p3.operations), 1)
        p3_h = p3.operations[0]
        p3_d = p3_h.copy.get_doc()
        self.assertEqual(p3_d.DocumentID, self.b2.DocumentID)
        ret_time = bsystem.get_max_return_time(p3_h)
        delay = (datetime.datetime.strptime(ret_time, "%Y-%m-%d").date() - datetime.date.today()).days
        self.assertEqual(delay, 14)


    def test_case_7(self):
        self.test_case_1()
        bsystem = booking_system.Booking_system()
        p1 = user_manager.User.get_by_id(1001)
        b1_not_checked_copies = [x for x in doc_manager.Book.get_document_copies(self.b1) if not x.checked_out]
        b2_not_checked_copies = [x for x in doc_manager.Book.get_document_copies(self.b2) if not x.checked_out]
        b3_not_checked_copies = [x for x in doc_manager.Book.get_document_copies(self.b3) if not x.checked_out]
        av1_not_checked_copies = [x for x in doc_manager.Book.get_document_copies(self.av1) if not x.checked_out]
        av2_not_checked_copies = [x for x in doc_manager.Book.get_document_copies(self.av2) if not x.checked_out]

        res = bsystem.check_out(self.p1, b1_not_checked_copies[0], "Librarian")
        self.assertEqual(res[0], 0)

        res = bsystem.check_out(self.p1, b2_not_checked_copies[0], "Librarian")
        self.assertEqual(res[0], 0)

        # Cannot checkout: is reference
        res = bsystem.check_out(self.p1, b3_not_checked_copies[0], "Librarian")
        self.assertEqual(res[0], 2)

        res = bsystem.check_out(self.p1, av1_not_checked_copies[0], "Librarian")
        self.assertEqual(res[0], 0)

        res = bsystem.check_out(self.p2, b1_not_checked_copies[1], "Librarian")
        self.assertEqual(res[0], 0)

        res = bsystem.check_out(self.p2, b2_not_checked_copies[1], "Librarian")
        self.assertEqual(res[0], 0)
        res = bsystem.check_out(self.p2, av2_not_checked_copies[0], "Librarian")
        self.assertEqual(res[0], 0)

        p1 = user_manager.User.get_by_id(1000)
        self.assertEqual(p1.name + " " + self.p1.surname, "Sergey Afonso")
        self.assertEqual(p1.address, "Via Margutta, 3")
        self.assertEqual(p1.phone, 30001)
        self.assertEqual(p1.card_id, 1000)
        self.assertEqual(p1.group, self.g_f)

        p1_operations = list(p1.operations)
        p1_docs = {self.b1: 4, self.b2: 4, self.av1: 2}
        # documents which user should have
        for p1_shd in p1_docs.keys():
            # documents which user actually have
            have = False
            for p1_h in p1_operations:
                p1_d = p1_h.copy.get_doc()
                if type(p1_d) == type(p1_shd) and p1_d.DocumentID == p1_shd.DocumentID:
                    self.assertFalse(have)
                    ret_time = bsystem.get_max_return_time(p1_h)
                    delay = datetime.datetime.strptime(ret_time, "%Y-%m-%d").date() - datetime.date.today()
                    self.assertEqual(delay.days, 7*p1_docs[p1_shd])
                    have = True
            self.assertTrue(have)

        p2 = user_manager.User.get_by_id(1001)
        self.assertEqual(p2.name + " " + self.p2.surname, "Nadia Teixeira")
        self.assertEqual(p2.address, "Via Sacra, 13")
        self.assertEqual(p2.phone, 30002)
        self.assertEqual(p2.card_id, 1001)
        self.assertEqual(p2.group, self.g_s)

        p2_operations = list(p2.operations)
        p2_docs = {self.b1: 3, self.b2: 2, self.av2: 2}
        # documents which user should have
        for p2_shd in p2_docs.keys():
            # documents which user actually have
            have = False
            for p2_h in p2_operations:
                p2_d = p2_h.copy.get_doc()
                if type(p2_d) == type(p2_shd) and p2_d.DocumentID == p2_shd.DocumentID:
                    self.assertFalse(have)
                    ret_time = bsystem.get_max_return_time(p2_h)
                    delay = datetime.datetime.strptime(ret_time, "%Y-%m-%d").date() - datetime.date.today()
                    datetime.datetime.strptime(ret_time, "%Y-%m-%d").date()
                    self.assertEqual(delay.days, 7*p2_docs[p2_shd])
                    have = True
            self.assertTrue(have)

    def test_case_8(self):
        self.test_case_1()

        p1 = user_manager.User.get_by_id(1000)
        b1 = doc_manager.Book.get_by_id(1)
        b2 = doc_manager.Book.get_by_id(2)
        p2 = user_manager.User.get_by_id(1001)
        av1 = doc_manager.AVMaterial.get_by_id(1)

        bs = booking_system.Booking_system()
        h1 = bs.check_out(p1, b2.get_document_copies()[0], 'Mr. Libro')[1]
        h1.date_check_out = '2018-02-02'
        h1.save()

        h3 = bs.check_out(p2, b1.get_document_copies()[1], 'Mr. Libro')[1]
        h3.date_check_out = '2018-02-05'
        h3.save()

        h2 = bs.check_out(p1, b1.get_document_copies()[0], 'Mr. Libro')[1]
        h2.date_check_out = '2018-02-09'
        h2.save()

        h4 = bs.check_out(p2, av1.get_document_copies()[0], 'Mr. Libro')[1]
        h4.date_check_out = '2018-02-17'
        h4.save()

        p1 = user_manager.User.get_by_id(1000)
        p2 = user_manager.User.get_by_id(1001)

        ans1 = []
        ans2 = []

        p1_history = bs.get_user_history(p1)
        for entry in p1_history:
            if (bs.check_overdue(entry) > 0):
                t = (entry.copy.get_doc().title, bs.check_overdue(entry) // 100)
                ans1.append(t)
        
        p2_history = bs.get_user_history(p2)
        for entry in p2_history:
            if (bs.check_overdue(entry) > 0):
                t = (entry.copy.get_doc().title, bs.check_overdue(entry) // 100)
                ans2.append(t)
        
        today = datetime.date.today()

        self.assertEqual(ans1[0][1], min(3 + (today -  datetime.date(2018, 3, 5)).days, 3000))
        self.assertEqual(ans1[0][0], b2.title)
        self.assertEqual(ans2[0][1], min(7 + (today -  datetime.date(2018, 3, 5)).days, 3000))
        self.assertEqual(ans2[0][0], b1.title)
        self.assertEqual(ans2[1][1], min(2 + (today -  datetime.date(2018, 3, 5)).days, 3000))
        self.assertEqual(ans2[1][0], av1.title)

    def test_case_9(self):
        self.test_case_1()

        # simulate re-run
        db_fname = "test_database.db"
        db_config.init_db(db_fname)
        db_config.create_tables()

        b1 = doc_manager.Book.get_by_id(1)
        self.assertEqual(len(doc_manager.Book.get_document_copies(b1)), 3)

        b2 = doc_manager.Book.get_by_id(2)
        self.assertEqual(len(doc_manager.Book.get_document_copies(b2)), 2)

        b3 = doc_manager.Book.get_by_id(3)
        self.assertEqual(len(doc_manager.Book.get_document_copies(b3)), 1)

        u = user_manager.User.get_list(20, 1)
        self.assertEqual(len(u), 3)


if __name__ == '__main__':
    unittest.main()
