#!/usr/bin/env python3
"""
Gerador de Gráficos Comparativos
Aluno: Hermeson A. | Matrícula: 20239035382
"""

import re
import json
from pathlib import Path

try:
    import matplotlib
    matplotlib.use('Agg')  # Backend sem display
    import matplotlib.pyplot as plt
    import numpy as np
    MATPLOTLIB_AVAILABLE = True
except ImportError:
    MATPLOTLIB_AVAILABLE = False
    print("⚠️  matplotlib não disponível. Instale com: pip install matplotlib")
    print("   Gerando apenas análise textual...")

class GeradorGraficos:
    """Gera gráficos comparativos dos resultados"""
    
    def __init__(self, arquivo_resultados):
        self.arquivo_resultados = Path(arquivo_resultados)
        self.resultados_dir = self.arquivo_resultados.parent
        self.graficos_dir = self.resultados_dir / "graficos"
        self.dados = []
        
    def criar_diretorio_graficos(self):
        """Cria diretório para salvar os gráficos"""
        self.graficos_dir.mkdir(exist_ok=True)
        
    def ler_resultados(self):
        """Lê e parseia o arquivo de resultados"""
        if not self.arquivo_resultados.exists():
            print(f"❌ Arquivo de resultados não encontrado: {self.arquivo_resultados}")
            return False
        
        with open(self.arquivo_resultados, 'r', encoding='utf-8') as f:
            conteudo = f.read()
        
        # Regex para extrair testes
        pattern = r'TESTE: (.+?)\n.*?--- Servidor: NGINX ---\n(.*?)--- Servidor: APACHE ---\n(.*?)(?:={80}|$)'
        
        matches = re.finditer(pattern, conteudo, re.DOTALL)
        
        for match in matches:
            nome_teste = match.group(1).strip()
            dados_nginx = self._extrair_metricas(match.group(2))
            dados_apache = self._extrair_metricas(match.group(3))
            
            self.dados.append({
                'nome': nome_teste,
                'nginx': dados_nginx,
                'apache': dados_apache
            })
        
        # Criar self.resultados como lista de tuplas (nginx, apache) para gráficos de linha
        self.resultados = [(d['nginx'], d['apache']) for d in self.dados]
        
        print(f"✓ {len(self.dados)} testes carregados")
        return len(self.dados) > 0
    
    def _extrair_metricas(self, texto):
        """Extrai métricas numéricas de um bloco de texto"""
        metricas = {}
        
        patterns = {
            'latencia_media': r'Latência média: ([\d.]+) ms',
            'latencia_mediana': r'Latência mediana: ([\d.]+) ms',
            'desvio_padrao': r'Desvio padrão: ([\d.]+) ms',
            'latencia_min': r'Latência mínima: ([\d.]+) ms',
            'latencia_max': r'Latência máxima: ([\d.]+) ms',
            'taxa_sucesso': r'Taxa de sucesso: ([\d.]+)%',
        }
        
        for key, pattern in patterns.items():
            match = re.search(pattern, texto)
            if match:
                metricas[key] = float(match.group(1))
        
        return metricas
    
    def gerar_grafico_latencia_media(self):
        """Gera gráfico comparativo de latência média"""
        if not MATPLOTLIB_AVAILABLE:
            return
        
        nomes_testes = [self._simplificar_nome(t['nome']) for t in self.dados]
        nginx_latencias = [t['nginx'].get('latencia_media', 0) for t in self.dados]
        apache_latencias = [t['apache'].get('latencia_media', 0) for t in self.dados]
        
        x = np.arange(len(nomes_testes))
        width = 0.35
        
        fig, ax = plt.subplots(figsize=(14, 8))
        bars1 = ax.bar(x - width/2, nginx_latencias, width, label='Nginx Python', color='#00A86B')
        bars2 = ax.bar(x + width/2, apache_latencias, width, label='Apache Python', color='#D2042D')
        
        ax.set_xlabel('Cenários de Teste', fontsize=12, fontweight='bold')
        ax.set_ylabel('Latência Média (ms)', fontsize=12, fontweight='bold')
        ax.set_title('Comparação de Latência Média: Nginx vs Apache\nHermeson A. - Matrícula: 20239035382', 
                     fontsize=14, fontweight='bold')
        ax.set_xticks(x)
        ax.set_xticklabels(nomes_testes, rotation=45, ha='right')
        ax.legend()
        ax.grid(True, alpha=0.3, axis='y')
        
        # Adicionar valores nas barras
        self._add_value_labels(ax, bars1)
        self._add_value_labels(ax, bars2)
        
        plt.tight_layout()
        arquivo = self.graficos_dir / 'latencia_media.png'
        plt.savefig(arquivo, dpi=300, bbox_inches='tight')
        plt.close()
        
        print(f"✓ Gráfico salvo: {arquivo}")
    
    def gerar_grafico_desvio_padrao(self):
        """Gera gráfico de desvio padrão (consistência)"""
        if not MATPLOTLIB_AVAILABLE:
            return
        
        nomes_testes = [self._simplificar_nome(t['nome']) for t in self.dados]
        nginx_desvios = [t['nginx'].get('desvio_padrao', 0) for t in self.dados]
        apache_desvios = [t['apache'].get('desvio_padrao', 0) for t in self.dados]
        
        x = np.arange(len(nomes_testes))
        width = 0.35
        
        fig, ax = plt.subplots(figsize=(14, 8))
        bars1 = ax.bar(x - width/2, nginx_desvios, width, label='Nginx Python', color='#00A86B')
        bars2 = ax.bar(x + width/2, apache_desvios, width, label='Apache Python', color='#D2042D')
        
        ax.set_xlabel('Cenários de Teste', fontsize=12, fontweight='bold')
        ax.set_ylabel('Desvio Padrão (ms)', fontsize=12, fontweight='bold')
        ax.set_title('Consistência (Desvio Padrão): Nginx vs Apache\nMenor é melhor\nHermeson A. - Matrícula: 20239035382', 
                     fontsize=14, fontweight='bold')
        ax.set_xticks(x)
        ax.set_xticklabels(nomes_testes, rotation=45, ha='right')
        ax.legend()
        ax.grid(True, alpha=0.3, axis='y')
        
        self._add_value_labels(ax, bars1)
        self._add_value_labels(ax, bars2)
        
        plt.tight_layout()
        arquivo = self.graficos_dir / 'desvio_padrao.png'
        plt.savefig(arquivo, dpi=300, bbox_inches='tight')
        plt.close()
        
        print(f"✓ Gráfico salvo: {arquivo}")
    
    def gerar_grafico_latencia_min_max(self):
        """Gera gráfico de latências mínima e máxima"""
        if not MATPLOTLIB_AVAILABLE:
            return
        
        # Separar por servidor
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 8))
        
        nomes_testes = [self._simplificar_nome(t['nome']) for t in self.dados]
        
        # Nginx
        nginx_min = [t['nginx'].get('latencia_min', 0) for t in self.dados]
        nginx_max = [t['nginx'].get('latencia_max', 0) for t in self.dados]
        
        x = np.arange(len(nomes_testes))
        width = 0.35
        
        ax1.bar(x - width/2, nginx_min, width, label='Mínima', color='#4CAF50')
        ax1.bar(x + width/2, nginx_max, width, label='Máxima', color='#FF5722')
        ax1.set_xlabel('Cenários de Teste', fontsize=11, fontweight='bold')
        ax1.set_ylabel('Latência (ms)', fontsize=11, fontweight='bold')
        ax1.set_title('Nginx Python - Latências Min/Max', fontsize=12, fontweight='bold')
        ax1.set_xticks(x)
        ax1.set_xticklabels(nomes_testes, rotation=45, ha='right', fontsize=9)
        ax1.legend()
        ax1.grid(True, alpha=0.3, axis='y')
        
        # Apache
        apache_min = [t['apache'].get('latencia_min', 0) for t in self.dados]
        apache_max = [t['apache'].get('latencia_max', 0) for t in self.dados]
        
        ax2.bar(x - width/2, apache_min, width, label='Mínima', color='#4CAF50')
        ax2.bar(x + width/2, apache_max, width, label='Máxima', color='#FF5722')
        ax2.set_xlabel('Cenários de Teste', fontsize=11, fontweight='bold')
        ax2.set_ylabel('Latência (ms)', fontsize=11, fontweight='bold')
        ax2.set_title('Apache Python - Latências Min/Max', fontsize=12, fontweight='bold')
        ax2.set_xticks(x)
        ax2.set_xticklabels(nomes_testes, rotation=45, ha='right', fontsize=9)
        ax2.legend()
        ax2.grid(True, alpha=0.3, axis='y')
        
        fig.suptitle('Análise de Latências Extremas\nHermeson A. - Matrícula: 20239035382', 
                     fontsize=14, fontweight='bold')
        
        plt.tight_layout()
        arquivo = self.graficos_dir / 'latencia_min_max.png'
        plt.savefig(arquivo, dpi=300, bbox_inches='tight')
        plt.close()
        
        print(f"✓ Gráfico salvo: {arquivo}")
    
    def gerar_grafico_vencedores(self):
        """Gera gráfico de placar de vitórias"""
        if not MATPLOTLIB_AVAILABLE:
            return
        
        vitorias_nginx = 0
        vitorias_apache = 0
        empates = 0
        
        for teste in self.dados:
            lat_nginx = teste['nginx'].get('latencia_media', float('inf'))
            lat_apache = teste['apache'].get('latencia_media', float('inf'))
            
            diff = abs(lat_nginx - lat_apache)
            if diff < 0.5:  # Empate se diferença < 0.5ms
                empates += 1
            elif lat_nginx < lat_apache:
                vitorias_nginx += 1
            else:
                vitorias_apache += 1
        
        # Gráfico de pizza
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 8))
        
        # Gráfico de pizza
        labels = ['Nginx Python', 'Apache Python', 'Empates']
        sizes = [vitorias_nginx, vitorias_apache, empates]
        colors = ['#00A86B', '#D2042D', '#FFA500']
        explode = (0.1, 0.1, 0)
        
        ax1.pie(sizes, explode=explode, labels=labels, colors=colors,
                autopct='%1.1f%%', shadow=True, startangle=90)
        ax1.set_title('Distribuição de Vitórias por Latência Média', 
                      fontsize=12, fontweight='bold')
        
        # Gráfico de barras
        servidores = ['Nginx\nPython', 'Apache\nPython', 'Empates']
        bars = ax2.bar(servidores, sizes, color=colors)
        ax2.set_ylabel('Número de Vitórias', fontsize=11, fontweight='bold')
        ax2.set_title('Placar Final', fontsize=12, fontweight='bold')
        ax2.grid(True, alpha=0.3, axis='y')
        
        # Adicionar valores
        for bar in bars:
            height = bar.get_height()
            ax2.text(bar.get_x() + bar.get_width()/2., height,
                    f'{int(height)}',
                    ha='center', va='bottom', fontweight='bold')
        
        fig.suptitle(f'Análise de Vencedores - Total de {len(self.dados)} Testes\nHermeson A. - Matrícula: 20239035382', 
                     fontsize=14, fontweight='bold')
        
        plt.tight_layout()
        arquivo = self.graficos_dir / 'placar_vencedores.png'
        plt.savefig(arquivo, dpi=300, bbox_inches='tight')
        plt.close()
        
        print(f"✓ Gráfico salvo: {arquivo}")
    
    def gerar_grafico_comparativo_geral(self):
        """Gera gráfico com múltiplas métricas"""
        if not MATPLOTLIB_AVAILABLE:
            return
        
        # Calcular médias gerais
        metricas = ['latencia_media', 'latencia_mediana', 'desvio_padrao']
        labels_metricas = ['Latência\nMédia', 'Latência\nMediana', 'Desvio\nPadrão']
        
        nginx_valores = []
        apache_valores = []
        
        for metrica in metricas:
            nginx_vals = [t['nginx'].get(metrica, 0) for t in self.dados]
            apache_vals = [t['apache'].get(metrica, 0) for t in self.dados]
            
            nginx_valores.append(sum(nginx_vals) / len(nginx_vals) if nginx_vals else 0)
            apache_valores.append(sum(apache_vals) / len(apache_vals) if apache_vals else 0)
        
        x = np.arange(len(labels_metricas))
        width = 0.35
        
        fig, ax = plt.subplots(figsize=(12, 8))
        bars1 = ax.bar(x - width/2, nginx_valores, width, label='Nginx Python', color='#00A86B')
        bars2 = ax.bar(x + width/2, apache_valores, width, label='Apache Python', color='#D2042D')
        
        ax.set_xlabel('Métricas', fontsize=12, fontweight='bold')
        ax.set_ylabel('Tempo (ms)', fontsize=12, fontweight='bold')
        ax.set_title('Comparação Geral de Métricas (Média de Todos os Testes)\nHermeson A. - Matrícula: 20239035382', 
                     fontsize=14, fontweight='bold')
        ax.set_xticks(x)
        ax.set_xticklabels(labels_metricas)
        ax.legend()
        ax.grid(True, alpha=0.3, axis='y')
        
        self._add_value_labels(ax, bars1)
        self._add_value_labels(ax, bars2)
        
        plt.tight_layout()
        arquivo = self.graficos_dir / 'comparativo_geral.png'
        plt.savefig(arquivo, dpi=300, bbox_inches='tight')
        plt.close()
        
        print(f"✓ Gráfico salvo: {arquivo}")
    
    def _simplificar_nome(self, nome):
        """Simplifica o nome do teste para caber no gráfico"""
        nome = nome.replace('Teste ', 'T')
        nome = nome.replace('requisições', 'req')
        nome = nome.replace('sequenciais', 'seq')
        nome = nome.replace('concorrentes', 'conc')
        nome = nome.replace('Arquivo ', '')
        if len(nome) > 40:
            nome = nome[:37] + '...'
        return nome
    
    def _add_value_labels(self, ax, bars):
        """Adiciona valores no topo das barras"""
        for bar in bars:
            height = bar.get_height()
            if height > 0:
                ax.text(bar.get_x() + bar.get_width()/2., height,
                       f'{height:.2f}',
                       ha='center', va='bottom', fontsize=8)
    
    def gerar_grafico_linhas_evolucao(self):
        """Gera gráfico de linhas da evolução de latência por teste"""
        print("Gerando gráfico de linhas - Evolução de Latência...")
        
        fig, ax = plt.subplots(figsize=(14, 8))
        
        testes = []
        nginx_lat = []
        apache_lat = []
        
        for i, (nginx, apache) in enumerate(self.resultados, 1):
            testes.append(f"T{i}")
            nginx_lat.append(nginx['latencia_media'])
            apache_lat.append(apache['latencia_media'])
        
        x = range(len(testes))
        
        ax.plot(x, nginx_lat, marker='o', linewidth=2, markersize=8, 
                label='Nginx', color='#2ecc71', linestyle='-')
        ax.plot(x, apache_lat, marker='s', linewidth=2, markersize=8,
                label='Apache', color='#e74c3c', linestyle='-')
        
        ax.set_xlabel('Teste', fontweight='bold', fontsize=11)
        ax.set_ylabel('Latência Média (ms)', fontweight='bold', fontsize=11)
        ax.set_title('Evolução da Latência Média por Teste', 
                    fontweight='bold', fontsize=13, pad=20)
        
        ax.set_xticks(x)
        ax.set_xticklabels(testes)
        ax.legend(fontsize=10)
        ax.grid(True, alpha=0.3)
        
        # Adicionar valores nos pontos
        for i, (nx, ap) in enumerate(zip(nginx_lat, apache_lat)):
            ax.text(i, nx, f'{nx:.1f}', ha='center', va='bottom', fontsize=8)
            ax.text(i, ap, f'{ap:.1f}', ha='center', va='top', fontsize=8)
        
        plt.tight_layout()
        arquivo = self.graficos_dir / 'linhas_evolucao_latencia.png'
        plt.savefig(arquivo, dpi=300, bbox_inches='tight')
        plt.close()
        
        print(f"✓ Gráfico salvo: {arquivo}")
    
    def gerar_grafico_linhas_min_max(self):
        """Gera gráfico de linhas com latências mínima e máxima"""
        print("Gerando gráfico de linhas - Latências Mínima e Máxima...")
        
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 10))
        
        testes = []
        nginx_min = []
        apache_min = []
        nginx_max = []
        apache_max = []
        
        for i, (nginx, apache) in enumerate(self.resultados, 1):
            testes.append(f"T{i}")
            nginx_min.append(nginx['latencia_min'])
            apache_min.append(apache['latencia_min'])
            nginx_max.append(nginx['latencia_max'])
            apache_max.append(apache['latencia_max'])
        
        x = range(len(testes))
        
        # Gráfico de latências mínimas
        ax1.plot(x, nginx_min, marker='o', linewidth=2, markersize=8,
                label='Nginx', color='#2ecc71', linestyle='-')
        ax1.plot(x, apache_min, marker='s', linewidth=2, markersize=8,
                label='Apache', color='#e74c3c', linestyle='-')
        
        ax1.set_ylabel('Latência Mínima (ms)', fontweight='bold', fontsize=11)
        ax1.set_title('Latências Mínimas por Teste', 
                     fontweight='bold', fontsize=12, pad=15)
        ax1.set_xticks(x)
        ax1.set_xticklabels(testes)
        ax1.legend(fontsize=10)
        ax1.grid(True, alpha=0.3)
        
        # Gráfico de latências máximas
        ax2.plot(x, nginx_max, marker='o', linewidth=2, markersize=8,
                label='Nginx', color='#2ecc71', linestyle='-')
        ax2.plot(x, apache_max, marker='s', linewidth=2, markersize=8,
                label='Apache', color='#e74c3c', linestyle='-')
        
        ax2.set_xlabel('Teste', fontweight='bold', fontsize=11)
        ax2.set_ylabel('Latência Máxima (ms)', fontweight='bold', fontsize=11)
        ax2.set_title('Latências Máximas por Teste', 
                     fontweight='bold', fontsize=12, pad=15)
        ax2.set_xticks(x)
        ax2.set_xticklabels(testes)
        ax2.legend(fontsize=10)
        ax2.grid(True, alpha=0.3)
        
        plt.tight_layout()
        arquivo = self.graficos_dir / 'linhas_min_max.png'
        plt.savefig(arquivo, dpi=300, bbox_inches='tight')
        plt.close()
        
        print(f"✓ Gráfico salvo: {arquivo}")
    
    def gerar_grafico_linhas_desvio(self):
        """Gera gráfico de linhas do desvio padrão com área de variação"""
        print("Gerando gráfico de linhas - Desvio Padrão com Área...")
        
        fig, ax = plt.subplots(figsize=(14, 8))
        
        testes = []
        nginx_media = []
        apache_media = []
        nginx_desvio = []
        apache_desvio = []
        
        for i, (nginx, apache) in enumerate(self.resultados, 1):
            testes.append(f"T{i}")
            nginx_media.append(nginx['latencia_media'])
            apache_media.append(apache['latencia_media'])
            nginx_desvio.append(nginx['desvio_padrao'])
            apache_desvio.append(apache['desvio_padrao'])
        
        x = np.array(range(len(testes)))
        nginx_media = np.array(nginx_media)
        apache_media = np.array(apache_media)
        nginx_desvio = np.array(nginx_desvio)
        apache_desvio = np.array(apache_desvio)
        
        # Linhas principais
        ax.plot(x, nginx_media, marker='o', linewidth=2, markersize=8,
               label='Nginx', color='#2ecc71', linestyle='-')
        ax.plot(x, apache_media, marker='s', linewidth=2, markersize=8,
               label='Apache', color='#e74c3c', linestyle='-')
        
        # Área de variação (média ± desvio padrão)
        ax.fill_between(x, nginx_media - nginx_desvio, nginx_media + nginx_desvio,
                        alpha=0.2, color='#2ecc71', label='Nginx ±σ')
        ax.fill_between(x, apache_media - apache_desvio, apache_media + apache_desvio,
                        alpha=0.2, color='#e74c3c', label='Apache ±σ')
        
        ax.set_xlabel('Teste', fontweight='bold', fontsize=11)
        ax.set_ylabel('Latência (ms)', fontweight='bold', fontsize=11)
        ax.set_title('Latência Média com Área de Variação (±σ)', 
                    fontweight='bold', fontsize=13, pad=20)
        
        ax.set_xticks(x)
        ax.set_xticklabels(testes)
        ax.legend(fontsize=9, loc='upper left')
        ax.grid(True, alpha=0.3)
        
        plt.tight_layout()
        arquivo = self.graficos_dir / 'linhas_desvio_area.png'
        plt.savefig(arquivo, dpi=300, bbox_inches='tight')
        plt.close()
        
        print(f"✓ Gráfico salvo: {arquivo}")
    
    def gerar_todos_graficos(self):
        """Gera todos os gráficos"""
        print("\n" + "=" * 80)
        print("GERANDO GRÁFICOS COMPARATIVOS")
        print("=" * 80)
        print()
        
        if not MATPLOTLIB_AVAILABLE:
            print("❌ matplotlib não disponível!")
            print("   Execute dentro do container:")
            print("   pip install matplotlib")
            return False
        
        self.criar_diretorio_graficos()
        
        if not self.ler_resultados():
            return False
        
        print(f"\nGerando {8} gráficos...")
        print()
        
        # Gráficos de barras
        self.gerar_grafico_latencia_media()
        self.gerar_grafico_desvio_padrao()
        self.gerar_grafico_latencia_min_max()
        self.gerar_grafico_vencedores()
        self.gerar_grafico_comparativo_geral()
        
        # Gráficos de linhas
        self.gerar_grafico_linhas_evolucao()
        self.gerar_grafico_linhas_min_max()
        self.gerar_grafico_linhas_desvio()
        
        print()
        print("=" * 80)
        print(f"✓ Todos os gráficos salvos em: {self.graficos_dir}")
        print("=" * 80)
        print()
        print("Gráficos gerados:")
        for arquivo in sorted(self.graficos_dir.glob('*.png')):
            print(f"  • {arquivo.name}")
        print()
        
        return True

def main():
    """Função principal"""
    arquivo_resultados = Path('/resultados/resultados_testes.txt')
    
    gerador = GeradorGraficos(arquivo_resultados)
    
    if gerador.gerar_todos_graficos():
        print("✅ Geração de gráficos concluída com sucesso!")
        return 0
    else:
        print("❌ Erro ao gerar gráficos")
        return 1

if __name__ == '__main__':
    import sys
    sys.exit(main())
