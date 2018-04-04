import unittest
import managers.doc_manager as doc_manager
import managers.booking_system as booking_system
import managers.user_manager as user_manager
import managers.group_manager as group_manager
import db_config
import datetime


class TestCases3(unittest.TestCase):
    def prepare_database(self):
        db_fname = "test_database.db"
        db_config.init_db(db_fname)
        db_config.drop_tables()
        db_config.create_tables()
        self.g_f = group_manager.Group.get(group_manager.Group.name == 'Faculty')
        self.g_s = group_manager.Group.get(group_manager.Group.name == 'Students')
        self.g_v = group_manager.Group.get(group_manager.Group.name == 'Visiting professors')

        self.d1 = doc_manager.Book.add(
            {
                "title": "Introduction to Algorithms",
                "author": "Thomas H. Cormen, Charles E. Leiserson, Ronald L. Rivest and Clifford Stein",
                "cost": 5000,
                "keywords": "",
                "edition": "Third edition",
                "publisher": "MIT Press",
                "year": 2009
            }
        )
        self.d2 = doc_manager.Book.add(
            {
                "title": "Design Patterns: Elements of Reusable Object-Oriented Software",
                "author": "Erich Gamma, Ralph Johnson, John Vlissides, Richard Helm",
                "cost": 1700,
                "keywords": "best seller",
                "edition": "First edition",
                "publisher": "Addison-Wesley Professional",
                "year": 2003
            }
        )
        self.d3 = doc_manager.AVMaterial.add(
            {
                "title": "Null References: The Billion Dollar Mistake",
                "author": "Tony Hoare",
                "cost": 700,
                "keywords": "",
            }
        )
        self.p1 = user_manager.User.add(
            {
                "name": "Sergey",
                "surname": "Afonso",
                "address": "Via Margutta, 3",
                "phone": 30001,
                "group": self.g_f,
                "email": "m.bobrov@innopolis.ru"
            }
        )
        self.p2 = user_manager.User.add(
            {
                "name": "Nadia",
                "surname": "Teixeira",
                "address": "Via Sacra, 13",
                "phone": 30002,
                "group": self.g_f,
                "email": "m.bobrov@innopolis.ru"
            }
        )
        self.p3 = user_manager.User.add(
            {
                "name": "Elvira",
                "surname": "Espindola",
                "address": "Via del Corso, 22",
                "phone": 30003,
                "group": self.g_f,
                "email": "m.bobrov@innopolis.ru"
            }
        )
        self.s = user_manager.User.add(
            {
                "name": "Andrey",
                "surname": "Velo",
                "address": "Avenida Mazatlan 250",
                "phone": 30004,
                "group": self.g_s,
                "email": "m.bobrov@innopolis.ru"
            }
        )
        self.v = user_manager.User.add(
            {
                "name": "Veronika",
                "surname": "Rama",
                "address": "Stret Atocha, 27",
                "phone": 30005,
                "group": self.g_v,
                "email": "m.bobrov@innopolis.ru"
            }
        )
        self.d1c1 = doc_manager.Copy.add(self.d1)
        self.d1c2 = doc_manager.Copy.add(self.d1)
        self.d1c3 = doc_manager.Copy.add(self.d1)
        self.d2c1 = doc_manager.Copy.add(self.d2)
        self.d2c2 = doc_manager.Copy.add(self.d2)
        self.d2c3 = doc_manager.Copy.add(self.d2)
        self.d3c1 = doc_manager.Copy.add(self.d3)
        self.d3c2 = doc_manager.Copy.add(self.d3)
        self.bsystem = booking_system.Booking_system()

    def test_case_1(self):
        self.prepare_database()

        # check out d1
        res = self.bsystem.check_out(self.d1, self.p1, "Librarian")
        self.assertEqual(res[0], 0)
        # (act like it checkouted 4 weeks ago)
        c = res[1]
        c.date_check_out = datetime.date.fromordinal(c.date_check_out.toordinal()-7*4)
        c.save()

        res = self.bsystem.check_out(self.d2, self.p1, "Librarian")
        self.assertEqual(res[0], 0)
        c = res[1]
        c.date_check_out = datetime.date.fromordinal(c.date_check_out.toordinal()-7*4)
        c.save()

        c = list(self.p1.operations)
        c = [i for i in c if i.copy.get_doc() == self.d1]
        self.assertEqual(len(c), 1)
        self.assertEqual(c[0].copy.get_doc(), self.d1)

        self.bsystem.return_by_entry(c[0], "librarian_re")

        c = list(self.p1.operations)
        c = [i for i in c if i.copy.get_doc() != self.d1]
        self.assertEqual(len(c), 1)

        date_return = self.bsystem.get_max_return_time(c[0])
        delay = (datetime.date.today() - datetime.datetime.strptime(date_return, "%Y-%m-%d").date()).days
        self.assertEqual(max(0, delay), 0)
        self.assertEqual(self.bsystem.check_overdue(c[0]), 0)

    def test_case_2(self):
        self.prepare_database()

        # check out d1
        res = self.bsystem.check_out(self.d1, self.p1, "Librarian")
        self.assertEqual(res[0], 0)
        # (act like it checkouted 4 weeks ago)
        c = res[1]
        c.date_check_out = datetime.date.fromordinal(c.date_check_out.toordinal()-7*4)
        c.save()

        res = self.bsystem.check_out(self.d2, self.p1, "Librarian")
        self.assertEqual(res[0], 0)
        c = res[1]
        c.date_check_out = datetime.date.fromordinal(c.date_check_out.toordinal()-7*4)
        c.save()

        res = self.bsystem.check_out(self.d1, self.s, "Librarian")
        self.assertEqual(res[0], 0)
        c = res[1]
        c.date_check_out = datetime.date.fromordinal(c.date_check_out.toordinal()-7*4)
        c.save()

        res = self.bsystem.check_out(self.d2, self.s, "Librarian")
        self.assertEqual(res[0], 0)
        c = res[1]
        c.date_check_out = datetime.date.fromordinal(c.date_check_out.toordinal()-7*4)
        c.save()

        res = self.bsystem.check_out(self.d1, self.v, "Librarian")
        self.assertEqual(res[0], 0)
        c = res[1]
        c.date_check_out = datetime.date.fromordinal(c.date_check_out.toordinal()-7*4)
        c.save()

        res = self.bsystem.check_out(self.d2, self.v, "Librarian")
        self.assertEqual(res[0], 0)
        c = res[1]
        c.date_check_out = datetime.date.fromordinal(c.date_check_out.toordinal()-7*4)
        c.save()

        # p1
        overdue_fine_expected = {(self.d1, 0, 0), (self.d2, 0, 0)}
        operations = list(self.p1.operations)
        self.assertEqual(len(operations), 2)
        overdue_fine = set()
        for c in operations:
            date_return = self.bsystem.get_max_return_time(c)
            delay = (datetime.date.today() - datetime.datetime.strptime(date_return, "%Y-%m-%d").date()).days
            overdue_fine.add((c.copy.get_doc(), max(0, delay), self.bsystem.check_overdue(c)))
        self.assertEqual(overdue_fine, overdue_fine_expected)

        # s
        overdue_fine_expected = {(self.d1, 7, 700), (self.d2, 14, 1400)}
        operations = list(self.s.operations)
        self.assertEqual(len(operations), 2)
        overdue_fine = set()
        for c in operations:
            date_return = self.bsystem.get_max_return_time(c)
            delay = (datetime.date.today() - datetime.datetime.strptime(date_return, "%Y-%m-%d").date()).days
            overdue_fine.add((c.copy.get_doc(), max(0, delay), self.bsystem.check_overdue(c)))
        self.assertEqual(overdue_fine, overdue_fine_expected)

        # v
        overdue_fine_expected = {(self.d1, 21, 2100), (self.d2, 21, 1700)}
        operations = list(self.v.operations)
        self.assertEqual(len(operations), 2)
        overdue_fine = set()
        for c in operations:
            date_return = self.bsystem.get_max_return_time(c)
            delay = (datetime.date.today() - datetime.datetime.strptime(date_return, "%Y-%m-%d").date()).days
            overdue_fine.add((c.copy.get_doc(), max(0, delay), self.bsystem.check_overdue(c)))
        self.assertEqual(overdue_fine, overdue_fine_expected)

    def test_case_3(self):
        self.prepare_database()

        # checkout 4 days ago and renew today
        def check_out_old_renew_today(d, p):
            res = self.bsystem.check_out(d, p, "Librarian")
            self.assertEqual(res[0], 0)
            # (act like it checkouted 4 days ago)
            c = res[1]
            c.date_check_out = str(datetime.date.fromordinal(c.date_check_out.toordinal()-4))
            c.save()
            # renew today
            self.bsystem.renew_by_entry(c, "Librarian_2")

        # check out d1 to p1
        check_out_old_renew_today(self.d1, self.p1)

        # check out d2 to s
        check_out_old_renew_today(self.d2, self.s)

        # check out d2 to v
        check_out_old_renew_today(self.d2, self.v)

        #####

        def check_operations(user, doc_date_expected):
            operations = list(user.operations.where(booking_system.History.date_return.is_null(True)))
            self.assertEqual(len(operations), 1)
            c = operations[0]
            doc_date = (c.copy.get_doc(), datetime.datetime.strptime(self.bsystem.get_max_return_time(c), "%Y-%m-%d").date())
            self.assertEqual(doc_date, doc_date_expected)

        # p1
        doc_date_expected = (self.d1, datetime.date.fromordinal(datetime.date.today().toordinal()+4*7))
        check_operations(self.p1, doc_date_expected)

        # s
        doc_date_expected = (self.d2, datetime.date.fromordinal(datetime.date.today().toordinal()+2*7))
        check_operations(self.s, doc_date_expected)

        # v
        doc_date_expected = (self.d2, datetime.date.fromordinal(datetime.date.today().toordinal()+7))
        check_operations(self.v, doc_date_expected)

    def test_case_4(self):
        self.prepare_database()

        # checkout 4 days ago and renew today
        def check_out_old(d, p):
            res = self.bsystem.check_out(d, p, "Librarian")
            self.assertEqual(res[0], 0)
            # (act like it checkouted 4 days ago)
            c = res[1]
            c.date_check_out = str(datetime.date.fromordinal(c.date_check_out.toordinal()-4))
            c.save()

        # check out d1 to p1
        check_out_old(self.d1, self.p1)

        # check out d2 to s
        check_out_old(self.d2, self.s)

        # check out d2 to v
        check_out_old(self.d2, self.v)

        ###

        # TODO: ASK TA

        # self.bsystem.outstanding_request(self.d2, self.p1)

        def renew_single_doc(user):
            opers = user.operations.where(booking_system.History.date_return.is_null(True))
            print(len(opers))
            c = opers[0]
            self.bsystem.renew_by_entry(c, "Librarian_2")

        renew_single_doc(self.p1)
        renew_single_doc(self.s)
        renew_single_doc(self.v)


    def test_case_5(self):
        self.prepare_database()

        # check out d3 to p1
        res = self.bsystem.check_out(self.d3, self.p1, "Librarian")
        self.assertEqual(res[0], 0)

        # check out d3 to s
        res = self.bsystem.check_out(self.d3, self.s, "Librarian")
        self.assertEqual(res[0], 0)

        # check out d3 to v
        res = self.bsystem.check_out(self.d3, self.v, "Librarian")
        self.assertEqual(res[0], 1)

        d3_waiting_list = user_manager.Queue.get_list(self.d3, 10, 1)[0]
        self.assertEqual(len(d3_waiting_list), 1)
        self.assertEqual(d3_waiting_list[0].get_doc(), self.d3)

        d3_waiting_list_users = [i.user for i in d3_waiting_list]
        d3_waiting_list_users_expected = [self.v]

        self.assertEqual(d3_waiting_list_users, d3_waiting_list_users_expected)

    def test_case_6(self):
        self.prepare_database()

        # check out d3 to p1
        res = self.bsystem.check_out(self.d3, self.p1, "Librarian")

        # check out d3 to p2
        res = self.bsystem.check_out(self.d3, self.p2, "Librarian")

        # check out d3 to s
        res = self.bsystem.check_out(self.d3, self.s, "Librarian")

        # check out d3 to v
        res = self.bsystem.check_out(self.d3, self.v, "Librarian")

        # check out d3 to p3
        res = self.bsystem.check_out(self.d3, self.p3, "Librarian")

        d3_waiting_list = user_manager.Queue.get_list(self.d3, 10, 1)[0]
        d3_waiting_list_users = [i.user for i in d3_waiting_list]
        d3_waiting_list_users_expected = [self.s, self.v, self.p3]

        self.assertEqual(d3_waiting_list_users, d3_waiting_list_users_expected)

    def test_case_7(self):
        self.test_case_6()

        d3_waiting_list = user_manager.Queue.get_list(self.d3, 10, 1)[0]
        d3_waiting_list_users = [i.user for i in d3_waiting_list]
        d3_waiting_list_users_expected = []

        # self.assertEqual(d3_waiting_list_users, d3_waiting_list_users_expected)


    def test_case_8(self):
        self.test_case_6()

        c = list(self.p2.operations)
        c = [i for i in c if i.copy.get_doc() == self.d3]
        self.assertEqual(len(c), 1)
        self.bsystem.return_by_entry(c[0], "librarian_re")

        operations = list(self.p2.operations.where(booking_system.History.date_return.is_null(True)))
        self.assertEqual(operations, [])

        d3_waiting_list = user_manager.Queue.get_list(self.d3, 10, 1)[0]
        d3_waiting_list_users = [i.user for i in d3_waiting_list]
        d3_waiting_list_users_expected = [self.s, self.v, self.p3]

        self.assertEqual(d3_waiting_list_users, d3_waiting_list_users_expected)

    def test_case_9(self):
        self.test_case_6()

        oper = list(self.p1.operations.where(booking_system.History.date_return.is_null(True)))[0]
        self.assertEqual(oper.copy.get_doc(), self.d3)
        self.bsystem.renew_by_entry(oper, "Librarian_2")

        operations = list(self.p2.operations.where(booking_system.History.date_return.is_null(True)))
        self.assertEqual(len(operations), 1)

        # TODO: ASK TA ABOUT THIS TEST
        doc_date_expected = (self.d3, datetime.date.fromordinal(datetime.date.today().toordinal()+2*7))
        operations = list(self.p1.operations.where(booking_system.History.date_return.is_null(True)))
        self.assertEqual(len(operations), 1)
        c = operations[0]
        doc_date = (c.copy.get_doc(), datetime.datetime.strptime(self.bsystem.get_max_return_time(c), "%Y-%m-%d").date())
        self.assertEqual(doc_date, doc_date_expected)

        d3_waiting_list = user_manager.Queue.get_list(self.d3, 10, 1)[0]
        d3_waiting_list_users = [i.user for i in d3_waiting_list]
        d3_waiting_list_users_expected = [self.s, self.v, self.p3]

        self.assertEqual(d3_waiting_list_users, d3_waiting_list_users_expected)

    def test_case_10(self):
        self.prepare_database()

        res = self.bsystem.check_out(self.d1, self.p1, "Librarian")
        self.assertEqual(res[0], 0)
        # checkout week ago
        c = res[1]
        c.date_check_out = str(datetime.date.fromordinal(c.date_check_out.toordinal()-7))
        c.save()

        res = self.bsystem.check_out(self.d1, self.v, "Librarian")
        self.assertEqual(res[0], 0)
        # checkout week ago
        c2 = res[1]
        c2.date_check_out = str(datetime.date.fromordinal(c2.date_check_out.toordinal()-7))
        c2.save()

        # renew 4 days ago
        res = self.bsystem.renew_by_entry(c, "Librarian_2")
        c = res[1]
        c.date_check_out = str(datetime.date.fromordinal(c.date_check_out.toordinal()-4))
        c.save()

        # renew 4 days ago
        res = self.bsystem.renew_by_entry(c2, "Librarian_2")
        c2 = res[1]
        c2.date_check_out = str(datetime.date.fromordinal(c2.date_check_out.toordinal()-4))
        c2.save()

        ####
        # renew today

        # try renew again today (fails)
        res = self.bsystem.renew_by_entry(c, "Librarian_3")
        self.assertEqual(res[0], 6)

        # try renew again today (fails)
        res = self.bsystem.renew_by_entry(c2, "Librarian_3")
        self.assertEqual(res[0], 6)

        def check_operations(user, doc_date_expected):
            operations = list(user.operations.where(booking_system.History.date_return.is_null(True)))
            self.assertEqual(len(operations), 1)
            c = operations[0]
            doc_date = (c.copy.get_doc(), datetime.datetime.strptime(self.bsystem.get_max_return_time(c), "%Y-%m-%d").date())
            print(doc_date)
            self.assertEqual(doc_date, doc_date_expected)

        # p1
        doc_date_expected = (self.d1, datetime.date.fromordinal(datetime.date.today().toordinal()+4*7-4))
        check_operations(self.p1, doc_date_expected)

        # v
        doc_date_expected = (self.d1, datetime.date.fromordinal(datetime.date.today().toordinal()+1*7-4))
        check_operations(self.v, doc_date_expected)



if __name__ == '__main__':
    unittest.main()
