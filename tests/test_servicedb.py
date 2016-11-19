from sreg.database.ServiceDB import ServiceDB

class TestServiceDB:

    def test_register_service(self):
        sdb = ServiceDB()
        response = sdb.register_service('test service', 'localhost', '8000', ServiceDB.SERVICE_RUNNING)
        assert response

    def test_update_service_status(self):
        sdb = ServiceDB()
        service_id = sdb.register_service('test service', 'localhost', '8000', ServiceDB.SERVICE_RUNNING)
        assert sdb.update_service_status(service_id, ServiceDB.SERVICE_STOPPED)

    def test_get_service_status(self):
        sdb = ServiceDB()
        service_id = sdb.register_service('test service', 'localhost', '8000', ServiceDB.SERVICE_RUNNING)
        assert sdb.get_service_status(service_id) == ServiceDB.SERVICE_RUNNING

    def test_get_service_location(self):
        sdb = ServiceDB()
        service_id = sdb.register_service('test service', 'localhost', '8000', ServiceDB.SERVICE_RUNNING)
        assert sdb.get_service_location(service_id) == ('localhost', '8000')

    def test_unregister_service(self):
        sdb = ServiceDB()
        service_id = sdb.register_service('test service', 'localhost', '8000', ServiceDB.SERVICE_RUNNING)
        assert sdb.unregister_service(service_id)
