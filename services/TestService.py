from repository import TestRepository


def test_index(db):
    something = TestRepository.get_items(db)
    return something
