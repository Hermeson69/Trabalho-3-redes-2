import subprocess
import time
import sys
import signal
import os
from pathlib import Path

class Colors:
    """Cores para output no terminal"""
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

class ProjetoRedesManager:
    """Gerenciador completo do projeto"""
    
    def __init__(self):
        self.project_dir = Path(__file__).parent
        self.containers_running = False
        
    def print_header(self):
        """Imprime o cabeçalho do projeto"""
        print("=" * 80)
        print(f"{Colors.BOLD}{Colors.HEADER}TRABALHO 3 - REDES DE COMPUTADORES II{Colors.ENDC}")
        print("=" * 80)
        print(f"{Colors.OKBLUE}Aluno:{Colors.ENDC} Hermeson A.")
        print(f"{Colors.OKBLUE}Matrícula:{Colors.ENDC} 20239035382")
        print(f"{Colors.OKBLUE}X-Custom-ID:{Colors.ENDC} f44d26f3aebff6f058eabbaf85366dfb")
        print(f"{Colors.OKBLUE}Subrede:{Colors.ENDC} 53.82.0.0/24")
        print("=" * 80)
        print()
    
    def run_command(self, command, description, capture_output=False, check=True):
        """Executa um comando e mostra o resultado"""
        print(f"{Colors.OKCYAN}>>> {description}...{Colors.ENDC}")
        
        try:
            if capture_output:
                result = subprocess.run(
                    command,
                    shell=True,
                    cwd=self.project_dir,
                    capture_output=True,
                    text=True,
                    check=check
                )
                return result
            else:
                subprocess.run(
                    command,
                    shell=True,
                    cwd=self.project_dir,
                    check=check
                )
                print(f"{Colors.OKGREEN}✓ {description} concluído{Colors.ENDC}\n")
        except subprocess.CalledProcessError as e:
            print(f"{Colors.FAIL}✗ Erro ao {description.lower()}{Colors.ENDC}")
            if capture_output and e.stderr:
                print(f"{Colors.FAIL}{e.stderr}{Colors.ENDC}")
            if check:
                raise
            return None
    
    def check_docker(self):
        """Verifica se Docker está disponível"""
        print(f"{Colors.OKBLUE}[1/8] Verificando Docker...{Colors.ENDC}")
        try:
            result = self.run_command(
                "docker --version",
                "Verificando versão do Docker",
                capture_output=True
            )
            print(f"{Colors.OKGREEN}✓ Docker encontrado: {result.stdout.strip()}{Colors.ENDC}\n")
            return True
        except:
            print(f"{Colors.FAIL}✗ Docker não encontrado! Instale o Docker primeiro.{Colors.ENDC}")
            return False
    
    def build_containers(self):
        """Constrói e sobe os containers"""
        print(f"{Colors.OKBLUE}[2/8] Construindo e subindo containers...{Colors.ENDC}")
        self.run_command(
            "docker compose up -d --build",
            "Construindo e iniciando containers"
        )
        self.containers_running = True
    
    def wait_for_servers(self):
        """Aguarda os servidores ficarem prontos"""
        print(f"{Colors.OKBLUE}[3/8] Aguardando servidores ficarem prontos...{Colors.ENDC}")
        
        servers = [
            ("nginx_server", "53.82.0.10", "Nginx Python"),
            ("apache_server", "53.82.0.20", "Apache Python")
        ]
        
        max_attempts = 30
        for container, ip, name in servers:
            print(f"  Aguardando {name} ({ip})...")
            
            for attempt in range(max_attempts):
                try:
                    result = subprocess.run(
                        f"docker exec load_client curl -s -o /dev/null -w '%{{http_code}}' http://{ip}/ 2>/dev/null",
                        shell=True,
                        cwd=self.project_dir,
                        capture_output=True,
                        text=True,
                        timeout=2
                    )
                    
                    if result.stdout.strip() == "200":
                        print(f"  {Colors.OKGREEN}✓ {name} pronto!{Colors.ENDC}")
                        break
                except:
                    pass
                
                if attempt == max_attempts - 1:
                    print(f"  {Colors.WARNING}⚠ {name} não respondeu, mas continuando...{Colors.ENDC}")
                else:
                    time.sleep(1)
        
        print()
    
    def show_status(self):
        """Mostra o status dos containers"""
        print(f"{Colors.OKBLUE}[4/8] Status dos containers:{Colors.ENDC}")
        self.run_command(
            "docker compose ps",
            "Listando containers",
            check=False
        )
    
    def run_tests(self):
        """Executa os testes de carga"""
        print(f"{Colors.OKBLUE}[5/8] Executando testes de carga...{Colors.ENDC}")
        print(f"{Colors.WARNING}Isso pode levar alguns minutos. Aguarde...{Colors.ENDC}\n")
        
        try:
            subprocess.run(
                "docker exec load_client python3 /app/load_test.py",
                shell=True,
                cwd=self.project_dir,
                check=True
            )
            print(f"\n{Colors.OKGREEN}✓ Testes concluídos com sucesso!{Colors.ENDC}\n")
        except subprocess.CalledProcessError:
            print(f"\n{Colors.FAIL}✗ Erro ao executar testes{Colors.ENDC}\n")
    
    def show_results(self):
        """Mostra um resumo dos resultados"""
        print(f"{Colors.OKBLUE}[6/8] Resumo dos resultados:{Colors.ENDC}")
        
        results_file = self.project_dir / "resultados" / "resultados_testes.txt"
        
        if results_file.exists():
            try:
                with open(results_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Mostrar apenas estatísticas principais
                print(f"{Colors.OKGREEN}✓ Resultados salvos em: resultados/resultados_testes.txt{Colors.ENDC}")
                print()
                
                # Contar requisições
                total_reqs = content.count("Total de requisições:")
                if total_reqs > 0:
                    print(f"  📊 Total de testes executados: {total_reqs // 2}")
                
                # Taxa de sucesso
                success_lines = [line for line in content.split('\n') if 'Taxa de sucesso: 100.00%' in line]
                if success_lines:
                    print(f"  {Colors.OKGREEN}✓ Taxa de sucesso: 100%{Colors.ENDC}")
                
                print()
                print(f"  Para ver resultados completos:")
                print(f"    • cat resultados/resultados_testes.txt")
                print(f"    • cat resultados/analise_comparativa.txt")
                print(f"    • cat resultados/comparacao_servidores.txt")
                print()
                
            except Exception as e:
                print(f"{Colors.WARNING}⚠ Erro ao ler resultados: {e}{Colors.ENDC}\n")
        else:
            print(f"{Colors.WARNING}⚠ Arquivo de resultados não encontrado{Colors.ENDC}\n")
    
    def run_analysis(self):
        """Executa a análise automática dos resultados"""
        print(f"{Colors.OKBLUE}[7/8] Gerando análise comparativa...{Colors.ENDC}")
        
        try:
            subprocess.run(
                "docker exec load_client python3 /app/analise_resultados.py",
                shell=True,
                cwd=self.project_dir,
                capture_output=True,
                check=True
            )
            print(f"{Colors.OKGREEN}✓ Análise gerada com sucesso!{Colors.ENDC}\n")
        except:
            print(f"{Colors.WARNING}⚠ Erro ao gerar análise (não crítico){Colors.ENDC}\n")
    
    def generate_graphs(self):
        """Gera gráficos comparativos"""
        print(f"{Colors.OKBLUE}[8/8] Gerando gráficos comparativos...{Colors.ENDC}")
        print(f"{Colors.WARNING}Isso pode levar alguns segundos...{Colors.ENDC}\n")
        
        try:
            result = subprocess.run(
                "docker exec load_client python3 /app/gerar_graficos.py",
                shell=True,
                cwd=self.project_dir,
                capture_output=True,
                text=True,
                check=True
            )
            
            # Mostrar output do script
            if result.stdout:
                print(result.stdout)
            
            print(f"{Colors.OKGREEN}✓ Gráficos gerados com sucesso!{Colors.ENDC}\n")
            
            # Listar gráficos gerados
            graficos_dir = self.project_dir / "resultados" / "graficos"
            if graficos_dir.exists():
                graficos = list(graficos_dir.glob("*.png"))
                if graficos:
                    print(f"{Colors.OKGREEN}📊 {len(graficos)} gráficos salvos em: resultados/graficos/{Colors.ENDC}")
                    for grafico in sorted(graficos):
                        print(f"  • {grafico.name}")
                    print()
            
        except subprocess.CalledProcessError as e:
            print(f"{Colors.WARNING}⚠ Erro ao gerar gráficos (não crítico){Colors.ENDC}")
            if e.stderr:
                print(f"{Colors.FAIL}{e.stderr}{Colors.ENDC}")
            print()
    
    def show_access_info(self):
        """Mostra informações de acesso aos serviços"""
        print("=" * 80)
        print(f"{Colors.BOLD}{Colors.HEADER}SERVIÇOS DISPONÍVEIS:{Colors.ENDC}")
        print("=" * 80)
        print(f"{Colors.OKGREEN}✓ Nginx Python:{Colors.ENDC}    http://localhost:8080")
        print(f"{Colors.OKGREEN}✓ Apache Python:{Colors.ENDC}   http://localhost:8081")
        print(f"{Colors.OKGREEN}✓ Prometheus:{Colors.ENDC}      http://localhost:9090")
        print(f"{Colors.OKGREEN}✓ Grafana:{Colors.ENDC}         http://localhost:3000 (admin/admin)")
        print("=" * 80)
        print()
        print(f"{Colors.OKCYAN}Pressione Ctrl+C para parar os containers e limpar tudo{Colors.ENDC}")
        print()
    
    def cleanup(self):
        """Derruba todos os containers e remove redes"""
        if not self.containers_running:
            return
        
        print()
        print("=" * 80)
        print(f"{Colors.WARNING}Limpando ambiente...{Colors.ENDC}")
        print("=" * 80)
        
        # Parar e remover containers
        print(f"{Colors.OKCYAN}>>> Parando containers...{Colors.ENDC}")
        subprocess.run(
            "docker compose down",
            shell=True,
            cwd=self.project_dir,
            capture_output=True
        )
        print(f"{Colors.OKGREEN}✓ Containers parados{Colors.ENDC}")
        
        # Remover volumes (opcional)
        print(f"{Colors.OKCYAN}>>> Removendo volumes...{Colors.ENDC}")
        subprocess.run(
            "docker compose down -v",
            shell=True,
            cwd=self.project_dir,
            capture_output=True
        )
        print(f"{Colors.OKGREEN}✓ Volumes removidos{Colors.ENDC}")
        
        # Remover rede customizada
        print(f"{Colors.OKCYAN}>>> Removendo redes...{Colors.ENDC}")
        subprocess.run(
            "docker network rm trabalho-3-redes-2_rede_customizada 2>/dev/null",
            shell=True,
            cwd=self.project_dir,
            capture_output=True
        )
        print(f"{Colors.OKGREEN}✓ Redes removidas{Colors.ENDC}")
        
        print()
        print(f"{Colors.OKGREEN}✓ Limpeza concluída com sucesso!{Colors.ENDC}")
        print("=" * 80)
    
    def run(self):
        """Executa o fluxo completo do projeto"""
        try:
            self.print_header()
            
            # Verificar Docker
            if not self.check_docker():
                return 1
            
            # Construir e subir containers
            self.build_containers()
            
            # Aguardar servidores
            self.wait_for_servers()
            
            # Mostrar status
            self.show_status()
            
            # Executar testes
            self.run_tests()
            
            # Gerar análise
            self.run_analysis()
            
            # Gerar gráficos
            self.generate_graphs()
            
            # Mostrar resultados
            self.show_results()
            
            # Mostrar informações de acesso
            self.show_access_info()
            
            # Manter rodando até Ctrl+C
            print(f"{Colors.BOLD}Containers rodando. Pressione Ctrl+C para parar...{Colors.ENDC}")
            print()
            
            # Aguardar indefinidamente
            while True:
                time.sleep(1)
                
        except KeyboardInterrupt:
            print()
            print(f"{Colors.WARNING}Interrompido pelo usuário (Ctrl+C){Colors.ENDC}")
        except Exception as e:
            print(f"{Colors.FAIL}Erro: {e}{Colors.ENDC}")
            return 1
        finally:
            # Sempre limpar ao sair
            self.cleanup()
        
        return 0

def signal_handler(sig, frame):
    """Handler para sinais (Ctrl+C)"""
    print()
    print(f"{Colors.WARNING}Sinal de interrupção recebido...{Colors.ENDC}")
    sys.exit(0)

def main():
    """Função principal"""
    # Registrar handler para Ctrl+C
    signal.signal(signal.SIGINT, signal_handler)
    
    # Criar e executar o gerenciador
    manager = ProjetoRedesManager()
    sys.exit(manager.run())

if __name__ == "__main__":
    main()
