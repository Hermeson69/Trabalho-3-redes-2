#!/usr/bin/env python3
"""
Configurações do projeto - Terceira Avaliação Redes 2
Aluno: Hermeson A.
Matrícula: 20239035382
"""
import hashlib

# Dados do aluno
MATRICULA = "20239035382"
NOME = "Hermeson A."
ALUNO_INFO = f"{MATRICULA} {NOME}"

# Cálculo da subrede baseado nos últimos 4 dígitos da matrícula
ultimos_4 = MATRICULA[-4:]  # "5382"
terceiro_octeto = ultimos_4[:2]  # "53"
quarto_octeto = ultimos_4[2:]   # "82"
SUBNET = f"{terceiro_octeto}.{quarto_octeto}.0.0/24"
NETWORK_BASE = f"{terceiro_octeto}.{quarto_octeto}.0"

# Cálculo do X-Custom-ID (MD5 hash)
x_custom_id_hash = hashlib.md5(ALUNO_INFO.encode()).hexdigest()
X_CUSTOM_ID = x_custom_id_hash

# IPs dos containers
IP_NGINX = f"{terceiro_octeto}.{quarto_octeto}.0.10"
IP_APACHE = f"{terceiro_octeto}.{quarto_octeto}.0.20"
IP_PROMETHEUS = f"{terceiro_octeto}.{quarto_octeto}.0.30"
IP_GRAFANA = f"{terceiro_octeto}.{quarto_octeto}.0.40"
IP_CLIENT = f"{terceiro_octeto}.{quarto_octeto}.0.50"

if __name__ == "__main__":
    print(f"=== Configuração do Projeto ===")
    print(f"Aluno: {NOME}")
    print(f"Matrícula: {MATRICULA}")
    print(f"Últimos 4 dígitos: {ultimos_4}")
    print(f"Subrede: {SUBNET}")
    print(f"X-Custom-ID (MD5): {X_CUSTOM_ID}")
    print(f"\nIPs dos containers:")
    print(f"  Nginx:      {IP_NGINX}")
    print(f"  Apache:     {IP_APACHE}")
    print(f"  Prometheus: {IP_PROMETHEUS}")
    print(f"  Grafana:    {IP_GRAFANA}")
    print(f"  Client:     {IP_CLIENT}")
