#!/usr/bin/env python3
"""
Servidor HTTP Python (Nginx)
Aluno: Hermeson A. | Matrícula: 20239035382
"""
import http.server
import socketserver
import os
from urllib.parse import urlparse
import json
from datetime import datetime
import time

PORT = 80

# Contadores para métricas
class Metrics:
    def __init__(self):
        self.requests_total = 0
        self.bytes_sent = 0
        self.start_time = time.time()
    
    def increment_request(self):
        self.requests_total += 1
    
    def add_bytes(self, bytes_count):
        self.bytes_sent += bytes_count

metrics = Metrics()

class CustomHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        parsed_path = urlparse(self.path)
        path = parsed_path.path
        
        # Incrementar contador de requisições
        metrics.increment_request()
        
        # Log do X-Custom-ID
        x_custom_id = self.headers.get('X-Custom-ID', 'N/A')
        print(f"[{datetime.now().isoformat()}] {self.command} {path} - X-Custom-ID: {x_custom_id}")
        
        # Endpoint de métricas Prometheus
        if path == '/metrics':
            self.send_response(200)
            self.send_header('Content-Type', 'text/plain; version=0.0.4')
            self.end_headers()
            uptime = time.time() - metrics.start_time
            prometheus_metrics = f"""# HELP http_requests_total Total HTTP requests
# TYPE http_requests_total counter
http_requests_total{{server="nginx",aluno="Hermeson_A",matricula="20239035382"}} {metrics.requests_total}

# HELP http_response_size_bytes Total bytes sent
# TYPE http_response_size_bytes counter
http_response_size_bytes{{server="nginx"}} {metrics.bytes_sent}

# HELP http_connections_active Active connections
# TYPE http_connections_active gauge
http_connections_active{{server="nginx"}} 1

# HELP process_uptime_seconds Server uptime in seconds
# TYPE process_uptime_seconds counter
process_uptime_seconds{{server="nginx"}} {uptime:.2f}
"""
            response_data = prometheus_metrics.encode()
            metrics.add_bytes(len(response_data))
            self.wfile.write(response_data)
            return
        
        # Endpoint de status da API
        if path == '/api/status':
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            response = {
                'status': 'ok',
                'server': 'python-nginx',
                'timestamp': datetime.now().isoformat(),
                'x_custom_id': x_custom_id
            }
            response_data = json.dumps(response).encode()
            metrics.add_bytes(len(response_data))
            self.wfile.write(response_data)
            return
        
        # Stub status para métricas
        if path == '/stub_status':
            self.send_response(200)
            self.send_header('Content-Type', 'text/plain')
            self.end_headers()
            status = f"""Active connections: 1
server accepts handled requests
 1 1 1
Reading: 0 Writing: 1 Waiting: 0
"""
            response_data = status.encode()
            metrics.add_bytes(len(response_data))
            self.wfile.write(response_data)
            return
        
        # Servir arquivos normalmente
        # Capturar tamanho do arquivo
        try:
            file_path = self.translate_path(path)
            if os.path.isfile(file_path):
                file_size = os.path.getsize(file_path)
                metrics.add_bytes(file_size)
        except:
            pass
        
        return super().do_GET()
    
    def log_message(self, format, *args):
        # Log customizado
        pass

def main():
    # Mudar para o diretório com os arquivos HTML
    os.chdir('/app/html')
    
    with socketserver.TCPServer(("", PORT), CustomHTTPRequestHandler) as httpd:
        print(f"========================================")
        print(f"Servidor Python (Nginx) rodando na porta {PORT}")
        print(f"Aluno: Hermeson A.")
        print(f"Matrícula: 20239035382")
        print(f"========================================")
        httpd.serve_forever()

if __name__ == '__main__':
    main()
