# Terceira Avaliação - Redes de Computadores II

## Comparação de Desempenho: Nginx vs Apache

**Aluno:** Hermeson A.  
**Matrícula:** 20239035382  
**X-Custom-ID:** f44d26f3aebff6f058eabbaf85366dfb

---

## 📋 Descrição do Projeto

Este projeto implementa uma análise comparativa de desempenho entre dois servidores web populares (**Nginx** e **Apache**) utilizando contêineres Docker, métricas com **Prometheus** e visualização com **Grafana**.

### Servidores Escolhidos

1. **Nginx** (porta 8080)
   - Justificativa: Conhecido por alta performance em arquivos estáticos e baixo consumo de memória
2. **Apache** (porta 8081)
   - Justificativa: Amplamente usado, robusto e com muitos módulos disponíveis

### Stack de Observabilidade

- **Prometheus**: Coleta de métricas dos servidores
- **Grafana**: Visualização de dados e dashboards
- **Exporters**: nginx-prometheus-exporter e apache-exporter

---

## 🌐 Arquitetura da Rede

**Subrede:** 53.82.0.0/24 (baseada nos últimos 4 dígitos da matrícula: 5382)

| Serviço           | IP         | Porta Externa |
| ----------------- | ---------- | ------------- |
| Nginx             | 53.82.0.10 | 8080          |
| Nginx Exporter    | 53.82.0.11 | -             |
| Apache            | 53.82.0.20 | 8081          |
| Apache Exporter   | 53.82.0.21 | -             |
| Prometheus        | 53.82.0.30 | 9090          |
| Grafana           | 53.82.0.40 | 3000          |
| Cliente de Testes | 53.82.0.50 | -             |

---

## 🚀 Como Executar

### Pré-requisitos

- Docker
- Docker Compose

### 1. Subir a infraestrutura

```bash
# Construir e iniciar todos os containers
docker-compose up -d

# Verificar se todos estão rodando
docker-compose ps
```

### 2. Verificar conectividade

```bash
# Testar Nginx
curl http://localhost:8080/

# Testar Apache
curl http://localhost:8081/

# Acessar Prometheus
# Abrir navegador em http://localhost:9090

# Acessar Grafana
# Abrir navegador em http://localhost:3000
# Usuário: admin, Senha: admin
```

### 3. Executar testes de carga

```bash
# Entrar no container do cliente
docker exec -it load_client sh

# Executar o script de teste
cd /app
python3 load_test.py

# Os resultados serão salvos em /resultados/resultados_testes.txt
```

### 4. Visualizar resultados

```bash
# Ver resultados no host
cat resultados/resultados_testes.txt
```

---

## 📊 Métricas Coletadas

### Métricas de Desempenho

- **Latência (ms)**: Tempo de resposta das requisições
  - Média, Mediana, Desvio Padrão, Mínimo, Máximo
- **Taxa de Sucesso (%)**: Porcentagem de requisições bem-sucedidas
- **Requisições por Segundo**: Throughput do servidor
- **Tamanho de Resposta**: Bytes transferidos

### Métricas de Sistema (via Prometheus)

- **CPU Usage**: Uso de processador
- **Memory Usage**: Uso de memória
- **Network I/O**: Tráfego de rede
- **Active Connections**: Conexões ativas

---

## 🧪 Cenários de Teste

### Teste 1: Arquivo Pequeno - Sequencial

- 50 requisições sequenciais
- Endpoint: `/small.txt` (~60 bytes)

### Teste 2: Arquivo Médio - Sequencial

- 50 requisições sequenciais
- Endpoint: `/medium.txt` (~10 KB)

### Teste 3: Arquivo Grande - Sequencial

- 30 requisições sequenciais
- Endpoint: `/large.txt` (~1 MB)

### Teste 4: Arquivo Pequeno - Concorrente

- 100 requisições com 10 threads concorrentes
- Endpoint: `/small.txt`

### Teste 5: Arquivo Médio - Concorrente

- 100 requisições com 10 threads concorrentes
- Endpoint: `/medium.txt`

### Teste 6: API Status - Alta Concorrência

- 200 requisições com 20 threads concorrentes
- Endpoint: `/api/status` (resposta JSON)

---

## 📈 Como Criar Dashboards no Grafana

1. Acessar http://localhost:3000
2. Login: admin/admin
3. Ir em **Dashboards** → **New** → **New Dashboard**
4. Adicionar painéis com queries Prometheus:

### Exemplos de Queries

```promql
# Taxa de requisições Nginx
rate(nginx_http_requests_total[1m])

# Taxa de requisições Apache
rate(apache_accesses_total[1m])

# Latência P95
histogram_quantile(0.95, rate(http_request_duration_seconds_bucket[5m]))
```

---

## 🔧 Estrutura do Projeto

```
.
├── docker-compose.yml          # Orquestração dos containers
├── config.py                   # Configurações do projeto
├── enunciado.txt              # Enunciado extraído do PDF
├── README.md                  # Este arquivo
├── nginx/
│   ├── nginx.conf             # Configuração do Nginx
│   └── html/                  # Arquivos de teste
│       ├── small.txt
│       ├── medium.txt
│       ├── large.txt
│       └── index.html
├── apache/
│   ├── httpd.conf             # Configuração do Apache
│   └── html/                  # Arquivos de teste
│       ├── small.txt
│       ├── medium.txt
│       ├── large.txt
│       └── index.html
├── prometheus/
│   └── prometheus.yml         # Configuração do Prometheus
├── grafana/
│   └── provisioning/
│       └── datasources/
│           └── prometheus.yml # Datasource Prometheus
├── client/
│   ├── dockerfile             # Imagem do cliente
│   └── load_test.py          # Script Python de testes
└── resultados/
    └── resultados_testes.txt # Resultados dos testes
```

---

## 📝 Cabeçalho HTTP Personalizado

Todas as requisições incluem o header:

```
X-Custom-ID: f44d26f3aebff6f058eabbaf85366dfb
```

Calculado como: `MD5("20239035382 Hermeson A.")`

---

## 🛠️ Comandos Úteis

```bash
# Ver logs dos containers
docker-compose logs -f nginx
docker-compose logs -f apache

# Reiniciar um serviço
docker-compose restart nginx

# Parar tudo
docker-compose down

# Parar e remover volumes
docker-compose down -v

# Rebuild de um serviço
docker-compose up -d --build load_client
```

---

## 📦 Dependências Python

O script de teste usa apenas bibliotecas padrão do Python 3:

- `http.client` - Requisições HTTP
- `hashlib` - Hash MD5
- `statistics` - Cálculos estatísticos
- `concurrent.futures` - Testes concorrentes

---

## 🎯 Resultados Esperados

Ao final dos testes, você terá:

1. ✅ Arquivo `resultados/resultados_testes.txt` com estatísticas completas
2. ✅ Métricas coletadas no Prometheus
3. ✅ Dashboards no Grafana mostrando comparações
4. ✅ Análise de qual servidor teve melhor desempenho em cada cenário

---

## 📧 Contato

**Hermeson A.**  
Matrícula: 20239035382  
Curso: Sistemas de Informação - UFPI

---

## 📄 Licença

Projeto acadêmico para a disciplina de Redes de Computadores II.
