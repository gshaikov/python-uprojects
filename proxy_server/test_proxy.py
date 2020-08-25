from proxy import get_host_port_path


class Test_get_host_port_path:
    def test_connect(self):
        req = b"CONNECT gateway.icloud.com:448 HTTP/1.1\rHeader: foo"
        domain, port, path = get_host_port_path(req)
        assert domain is None
        assert port is None
        assert path is None

    def test_get(self):
        req = (
            b"GET http://gateway.icloud.com:448 HTTP/1.1\r\n"
            b"Host: gateway.icloud.com:44"
        )
        domain, port, path = get_host_port_path(req)
        assert domain == "gateway.icloud.com"
        assert port == 448
        assert path == "/"

    def test_get_path(self):
        req = (
            b"GET http://gateway.icloud.com:448/foo/bar HTTP/1.1\r\n"
            b"Host: gateway.icloud.com:44"
        )
        domain, port, path = get_host_port_path(req)
        assert domain == "gateway.icloud.com"
        assert port == 448
        assert path == "/foo/bar"

    def test_get_no_port(self):
        req = b"GET http://gateway.icloud.com HTTP/1.1\r\nHeader: foo"
        domain, port, path = get_host_port_path(req)
        assert domain == "gateway.icloud.com"
        assert port == 80
        assert path == "/"

    def test_none(self):
        req = b"GET / HTTP/1.1\r\nHost: gateway.icloud.com:44"
        domain, port, path = get_host_port_path(req)
        assert domain is None
        assert port == 80
        assert path == "/"
