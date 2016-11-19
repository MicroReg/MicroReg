from sreg.database.MicroDB import MicroDB

class TestMicroDB:

    def test_insert(self):
        db = MicroDB()
        assert db.insert("k1","val1") == True

    def test_insert_repeatkey(self):
        db = MicroDB()
        db.insert("k1","val1")
        assert db.insert("k1","val2") == True

    def test_update(self):
        db = MicroDB()
        db.insert("k1","val1")
        assert db.update("k1","val2") == True

    def test_update_failure(self):
        db = MicroDB()
        assert db.update("k1","val1") == False

    def test_get(self):
        db = MicroDB()
        db.insert("k1","val1")
        assert db.get("k1") == "val1"

    def test_get_failed(self):
        db = MicroDB()
        try:
            db.get("k1")
        except KeyError:
            assert True

    def test_remove(self):
        db = MicroDB()
        db.insert("k1","val1")
        assert db.remove("k1") == True

    def test_remove_failed(self):
        db = MicroDB()
        try:
            db.remove("k1")
        except KeyError:
            assert True
