# 📊 Gráficos de Análise de Performance

**Trabalho 3 - Redes de Computadores II**  
**Aluno:** Hermeson A. | **Matrícula:** 20239035382

---

## 📈 Gráficos Gerados Automaticamente

O script `main.py` gera automaticamente **5 gráficos profissionais** em PNG (300 DPI) comparando o desempenho dos servidores Nginx Python e Apache Python.

Todos os gráficos são salvos em: `resultados/graficos/`

---

## 🎨 Tipos de Gráficos

### 1. **latencia_media.png** - Comparação de Latência Média

**Descrição:** Gráfico de barras comparando a latência média de cada servidor em todos os cenários de teste.

**Informações mostradas:**

- Latência média em milissegundos (ms)
- 6 cenários de teste diferentes
- Comparação lado a lado Nginx vs Apache
- Valores exatos no topo de cada barra

**Cores:**

- 🟢 Verde: Nginx Python
- 🔴 Vermelho: Apache Python

**Interpretação:**

- Barras mais baixas = melhor performance
- Compare visualmente qual servidor foi mais rápido em cada cenário

---

### 2. **desvio_padrao.png** - Análise de Consistência

**Descrição:** Gráfico mostrando o desvio padrão (consistência) das latências.

**Informações mostradas:**

- Desvio padrão em milissegundos (ms)
- Quanto menor, mais consistente é o servidor
- Comparação lado a lado de todos os cenários

**Interpretação:**

- Desvio baixo = servidor consistente e previsível
- Desvio alto = servidor com performance variável
- Importante para aplicações que precisam de latência estável

---

### 3. **latencia_min_max.png** - Latências Extremas

**Descrição:** Dois gráficos lado a lado mostrando latências mínima e máxima.

**Painel Esquerdo:** Nginx Python

- 🟢 Verde: Latência mínima
- 🔴 Vermelho: Latência máxima

**Painel Direito:** Apache Python

- 🟢 Verde: Latência mínima
- 🔴 Vermelho: Latência máxima

**Interpretação:**

- Latência mínima: melhor caso possível
- Latência máxima: pior caso observado
- Diferença entre min/max indica variabilidade

---

### 4. **placar_vencedores.png** - Placar de Vitórias

**Descrição:** Dois gráficos mostrando quem venceu mais testes.

**Painel Esquerdo:** Gráfico de pizza

- Distribuição percentual de vitórias
- 🟢 Verde: Nginx Python
- 🔴 Vermelho: Apache Python
- 🟠 Laranja: Empates

**Painel Direito:** Gráfico de barras

- Número absoluto de vitórias
- Comparação direta

**Critério de Vitória:**

- Servidor com menor latência média no cenário
- Empate se diferença < 0.5ms

---

### 5. **comparativo_geral.png** - Média Geral de Métricas

**Descrição:** Gráfico comparando a média de todas as métricas através de todos os testes.

**Métricas Comparadas:**

- Latência Média
- Latência Mediana
- Desvio Padrão

**Informações mostradas:**

- Média de cada métrica considerando todos os 6 testes
- Comparação lado a lado
- Valores exatos

**Interpretação:**

- Visão geral do desempenho de cada servidor
- Qual servidor é melhor "em média"

---

## 🛠️ Tecnologias Utilizadas

### Matplotlib

- Biblioteca Python para visualização de dados
- Gráficos profissionais e publicáveis
- Formato PNG em alta resolução (300 DPI)

### NumPy

- Computação numérica
- Operações em arrays
- Cálculos estatísticos

---

## 📂 Estrutura de Arquivos

```
resultados/
├── graficos/                      # Pasta de gráficos
│   ├── latencia_media.png        # ~200 KB
│   ├── desvio_padrao.png         # ~200 KB
│   ├── latencia_min_max.png      # ~300 KB (2 gráficos)
│   ├── placar_vencedores.png     # ~250 KB (2 gráficos)
│   └── comparativo_geral.png     # ~150 KB
│
├── resultados_testes.txt         # Dados brutos
├── analise_comparativa.txt       # Análise textual
├── comparacao_servidores.txt     # Comparação detalhada
└── resumo_executivo.txt          # Resumo executivo
```

---

## 🚀 Como Visualizar os Gráficos

### No Linux:

```bash
# Abrir todos os gráficos
eog resultados/graficos/*.png

# Abrir gráfico específico
xdg-open resultados/graficos/latencia_media.png

# Usando visualizador de imagens
firefox resultados/graficos/placar_vencedores.png
gwenview resultados/graficos/
```

### No macOS:

```bash
# Abrir todos os gráficos
open resultados/graficos/*.png

# Abrir gráfico específico
open resultados/graficos/latencia_media.png
```

### No Windows:

```bash
# Abrir no explorador
explorer resultados\graficos

# Ou copiar para sua máquina
docker cp load_client:/resultados/graficos ./graficos_backup
```

---

## 🎨 Personalização

O arquivo `client/gerar_graficos.py` contém todo o código de geração dos gráficos.

Você pode personalizar:

- **Cores:** Alterar `color='#00A86B'` para suas cores preferidas
- **Tamanho:** Modificar `figsize=(14, 8)`
- **Resolução:** Alterar `dpi=300` para maior/menor resolução
- **Tipo de gráfico:** Trocar `bar()` por `plot()`, `scatter()`, etc.
- **Título/Labels:** Editar os textos dos títulos e eixos

---

## 📊 Exemplo de Código

```python
# Gerar gráfico de barras comparativo
import matplotlib.pyplot as plt
import numpy as np

nomes = ['Teste 1', 'Teste 2', 'Teste 3']
nginx = [10.5, 15.2, 12.8]
apache = [9.8, 16.1, 11.5]

x = np.arange(len(nomes))
width = 0.35

fig, ax = plt.subplots(figsize=(12, 8))
ax.bar(x - width/2, nginx, width, label='Nginx', color='#00A86B')
ax.bar(x + width/2, apache, width, label='Apache', color='#D2042D')

ax.set_xlabel('Testes')
ax.set_ylabel('Latência (ms)')
ax.set_title('Comparação de Performance')
ax.set_xticks(x)
ax.set_xticklabels(nomes)
ax.legend()

plt.savefig('meu_grafico.png', dpi=300)
```

---

## 📈 Métricas Visualizadas

### Latência Média

- Tempo médio de resposta
- Métrica principal de performance
- **Menor é melhor**

### Latência Mediana

- Valor central das latências
- Menos afetada por outliers
- **Menor é melhor**

### Desvio Padrão

- Variabilidade das latências
- Indica consistência
- **Menor é melhor** (mais consistente)

### Latência Mínima

- Melhor tempo observado
- Potencial máximo do servidor
- **Menor é melhor**

### Latência Máxima

- Pior tempo observado
- Identifica problemas de pico
- **Menor é melhor**

### Taxa de Sucesso

- Porcentagem de requisições bem-sucedidas
- **100% é o ideal**

---

## 🎯 Interpretação dos Resultados

### Nginx Python vence quando:

- ✅ Latência média mais baixa
- ✅ Melhor sob alta concorrência
- ✅ APIs REST e endpoints dinâmicos

### Apache Python vence quando:

- ✅ Latência média mais baixa
- ✅ Melhor em cargas sequenciais
- ✅ Arquivos estáticos pequenos/médios

### Empate técnico quando:

- ≈ Diferença menor que 0.5ms
- ≈ Performance praticamente idêntica

---

## 🔍 Análise Visual Rápida

### O que procurar nos gráficos:

1. **Altura das barras**

   - Mais baixo = melhor (latências)
   - Compare as alturas relativas

2. **Consistência**

   - Barras de tamanho similar = servidor consistente
   - Muita variação = servidor instável

3. **Distribuição de vitórias**

   - Pizza: quem tem a maior fatia?
   - Barras: quem tem mais vitórias absolutas?

4. **Extremos (min/max)**

   - Diferença grande = servidor com picos
   - Diferença pequena = servidor estável

5. **Comparativo geral**
   - Visão holística
   - Quem é melhor "no geral"?

---

## 💡 Dicas

### Para Apresentações:

- Use os gráficos em slides
- Mostre o placar de vencedores primeiro
- Depois detalhe cada cenário

### Para Relatórios:

- Inclua todos os 5 gráficos
- Explique cada um
- Relacione com os dados TXT

### Para Análise Técnica:

- Compare com os dados brutos (resultados_testes.txt)
- Verifique consistência com analise_comparativa.txt
- Cruze informações com resumo_executivo.txt

---

## 🐛 Troubleshooting

### Gráficos não foram gerados?

```bash
# Verificar se matplotlib está instalado
docker exec load_client pip list | grep matplotlib

# Instalar manualmente se necessário
docker exec load_client pip install matplotlib numpy

# Re-gerar gráficos
docker exec load_client python3 /app/gerar_graficos.py
```

### Gráficos aparecem cortados?

- Aumentar `figsize` no código
- Usar `plt.tight_layout()`
- Aumentar margens: `bbox_inches='tight'`

### Cores não aparecem?

- Verificar terminal suporta cores
- Backend matplotlib configurado: `matplotlib.use('Agg')`

---

## 📚 Referências

### Matplotlib

- Documentação: https://matplotlib.org/stable/
- Galeria: https://matplotlib.org/stable/gallery/
- Tutoriais: https://matplotlib.org/stable/tutorials/

### NumPy

- Documentação: https://numpy.org/doc/
- Quickstart: https://numpy.org/doc/stable/user/quickstart.html

### Artigos sobre Performance

- Web Server Benchmarks
- HTTP Performance Testing
- Load Testing Best Practices

---

## 🎓 Para Aprender Mais

### Tipos de Gráficos Alternativos:

1. **Box Plot** - Distribuição estatística completa
2. **Violin Plot** - Densidade de distribuição
3. **Heatmap** - Matriz de correlação
4. **Line Plot** - Evolução temporal
5. **Scatter Plot** - Correlação entre métricas

### Métricas Adicionais:

1. **Percentis (P50, P95, P99)** - Latências em diferentes percentis
2. **Throughput** - Requisições por segundo
3. **Bandwidth** - MB/s transferidos
4. **CPU/Memory Usage** - Uso de recursos

---

## ✅ Checklist de Qualidade

- [x] 5 tipos diferentes de gráficos
- [x] Alta resolução (300 DPI)
- [x] Cores consistentes (verde/vermelho)
- [x] Títulos descritivos
- [x] Eixos rotulados
- [x] Valores exatos mostrados
- [x] Legendas claras
- [x] Grid para facilitar leitura
- [x] Informações do aluno
- [x] Salvo em PNG

---

**Desenvolvido por:** Hermeson A.  
**Matrícula:** 20239035382  
**Data:** 12 de novembro de 2025

**Tecnologias:** Python + Matplotlib + NumPy
