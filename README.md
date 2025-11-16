# Comparação de Desempenho: Nginx vs Apache

**Aluno:** Hermeson A. | **Matrícula:** 20239035382  
**X-Custom-ID:** f44d26f3aebff6f058eabbaf85366dfb

## Descrição

Análise comparativa de desempenho entre servidores web Nginx e Apache usando Python HTTP servers, Docker, Prometheus e Grafana. Implementação 100% Python (sem shell scripts).

## Arquitetura

**Subrede:** 53.82.0.0/24

| Serviço    | IP         | Porta | Acesso                |
| ---------- | ---------- | ----- | --------------------- |
| Nginx      | 53.82.0.10 | 8080  | http://localhost:8080 |
| Apache     | 53.82.0.20 | 8081  | http://localhost:8081 |
| Prometheus | 53.82.0.30 | 9090  | http://localhost:9090 |
| Grafana    | 53.82.0.40 | 3000  | http://localhost:3000 |

## Como Executar

### Execução Automática (Recomendado)

```bash
python3 main.py
```

Executa tudo automaticamente:

- Build e start dos containers
- 10 cenários de teste (740 requisições)
- Análise comparativa
- 8 gráficos (5 barras + 3 linhas)
- Cleanup ao final

### Execução Manual

```bash
# Subir containers
docker-compose up -d

# Executar testes
docker exec load_client python3 /app/load_test.py

# Gerar análise
docker exec load_client python3 /app/analise_resultados.py

# Gerar gráficos
docker exec load_client python3 /app/gerar_graficos.py

# Parar containers
docker-compose down -v
```

## Cenários de Teste

| #   | Descrição                      | Requisições | Threads | Arquivo            |
| --- | ------------------------------ | ----------- | ------- | ------------------ |
| 1   | Pequeno - Sequencial           | 50          | 1       | small.txt (60B)    |
| 2   | Médio - Sequencial             | 50          | 1       | medium.txt (10KB)  |
| 3   | Grande - Sequencial            | 30          | 1       | large.txt (1MB)    |
| 4   | Pequeno - Concorrente          | 100         | 10      | small.txt          |
| 5   | Médio - Concorrente            | 100         | 10      | medium.txt         |
| 6   | Grande - Concorrente           | 50          | 10      | large.txt          |
| 7   | Extra Grande - Sequencial      | 20          | 1       | xlarge.txt (10MB)  |
| 8   | Extra Grande - Concorrente     | 30          | 5       | xlarge.txt         |
| 9   | XXL - Sequencial               | 10          | 1       | xxlarge.txt (50MB) |
| 10  | API Status - Alta Concorrência | 200         | 20      | /api/status        |

**Total:** 740 requisições

## Métricas Analisadas

- Latência (média, mediana, mín, máx)
- Desvio padrão
- Taxa de sucesso
- Throughput
- Tamanho de resposta

## Resultados

Os resultados são salvos em `resultados/`:

```
resultados/
├── resultados_testes.txt      # Dados brutos dos testes
├── analise_comparativa.txt    # Tabelas comparativas
├── comparacao_servidores.txt  # Resumo executivo
└── graficos/                  # 8 gráficos PNG (300 DPI)
    ├── latencia_media.png
    ├── desvio_padrao.png
    ├── latencia_min_max.png
    ├── placar_vencedores.png
    ├── comparativo_geral.png
    ├── linhas_evolucao_latencia.png
    ├── linhas_min_max.png
    └── linhas_desvio_area.png
```

## Estrutura do Projeto

```
.
├── main.py                    # Gerenciador principal Python
├── docker-compose.yml         # Orquestração Docker
├── config.py                  # Configurações
├── server/
│   ├── nginx_server.py        # Servidor Python (Nginx)
│   ├── apache_server.py       # Servidor Python (Apache)
│   ├── Dockerfile.nginx
│   ├── Dockerfile.apache
│   ├── html-nginx/            # Arquivos de teste
│   └── html-apache/           # Arquivos de teste
├── client/
│   ├── load_test.py           # Testes de carga
│   ├── analise_resultados.py  # Análise estatística
│   ├── gerar_graficos.py      # Geração de gráficos
│   └── dockerfile
├── prometheus/
│   └── prometheus.yml
├── grafana/
│   └── provisioning/
└── resultados/                # Resultados e gráficos
```

## Tecnologias

**Python:** http.server, socketserver, http.client, concurrent.futures, statistics, matplotlib, numpy  
**Docker:** Containers Alpine Linux 3.11  
**Observabilidade:** Prometheus, Grafana  
**Rede:** Subrede customizada (53.82.0.0/24)

## Dependências

- Docker + Docker Compose
- Python 3.11+
- matplotlib e numpy (instalados automaticamente no container)

## Serviços Disponíveis

Após executar `python3 main.py`:

- **Nginx:** http://localhost:8080
- **Apache:** http://localhost:8081
- **Prometheus:** http://localhost:9090
- **Grafana:** http://localhost:3000 (admin/admin)

Pressione `Ctrl+C` para parar tudo e fazer cleanup automático.

## Observabilidade: Prometheus & Grafana

### Prometheus

**URL:** http://localhost:9090

Acesse **Status → Targets** para verificar se os servidores estão sendo monitorados (devem aparecer: prometheus, nginx_server, apache_server).

### Grafana

**URL:** http://localhost:3000  
**Login:** admin / admin

Crie dashboards usando o Prometheus como data source. Queries disponíveis em: [`QUERIES_PROMETHEUS.txt`](QUERIES_PROMETHEUS.txt)

---

**Disciplina:** Redes de Computadores II | **Curso:** Sistemas de Informação - UFPI
