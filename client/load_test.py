#!/usr/bin/env python3
"""
Testes de Carga HTTP
Aluno: Hermeson A. | Matrícula: 20239035382
"""
import http.client
import hashlib
import time
import statistics
import json
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import List, Dict, Tuple

# Configurações
MATRICULA = "20239035382"
NOME = "Hermeson A."
ALUNO_INFO = f"{MATRICULA} {NOME}"
X_CUSTOM_ID = hashlib.md5(ALUNO_INFO.encode()).hexdigest()

# Servidores
SERVERS = {
    'nginx': ('53.82.0.10', 80),
    'apache': ('53.82.0.20', 80)
}

# Endpoints de teste
ENDPOINTS = [
    '/small.txt',
    '/medium.txt',
    '/large.txt',
    '/api/status',
    '/'
]

class LoadTester:
    def __init__(self, server_name: str, host: str, port: int):
        self.server_name = server_name
        self.host = host
        self.port = port
        self.results = []
    
    def make_request(self, endpoint: str) -> Dict:
        """Faz uma requisição HTTP e retorna métricas"""
        start_time = time.time()
        
        try:
            conn = http.client.HTTPConnection(self.host, self.port, timeout=10)
            headers = {
                'X-Custom-ID': X_CUSTOM_ID,
                'User-Agent': f'LoadTester-{MATRICULA}'
            }
            
            conn.request('GET', endpoint, headers=headers)
            response = conn.getresponse()
            data = response.read()
            
            end_time = time.time()
            latency = (end_time - start_time) * 1000  # em ms
            
            result = {
                'endpoint': endpoint,
                'status_code': response.status,
                'latency_ms': latency,
                'response_size': len(data),
                'success': 200 <= response.status < 300,
                'timestamp': datetime.now().isoformat()
            }
            
            conn.close()
            return result
            
        except Exception as e:
            end_time = time.time()
            return {
                'endpoint': endpoint,
                'status_code': 0,
                'latency_ms': (end_time - start_time) * 1000,
                'response_size': 0,
                'success': False,
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            }
    
    def run_sequential_test(self, endpoint: str, num_requests: int) -> List[Dict]:
        """Executa teste sequencial"""
        print(f"  [{self.server_name}] Teste sequencial: {num_requests} requisições para {endpoint}")
        results = []
        
        for i in range(num_requests):
            result = self.make_request(endpoint)
            results.append(result)
            
            if (i + 1) % 10 == 0:
                print(f"    Progresso: {i + 1}/{num_requests}")
        
        return results
    
    def run_concurrent_test(self, endpoint: str, num_requests: int, concurrency: int) -> List[Dict]:
        """Executa teste concorrente"""
        print(f"  [{self.server_name}] Teste concorrente: {num_requests} requisições, {concurrency} threads para {endpoint}")
        results = []
        
        with ThreadPoolExecutor(max_workers=concurrency) as executor:
            futures = [executor.submit(self.make_request, endpoint) for _ in range(num_requests)]
            
            completed = 0
            for future in as_completed(futures):
                result = future.result()
                results.append(result)
                completed += 1
                
                if completed % 10 == 0:
                    print(f"    Progresso: {completed}/{num_requests}")
        
        return results
    
    def calculate_statistics(self, results: List[Dict]) -> Dict:
        """Calcula estatísticas dos resultados"""
        if not results:
            return {}
        
        successful = [r for r in results if r['success']]
        failed = [r for r in results if not r['success']]
        
        latencies = [r['latency_ms'] for r in successful]
        
        if not latencies:
            return {
                'total_requests': len(results),
                'successful': 0,
                'failed': len(failed),
                'success_rate': 0.0
            }
        
        return {
            'total_requests': len(results),
            'successful': len(successful),
            'failed': len(failed),
            'success_rate': (len(successful) / len(results)) * 100,
            'latency_mean_ms': statistics.mean(latencies),
            'latency_median_ms': statistics.median(latencies),
            'latency_stdev_ms': statistics.stdev(latencies) if len(latencies) > 1 else 0,
            'latency_min_ms': min(latencies),
            'latency_max_ms': max(latencies),
            'total_response_size': sum(r['response_size'] for r in successful)
        }

def format_results_to_txt(test_name: str, server_results: Dict[str, Dict]) -> str:
    """Formata resultados para arquivo TXT"""
    lines = []
    lines.append("=" * 80)
    lines.append(f"TESTE: {test_name}")
    lines.append(f"Data/Hora: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    lines.append(f"Aluno: {NOME}")
    lines.append(f"Matrícula: {MATRICULA}")
    lines.append(f"X-Custom-ID: {X_CUSTOM_ID}")
    lines.append("=" * 80)
    lines.append("")
    
    for server_name, stats in server_results.items():
        lines.append(f"--- Servidor: {server_name.upper()} ---")
        lines.append(f"Total de requisições: {stats['total_requests']}")
        lines.append(f"Requisições bem-sucedidas: {stats['successful']}")
        lines.append(f"Requisições falhadas: {stats['failed']}")
        lines.append(f"Taxa de sucesso: {stats['success_rate']:.2f}%")
        
        if stats['successful'] > 0:
            lines.append(f"Latência média: {stats['latency_mean_ms']:.2f} ms")
            lines.append(f"Latência mediana: {stats['latency_median_ms']:.2f} ms")
            lines.append(f"Desvio padrão: {stats['latency_stdev_ms']:.2f} ms")
            lines.append(f"Latência mínima: {stats['latency_min_ms']:.2f} ms")
            lines.append(f"Latência máxima: {stats['latency_max_ms']:.2f} ms")
            lines.append(f"Tamanho total de resposta: {stats['total_response_size']} bytes")
        
        lines.append("")
    
    lines.append("=" * 80)
    lines.append("")
    
    return "\n".join(lines)

def main():
    print(f"=== TESTE DE CARGA DE SERVIDORES WEB ===")
    print(f"Aluno: {NOME}")
    print(f"Matrícula: {MATRICULA}")
    print(f"X-Custom-ID: {X_CUSTOM_ID}")
    print("=" * 80)
    
    # Arquivo de resultados
    output_file = "/resultados/resultados_testes.txt"
    
    # Limpar arquivo
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("")
    
    # Cenários de teste
    test_scenarios = [
        {
            'name': 'Teste 1: Arquivo Pequeno - 50 requisições sequenciais',
            'endpoint': '/small.txt',
            'num_requests': 50,
            'concurrent': False
        },
        {
            'name': 'Teste 2: Arquivo Médio - 50 requisições sequenciais',
            'endpoint': '/medium.txt',
            'num_requests': 50,
            'concurrent': False
        },
        {
            'name': 'Teste 3: Arquivo Grande - 30 requisições sequenciais',
            'endpoint': '/large.txt',
            'num_requests': 30,
            'concurrent': False
        },
        {
            'name': 'Teste 4: Arquivo Pequeno - 100 requisições concorrentes (10 threads)',
            'endpoint': '/small.txt',
            'num_requests': 100,
            'concurrent': True,
            'concurrency': 10
        },
        {
            'name': 'Teste 5: Arquivo Médio - 100 requisições concorrentes (10 threads)',
            'endpoint': '/medium.txt',
            'num_requests': 100,
            'concurrent': True,
            'concurrency': 10
        },
        {
            'name': 'Teste 6: Arquivo Grande - 50 requisições concorrentes (10 threads)',
            'endpoint': '/large.txt',
            'num_requests': 50,
            'concurrent': True,
            'concurrency': 10
        },
        {
            'name': 'Teste 7: Arquivo Extra Grande (10MB) - 20 requisições sequenciais',
            'endpoint': '/xlarge.txt',
            'num_requests': 20,
            'concurrent': False,
            'concurrency': 1
        },
        {
            'name': 'Teste 8: Arquivo Extra Grande (10MB) - 30 requisições concorrentes (5 threads)',
            'endpoint': '/xlarge.txt',
            'num_requests': 30,
            'concurrent': True,
            'concurrency': 5
        },
        {
            'name': 'Teste 9: Arquivo XXL (50MB) - 10 requisições sequenciais',
            'endpoint': '/xxlarge.txt',
            'num_requests': 10,
            'concurrent': False,
            'concurrency': 1
        },
        {
            'name': 'Teste 10: API Status - 200 requisições concorrentes (20 threads)',
            'endpoint': '/api/status',
            'num_requests': 200,
            'concurrent': True,
            'concurrency': 20
        }
    ]
    
    # Executar testes
    for scenario in test_scenarios:
        print(f"\n{scenario['name']}")
        print("-" * 80)
        
        server_results = {}
        
        for server_name, (host, port) in SERVERS.items():
            tester = LoadTester(server_name, host, port)
            
            if scenario['concurrent']:
                results = tester.run_concurrent_test(
                    scenario['endpoint'],
                    scenario['num_requests'],
                    scenario['concurrency']
                )
            else:
                results = tester.run_sequential_test(
                    scenario['endpoint'],
                    scenario['num_requests']
                )
            
            stats = tester.calculate_statistics(results)
            server_results[server_name] = stats
        
        # Salvar resultados
        formatted_results = format_results_to_txt(scenario['name'], server_results)
        with open(output_file, 'a', encoding='utf-8') as f:
            f.write(formatted_results)
        
        print(f"Resultados salvos em {output_file}")
    
    print("\n" + "=" * 80)
    print("TODOS OS TESTES CONCLUÍDOS!")
    print(f"Resultados completos em: {output_file}")

if __name__ == '__main__':
    main()
