# 🚀 Como Executar o Projeto

**Trabalho 3 - Redes de Computadores II**  
**Aluno:** Hermeson A. | **Matrícula:** 20239035382

---

## ⚡ Execução com um único comando!

Todo o projeto agora é gerenciado pelo script Python `main.py`:

```bash
python3 main.py
```

**Ou:**

```bash
./main.py
```

---

## 🎯 O que o script faz automaticamente:

1. ✅ **Verifica** se o Docker está instalado
2. ✅ **Constrói** as imagens Docker dos servidores Python
3. ✅ **Sobe** todos os containers (nginx, apache, prometheus, grafana, cliente)
4. ✅ **Aguarda** os servidores ficarem prontos
5. ✅ **Executa** os testes de carga (630 requisições)
6. ✅ **Gera** análises comparativas
7. ✅ **Mostra** os resultados
8. ✅ **Mantém** os containers rodando
9. ✅ **Ao sair (Ctrl+C)**: Derruba TUDO automaticamente
   - Para containers
   - Remove volumes
   - Remove redes Docker

---

## 📊 Durante a execução você verá:

```
================================================================================
TRABALHO 3 - REDES DE COMPUTADORES II
================================================================================
Aluno: Hermeson A.
Matrícula: 20239035382
X-Custom-ID: f44d26f3aebff6f058eabbaf85366dfb
Subrede: 53.82.0.0/24
================================================================================

[1/7] Verificando Docker...
✓ Docker encontrado: Docker version 24.0.7

[2/7] Construindo e subindo containers...
✓ Construindo e iniciando containers concluído

[3/7] Aguardando servidores ficarem prontos...
  Aguardando Nginx Python (53.82.0.10)...
  ✓ Nginx Python pronto!
  Aguardando Apache Python (53.82.0.20)...
  ✓ Apache Python pronto!

[4/7] Status dos containers:
✓ Listando containers concluído

[5/7] Executando testes de carga...
Isso pode levar alguns minutos. Aguarde...

=== TESTE DE CARGA DE SERVIDORES WEB ===
[...saída dos testes...]
✓ Testes concluídos com sucesso!

[6/7] Resumo dos resultados:
✓ Resultados salvos em: resultados/resultados_testes.txt

  📊 Total de testes executados: 6
  ✓ Taxa de sucesso: 100%

[7/7] Gerando análise comparativa...
✓ Análise gerada com sucesso!

================================================================================
SERVIÇOS DISPONÍVEIS:
================================================================================
✓ Nginx Python:    http://localhost:8080
✓ Apache Python:   http://localhost:8081
✓ Prometheus:      http://localhost:9090
✓ Grafana:         http://localhost:3000 (admin/admin)
================================================================================

Pressione Ctrl+C para parar os containers e limpar tudo

Containers rodando. Pressione Ctrl+C para parar...
```

---

## ⏹️ Para Parar:

Simplesmente pressione **Ctrl+C** no terminal onde o script está rodando.

O script automaticamente:

- ✅ Para todos os containers
- ✅ Remove os containers
- ✅ Remove os volumes
- ✅ Remove as redes Docker

---

## 📁 Resultados Gerados:

Após a execução, você terá os seguintes arquivos em `resultados/`:

- **resultados_testes.txt** - Dados brutos de todos os testes
- **resumo_executivo.txt** - Análise executiva completa
- **comparacao_servidores.txt** - Comparação detalhada Nginx vs Apache
- **analise_comparativa.txt** - Análise automática gerada

---

## 🐍 Código 100% Python

O script `main.py` usa **APENAS** a biblioteca padrão do Python:

```python
import subprocess  # Para executar comandos Docker
import time        # Para aguardar servidores
import sys         # Para exit codes
import signal      # Para capturar Ctrl+C
import os          # Para operações de sistema
from pathlib import Path  # Para caminhos de arquivos
```

**Nenhuma dependência externa!** 🎉

---

## 🔧 Requisitos:

- ✅ Python 3.6+ (já instalado na maioria dos sistemas)
- ✅ Docker e Docker Compose instalados
- ✅ Permissões para executar Docker

---

## 🎯 Exemplo de Uso Completo:

```bash
# 1. Navegar até a pasta do projeto
cd /home/hermeson/Federal/Trabalho-3-redes-2

# 2. Executar o script
python3 main.py

# 3. Aguardar a execução automática
# (O script faz tudo sozinho!)

# 4. Acessar os serviços (em outro terminal ou navegador)
curl http://localhost:8080  # Nginx Python
curl http://localhost:8081  # Apache Python
firefox http://localhost:3000  # Grafana

# 5. Quando terminar, pressionar Ctrl+C
# (O script limpa tudo automaticamente!)
```

---

## 📊 Ver Resultados Depois:

Se você quiser ver os resultados depois de parar o script:

```bash
# Ver resultados completos
cat resultados/resultados_testes.txt

# Ver análise comparativa
cat resultados/analise_comparativa.txt

# Ver comparação detalhada
cat resultados/comparacao_servidores.txt

# Ver resumo executivo
cat resultados/resumo_executivo.txt
```

---

## 🐛 Troubleshooting:

### Erro: "Docker não encontrado"

```bash
# Instalar Docker primeiro
sudo apt-get update
sudo apt-get install docker.io docker-compose
```

### Erro: "Permission denied"

```bash
# Adicionar usuário ao grupo docker
sudo usermod -aG docker $USER
# Fazer logout/login ou:
newgrp docker
```

### Porta já em uso

```bash
# Parar containers antigos
docker compose down
# Ou ver o que está usando a porta
sudo lsof -i :8080
```

---

## ✨ Vantagens desta Abordagem:

✅ **Um único comando** para rodar tudo  
✅ **Limpeza automática** ao sair  
✅ **Sem scripts shell** - apenas Python  
✅ **Cores no terminal** para melhor visualização  
✅ **Tratamento de erros** robusto  
✅ **Feedback contínuo** do progresso  
✅ **Captura Ctrl+C** graciosamente

---

## 🎓 Para Apresentação/Demonstração:

```bash
# Simplesmente execute:
python3 main.py

# O script irá:
# - Construir tudo do zero
# - Executar todos os testes
# - Gerar todas as análises
# - Mostrar os resultados
# - Manter os serviços rodando para demonstração

# Quando terminar:
# Ctrl+C → Limpa tudo automaticamente
```

---

## 📝 Nota Importante:

**TODOS os scripts shell (run.sh, status.sh) foram substituídos por este único script Python!**

Agora você só precisa de:

- ✅ `python3 main.py` - Para TUDO!

---

**Desenvolvido por:** Hermeson A.  
**Matrícula:** 20239035382  
**Data:** 12 de novembro de 2025
