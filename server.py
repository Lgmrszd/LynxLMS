from lynxlms_server import *


def main():
    config.init_main()
    d = Document.create(
        title="Title",
        author="Author",
        cost=100,
        keywords="keywords",
        doc_type="Book",
        edition="first",
        publisher="cool pub",
        year=1999
    )
    d.save()
    u = User.create(
        name="Name",
        surname="Surname",
        address="Address",
        phone=14241,
        group=Group.get(Group.name == "Students")
    )
    u.save()


if __name__ == '__main__':
    main()
