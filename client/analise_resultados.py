"""
Análise de Resultados dos Testes de Carga
Aluno: Hermeson A. | Matrícula: 20239035382
"""

import re
from pathlib import Path

def ler_resultados(arquivo):
    """Lê o arquivo de resultados e extrai métricas"""
    with open(arquivo, 'r', encoding='utf-8') as f:
        conteudo = f.read()
    
    # Regex para extrair informações dos testes
    testes = []
    
    # Padrão para encontrar cada teste
    pattern_teste = r'TESTE: (.+?)\n.*?--- Servidor: NGINX ---\n(.*?)--- Servidor: APACHE ---\n(.*?)(?:={80}|$)'
    
    matches = re.finditer(pattern_teste, conteudo, re.DOTALL)
    
    for match in matches:
        nome_teste = match.group(1).strip()
        dados_nginx = match.group(2)
        dados_apache = match.group(3)
        
        # Extrair métricas do Nginx
        nginx_metrics = extrair_metricas(dados_nginx)
        
        # Extrair métricas do Apache
        apache_metrics = extrair_metricas(dados_apache)
        
        testes.append({
            'nome': nome_teste,
            'nginx': nginx_metrics,
            'apache': apache_metrics
        })
    
    return testes

def extrair_metricas(texto):
    """Extrai métricas numéricas de um bloco de texto"""
    metricas = {}
    
    # Padrões para extrair valores
    patterns = {
        'total': r'Total de requisições: (\d+)',
        'sucesso': r'Requisições bem-sucedidas: (\d+)',
        'falhas': r'Requisições falhadas: (\d+)',
        'taxa_sucesso': r'Taxa de sucesso: ([\d.]+)%',
        'latencia_media': r'Latência média: ([\d.]+) ms',
        'latencia_mediana': r'Latência mediana: ([\d.]+) ms',
        'desvio_padrao': r'Desvio padrão: ([\d.]+) ms',
        'latencia_min': r'Latência mínima: ([\d.]+) ms',
        'latencia_max': r'Latência máxima: ([\d.]+) ms',
        'tamanho_total': r'Tamanho total de resposta: ([\d.]+) bytes'
    }
    
    for key, pattern in patterns.items():
        match = re.search(pattern, texto)
        if match:
            valor = match.group(1)
            try:
                metricas[key] = float(valor)
            except ValueError:
                metricas[key] = valor
    
    return metricas

def gerar_tabela_comparativa(testes):
    """Gera uma tabela comparativa dos resultados"""
    output = []
    output.append("=" * 100)
    output.append("TABELA COMPARATIVA DE RESULTADOS")
    output.append("=" * 100)
    output.append("")
    
    for i, teste in enumerate(testes, 1):
        output.append(f"TESTE {i}: {teste['nome']}")
        output.append("-" * 100)
        
        nginx = teste['nginx']
        apache = teste['apache']
        
        # Formatar tabela
        output.append(f"{'Métrica':<30} | {'Nginx':>15} | {'Apache':>15} | {'Diferença':>15} | Vencedor")
        output.append("-" * 100)
        
        # Latência média
        if 'latencia_media' in nginx and 'latencia_media' in apache:
            n_val = nginx['latencia_media']
            a_val = apache['latencia_media']
            diff = ((n_val - a_val) / a_val * 100) if a_val > 0 else 0
            vencedor = "Apache ⭐" if a_val < n_val else "Nginx ⭐" if n_val < a_val else "Empate"
            output.append(f"{'Latência Média (ms)':<30} | {n_val:>15.2f} | {a_val:>15.2f} | {diff:>14.1f}% | {vencedor}")
        
        # Latência mediana
        if 'latencia_mediana' in nginx and 'latencia_mediana' in apache:
            n_val = nginx['latencia_mediana']
            a_val = apache['latencia_mediana']
            diff = ((n_val - a_val) / a_val * 100) if a_val > 0 else 0
            vencedor = "Apache ⭐" if a_val < n_val else "Nginx ⭐" if n_val < a_val else "Empate"
            output.append(f"{'Latência Mediana (ms)':<30} | {n_val:>15.2f} | {a_val:>15.2f} | {diff:>14.1f}% | {vencedor}")
        
        # Desvio padrão
        if 'desvio_padrao' in nginx and 'desvio_padrao' in apache:
            n_val = nginx['desvio_padrao']
            a_val = apache['desvio_padrao']
            diff = ((n_val - a_val) / a_val * 100) if a_val > 0 else 0
            vencedor = "Apache ⭐" if a_val < n_val else "Nginx ⭐" if n_val < a_val else "Empate"
            output.append(f"{'Desvio Padrão (ms)':<30} | {n_val:>15.2f} | {a_val:>15.2f} | {diff:>14.1f}% | {vencedor}")
        
        # Latência mínima
        if 'latencia_min' in nginx and 'latencia_min' in apache:
            n_val = nginx['latencia_min']
            a_val = apache['latencia_min']
            diff = ((n_val - a_val) / a_val * 100) if a_val > 0 else 0
            vencedor = "Apache ⭐" if a_val < n_val else "Nginx ⭐" if n_val < a_val else "Empate"
            output.append(f"{'Latência Mínima (ms)':<30} | {n_val:>15.2f} | {a_val:>15.2f} | {diff:>14.1f}% | {vencedor}")
        
        # Latência máxima
        if 'latencia_max' in nginx and 'latencia_max' in apache:
            n_val = nginx['latencia_max']
            a_val = apache['latencia_max']
            diff = ((n_val - a_val) / a_val * 100) if a_val > 0 else 0
            vencedor = "Apache ⭐" if a_val < n_val else "Nginx ⭐" if n_val < a_val else "Empate"
            output.append(f"{'Latência Máxima (ms)':<30} | {n_val:>15.2f} | {a_val:>15.2f} | {diff:>14.1f}% | {vencedor}")
        
        # Taxa de sucesso
        if 'taxa_sucesso' in nginx and 'taxa_sucesso' in apache:
            n_val = nginx['taxa_sucesso']
            a_val = apache['taxa_sucesso']
            output.append(f"{'Taxa de Sucesso (%)':<30} | {n_val:>15.2f} | {a_val:>15.2f} | {0:>14.1f}% | Empate")
        
        output.append("")
    
    output.append("=" * 100)
    return "\n".join(output)

def calcular_estatisticas_gerais(testes):
    """Calcula estatísticas gerais de todos os testes"""
    output = []
    output.append("=" * 100)
    output.append("ESTATÍSTICAS GERAIS")
    output.append("=" * 100)
    output.append("")
    
    # Coletar todas as latências médias
    latencias_nginx = []
    latencias_apache = []
    
    for teste in testes:
        if 'latencia_media' in teste['nginx']:
            latencias_nginx.append(teste['nginx']['latencia_media'])
        if 'latencia_media' in teste['apache']:
            latencias_apache.append(teste['apache']['latencia_media'])
    
    if latencias_nginx and latencias_apache:
        media_nginx = sum(latencias_nginx) / len(latencias_nginx)
        media_apache = sum(latencias_apache) / len(latencias_apache)
        
        output.append(f"Latência Média Geral:")
        output.append(f"  Nginx:  {media_nginx:.2f} ms")
        output.append(f"  Apache: {media_apache:.2f} ms")
        output.append(f"  Diferença: {abs(media_nginx - media_apache):.2f} ms")
        
        if media_apache < media_nginx:
            pct = ((media_nginx - media_apache) / media_apache * 100)
            output.append(f"  Vencedor: Apache (⭐ {pct:.1f}% mais rápido)")
        elif media_nginx < media_apache:
            pct = ((media_apache - media_nginx) / media_nginx * 100)
            output.append(f"  Vencedor: Nginx (⭐ {pct:.1f}% mais rápido)")
        else:
            output.append(f"  Vencedor: Empate")
        output.append("")
    
    # Contar vitórias
    vitorias_nginx = 0
    vitorias_apache = 0
    empates = 0
    
    for teste in testes:
        if 'latencia_media' in teste['nginx'] and 'latencia_media' in teste['apache']:
            n = teste['nginx']['latencia_media']
            a = teste['apache']['latencia_media']
            
            if abs(n - a) < 0.5:  # Diferença menor que 0.5ms = empate
                empates += 1
            elif a < n:
                vitorias_apache += 1
            else:
                vitorias_nginx += 1
    
    output.append(f"Placar de Vitórias (por latência média):")
    output.append(f"  Nginx:  {vitorias_nginx} vitórias")
    output.append(f"  Apache: {vitorias_apache} vitórias")
    output.append(f"  Empates: {empates}")
    output.append("")
    
    if vitorias_apache > vitorias_nginx:
        output.append("🏆 VENCEDOR GERAL: APACHE")
    elif vitorias_nginx > vitorias_apache:
        output.append("🏆 VENCEDOR GERAL: NGINX")
    else:
        output.append("🏆 RESULTADO: EMPATE TÉCNICO")
    
    output.append("")
    output.append("=" * 100)
    return "\n".join(output)

def main():
    """Função principal"""
    print("=" * 100)
    print("ANÁLISE DE RESULTADOS DOS TESTES DE CARGA")
    print("Aluno: Hermeson A.")
    print("Matrícula: 20239035382")
    print("=" * 100)
    print()
    
    # Caminho do arquivo de resultados
    arquivo_resultados = Path('/resultados/resultados_testes.txt')
    
    if not arquivo_resultados.exists():
        print(f"❌ Arquivo de resultados não encontrado: {arquivo_resultados}")
        print("Execute os testes primeiro: python3 load_test.py")
        return
    
    print("📊 Lendo arquivo de resultados...")
    testes = ler_resultados(arquivo_resultados)
    print(f"✅ {len(testes)} testes encontrados")
    print()
    
    # Gerar tabela comparativa
    print("📈 Gerando tabela comparativa...")
    tabela = gerar_tabela_comparativa(testes)
    print(tabela)
    print()
    
    # Gerar estatísticas gerais
    print("📊 Calculando estatísticas gerais...")
    stats = calcular_estatisticas_gerais(testes)
    print(stats)
    print()
    
    # Salvar análise em arquivo
    arquivo_analise = Path('/resultados/analise_comparativa.txt')
    with open(arquivo_analise, 'w', encoding='utf-8') as f:
        f.write("ANÁLISE COMPARATIVA DOS TESTES DE CARGA\n")
        f.write("Aluno: Hermeson A.\n")
        f.write("Matrícula: 20239035382\n")
        f.write("\n")
        f.write(tabela)
        f.write("\n\n")
        f.write(stats)
    
    print(f"💾 Análise salva em: {arquivo_analise}")
    print()
    print("✅ Análise concluída com sucesso!")

if __name__ == '__main__':
    main()
