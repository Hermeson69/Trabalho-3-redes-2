# 🚀 INÍCIO RÁPIDO

**Aluno:** Hermeson A.  
**Matrícula:** 20239035382

## Comandos principais

```bash
# 1. Iniciar tudo
docker-compose up -d

# 2. Verificar containers
docker-compose ps

# 3. Executar testes
docker exec load_client python3 /app/load_test.py

# 4. Ver resultados
cat resultados/resultados_testes.txt

# 5. Parar tudo
docker-compose down
```

## Acessos

- **Nginx:** http://localhost:8080
- **Apache:** http://localhost:8081
- **Prometheus:** http://localhost:9090
- **Grafana:** http://localhost:3000 (admin/admin)

## Estrutura de rede

- Subrede: **53.82.0.0/24**
- Nginx: 53.82.0.10
- Apache: 53.82.0.20
- Prometheus: 53.82.0.30
- Grafana: 53.82.0.40

## X-Custom-ID

```
f44d26f3aebff6f058eabbaf85366dfb
```

Calculado como: `MD5("20239035382 Hermeson A.")`

## Arquivos importantes

- `docker-compose.yml` - Infraestrutura completa
- `client/load_test.py` - Script de testes Python
- `resultados/resultados_testes.txt` - Resultados detalhados
- `resultados/resumo_executivo.txt` - Análise completa
- `README.md` - Documentação completa

## Tecnologias usadas

✅ Docker + Docker Compose  
✅ Nginx (servidor web 1)  
✅ Apache (servidor web 2)  
✅ Prometheus (coleta de métricas)  
✅ Grafana (visualização)  
✅ Python 3 (testes de carga)  
✅ HTTP com X-Custom-ID header

---

**Trabalho desenvolvido sem instalação de pacotes Python extras.**  
**Usa apenas bibliotecas padrão do Python 3.** ✨
