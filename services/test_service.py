from repository import TestRepository


def test_index(db):
    something = test_repository.get_items(db)
    return something
