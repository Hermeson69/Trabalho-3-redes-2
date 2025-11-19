
import http.server
import socketserver
import os
from urllib.parse import urlparse
import json
from datetime import datetime
import time
import resource

PORT = 80

# Contadores para métricas
class Metrics:
    def __init__(self):
        self.requests_total = 0
        self.bytes_sent = 0
        self.start_time = time.time()
        self.requests_2xx = 0
        self.requests_4xx = 0
        self.requests_5xx = 0
        self.requests_by_path = {}
        self.total_request_time = 0.0
        self.request_times = []
        # Métricas específicas do Apache
        self.busy_workers = 0
        self.idle_workers = 10
        self.worker_connections = 0
        # Métricas em comum
        self.last_cpu_time = 0.0
        self.last_memory = 0
    
    def increment_request(self, status_code=200, path='/', request_time=0.01):
        self.requests_total += 1
        if 200 <= status_code < 300:
            self.requests_2xx += 1
        elif 400 <= status_code < 500:
            self.requests_4xx += 1
        elif 500 <= status_code < 600:
            self.requests_5xx += 1
        
        self.requests_by_path[path] = self.requests_by_path.get(path, 0) + 1
        self.total_request_time += request_time
        self.request_times.append(request_time)
        if len(self.request_times) > 1000:
            self.request_times.pop(0)
        
        # Simular alocar/liberar workers
        if self.busy_workers < 10:
            self.busy_workers = min(self.busy_workers + 1, 10)
            self.idle_workers = 10 - self.busy_workers
        self.worker_connections += 1
    
    def add_bytes(self, bytes_count):
        self.bytes_sent += bytes_count
        # Liberar alguns workers após completar
        if self.busy_workers > 0:
            self.busy_workers = max(self.busy_workers - 1, 0)
            self.idle_workers = 10 - self.busy_workers
    
    def get_avg_response_time(self):
        if not self.request_times:
            return 0.0
        return sum(self.request_times) / len(self.request_times)
    
    def get_cpu_usage(self):
        return resource.getrusage(resource.RUSAGE_SELF).ru_utime + resource.getrusage(resource.RUSAGE_SELF).ru_stime
    
    def get_memory_usage(self):
        return resource.getrusage(resource.RUSAGE_SELF).ru_maxrss * 1024
    
    def get_error_rate(self):
        if self.requests_total == 0:
            return 0.0
        return ((self.requests_4xx + self.requests_5xx) / self.requests_total) * 100
    
    def get_success_rate(self):
        if self.requests_total == 0:
            return 0.0
        return (self.requests_2xx / self.requests_total) * 100

metrics = Metrics()

class ApacheHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        parsed_path = urlparse(self.path)
        path = parsed_path.path
        request_start = time.time()
        
        # Log do X-Custom-ID
        x_custom_id = self.headers.get('X-Custom-ID', 'N/A')
        print(f"[{datetime.now().isoformat()}] Apache: {self.command} {path} - X-Custom-ID: {x_custom_id}")
        
        # Endpoint de métricas Prometheus
        if path == '/metrics':
            request_time = time.time() - request_start
            metrics.increment_request(200, path, request_time)
            self.send_response(200)
            self.send_header('Content-Type', 'text/plain; version=0.0.4')
            self.end_headers()
            uptime = time.time() - metrics.start_time
            prometheus_metrics = f"""# HELP http_requests_total Total HTTP requests
# TYPE http_requests_total counter
http_requests_total{{server="apache",aluno="Hermeson_A",matricula="20239035382"}} {metrics.requests_total}

# HELP http_response_size_bytes Total bytes sent
# TYPE http_response_size_bytes counter
http_response_size_bytes{{server="apache"}} {metrics.bytes_sent}

# HELP http_connections_active Active connections
# TYPE http_connections_active gauge
http_connections_active{{server="apache"}} 1

# HELP process_uptime_seconds Server uptime in seconds
# TYPE process_uptime_seconds counter
process_uptime_seconds{{server="apache"}} {uptime:.2f}

# HELP process_cpu_seconds_total Total user and system CPU time spent in seconds
# TYPE process_cpu_seconds_total counter
process_cpu_seconds_total{{server="apache"}} {resource.getrusage(resource.RUSAGE_SELF).ru_utime + resource.getrusage(resource.RUSAGE_SELF).ru_stime:.2f}

# HELP process_resident_memory_bytes Resident memory size in bytes
# TYPE process_resident_memory_bytes gauge
process_resident_memory_bytes{{server="apache"}} {resource.getrusage(resource.RUSAGE_SELF).ru_maxrss * 1024}

# HELP http_requests_2xx HTTP requests with 2xx status
# TYPE http_requests_2xx counter
http_requests_2xx{{server="apache"}} {metrics.requests_2xx}

# HELP http_requests_4xx HTTP requests with 4xx status
# TYPE http_requests_4xx counter
http_requests_4xx{{server="apache"}} {metrics.requests_4xx}

# HELP http_requests_5xx HTTP requests with 5xx status
# TYPE http_requests_5xx counter
http_requests_5xx{{server="apache"}} {metrics.requests_5xx}

# HELP http_request_duration_seconds Average request duration
# TYPE http_request_duration_seconds gauge
http_request_duration_seconds{{server="apache"}} {metrics.get_avg_response_time():.4f}

# HELP http_requests_per_second Requests per second
# TYPE http_requests_per_second gauge
http_requests_per_second{{server="apache"}} {metrics.requests_total / max(uptime, 0.001):.2f}

# HELP http_bytes_per_second Bytes sent per second
# TYPE http_bytes_per_second gauge
http_bytes_per_second{{server="apache"}} {metrics.bytes_sent / max(uptime, 0.001):.2f}

# HELP apache_busy_workers Number of busy worker processes
# TYPE apache_busy_workers gauge
apache_busy_workers{{server="apache"}} {metrics.busy_workers}

# HELP apache_idle_workers Number of idle worker processes
# TYPE apache_idle_workers gauge
apache_idle_workers{{server="apache"}} {metrics.idle_workers}

# HELP apache_total_workers Total available worker processes
# TYPE apache_total_workers gauge
apache_total_workers{{server="apache"}} 10

# HELP apache_worker_connections Total worker connections handled
# TYPE apache_worker_connections counter
apache_worker_connections{{server="apache"}} {metrics.worker_connections}

# HELP apache_worker_utilization Worker utilization percentage
# TYPE apache_worker_utilization gauge
apache_worker_utilization{{server="apache"}} {(metrics.busy_workers / 10 * 100):.2f}

# HELP http_success_rate HTTP success rate percentage (2xx)
# TYPE http_success_rate gauge
http_success_rate{{server="apache"}} {metrics.get_success_rate():.2f}

# HELP http_error_rate HTTP error rate percentage (4xx + 5xx)
# TYPE http_error_rate gauge
http_error_rate{{server="apache"}} {metrics.get_error_rate():.2f}

# HELP system_cpu_percent_usage Current CPU usage percentage
# TYPE system_cpu_percent_usage gauge
system_cpu_percent_usage{{server="apache"}} {(metrics.get_cpu_usage() % 100):.2f}

# HELP system_memory_usage_bytes Current memory usage in bytes
# TYPE system_memory_usage_bytes gauge
system_memory_usage_bytes{{server="apache"}} {metrics.get_memory_usage()}

# HELP system_memory_usage_percent Memory usage percentage
# TYPE system_memory_usage_percent gauge
system_memory_usage_percent{{server="apache"}} {(metrics.get_memory_usage() / 1073741824 * 100):.2f}
"""
            response_data = prometheus_metrics.encode()
            metrics.add_bytes(len(response_data))
            self.wfile.write(response_data)
            return
        
        # Endpoint de status da API
        if path == '/api/status':
            request_time = time.time() - request_start
            metrics.increment_request(200, path, request_time)
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            response = {
                'status': 'ok',
                'server': 'python-apache',
                'timestamp': datetime.now().isoformat(),
                'x_custom_id': x_custom_id
            }
            response_data = json.dumps(response).encode()
            metrics.add_bytes(len(response_data))
            self.wfile.write(response_data)
            return
        
        # Server status para métricas
        if path == '/server-status':
            request_time = time.time() - request_start
            metrics.increment_request(200, path, request_time)
            self.send_response(200)
            self.send_header('Content-Type', 'text/plain')
            self.end_headers()
            status = f"""Total Accesses: 1
Total kBytes: 1
CPULoad: 0.1
Uptime: 100
ReqPerSec: 0.01
BytesPerSec: 10.24
BytesPerReq: 1024
BusyWorkers: 1
IdleWorkers: 9
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
        
        request_time = time.time() - request_start
        metrics.increment_request(200, path, request_time)
        return super().do_GET()
    
    def log_message(self, format, *args):
        # Log customizado
        pass

def main():
    # Mudar para o diretório com os arquivos HTML
    os.chdir('/app/html')
    
    with socketserver.TCPServer(("", PORT), ApacheHTTPRequestHandler) as httpd:
        print(f"========================================")
        print(f"Servidor Python (Apache) rodando na porta {PORT}")
        print(f"Aluno: Hermeson A.")
        print(f"Matrícula: 20239035382")
        print(f"========================================")
        httpd.serve_forever()

if __name__ == '__main__':
    main()
