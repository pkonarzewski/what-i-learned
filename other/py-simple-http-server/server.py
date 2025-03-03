# python -m http.server

from http.server import HTTPServer, BaseHTTPRequestHandler


class HTTPequestHandler(BaseHTTPRequestHandler):
    pass


def run(server_class=HTTPServer, handler_class=HTTPequestHandler):
    server_address = ("", 8000)
    httpd = server_class(server_address, handler_class)
    print("Starting server...")
    httpd.serve_forever()


if __name__ == "__main__":
    run()
