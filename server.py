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
    print(d.get_main_fields())
    print(d.get_additional_fields())
    print("====")
    print(d.get_main_fields_names())
    print(d.get_additional_fields_names())


if __name__ == '__main__':
    main()
