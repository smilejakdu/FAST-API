from repository import test_repository


def test_index(db):
    something = test_repository.get_items(db)
    return something
