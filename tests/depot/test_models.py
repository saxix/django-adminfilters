from adminfilters.depot.models import StoredFilter


def test_str():
    return str(StoredFilter(name="Name")) == "Name"
