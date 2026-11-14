import http.server
import socketserver
import json
import os

PORT = 8000
DB_FILE = "database.json"

class LaricaHandler(http.server.SimpleHTTPRequestHandler):
    def log_message(self, format, *args):
     print(f"[{self.log_date_time_string()}] {format%args}")

    def do_GET(self):
        # Ignora a requisição de favicon para evitar erros desnecessários
        if self.path == "/favicon.ico":
            self.send_response(204)
            self.end_headers()
            return

        if self.path == "/" or self.path == "":
            self.path = "/index.html"

        if self.path == "/api/db":
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Cache-Control", "no-store")
            self.end_headers()
            
            if not os.path.exists(DB_FILE) or os.path.getsize(DB_FILE) == 0:
                default_data = {"store": {"isOpen": True}, "menu": [], "orders": [], "coupons": {}}
                with open(DB_FILE, "w", encoding="utf-8") as f:
                    json.dump(default_data, f)
            
            try:
                with open(DB_FILE, "r", encoding="utf-8") as f:
                    content = f.read()
                    if not content.strip():
                        content = "{}"
                    self.wfile.write(content.encode("utf-8"))
            except Exception as e:
                self.wfile.write(b'{"store":{},"menu":[],"orders":[],"coupons":{}}')
        else:
            # Tratamento seguro para arquivos estáticos (index.html, etc.)
            try:
                super().do_GET()
            except Exception as e:
                self.send_response(404)
                self.end_headers()
                self.wfile.write(b"Arquivo nao encontrado.")

    def do_POST(self):
        if self.path == "/api/db":
            try:
                content_length = int(self.headers.get("Content-Length", 0))
                post_data = self.rfile.read(content_length).decode("utf-8")
                json.loads(post_data)
                
                with open(DB_FILE, "w", encoding="utf-8") as f:
                    f.write(post_data)
                    
                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(b'{"status":"ok"}')
            except Exception as e:
                self.send_response(400)
                self.end_headers()
                self.wfile.write(b'{"status":"error"}')
        else:
            self.send_response(404)
            self.end_headers()

if __name__ == "__main__":
    with socketserver.TCPServer(("0.0.0.0", PORT), LaricaHandler) as httpd:
        print(f"Servidor LaricaOnline rodando na porta {PORT}...")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nServidor encerrado.")
