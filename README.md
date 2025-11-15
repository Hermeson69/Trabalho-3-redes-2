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

### Prometheus (Métricas)

**URL:** http://localhost:9090

**⚠️ IMPORTANTE: Verificar Targets primeiro!**

1. Acesse http://localhost:9090
2. Clique em **Status → Targets**
3. Devem aparecer 3 endpoints:
   - ✅ `prometheus` (localhost:9090) - UP
   - ✅ `nginx_server` (53.82.0.10:80) - UP
   - ✅ `apache_server` (53.82.0.20:80) - UP

**Se nginx_server ou apache_server estiverem DOWN:**

- Execute os testes: `python3 main.py` (os servidores precisam estar rodando)
- Verifique os logs: `docker logs nginx_server` ou `docker logs apache_server`
- Teste manualmente: `curl http://localhost:8080/metrics` e `curl http://localhost:8081/metrics`

**Testar queries no Prometheus:**

1. Acesse http://localhost:9090
2. Clique na aba **Graph**
3. **⚠️ COPIE AS QUERIES DO ARQUIVO `QUERIES_PROMETHEUS.txt` (não daqui!)**
4. Cole no campo de query e clique **Execute**

Queries disponíveis em: [`QUERIES_PROMETHEUS.txt`](QUERIES_PROMETHEUS.txt)

```promql
# Veja exemplos:
http_requests_total{server="nginx"}
rate(http_requests_total[1m])
process_uptime_seconds
```

**Se as queries não retornarem dados:**

- Execute os testes para gerar requisições
- Aguarde 5-10 segundos para o Prometheus coletar
- As métricas só aparecem APÓS as requisições serem feitas

### Grafana (Dashboards)

**URL:** http://localhost:3000  
**Login:** admin / admin

**Passo a passo completo:**

1. **Login**

   - Acesse http://localhost:3000
   - Usuário: `admin` / Senha: `admin`
   - (Pode pular a troca de senha)

2. **Verificar Data Source**

   - Menu lateral (☰) → Connections → Data sources
   - Deve ter "Prometheus" listado
   - Clique em "Prometheus" → Test (deve mostrar "Data source is working")

3. **Criar Dashboard**

   - Menu lateral (☰) → Dashboards → New → New Dashboard
   - Clique em **+ Add visualization**
   - Selecione **Prometheus**

4. **Adicionar Painel com Query**

   - **⚠️ COPIE A QUERY DO ARQUIVO `QUERIES_PROMETHEUS.txt`**
   - No campo de query (parte inferior), cole:
     ```
     http_requests_total
     ```
   - Clique em **Run queries** (canto superior direito)
   - Deve mostrar 2 linhas: uma para nginx, outra para apache

5. **Configurar Visualização**

   - No painel direito, em **Legend**, adicione: `{{server}}`
   - Em **Panel options → Title**, coloque: "Requisições por Segundo"
   - Clique **Apply** (canto superior direito)

6. **Adicionar mais painéis**

   - Clique **Add** (canto superior direito) → Visualization
   - Repita o processo com outras queries

7. **Salvar Dashboard**
   - Clique no ícone de disquete (Save) no topo
   - Nome: "Comparação Nginx vs Apache"
   - Clique **Save**

**Painéis recomendados:**

> **💡 IMPORTANTE:** Copie as queries do arquivo [`QUERIES_PROMETHEUS.txt`](QUERIES_PROMETHEUS.txt) para evitar erro de aspas!

**Painel 1 - Taxa de Requisições (Time Series)**

- Query: `rate(http_requests_total[1m])`
- Mostra req/s de ambos servidores em tempo real

**Painel 2 - Total de Requisições (Stat)**

- Copie do QUERIES_PROMETHEUS.txt:
  - Query A: `http_requests_total{server="nginx"}`
  - Query B: `http_requests_total{server="apache"}`
- Mostra contadores lado a lado

**Painel 3 - Uptime (Gauge)**

- Query: `process_uptime_seconds`
- Tempo online dos servidores

**Painel 4 - Throughput (Time Series)**

- Query: `rate(http_response_size_bytes[5m])`
- Bytes/segundo transferidos

**Dicas:**

- Ajuste **Time Range** (canto superior direito): últimos 5m, 15m, 1h
- Ative **Auto-refresh** para atualização automática (5s recomendado)
- Use `{{server}}` na Legend para mostrar nome do servidor
- Execute os testes novamente para gerar mais dados

## Troubleshooting

### Grafana só mostra métricas do Prometheus, não do Nginx/Apache

**Causa:** Os servidores não estão expondo métricas ou o Prometheus não está coletando.

**Solução:**

1. **Verificar se os servidores estão rodando:**

   ```bash
   docker ps
   # Deve mostrar: nginx_server e apache_server rodando
   ```

2. **Testar endpoints de métricas manualmente:**

   ```bash
   curl http://localhost:8080/metrics
   curl http://localhost:8081/metrics
   # Devem retornar métricas em formato Prometheus
   ```

3. **Verificar targets no Prometheus:**

   - Acesse http://localhost:9090/targets
   - `nginx_server` e `apache_server` devem estar **UP** (verde)
   - Se estiverem DOWN (vermelho), veja os erros

4. **Gerar dados executando testes:**

   ```bash
   python3 main.py
   # Os testes vão gerar requisições e criar métricas
   ```

5. **Aguardar coleta do Prometheus:**

   - Prometheus coleta a cada 5 segundos (configurado em `scrape_interval`)
   - Aguarde 10-15 segundos após os testes

6. **Testar query no Prometheus antes do Grafana:**
   ```promql
   http_requests_total
   ```
   - Se funcionar no Prometheus mas não no Grafana, recarregue a página do Grafana

### Targets DOWN no Prometheus

**Se nginx_server ou apache_server aparecem DOWN:**

```bash
# Ver logs do servidor
docker logs nginx_server
docker logs apache_server

# Reiniciar containers
docker restart nginx_server apache_server

# Verificar rede
docker network inspect trabalho-3-redes-2_rede_customizada
```

### No data no Grafana

**Se aparecer erro de sintaxe com aspas:**

1. **NÃO copie do README** - use o arquivo [`QUERIES_PROMETHEUS.txt`](QUERIES_PROMETHEUS.txt)
2. **OU digite manualmente** usando aspas retas (Shift + ')
3. Exemplo correto: `http_requests_total{server="nginx"}`

**Se não houver dados:**

1. Verifique Time Range (canto superior direito) - use "Last 5 minutes"
2. Clique em "Run queries" novamente
3. Execute os testes para gerar dados novos: `python3 main.py`
4. Verifique se o Data Source está configurado (Connections → Data sources → Prometheus)

---

**Disciplina:** Redes de Computadores II | **Curso:** Sistemas de Informação - UFPI
