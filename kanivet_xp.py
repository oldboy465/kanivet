# -*- coding: utf-8 -*-
"""
========================================================================================
    KANIVET XP — CYBER-GIT MDNATOR UNIVERSAL SUITE (ENTERPRISE EDITION v5.0)
========================================================================================
    Autor Principal : Philipe Sampaio Lima (@OldBoy465)
    Co-Autoria      : Engenharia de Prompts & Inteligência Artificial
    Ano             : 2026
    Contatos        : cienciaegestao@gmail.com | WhatsApp: +55 98 98250-6920
========================================================================================
    ARQUITETURA MONOLÍTICA COMPLETA - STANDALONE DESKTOP APPLICATION:
      1. Sanitizador Heurístico Universal & Git Pusher (Tokens, PAT, Deploy Blindado)
      2. Central de Operações Git Baremetal (12+ Funções Operacionais + Clone)
      3. Motor MDnator v4.0 Matrix Engine (Compilador de Códigos, Firmware ESP32/Arduino)
      4. Módulo InfoPlan (Análise Estrutural, Dimensional e Estatística de Planilhas)
      5. Listador de Estruturas (Emulador Nativo Avançado de tree /F + Dump Datado)
      6. Telemetria de Hardware em Tempo Real "Hardware-Z" (CPU, Memória, Disco, SO)
      7. Manual Integrado Retro Windows Help & Dialog de Ajuda Interativa
========================================================================================
"""

import sys
import os
import re
import math
import time
import shutil
import platform
import subprocess
import threading
from datetime import datetime
from typing import List, Tuple, Optional, Dict, Any

# Interface Gráfica Nativa Padrão Python
import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext

# Telemetria de Hardware opcional (psutil)
try:
    import psutil
    PSUTIL_AVAILABLE = True
except ImportError:
    psutil = None
    PSUTIL_AVAILABLE = False

# Análise de Planilhas (Pandas e Openpyxl / XLRD)
try:
    import pandas as pd
    PANDAS_AVAILABLE = True
except ImportError:
    pd = None
    PANDAS_AVAILABLE = False

try:
    from openpyxl.utils import get_column_letter
    OPENPYXL_AVAILABLE = True
except ImportError:
    def get_column_letter(col_idx: int) -> str:
        """Fallback puro em Python para calcular letras de colunas Excel (A, B... AA...)."""
        result = []
        while col_idx > 0:
            col_idx, remainder = divmod(col_idx - 1, 26)
            result.append(chr(65 + remainder))
        return "".join(reversed(result))
    OPENPYXL_AVAILABLE = False


# ======================================================================================
# BANNER ASCII E CONSTANTES VISUAIS (RETRO WINDOWS XP & JAVA SWING)
# ======================================================================================
KANIVET_ASCII_BANNER = r"""
 ██╗  ██╗ █████╗ ███╗   ██╗██╗██╗   ██╗███████╗████████╗   ██╗  ██╗██████╗ 
 ██║ ██╔╝██╔══██╗████╗  ██║██║██║   ██║██╔════╝╚══██╔══╝   ╚██╗██╔╝██╔══██╗
 █████╔╝ ███████║██╔██╗ ██║██║██║   ██║█████╗     ██║       ╚███╔╝ ██████╔╝
 ██╔═██╗ ██╔══██║██║╚██╗██║██║╚██╗ ██╔╝██╔══╝     ██║       ██╔██╗ ██╔═══╝ 
 ██║  ██╗██║  ██║██║ ╚████║██║ ╚████╔╝ ███████╗    ██║      ██╔╝ ██╗██║     
 ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═══╝╚═╝  ╚═══╝  ╚══════╝    ╚═╝      ╚═╝  ╚═╝╚═╝     
   >> UNIVERSAL SUITE: GIT BAREMETAL, MDNATOR, INFOPLAN & HARDWARE-Z <<
"""

# Paleta clássica Windows XP / Java Swing
XP_BG_BASE = "#ECE9D8"          # Bege clássico das janelas do Windows XP
XP_PANEL_BG = "#F0EEE0"         # Painel levemente clareado
XP_ACCENT = "#0A246A"           # Azul escuro barra de título clássica
XP_BTN_BG = "#E1DFD6"           # Botão chanfrado neutro
XP_BTN_ACTIVE = "#D4DFD0"       # Botão ativo suave
CRT_BG = "#000000"              # Preto absoluto fósforo
CRT_FG = "#00FF66"              # Verde fósforo Matrix / CRT
CRT_CURSOR = "#33FF33"

# ======================================================================================
# MOTOR DE SANITIZAÇÃO HEURÍSTICA MULTILINGUAGEM
# ======================================================================================
EXACT_SECRET_PATTERNS = [
    # Telegram Bot Token (Ex: 8957193092:AAFSflRHyWrwGeqSygqgCMoL5OQNJqAld9M)
    (r'\b\d{8,11}:[a-zA-Z0-9_-]{34,36}\b', 'SEU_TELEGRAM_BOT_TOKEN_AQUI'),

    # GitHub Tokens (PAT clássico, fine-grained, oauth)
    (r'\bghp_[a-zA-Z0-9]{36}\b', 'ghp_SEU_GITHUB_PAT_AQUI'),
    (r'\bgithub_pat_[a-zA-Z0-9_]{60,100}\b', 'github_pat_SEU_GITHUB_PAT_AQUI'),
    (r'\bgho_[a-zA-Z0-9]{36}\b', 'gho_SEU_GITHUB_OAUTH_AQUI'),

    # Chaves de IA (OpenAI, Anthropic)
    (r'\bsk-[a-zA-Z0-9T3BlbkFJ]{30,60}\b', 'sk-SUA_CHAVE_OPENAI_AQUI'),
    (r'\bsk-ant-[a-zA-Z0-9_-]{60,100}\b', 'sk-ant-SUA_CHAVE_ANTHROPIC_AQUI'),

    # Google Cloud / Firebase API Keys
    (r'\bAIza[0-9A-Za-z-_]{35}\b', 'AIza_SUA_GOOGLE_API_KEY_AQUI'),

    # AWS Access Key ID
    (r'\b(AKIA|ABIA|ACCA|ASIA)[0-9A-Z]{16}\b', 'AKIA_SUA_AWS_ACCESS_KEY_AQUI'),

    # Generic JWT Token
    (r'\beyJ[a-zA-Z0-9_-]{10,}\.eyJ[a-zA-Z0-9_-]{10,}\.[a-zA-Z0-9_-]{10,}\b', 'SEU_JWT_TOKEN_AQUI'),

    # Telegram Chat ID numérico
    (r'((?:CHAT_ID|chat_id|AUTHORIZED_CHAT_ID|authorized_chat_id)\s*[:=]\s*)-?\d{8,12}\b', r'\g<1>0000000000')
]

GENERIC_ASSIGNMENT_PATTERNS = [
    # C/C++, Arduino e ESP32: const char* PASS = "..." ou String TOKEN = "..."
    (
        r'((?:password|passwd|pass|token|secret|api_key|apikey|auth|private_key|bot_token)\s*=\s*")[^"\r\n]+(")',
        r'\1SEU_TOKEN_AQUI\2',
        re.IGNORECASE
    ),
    # Python, JS, PHP, Ruby, Bash: pass = '...' ou token = "..."
    (
        r'((?:password|passwd|pass|token|secret|api_key|apikey|auth_token|bot_token)\s*=\s*[\'"])[^\'"\r\n]+([\'"])',
        r'\1SEU_TOKEN_AQUI\2',
        re.IGNORECASE
    ),
    # JSON / YAML / Configs: "password": "..."
    (
        r'((?:["\']?(?:password|passwd|pass|token|secret|api_key|apikey|auth)["\']?\s*[:=]\s*["\']))[^\'"\r\n]+(["\'])',
        r'\1SEU_TOKEN_AQUI\2',
        re.IGNORECASE
    )
]

IGNORE_DIRS = {
    '.git', '.build_cache', '.vscode', '.idea', '__pycache__',
    'build', 'dist', 'node_modules', '.pio', '.platformio', 'venv', '.env_dir'
}

RESTRICTED_EXACT_FILES = {
    '.env', '.env.local', 'secrets.json', 'id_rsa', 'id_dsa', 'id_ed25519',
    'Listador de Estruturas.bat'
}

RESTRICTED_EXTENSIONS = {
    '.bin', '.o', '.d', '.libsdetect.d', '.merged', '.cache', '.bat',
    '.pem', '.key', '.pkcs12', '.pfx', '.crt', '.sqlite', '.sqlite3', '.db'
}

UNIVERSAL_GITIGNORE = """# Ambientes Virtuais & Dependências Locais
node_modules/
venv/
env/
.env
.env.*
*.env

# Builds, Compilações C/C++, Arduino & ESP32
.build_cache/
build/
dist/
.pio/
*.bin
*.o
*.d
*.libsdetect.d
*.merged
*.cache
__pycache__/
*.py[cod]

# IDEs & Sistema Operacional
.vscode/
.idea/
Thumbs.db
Desktop.ini
.DS_Store

# Certificados, Chaves Privadas e Bancos Locais
*.pem
*.key
*.pfx
*.crt
*.sqlite
*.sqlite3
*.db
estrutura_*.txt
"""

# ======================================================================================
# MOTOR MDNATOR v4.0 - SCANNER DE CÓDIGO E FIRMWARE
# ======================================================================================
TEXT_CODE_EXTENSIONS = {
    '.py', '.js', '.ts', '.css', '.html', '.md', '.txt', '.json', '.xml',
    '.sql', '.java', '.c', '.cpp', '.h', '.hpp', '.cs', '.sh',
    '.bat', '.cmd', '.php', '.ino', '.io', '.properties', '.ini',
    '.yaml', '.yml', '.r', '.m', '.go', '.rs'
}

LANG_MAP = {
    '.py': 'python',
    '.js': 'javascript',
    '.ts': 'typescript',
    '.css': 'css',
    '.html': 'html',
    '.md': 'markdown',
    '.json': 'json',
    '.sql': 'sql',
    '.php': 'php',
    '.c': 'c',
    '.cpp': 'cpp',
    '.h': 'cpp',
    '.hpp': 'cpp',
    '.cs': 'csharp',
    '.bat': 'bat',
    '.cmd': 'bat',
    '.sh': 'bash',
    '.ino': 'arduino',
    '.io': 'cpp',            # PlatformIO / ESP32 header
    '.ini': 'ini',
    '.properties': 'properties',
    '.yaml': 'yaml',
    '.yml': 'yaml',
    '.go': 'go',
    '.rs': 'rust'
}

def safe_read_file_text(file_path: str) -> Tuple[str, int]:
    """Leitura resiliente multi-encoding de arquivos de código."""
    encodings = ['utf-8', 'utf-8-sig', 'latin-1', 'cp1252', 'ascii']
    for enc in encodings:
        try:
            with open(file_path, 'r', encoding=enc) as f:
                content = f.read()
                line_count = content.count('\n') + (1 if content else 0)
                return content, line_count
        except (UnicodeDecodeError, Exception):
            continue
    raise ValueError(f"Não foi possível ler o arquivo: {file_path}")


# ======================================================================================
# MOTOR INFOPLAN - ANÁLISE DE PLANILHAS EXCEL
# ======================================================================================
AMOSTRA_VALORES = 10
AMOSTRA_LINHAS = 10

def formatar_valor_planilha(valor: Any) -> str:
    if pd is not None and pd.isna(valor):
        return "[VAZIO]"
    if isinstance(valor, (datetime,)):
        return valor.strftime("%d/%m/%Y %H:%M:%S")
    if isinstance(valor, float):
        if math.isnan(valor):
            return "[VAZIO]"
        if valor.is_integer():
            return str(int(valor))
        return f"{valor:.4f}"
    return str(valor)

def identificar_tipo_serie(serie) -> str:
    if pd is None:
        return "INDETERMINADO"
    serie_valida = serie.dropna()
    if len(serie_valida) == 0:
        return "VAZIO / SEM DADOS"
    if pd.api.types.is_bool_dtype(serie):
        return "BOOLEANO"
    if pd.api.types.is_datetime64_any_dtype(serie):
        return "DATA / DATA-HORA"
    if pd.api.types.is_integer_dtype(serie):
        return "INTEIRO"
    if pd.api.types.is_float_dtype(serie):
        return "NÚMERO DECIMAL"
    if pd.api.types.is_numeric_dtype(serie):
        return "NUMÉRICO"
    if serie.dtype == "object":
        convertido = pd.to_datetime(serie_valida, errors="coerce", dayfirst=True)
        if convertido.notna().mean() >= 0.80:
            return "DATA / DATA-HORA (ARMAZENADA COMO TEXTO)"
    return "TEXTO"

def estatisticas_coluna(serie, tipo_str: str) -> List[str]:
    resultado = []
    if pd is None:
        return resultado
    validos = serie.dropna()
    if len(validos) == 0:
        return resultado

    if tipo_str in ["INTEIRO", "NÚMERO DECIMAL", "NUMÉRICO"]:
        nums = pd.to_numeric(validos, errors="coerce").dropna()
        if len(nums) > 0:
            resultado.append(f"  • Soma: {nums.sum():,.4f}")
            resultado.append(f"  • Média: {nums.mean():,.4f}")
            resultado.append(f"  • Mínimo: {nums.min()}")
            resultado.append(f"  • Máximo: {nums.max()}")
            resultado.append(f"  • Mediana: {nums.median()}")
            resultado.append(f"  • Desvio Padrão: {nums.std():,.4f}")
    elif "DATA" in tipo_str:
        datas = pd.to_datetime(validos, errors="coerce", dayfirst=True).dropna()
        if len(datas) > 0:
            resultado.append("  • Data Mínima: " + datas.min().strftime("%d/%m/%Y %H:%M:%S"))
            resultado.append("  • Data Máxima: " + datas.max().strftime("%d/%m/%Y %H:%M:%S"))
    return resultado

def gerar_relatorio_infoplan(caminho: str) -> str:
    if not PANDAS_AVAILABLE:
        raise ImportError(
            "O módulo 'pandas' não está instalado neste interpretador.\n"
            "Por favor, execute: pip install pandas openpyxl xlrd"
        )

    extensao = os.path.splitext(caminho)[1].lower()
    if extensao == ".xls":
        engine = "xlrd"
    elif extensao == ".xlsx":
        engine = "openpyxl"
    else:
        raise ValueError("Formato não suportado. Selecione um arquivo .xls ou .xlsx.")

    tamanho_bytes = os.path.getsize(caminho)
    tamanho_mb = tamanho_bytes / (1024 * 1024)
    data_modificacao = datetime.fromtimestamp(os.path.getmtime(caminho))

    todas_as_abas = pd.read_excel(caminho, sheet_name=None, engine=engine)

    relatorio = [
        "=" * 85,
        "   KANIVET XP // INFOPLAN - RADIOGRAFIA ESTRUTURAL E ESTATÍSTICA DE PLANILHA",
        "=" * 85,
        "",
        "METADADOS DO ARQUIVO:",
        "-" * 85,
        f"  Nome do Arquivo    : {os.path.basename(caminho)}",
        f"  Caminho Completo   : {os.path.abspath(caminho)}",
        f"  Extensão           : {extensao.upper()}",
        f"  Tamanho Físico     : {tamanho_bytes:,} bytes ({tamanho_mb:.2f} MB)",
        f"  Última Modificação : {data_modificacao.strftime('%d/%m/%Y %H:%M:%S')}",
        f"  Total de Abas      : {len(todas_as_abas)}",
        "",
        "ABAS DETECTADAS:",
        "-" * 85,
    ]

    for idx, nome_aba in enumerate(todas_as_abas.keys(), start=1):
        relatorio.append(f"  [{idx:02d}] {nome_aba}")

    relatorio.append("")

    for numero_aba, (nome_aba, df) in enumerate(todas_as_abas.items(), start=1):
        relatorio.extend([
            "=" * 85,
            f"ABA #{numero_aba:02d}: {nome_aba}",
            "=" * 85,
            "",
            "DIMENSÕES DA ABA:",
            "-" * 85,
        ])

        qtd_linhas = len(df)
        qtd_colunas = len(df.columns)
        relatorio.append(f"  Linhas Totais : {qtd_linhas:,}")
        relatorio.append(f"  Colunas       : {qtd_colunas:,}")

        if qtd_linhas > 0 and qtd_colunas > 0:
            celula_final = f"{get_column_letter(qtd_colunas)}{qtd_linhas + 1}"
            relatorio.append(f"  Range de Dados: A1:{celula_final}")

        relatorio.extend(["", "ANÁLISE DETALHADA DAS COLUNAS:", "-" * 85])

        for col_idx, coluna in enumerate(df.columns, start=1):
            serie = df[coluna]
            letra_col = get_column_letter(col_idx)
            tipo_detectado = identificar_tipo_serie(serie)
            total_reg = len(serie)
            preenchidos = serie.notna().sum()
            vazios = serie.isna().sum()
            pct_preenchido = (preenchidos / total_reg * 100) if total_reg > 0 else 0
            unicos = serie.nunique(dropna=True)

            relatorio.extend([
                "",
                f"  [COLUNA {col_idx:02d} | Letra: {letra_col}] => {repr(str(coluna))}",
                f"    • Tipo Heurístico      : {tipo_detectado}",
                f"    • Tipo Pandas Nativo   : {serie.dtype}",
                f"    • Registros Totais     : {total_reg:,}",
                f"    • Preenchidos / Vazios : {preenchidos:,} / {vazios:,} ({pct_preenchido:.2f}% preenchido)",
                f"    • Valores Únicos       : {unicos:,}",
            ])

            stats = estatisticas_coluna(serie, tipo_detectado)
            if stats:
                relatorio.append("    • Estatísticas Descritivas:")
                relatorio.extend(["    " + s for s in stats])

            valores_unicos = serie.dropna().astype(str).unique().tolist()
            relatorio.append(f"    • Amostra de Valores Únicos (Primeiros {AMOSTRA_VALORES}):")
            if valores_unicos:
                for v in valores_unicos[:AMOSTRA_VALORES]:
                    relatorio.append(f"        - {v}")
            else:
                relatorio.append("        [Nenhum dado legível]")

            # Amostra posicional exata de células
            relatorio.append("    • Amostra Posicional de Células:")
            qtd_amostra = min(AMOSTRA_VALORES, len(serie))
            for pos in range(qtd_amostra):
                end_cel = f"{letra_col}{pos + 2}"
                val_cel = formatar_valor_planilha(serie.iloc[pos])
                relatorio.append(f"        {end_cel} = {val_cel}")

        relatorio.extend(["", "PRIMEIRAS LINHAS DA TABELA (HEAD):", "-" * 85])
        if df.empty:
            relatorio.append("  [Aba vazia ou sem registros]")
        else:
            amostra_df = df.head(AMOSTRA_LINHAS)
            for row_idx, (_, row) in enumerate(amostra_df.iterrows(), start=2):
                relatorio.append(f"\n  Linha #{row_idx:02d}:")
                for c_i, val in enumerate(row, start=1):
                    c_nome = df.columns[c_i - 1]
                    end_c = f"{get_column_letter(c_i)}{row_idx}"
                    relatorio.append(f"    {end_c} [{c_nome}] = {formatar_valor_planilha(val)}")

        relatorio.extend(["", "BALANÇO GERAL DE PREENCHIMENTO DA ABA:", "-" * 85])
        if qtd_linhas > 0 and qtd_colunas > 0:
            total_cells = qtd_linhas * qtd_colunas
            preenchidas_total = df.notna().sum().sum()
            vazias_total = total_cells - preenchidas_total
            taxa_preenchimento = (preenchidas_total / total_cells) * 100
            relatorio.append(f"  Células Totais       : {total_cells:,}")
            relatorio.append(f"  Células Preenchidas  : {preenchidas_total:,}")
            relatorio.append(f"  Células Vazias       : {vazias_total:,}")
            relatorio.append(f"  Taxa de Ocupação     : {taxa_preenchimento:.2f}%")

        relatorio.append("")

    relatorio.extend(["=" * 85, "   [FIM DA RADIOGRAFIA INFOPLAN - KANIVET XP]", "=" * 85])
    return "\n".join(relatorio)


# ======================================================================================
# MOTOR DE TELEMETRIA DO SISTEMA / HARDWARE-Z
# ======================================================================================
def obter_telemetria_hardware() -> Dict[str, Any]:
    """Coleta telemetria profunda do hardware e do sistema operacional."""
    dados = {
        "so": f"{platform.system()} {platform.release()} (Build {platform.version()})",
        "arquitetura": platform.machine(),
        "processador": platform.processor() or "Processador Padrão",
        "python_version": platform.python_version(),
        "hostname": platform.node(),
        "cpus_logicas": os.cpu_count() or 1,
        "cpus_fisicas": "N/D",
        "ram_total": "N/D",
        "ram_usada": "N/D",
        "ram_livre": "N/D",
        "ram_percent": "N/D",
        "disco_total": "N/D",
        "disco_usado": "N/D",
        "disco_livre": "N/D",
        "disco_percent": "N/D",
        "uptime": "N/D"
    }

    if PSUTIL_AVAILABLE:
        try:
            dados["cpus_fisicas"] = psutil.cpu_count(logical=False) or "N/D"
            mem = psutil.virtual_memory()
            dados["ram_total"] = f"{mem.total / (1024**3):.2f} GB"
            dados["ram_usada"] = f"{mem.used / (1024**3):.2f} GB"
            dados["ram_livre"] = f"{mem.available / (1024**3):.2f} GB"
            dados["ram_percent"] = f"{mem.percent}%"

            disco = psutil.disk_usage(os.path.abspath(os.sep))
            dados["disco_total"] = f"{disco.total / (1024**3):.2f} GB"
            dados["disco_usado"] = f"{disco.used / (1024**3):.2f} GB"
            dados["disco_livre"] = f"{disco.free / (1024**3):.2f} GB"
            dados["disco_percent"] = f"{disco.percent}%"

            boot_time = datetime.fromtimestamp(psutil.boot_time())
            tempo_ativo = datetime.now() - boot_time
            dados["uptime"] = f"{tempo_ativo.days}d {tempo_ativo.seconds // 3600}h {(tempo_ativo.seconds // 60) % 60}m"
        except Exception:
            pass
    else:
        # Fallback padrão via shutil nativo para disco
        try:
            total, used, free = shutil.disk_usage(os.path.abspath(os.sep))
            dados["disco_total"] = f"{total / (1024**3):.2f} GB"
            dados["disco_usado"] = f"{used / (1024**3):.2f} GB"
            dados["disco_livre"] = f"{free / (1024**3):.2f} GB"
            dados["disco_percent"] = f"{(used / total) * 100:.1f}%"
        except Exception:
            pass

    return dados


# ======================================================================================
# JANELA PRINCIPAL DA APLICAÇÃO (KANIVET XP)
# ======================================================================================
class KanivetXPApp:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Kanivet XP — Cyber-Git MDnator Universal Suite [Edition 2026]")
        self.root.geometry("1080x820")
        self.root.minsize(980, 720)

        # Configuração do Estilo Visual Retro Windows XP / Java Swing
        self._configurar_estilos_retro()

        # Variáveis Globais de Estado
        self.src_project_path = tk.StringVar(value=os.path.abspath(os.getcwd()))
        self.git_name_var = tk.StringVar(value="oldboy465")
        self.git_email_var = tk.StringVar(value="167724562+oldboy465@users.noreply.github.com")
        self.repo_url_var = tk.StringVar(value="https://github.com/oldboy465/meu_projeto.git")
        self.token_var = tk.StringVar()
        self.branch_var = tk.StringVar(value="main")
        self.commit_msg_var = tk.StringVar(value="Release seguro via Kanivet XP (Sanitizado)")
        self.force_push_var = tk.BooleanVar(value=True)
        self.show_token_var = tk.BooleanVar(value=False)
        self.clone_url_var = tk.StringVar()

        # Inicia a interface e os menus
        self._construir_menu_superior()
        self._construir_layout_principal()
        self._iniciar_relogio_status()
        self._atualizar_url_remota_automatica()

        # Log inicial no console CRT
        self.log(KANIVET_ASCII_BANNER)
        self.log(f"[*] SISTEMA KANIVET XP CARREGADO COM SUCESSO [{datetime.now().strftime('%d/%m/%Y %H:%M:%S')}]")
        self.log(f"[*] DIRETÓRIO BASE ATUAL: {self.src_project_path.get()}")
        self.log("[*] AUTORIA: Philipe Sampaio Lima (@OldBoy465) — Edição 2026")
        self.log("[*] AGUARDANDO COMANDOS DO OPERADOR...")
        self.log("=" * 85)

    def _configurar_estilos_retro(self):
        """Aplica o tema 'clam' customizado com cores retro Windows XP / Java Swing."""
        self.style = ttk.Style()
        try:
            self.style.theme_use("clam")
        except Exception:
            pass

        self.root.configure(bg=XP_BG_BASE)

        # Estilização TTK para emular botões chanfrados e painéis clássicos
        self.style.configure(".", background=XP_BG_BASE, foreground="#000000", font=("Tahoma", 9))
        self.style.configure("TFrame", background=XP_BG_BASE)
        self.style.configure("TLabelframe", background=XP_BG_BASE, relief="groove")
        self.style.configure("TLabelframe.Label", background=XP_BG_BASE, foreground=XP_ACCENT, font=("Tahoma", 9, "bold"))
        self.style.configure("TLabel", background=XP_BG_BASE, font=("Tahoma", 9))
        self.style.configure("TCheckbutton", background=XP_BG_BASE, font=("Tahoma", 9))
        self.style.configure("TNotebook", background=XP_BG_BASE, tabmargins=[2, 4, 2, 0])
        self.style.configure("TNotebook.Tab", background=XP_BTN_BG, padding=[10, 4], font=("Tahoma", 9, "bold"))
        self.style.map("TNotebook.Tab", background=[("selected", XP_BG_BASE), ("active", XP_BTN_ACTIVE)])

        self.style.configure("Retro.TButton", font=("Tahoma", 9, "bold"), relief="raised", background=XP_BTN_BG, padding=4)
        self.style.map("Retro.TButton",
            background=[("pressed", "#BFBCAD"), ("active", XP_BTN_ACTIVE)],
            relief=[("pressed", "sunken")]
        )

        self.style.configure("RetroAction.TButton", font=("Tahoma", 9, "bold"), relief="raised", background="#DCE8D5", foreground="#004D00", padding=5)
        self.style.map("RetroAction.TButton",
            background=[("pressed", "#BAD1B0"), ("active", "#C8E2BD")],
            relief=[("pressed", "sunken")]
        )

        self.style.configure("RetroDanger.TButton", font=("Tahoma", 9, "bold"), relief="raised", background="#F2DEDE", foreground="#8A1F11", padding=5)
        self.style.map("RetroDanger.TButton",
            background=[("pressed", "#E4B9B9"), ("active", "#ECCACA")],
            relief=[("pressed", "sunken")]
        )

    # ----------------------------------------------------------------------------------
    # MENU SUPERIOR
    # ----------------------------------------------------------------------------------
    def _construir_menu_superior(self):
        menubar = tk.Menu(self.root, bg=XP_BG_BASE, font=("Tahoma", 9))

        # Menu Arquivo
        menu_arquivo = tk.Menu(menubar, tearoff=0, bg=XP_PANEL_BG, font=("Tahoma", 9))
        menu_arquivo.add_command(label="📁 Selecionar Pasta do Projeto...", command=self.selecionar_pasta_projeto)
        menu_arquivo.add_command(label="📂 Abrir Pasta Atual no Explorer", command=self.abrir_pasta_no_explorer)
        menu_arquivo.add_separator()
        menu_arquivo.add_command(label="🧹 Limpar Console CRT", command=self.limpar_console)
        menu_arquivo.add_separator()
        menu_arquivo.add_command(label="❌ Sair do Sistema", command=self.root.quit)
        menubar.add_cascade(label="Arquivo", menu=menu_arquivo)

        # Menu Git Baremetal
        menu_git = tk.Menu(menubar, tearoff=0, bg=XP_PANEL_BG, font=("Tahoma", 9))
        menu_git.add_command(label="git status", command=lambda: self.executar_git(["git", "status"]))
        menu_git.add_command(label="git log -n 5", command=lambda: self.executar_git(["git", "log", "-n", "5", "--oneline"]))
        menu_git.add_command(label="git diff", command=lambda: self.executar_git(["git", "diff"]))
        menu_git.add_command(label="git fetch --all", command=lambda: self.executar_git(["git", "fetch", "--all"]))
        menu_git.add_command(label="git branch -a", command=lambda: self.executar_git(["git", "branch", "-a"]))
        menu_git.add_separator()
        menu_git.add_command(label="git stash", command=lambda: self.executar_git(["git", "stash"]))
        menu_git.add_command(label="git stash pop", command=lambda: self.executar_git(["git", "stash", "pop"]))
        menubar.add_cascade(label="Operações Git", menu=menu_git)

        # Menu Ferramentas
        menu_ferramentas = tk.Menu(menubar, tearoff=0, bg=XP_PANEL_BG, font=("Tahoma", 9))
        menu_ferramentas.add_command(label="⚡ MDnator: Compilar Projeto em Markdown", command=self.mdnator_compilar_projeto)
        menu_ferramentas.add_command(label="📊 InfoPlan: Analisar Planilha Excel...", command=self.infoplan_analisar_arquivo)
        menu_ferramentas.add_command(label="🌳 Listador: Gerar Dump de Estrutura (.TXT)", command=self.gerar_dump_estrutura_txt)
        menu_ferramentas.add_separator()
        menu_ferramentas.add_command(label="💻 Hardware-Z: Diagnóstico em Tempo Real", command=self.exibir_diagnostico_hardware)
        menubar.add_cascade(label="Ferramentas", menu=menu_ferramentas)

        # Menu Ajuda
        menu_ajuda = tk.Menu(menubar, tearoff=0, bg=XP_PANEL_BG, font=("Tahoma", 9))
        menu_ajuda.add_command(label="📖 Manual do Usuário / Orientações...", command=self.abrir_manual_usuario)
        menu_ajuda.add_separator()
        menu_ajuda.add_command(label="ℹ️ Sobre o Kanivet XP...", command=self.abrir_dialogo_sobre)
        menubar.add_cascade(label="Ajuda", menu=menu_ajuda)

        self.root.config(menu=menubar)

    # ----------------------------------------------------------------------------------
    # LAYOUT PRINCIPAL (SELETOR + NOTEBOOK + CONSOLE CRT + STATUSBAR)
    # ----------------------------------------------------------------------------------
    def _construir_layout_principal(self):
        # 1. Seletor Global de Projeto (Barra Superior)
        top_frame = ttk.LabelFrame(self.root, text=" 📂 Seletor Global de Diretório / Projeto Ativo ", padding=8)
        top_frame.pack(fill=tk.X, padx=10, pady=(6, 4))

        entry_path = ttk.Entry(top_frame, textvariable=self.src_project_path, font=("Consolas", 10))
        entry_path.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 6))
        self.src_project_path.trace_add("write", lambda *args: self._atualizar_url_remota_automatica())

        btn_browse = ttk.Button(top_frame, text="Selecionar Pasta...", style="Retro.TButton", command=self.selecionar_pasta_projeto)
        btn_browse.pack(side=tk.RIGHT, padx=(0, 4))

        btn_open_exp = ttk.Button(top_frame, text="Abrir no Explorer", style="Retro.TButton", command=self.abrir_pasta_no_explorer)
        btn_open_exp.pack(side=tk.RIGHT, padx=(0, 4))

        # 2. Divisor Principal (Splitter Vertical entre Abas e Console CRT)
        self.paned = ttk.PanedWindow(self.root, orient=tk.VERTICAL)
        self.paned.pack(fill=tk.BOTH, expand=True, padx=10, pady=4)

        # Container Superior do Notebook
        notebook_container = ttk.Frame(self.paned)
        self.paned.add(notebook_container, weight=3)

        self.notebook = ttk.Notebook(notebook_container)
        self.notebook.pack(fill=tk.BOTH, expand=True)

        # Construção das 6 Abas Integradas
        self._construir_aba_sanitizador()
        self._construir_aba_git_central()
        self._construir_aba_mdnator()
        self._construir_aba_infoplan()
        self._construir_aba_listador_tree()
        self._construir_aba_hardware_z()

        # Container Inferior do Console CRT Retro
        crt_frame = ttk.LabelFrame(self.paned, text=" 💻 Console CRT Retro em Tempo Real (Fósforo Verde) ", padding=4)
        self.paned.add(crt_frame, weight=2)

        # Barra de ferramentas do Console
        crt_toolbar = ttk.Frame(crt_frame)
        crt_toolbar.pack(fill=tk.X, pady=(0, 2))

        ttk.Label(crt_toolbar, text="STATUS OPERACIONAL: CONEXÃO NATIVA ESTABELECIDA", font=("Tahoma", 8, "bold"), foreground="#005500").pack(side=tk.LEFT)
        btn_clear_log = ttk.Button(crt_toolbar, text="Limpar Terminal", style="Retro.TButton", command=self.limpar_console)
        btn_clear_log.pack(side=tk.RIGHT)

        self.console_text = scrolledtext.ScrolledText(
            crt_frame,
            wrap=tk.WORD,
            bg=CRT_BG,
            fg=CRT_FG,
            insertbackground=CRT_CURSOR,
            font=("Consolas", 9),
            relief="sunken",
            bd=2
        )
        self.console_text.pack(fill=tk.BOTH, expand=True)

        # 3. Barra de Status Retro Inferior
        self.status_bar = ttk.Frame(self.root, relief="sunken", padding=(6, 3))
        self.status_bar.pack(fill=tk.X, side=tk.BOTTOM)

        self.lbl_status_msg = ttk.Label(self.status_bar, text="Pronto.", font=("Tahoma", 8))
        self.lbl_status_msg.pack(side=tk.LEFT)

        self.lbl_relogio = ttk.Label(self.status_bar, text="", font=("Tahoma", 8, "bold"))
        self.lbl_relogio.pack(side=tk.RIGHT, padx=5)

    def _iniciar_relogio_status(self):
        """Atualiza o relógio em tempo real na barra de status."""
        agora = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        self.lbl_relogio.config(text=f"🕐 {agora} | Kanivet XP v5.0")
        self.root.after(1000, self._iniciar_relogio_status)

    def _atualizar_url_remota_automatica(self):
        """Deduz automaticamente o nome da pasta do projeto e monta a URL do GitHub."""
        caminho = self.src_project_path.get().strip()
        if caminho:
            nome_pasta = os.path.basename(os.path.normpath(caminho))
            usuario = self.git_name_var.get().strip() or "usuario"
            if nome_pasta:
                self.repo_url_var.set(f"https://github.com/{usuario}/{nome_pasta}.git")

    def log(self, texto: str):
        """Imprime mensagem no console CRT retro de forma thread-safe."""
        def _append():
            self.console_text.insert(tk.END, texto + "\n")
            self.console_text.see(tk.END)
        self.root.after(0, _append)

    def set_status(self, msg: str):
        """Atualiza a mensagem na status bar inferior."""
        self.root.after(0, lambda: self.lbl_status_msg.config(text=msg))

    def limpar_console(self):
        self.console_text.delete("1.0", tk.END)

    def selecionar_pasta_projeto(self):
        pasta = filedialog.askdirectory(title="Selecione o Diretório do Projeto", initialdir=self.src_project_path.get())
        if pasta:
            self.src_project_path.set(pasta)
            self.log(f"[DIRETÓRIO] Novo projeto ativo conectado: {pasta}")

    def abrir_pasta_no_explorer(self):
        caminho = self.src_project_path.get().strip()
        if not os.path.exists(caminho):
            messagebox.showwarning("Aviso", "O caminho selecionado não existe!")
            return
        try:
            if platform.system() == "Windows":
                os.startfile(caminho)
            elif platform.system() == "Darwin":
                subprocess.Popen(["open", caminho])
            else:
                subprocess.Popen(["xdg-open", caminho])
        except Exception as e:
            messagebox.showerror("Erro", f"Não foi possível abrir o gerenciador de arquivos:\n{e}")

    # ==================================================================================
    # ABA 1: DEPLOY & SANITIZADOR UNIVERSAL DE CÓDIGO
    # ==================================================================================
    def _construir_aba_sanitizador(self):
        tab = ttk.Frame(self.notebook, padding=10)
        self.notebook.add(tab, text="🛡️ Sanitizador & Git Pusher")

        # Container em Grid
        grid_frame = ttk.LabelFrame(tab, text=" Parâmetros de Identificação Git & Segurança de Deploy ", padding=10)
        grid_frame.pack(fill=tk.X, pady=(0, 10))

        ttk.Label(grid_frame, text="Git user.name:").grid(row=0, column=0, sticky=tk.W, pady=3)
        ttk.Entry(grid_frame, textvariable=self.git_name_var, width=30).grid(row=0, column=1, sticky=tk.W, padx=6, pady=3)

        ttk.Label(grid_frame, text="Git user.email:").grid(row=1, column=0, sticky=tk.W, pady=3)
        ttk.Entry(grid_frame, textvariable=self.git_email_var, width=50).grid(row=1, column=1, sticky=tk.EW, padx=6, pady=3)

        ttk.Label(grid_frame, text="URL do Repositório:").grid(row=2, column=0, sticky=tk.W, pady=3)
        ttk.Entry(grid_frame, textvariable=self.repo_url_var, width=50).grid(row=2, column=1, sticky=tk.EW, padx=6, pady=3)

        ttk.Label(grid_frame, text="GitHub Token (PAT):").grid(row=3, column=0, sticky=tk.W, pady=3)
        token_sub = ttk.Frame(grid_frame)
        token_sub.grid(row=3, column=1, sticky=tk.EW, padx=6, pady=3)

        self.entry_token = ttk.Entry(token_sub, textvariable=self.token_var, show="*")
        self.entry_token.pack(side=tk.LEFT, fill=tk.X, expand=True)

        ttk.Checkbutton(
            token_sub,
            text="Mostrar",
            variable=self.show_token_var,
            command=self._toggle_token_visibility
        ).pack(side=tk.RIGHT, padx=(6, 0))

        ttk.Label(grid_frame, text="Mensagem de Commit:").grid(row=4, column=0, sticky=tk.W, pady=3)
        ttk.Entry(grid_frame, textvariable=self.commit_msg_var, width=50).grid(row=4, column=1, sticky=tk.EW, padx=6, pady=3)

        ttk.Label(grid_frame, text="Opções de Envio:").grid(row=5, column=0, sticky=tk.W, pady=3)
        opts_sub = ttk.Frame(grid_frame)
        opts_sub.grid(row=5, column=1, sticky=tk.W, padx=6, pady=3)

        ttk.Label(opts_sub, text="Branch:").pack(side=tk.LEFT)
        ttk.Entry(opts_sub, textvariable=self.branch_var, width=12).pack(side=tk.LEFT, padx=(4, 15))

        ttk.Checkbutton(opts_sub, text="Forçar Envio (--force)", variable=self.force_push_var).pack(side=tk.LEFT)

        grid_frame.columnconfigure(1, weight=1)

        # Botão de Ação em Destaque
        self.btn_run_sanitizer = ttk.Button(
            tab,
            text="🛡️ SANITIZAR PROJETO INTEIRO & ENVIAR AO GITHUB COM PAT",
            style="RetroAction.TButton",
            command=self.iniciar_pipeline_sanitizacao
        )
        self.btn_run_sanitizer.pack(fill=tk.X, ipady=6, pady=5)

        # Informações de Regras Ativas
        info_frame = ttk.LabelFrame(tab, text=" Heurística de Neutralização Ativa ", padding=8)
        info_frame.pack(fill=tk.BOTH, expand=True, pady=(5, 0))

        info_text = (
            "• Neutralização Exata: Telegram Bot Tokens, Chat IDs, GitHub PAT/OAuth, OpenAI/Claude API Keys,\n"
            "  Google Cloud AIza, AWS Access Keys, JWT Tokens assinados.\n"
            "• Neutralização Heurística em Código: Declarações sensíveis de 'password', 'secret', 'token', 'api_key'\n"
            "  em Python, C/C++, Arduino (.ino/.io), JavaScript, JSON, YAML e Shell Scripts.\n"
            "• Proteção de Arquivos: .env, certificados (.pem, .key), bancos de dados (.db, .sqlite) e pastas de build\n"
            "  são completamente bloqueados e excluídos do repositório final de publicação."
        )
        ttk.Label(info_frame, text=info_text, justify=tk.LEFT, foreground="#2A4B7C").pack(anchor=tk.W)

    def _toggle_token_visibility(self):
        self.entry_token.config(show="" if self.show_token_var.get() else "*")

    def sanitizar_codigo(self, nome_arquivo: str, conteudo: str) -> Tuple[str, bool]:
        """Aplica heurística profunda de regex para neutralizar segredos."""
        modificado = conteudo
        alterado = False

        # 1. Padrões Exatos de Chaves
        for padrao, substituto in EXACT_SECRET_PATTERNS:
            if re.search(padrao, modificado):
                modificado = re.sub(padrao, substituto, modificado)
                alterado = True

        # 2. Atribuições Genéricas em Código
        for padrao, substituto, flags in GENERIC_ASSIGNMENT_PATTERNS:
            if re.search(padrao, modificado, flags=flags):
                modificado = re.sub(padrao, substituto, modificado, flags=flags)
                alterado = True

        return modificado, alterado

    def iniciar_pipeline_sanitizacao(self):
        caminho_origem = self.src_project_path.get().strip()
        if not os.path.exists(caminho_origem):
            messagebox.showerror("Erro", "O diretório do projeto ativo informado não existe!")
            return

        self.btn_run_sanitizer.config(state=tk.DISABLED)
        self.set_status("Sanitizando e enviando projeto ao GitHub...")

        threading.Thread(target=self._worker_sanitizacao_e_deploy, daemon=True).start()

    def _worker_sanitizacao_e_deploy(self):
        src = os.path.abspath(self.src_project_path.get().strip())
        nome_pasta = os.path.basename(src)
        dir_pai = os.path.dirname(src)
        dest = os.path.join(dir_pai, f"{nome_pasta}_clean_export")
        repo_url = self.repo_url_var.get().strip()
        branch = self.branch_var.get().strip()
        user_name = self.git_name_var.get().strip()
        user_email = self.git_email_var.get().strip()
        token = self.token_var.get().strip()
        commit_msg = self.commit_msg_var.get().strip() or "Release seguro via Kanivet XP"
        force_push = self.force_push_var.get()

        try:
            self.log("=" * 80)
            self.log("INICIANDO MOTOR UNIVERSAL DE SANITIZAÇÃO HEURÍSTICA & DEPLOY")
            self.log(f"Projeto : {nome_pasta}")
            self.log(f"Origem  : {src}")
            self.log(f"Destino : {dest}")
            self.log(f"Autor   : {user_name} <{user_email}>")
            self.log("=" * 80)

            # Preserva metadados Git se já existirem no destino para agilizar deltas
            git_backup_dir = os.path.join(dest, ".git")
            temp_git_dir = os.path.join(dir_pai, f"_temp_git_{nome_pasta}")
            has_existing_git = os.path.exists(git_backup_dir)

            if os.path.exists(dest):
                self.log("[+] Limpando diretório de exportação limpa anterior...")
                if has_existing_git:
                    if os.path.exists(temp_git_dir):
                        shutil.rmtree(temp_git_dir)
                    shutil.move(git_backup_dir, temp_git_dir)

                shutil.rmtree(dest)
                os.makedirs(dest)

                if has_existing_git and os.path.exists(temp_git_dir):
                    shutil.move(temp_git_dir, git_backup_dir)
            else:
                os.makedirs(dest)

            total_copiados = 0
            sanitizados_count = 0

            # Cópia Seletiva e Sanitização Profunda
            for root, dirs, files in os.walk(src):
                dirs[:] = [d for d in dirs if d not in IGNORE_DIRS]

                rel_path = os.path.relpath(root, src)
                target_root = dest if rel_path == "." else os.path.join(dest, rel_path)
                os.makedirs(target_root, exist_ok=True)

                for f in files:
                    _, ext = os.path.splitext(f)
                    lower_f = f.lower()

                    if ext.lower() in RESTRICTED_EXTENSIONS or f in RESTRICTED_EXACT_FILES:
                        self.log(f"[BLOQUEADO] Arquivo proibido/sensível descartado: {f}")
                        continue
                    if lower_f.startswith("estrutura_") or lower_f.startswith(".env"):
                        self.log(f"[BLOQUEADO] Arquivo de ambiente/dump ignorado: {f}")
                        continue

                    src_file = os.path.join(root, f)
                    dest_file = os.path.join(target_root, f)

                    try:
                        with open(src_file, "r", encoding="utf-8", errors="ignore") as rf:
                            raw_code = rf.read()

                        clean_code, changed = self.sanitizar_codigo(f, raw_code)

                        with open(dest_file, "w", encoding="utf-8") as wf:
                            wf.write(clean_code)

                        if changed:
                            sanitizados_count += 1
                            self.log(f"[HIGIENIZADO] Segredo neutralizado em: {f}")
                        else:
                            self.log(f"[SEGURO] {f}")
                    except Exception:
                        shutil.copy2(src_file, dest_file)
                        self.log(f"[BINÁRIO] Copiado diretamente: {f}")

                    total_copiados += 1

            # Criação do .gitignore universal
            gitignore_path = os.path.join(dest, ".gitignore")
            with open(gitignore_path, "w", encoding="utf-8") as gf:
                gf.write(UNIVERSAL_GITIGNORE.strip())
            self.log("[+] Arquivo .gitignore universal gerado com sucesso.")

            self.log(f"\n[ESTATÍSTICAS] {total_copiados} arquivos exportados | {sanitizados_count} arquivos higienizados.")

            # Pipeline de Comandos Git
            def _exec_git(args, mask_log=False):
                cmd_str = " ".join(args)
                if not mask_log:
                    self.log(f"> {cmd_str}")
                p = subprocess.run(args, cwd=dest, capture_output=True, text=True, shell=True)
                if p.stdout.strip():
                    self.log(p.stdout.strip())
                if p.stderr.strip() and p.returncode != 0:
                    self.log(f"[AVISO GIT] {p.stderr.strip()}")
                return p.returncode

            self.log("\n[GIT] Inicializando repositório limpo e configurando identidade...")

            if not os.path.exists(os.path.join(dest, ".git")):
                _exec_git(["git", "init"])

            _exec_git(["git", "config", "user.name", f'"{user_name}"'])
            _exec_git(["git", "config", "user.email", f'"{user_email}"'])

            target_push_url = repo_url
            if token:
                if "https://" in repo_url:
                    clean_host = repo_url.replace("https://", "")
                    if "@" in clean_host:
                        clean_host = clean_host.split("@", 1)[1]
                    target_push_url = f"https://{user_name}:{token}@{clean_host}"
                    self.log("[AUTH] Personal Access Token anexado ao transporte HTTPS.")

            _exec_git(["git", "remote", "remove", "origin"])
            _exec_git(["git", "remote", "add", "origin", target_push_url], mask_log=bool(token))
            _exec_git(["git", "branch", "-M", branch])
            _exec_git(["git", "add", "."])

            commit_res = _exec_git(["git", "commit", "-m", f'"{commit_msg}"'])
            if commit_res != 0:
                self.log("[INFO] Nenhuma alteração nova detectada na árvore para comitar.")

            self.log(f"\n[GIT] Enviando projeto para a branch '{branch}' no GitHub...")
            push_cmd = ["git", "push", "-u", "origin", branch]
            if force_push:
                push_cmd.append("--force")

            push_res = _exec_git(push_cmd, mask_log=bool(token))

            if push_res == 0:
                self.log("\n" + "═" * 70)
                self.log("🚀 SUCESSO ABSOLUTO: REPOSITÓRIO ENVIADO E SEGURO!")
                self.log("═" * 70)
                self.root.after(0, lambda: messagebox.showinfo(
                    "Sucesso Absoluto",
                    f"O projeto '{nome_pasta}' foi sanitizado e enviado com sucesso ao GitHub!\n\nPasta limpa gerada em:\n{dest}"
                ))
            else:
                self.log("\n❌ Falha na autorização de push remoto.")
                self.log("Verifique se o seu Token de Acesso Pessoal (PAT) possui permissão 'repo' ativada.")
                self.root.after(0, lambda: messagebox.showwarning(
                    "Autenticação Necessária",
                    "O envio foi recusado pelo GitHub. Certifique-se de que o Token PAT foi informado e tem permissão de escrita ('repo')."
                ))

        except Exception as e:
            self.log(f"\n[ERRO CRÍTICO] Falha durante a sanitização: {e}")
            self.root.after(0, lambda: messagebox.showerror("Erro Crítico", str(e)))
        finally:
            self.root.after(0, lambda: self.btn_run_sanitizer.config(state=tk.NORMAL))
            self.set_status("Pronto.")

    # ==================================================================================
    # ABA 2: CENTRAL DE OPERAÇÕES GIT (12+ FUNÇÕES BAREMETAL)
    # ==================================================================================
    def _construir_aba_git_central(self):
        tab = ttk.Frame(self.notebook, padding=10)
        self.notebook.add(tab, text="🌿 Central Git Baremetal")

        grid_frame = ttk.LabelFrame(tab, text=" Painel de Comandos Git em Tempo Real ", padding=8)
        grid_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))

        # 12 Funções descritivas em Grade
        botoes_git = [
            ("git status", "Verificar modificações e arquivos staged", lambda: self.executar_git(["git", "status"])),
            ("git log -n 5", "Visualizar os 5 últimos commits da árvore", lambda: self.executar_git(["git", "log", "-n", "5", "--oneline", "--graph", "--decorate"])),
            ("git diff", "Comparar linha a linha as alterações locais", lambda: self.executar_git(["git", "diff"])),
            ("git fetch --all", "Baixar referências e ponteiros remotos", lambda: self.executar_git(["git", "fetch", "--all"])),
            ("git pull", "Puxar e mesclar atualizações da branch ativa", lambda: self.executar_git(["git", "pull", "origin", self.branch_var.get().strip()])),
            ("git add .", "Adicionar todas as alterações ao Stage", lambda: self.executar_git(["git", "add", "."])),
            ("git commit -m", "Gravar alterações usando a mensagem definida", lambda: self.executar_git(["git", "commit", "-m", f'"{self.commit_msg_var.get().strip()}"'])),
            ("git push", "Enviar commits locais para o servidor remoto", lambda: self.executar_git(["git", "push", "origin", self.branch_var.get().strip()])),
            ("git remote -v", "Listar endereços dos servidores remotos", lambda: self.executar_git(["git", "remote", "-v"])),
            ("git branch -a", "Exibir todas as ramificações locais e remotas", lambda: self.executar_git(["git", "branch", "-a"])),
            ("git stash", "Salvar temporariamente alterações em progresso", lambda: self.executar_git(["git", "stash"])),
            ("git stash pop", "Restaurar alterações salvas do stash", lambda: self.executar_git(["git", "stash", "pop"]))
        ]

        for i, (cmd_name, desc, func) in enumerate(botoes_git):
            r = i // 2
            c = i % 2
            cell_frame = ttk.Frame(grid_frame, padding=4)
            cell_frame.grid(row=r, column=c, sticky=tk.EW, padx=5, pady=3)

            btn = ttk.Button(cell_frame, text=cmd_name, style="Retro.TButton", command=func, width=18)
            btn.pack(side=tk.LEFT, padx=(0, 6))

            lbl_desc = ttk.Label(cell_frame, text=desc, font=("Tahoma", 8), foreground="#444444")
            lbl_desc.pack(side=tk.LEFT, fill=tk.X, expand=True)

        grid_frame.columnconfigure(0, weight=1)
        grid_frame.columnconfigure(1, weight=1)

        # Painel Inferior de Clonagem
        clone_frame = ttk.LabelFrame(tab, text=" Clonar Repositório Remoto (git clone) ", padding=8)
        clone_frame.pack(fill=tk.X)

        ttk.Label(clone_frame, text="URL do Repositório:").pack(side=tk.LEFT, padx=(0, 6))
        ttk.Entry(clone_frame, textvariable=self.clone_url_var, font=("Consolas", 9)).pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 6))
        ttk.Button(clone_frame, text="Clonar Repositório...", style="RetroAction.TButton", command=self.executar_git_clone).pack(side=tk.RIGHT)

    def executar_git(self, args: List[str]):
        """Executa um comando Git na pasta ativa em thread separada."""
        caminho = self.src_project_path.get().strip()
        if not os.path.exists(caminho):
            messagebox.showwarning("Aviso", "O diretório do projeto ativo informado não existe!")
            return

        def _worker():
            cmd_str = " ".join(args)
            self.log(f"\n[GIT EXEC] {cmd_str} (em: {caminho})")
            self.set_status(f"Executando {cmd_str}...")
            try:
                p = subprocess.run(args, cwd=caminho, capture_output=True, text=True, shell=True)
                if p.stdout.strip():
                    self.log(p.stdout.strip())
                if p.stderr.strip():
                    self.log(f"[SAÍDA STDERR] {p.stderr.strip()}")
                if p.returncode == 0:
                    self.log(f"[GIT OK] Comando concluído com código 0.")
                else:
                    self.log(f"[GIT AVISO] Comando finalizou com código {p.returncode}.")
            except Exception as e:
                self.log(f"[ERRO GIT] Falha ao invocar processo: {e}")
            finally:
                self.set_status("Pronto.")

        threading.Thread(target=_worker, daemon=True).start()

    def executar_git_clone(self):
        url = self.clone_url_var.get().strip()
        if not url:
            messagebox.showwarning("Aviso", "Insira a URL do repositório a ser clonado!")
            return

        pasta_destino = filedialog.askdirectory(title="Selecione a Pasta de Destino para o Clone")
        if not pasta_destino:
            return

        def _worker():
            self.log(f"\n[GIT CLONE] Clonando {url} para: {pasta_destino}")
            self.set_status("Clonando repositório remoto...")
            try:
                p = subprocess.run(["git", "clone", url], cwd=pasta_destino, capture_output=True, text=True, shell=True)
                if p.stdout.strip():
                    self.log(p.stdout.strip())
                if p.stderr.strip():
                    self.log(p.stderr.strip())

                if p.returncode == 0:
                    self.log("[CLONE SUCESSO] Repositório clonado com êxito!")
                    self.root.after(0, lambda: messagebox.showinfo("Sucesso", "Repositório clonado com sucesso!"))
                else:
                    self.log(f"[CLONE FALHA] Código de erro: {p.returncode}")
                    self.root.after(0, lambda: messagebox.showerror("Erro de Clone", "Não foi possível clonar o repositório."))
            except Exception as e:
                self.log(f"[ERRO CLONE] {e}")
            finally:
                self.set_status("Pronto.")

        threading.Thread(target=_worker, daemon=True).start()

    # ==================================================================================
    # ABA 3: MDNATOR v4.0 (COMPILAÇÃO DE PROJETO EM MARKDOWN)
    # ==================================================================================
    def _construir_aba_mdnator(self):
        tab = ttk.Frame(self.notebook, padding=10)
        self.notebook.add(tab, text="⚡ Motor MDnator v4.0")

        header_frame = ttk.LabelFrame(tab, text=" Transformação Universal de Códigos & Firmware Embarcado ", padding=10)
        header_frame.pack(fill=tk.X, pady=(0, 10))

        desc_text = (
            "O Motor MDnator v4.0 varre profundamente pastas de software, projetos ESP32, Arduino Uno,\n"
            "Full-Stack Python, C/C++, Java e scripts, compilando todo o código-fonte e a árvore de diretórios\n"
            "em um único arquivo Markdown (.md) estruturado com badges de linguagem, ideal para documentação ou LLMs."
        )
        ttk.Label(header_frame, text=desc_text, justify=tk.LEFT).pack(anchor=tk.W)

        btn_box = ttk.Frame(tab)
        btn_box.pack(fill=tk.X, pady=8)

        btn_compilar = ttk.Button(
            btn_box,
            text="⚡ COMPILAR PROJETO ATIVO EM MARKDOWN ÚNICO (.MD)",
            style="RetroAction.TButton",
            command=self.mdnator_compilar_projeto
        )
        btn_compilar.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 6), ipady=5)

        btn_metricas = ttk.Button(
            btn_box,
            text="📊 INSPECIONAR MÉTRICAS DE CÓDIGO",
            style="Retro.TButton",
            command=self.mdnator_inspecionar_metricas
        )
        btn_metricas.pack(side=tk.RIGHT, fill=tk.X, expand=True, padx=(6, 0), ipady=5)

        # Quadro de Extensões Suportadas
        ext_frame = ttk.LabelFrame(tab, text=" Formatos e Linguagens Mapeadas Nativamente ", padding=8)
        ext_frame.pack(fill=tk.BOTH, expand=True, pady=(5, 0))

        ext_info = (
            "• Firmware Embarcado : Arduino Sketch (.ino), PlatformIO / ESP32 Header (.io), C (.c), C++ (.cpp, .h, .hpp)\n"
            "• Web & Scripts      : Python (.py), TypeScript (.ts), JavaScript (.js), HTML (.html), CSS (.css), PHP (.php)\n"
            "• Dados & Configs    : JSON (.json), XML (.xml), YAML (.yaml, .yml), SQL (.sql), INI (.ini), Properties\n"
            "• Documentos & Texto : Markdown (.md), Text Files (.txt), Shell Scripts (.sh, .bat, .cmd)\n\n"
            "Diretórios ignorados por padrão: __pycache__, .git, .vscode, .pio, node_modules, venv, build, dist."
        )
        ttk.Label(ext_frame, text=ext_info, justify=tk.LEFT, foreground="#2C4E34").pack(anchor=tk.W)

    def mdnator_inspecionar_metricas(self):
        caminho = self.src_project_path.get().strip()
        if not os.path.exists(caminho):
            messagebox.showwarning("Aviso", "O diretório informado não existe!")
            return

        def _worker():
            self.set_status("Inspecionando métricas de código...")
            self.log(f"\n[MDNATOR MÉTRICAS] Inspecionando: {caminho}")
            total_arquivos = 0
            total_linhas = 0
            contagem_ext = {}

            for dirpath, dirnames, filenames in os.walk(caminho):
                dirnames[:] = [d for d in dirnames if d not in IGNORE_DIRS]
                for f in filenames:
                    _, ext = os.path.splitext(f)
                    ext_lower = ext.lower()
                    if ext_lower in TEXT_CODE_EXTENSIONS:
                        total_arquivos += 1
                        contagem_ext[ext_lower] = contagem_ext.get(ext_lower, 0) + 1
                        full_p = os.path.join(dirpath, f)
                        try:
                            _, l_count = safe_read_file_text(full_p)
                            total_linhas += l_count
                        except Exception:
                            pass

            self.log("=" * 60)
            self.log(f"MÉTRICAS DO PROJETO: {os.path.basename(caminho)}")
            self.log(f"  • Total de Arquivos Elegíveis : {total_arquivos:,}")
            self.log(f"  • Linhas de Código Estimadas  : {total_linhas:,}")
            self.log("  • Distribuição por Formato:")
            for ext, count in sorted(contagem_ext.items(), key=lambda x: x[1], reverse=True):
                self.log(f"      {ext:10s} : {count:4d} arquivo(s)")
            self.log("=" * 60)
            self.set_status("Pronto.")

        threading.Thread(target=_worker, daemon=True).start()

    def mdnator_compilar_projeto(self):
        caminho = self.src_project_path.get().strip()
        if not os.path.exists(caminho):
            messagebox.showwarning("Aviso", "O diretório informado não existe!")
            return

        nome_projeto = os.path.basename(os.path.normpath(caminho)) or "projeto"
        sugestao_saida = os.path.join(caminho, f"{nome_projeto}_MDNATOR_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md")

        caminho_saida = filedialog.asksaveasfilename(
            title="Salvar Compilação Markdown do MDnator",
            defaultextension=".md",
            initialfile=os.path.basename(sugestao_saida),
            filetypes=[("Documentos Markdown", "*.md"), ("Arquivos de Texto", "*.txt"), ("Todos os Arquivos", "*.*")]
        )
        if not caminho_saida:
            return

        def _worker():
            self.set_status("Compilando projeto em Markdown...")
            self.log(f"\n[MDNATOR v4.0] Iniciando varredura profunda em: {caminho}")

            estrutura = [
                f"# 🟩 KANIVET XP // MDNATOR v4.0 - COMPILAÇÃO DE CÓDIGO & FIRMWARE\n\n",
                f"> **Projeto Alvo:** `{nome_projeto}`\n",
                f"> **Caminho Host:** `{caminho}`\n",
                f"> **Data de Geração:** `{datetime.now().strftime('%d/%m/%Y %H:%M:%S')}`\n",
                f"> **Compilador Base:** `MDnator Matrix Engine / Cyber-Git Suite`\n\n",
                "---\n\n",
                "## 🌳 Mapeamento de Diretórios (Árvore do Projeto)\n\n```text\n"
            ]
            conteudos = ["\n\n## 📄 Códigos-Fonte e Firmware Embarcado Decodificados\n\n"]

            total_arquivos = 0
            total_linhas = 0

            for dirpath, dirnames, filenames in os.walk(caminho):
                dirnames[:] = [d for d in dirnames if d not in IGNORE_DIRS]
                rel_dir = os.path.relpath(dirpath, caminho)
                prefixo = "" if rel_dir == "." else "│   " * (rel_dir.count(os.sep) + 1)

                if rel_dir != ".":
                    estrutura.append(f"{'│   ' * rel_dir.count(os.sep)}├── 📁 {os.path.basename(dirpath)}/\n")

                for filename in filenames:
                    _, ext = os.path.splitext(filename)
                    if ext.lower() in TEXT_CODE_EXTENSIONS:
                        f_path = os.path.join(dirpath, filename)
                        rel_file = os.path.relpath(f_path, caminho)
                        estrutura.append(f"{prefixo}├── 💾 {filename}\n")
                        total_arquivos += 1

                        lang = LANG_MAP.get(ext.lower(), "")
                        badge_tag = ""
                        if ext.lower() in ['.io', '.ino']:
                            badge_tag = " [FIRMWARE EMBARCADO ESP32 / ARDUINO]"

                        try:
                            code_content, l_count = safe_read_file_text(f_path)
                            total_linhas += l_count
                            conteudos.append(
                                f"\n### 💾 Módulo: `{rel_file}` ({l_count} linhas){badge_tag}\n\n"
                                f"```{lang}\n{code_content}\n```\n\n---\n"
                            )
                        except Exception as e:
                            conteudos.append(
                                f"\n### 💾 Módulo: `{rel_file}` (ERRO DE LEITURA){badge_tag}\n\n"
                                f"```{lang}\n// Falha ao descriptografar arquivo: {str(e)}\n```\n\n---\n"
                            )

            estrutura.append("```\n")
            resumo = (
                f"\n> **Métricas Finais da Ingestão:** {total_arquivos:,} arquivos compilados com sucesso, "
                f"totalizando {total_linhas:,} linhas de código.\n\n---\n"
            )

            relatorio_final = "".join(estrutura) + resumo + "".join(conteudos)

            try:
                with open(caminho_saida, "w", encoding="utf-8") as wf:
                    wf.write(relatorio_final)

                self.log(f"[MDNATOR SUCESSO] Arquivo Markdown gravado com êxito:\n  {caminho_saida}")
                self.root.after(0, lambda: messagebox.showinfo(
                    "MDnator Concluído",
                    f"Projeto compilado com sucesso em arquivo Markdown único!\n\nSalvo em:\n{caminho_saida}"
                ))
            except Exception as e:
                self.log(f"[MDNATOR ERRO] Falha de gravação: {e}")
                self.root.after(0, lambda: messagebox.showerror("Erro de Gravação", str(e)))
            finally:
                self.set_status("Pronto.")

        threading.Thread(target=_worker, daemon=True).start()

    # ==================================================================================
    # ABA 4: INFOPLAN (ANALISADOR DE PLANILHAS EXCEL)
    # ==================================================================================
    def _construir_aba_infoplan(self):
        tab = ttk.Frame(self.notebook, padding=10)
        self.notebook.add(tab, text="📊 Módulo InfoPlan")

        header_frame = ttk.LabelFrame(tab, text=" Engenharia Reversa e Diagnóstico Estatístico de Planilhas Excel ", padding=10)
        header_frame.pack(fill=tk.X, pady=(0, 10))

        info_text = (
            "O Módulo InfoPlan realiza a radiografia estrutural, dimensional e estatística completa\n"
            "de qualquer planilha nos formatos .XLSX e .XLS. Identifica dimensões de cada aba, percentual\n"
            "de preenchimento, tipos heurísticos de dados, estatísticas de dispersão e gera amostras posicionais de células."
        )
        ttk.Label(header_frame, text=info_text, justify=tk.LEFT).pack(anchor=tk.W)

        btn_box = ttk.Frame(tab)
        btn_box.pack(fill=tk.X, pady=8)

        btn_analisar = ttk.Button(
            btn_box,
            text="📊 SELECIONAR PLANILHA E GERAR RELATÓRIO COMPLETO...",
            style="RetroAction.TButton",
            command=self.infoplan_analisar_arquivo
        )
        btn_analisar.pack(fill=tk.X, ipady=6)

        # Informações sobre Bibliotecas
        diag_frame = ttk.LabelFrame(tab, text=" Estado das Bibliotecas de Análise no Ambiente ", padding=8)
        diag_frame.pack(fill=tk.BOTH, expand=True, pady=(5, 0))

        status_pandas = "INSTALADO / ATIVO" if PANDAS_AVAILABLE else "NÃO DETECTADO (Execute: pip install pandas openpyxl xlrd)"
        status_openpyxl = "INSTALADO / ATIVO" if OPENPYXL_AVAILABLE else "MODO FALLBACK PURO ATIVO"

        diag_content = (
            f"• Motor Pandas Engine   : {status_pandas}\n"
            f"• Motor Openpyxl Utils  : {status_openpyxl}\n\n"
            "Métricas extraídas em cada relatório:\n"
            "  - Metadados do arquivo (bytes, MB, última alteração e contagem de abas).\n"
            "  - Dimensões por aba (linhas, colunas e range aproximado de células, ex: A1:H500).\n"
            "  - Tipagem automática por coluna: Booleano, Inteiro, Decimal, Data, Texto, Vazio.\n"
            "  - Estatísticas de dispersão: Soma, Média, Mínimo, Máximo, Mediana, Desvio Padrão.\n"
            "  - Amostra das primeiras 10 linhas e células mapeadas."
        )
        ttk.Label(diag_frame, text=diag_content, justify=tk.LEFT, foreground="#1B3A57").pack(anchor=tk.W)

    def infoplan_analisar_arquivo(self):
        caminho = filedialog.askopenfilename(
            title="Selecione a Planilha Excel para Análise",
            filetypes=[
                ("Planilhas Excel (*.xlsx;*.xls)", "*.xlsx *.xls"),
                ("Excel XLSX", "*.xlsx"),
                ("Excel XLS", "*.xls"),
                ("Todos os Arquivos", "*.*")
            ]
        )
        if not caminho:
            return

        def _worker():
            self.set_status("Analisando planilha com InfoPlan...")
            self.log(f"\n[INFOPLAN] Iniciando diagnóstico estrutural de: {os.path.basename(caminho)}")

            try:
                relatorio = gerar_relatorio_infoplan(caminho)

                nome_base = os.path.splitext(os.path.basename(caminho))[0]
                sugestao_saida = f"{nome_base}_INFOPLAN_RADIOGRAFIA.txt"

                def _salvar_dialog():
                    caminho_saida = filedialog.asksaveasfilename(
                        title="Salvar Radiografia da Planilha",
                        defaultextension=".txt",
                        initialfile=sugestao_saida,
                        filetypes=[("Arquivo de Texto", "*.txt"), ("Markdown", "*.md"), ("Todos os Arquivos", "*.*")]
                    )
                    if caminho_saida:
                        with open(caminho_saida, "w", encoding="utf-8") as f:
                            f.write(relatorio)
                        self.log(f"[INFOPLAN SUCESSO] Relatório salvo em:\n  {caminho_saida}")
                        messagebox.showinfo("Sucesso", f"Planilha analisada com sucesso!\n\nRelatório salvo em:\n{caminho_saida}")

                self.root.after(0, _salvar_dialog)

            except Exception as e:
                self.log(f"[INFOPLAN ERRO] Falha na análise: {e}")
                self.root.after(0, lambda: messagebox.showerror("Erro InfoPlan", str(e)))
            finally:
                self.set_status("Pronto.")

        threading.Thread(target=_worker, daemon=True).start()

    # ==================================================================================
    # ABA 5: LISTADOR DE ESTRUTURAS (TREE /F & DUMP DATADO)
    # ==================================================================================
    def _construir_aba_listador_tree(self):
        tab = ttk.Frame(self.notebook, padding=10)
        self.notebook.add(tab, text="🌳 Listador de Estruturas")

        header_frame = ttk.LabelFrame(tab, text=" Emulador e Expansor Nativo do Utilitário Windows Tree ", padding=10)
        header_frame.pack(fill=tk.X, pady=(0, 10))

        info_text = (
            "Gera a listagem completa e hierárquica de todas as pastas, subpastas e arquivos (com extensão)\n"
            "do diretório ativo, recriando e expandindo nativamente o comportamento do script 'Listador de Estruturas.bat'.\n"
            "Cria automaticamente um arquivo nomeado no padrão: estrutura_YYYY-MM-DD_HHhMMm.txt."
        )
        ttk.Label(header_frame, text=info_text, justify=tk.LEFT).pack(anchor=tk.W)

        btn_box = ttk.Frame(tab)
        btn_box.pack(fill=tk.X, pady=8)

        btn_dump_txt = ttk.Button(
            btn_box,
            text="💾 GERAR ARQUIVO DE ESTRUTURA (DUMP TXT DATADO)",
            style="RetroAction.TButton",
            command=self.gerar_dump_estrutura_txt
        )
        btn_dump_txt.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 6), ipady=5)

        btn_ver_console = ttk.Button(
            btn_box,
            text="🖥️ EXIBIR ÁRVORE DIRETAMENTE NO CONSOLE CRT",
            style="Retro.TButton",
            command=self.exibir_arvore_no_console
        )
        btn_ver_console.pack(side=tk.RIGHT, fill=tk.X, expand=True, padx=(6, 0), ipady=5)

        tree_info_frame = ttk.LabelFrame(tab, text=" Especificações do Dump ", padding=8)
        tree_info_frame.pack(fill=tk.BOTH, expand=True, pady=(5, 0))

        tree_spec = (
            "• Nome do Arquivo : estrutura_YYYY-MM-DD_HHhMMm.txt\n"
            "• Local de Saída  : Raiz da pasta do projeto ativo selecionada na barra superior.\n"
            "• Conteúdo        : Cabeçalho 'ESTRUTURA', árvore ASCII recursiva completa e rodapé com timestamp oficial.\n"
            "• Compatibilidade : Executável em qualquer SO (Windows, Linux, macOS) sem depender do tree.com do DOS."
        )
        ttk.Label(tree_info_frame, text=tree_spec, justify=tk.LEFT, foreground="#2C4E34").pack(anchor=tk.W)

    def _gerar_arvore_ascii(self, root_dir: str) -> Tuple[List[str], int, int]:
        """Gera a árvore ASCII hierárquica recursiva do diretório."""
        linhas = []
        total_dirs = 0
        total_files = 0

        for dirpath, dirnames, filenames in os.walk(root_dir):
            dirnames[:] = [d for d in dirnames if d not in IGNORE_DIRS]
            rel_path = os.path.relpath(dirpath, root_dir)

            if rel_path != ".":
                nivel = rel_path.count(os.sep)
                prefixo_dir = "│   " * nivel
                linhas.append(f"{prefixo_dir}├── 📁 {os.path.basename(dirpath)}\\")
                total_dirs += 1
            else:
                linhas.append(f"📁 {os.path.basename(root_dir)}\\")

            nivel_filhos = 0 if rel_path == "." else rel_path.count(os.sep) + 1
            prefixo_file = "│   " * nivel_filhos
            for f in sorted(filenames):
                linhas.append(f"{prefixo_file}├── 📄 {f}")
                total_files += 1

        return linhas, total_dirs, total_files

    def gerar_dump_estrutura_txt(self):
        caminho = self.src_project_path.get().strip()
        if not os.path.exists(caminho):
            messagebox.showwarning("Aviso", "O diretório informado não existe!")
            return

        def _worker():
            self.set_status("Gerando dump de estrutura...")
            timestamp = datetime.now()
            nome_arquivo = f"estrutura_{timestamp.strftime('%Y-%m-%d_%Hh%Mm')}.txt"
            caminho_saida = os.path.join(caminho, nome_arquivo)

            linhas_arvore, total_dirs, total_files = self._gerar_arvore_ascii(caminho)

            cabecalho = [
                "ESTRUTURA",
                f"Diretório Raiz: {caminho}",
                "",
                f"Listagem de pastas e arquivos para o volume {os.path.basename(caminho)}",
                "=" * 60,
                ""
            ]

            rodape = [
                "",
                "=" * 60,
                f"Total de Diretórios : {total_dirs}",
                f"Total de Arquivos    : {total_files}",
                f"Arquivo gerado em   : {timestamp.strftime('%d/%m/%Y às %H:%M:%S')}",
                "=" * 60,
                ""
            ]

            conteudo_completo = "\n".join(cabecalho + linhas_arvore + rodape)

            try:
                with open(caminho_saida, "w", encoding="utf-8") as wf:
                    wf.write(conteudo_completo)

                self.log(f"\n[ESTRUTURA DUMP] Arquivo criado com sucesso em:\n  {caminho_saida}")
                self.log(f"  • Pastas listadas: {total_dirs} | Arquivos listados: {total_files}")
                self.root.after(0, lambda: messagebox.showinfo(
                    "Estrutura Gerada",
                    f"Arquivo '{nome_arquivo}' criado com sucesso em:\n{caminho}"
                ))
            except Exception as e:
                self.log(f"[ERRO ESTRUTURA] {e}")
                self.root.after(0, lambda: messagebox.showerror("Erro de Gravação", str(e)))
            finally:
                self.set_status("Pronto.")

        threading.Thread(target=_worker, daemon=True).start()

    def exibir_arvore_no_console(self):
        caminho = self.src_project_path.get().strip()
        if not os.path.exists(caminho):
            messagebox.showwarning("Aviso", "O diretório informado não existe!")
            return

        def _worker():
            self.set_status("Exibindo árvore de arquivos no console...")
            self.log(f"\n[ÁRVORE DE ARQUIVOS] Mapeando: {caminho}")
            linhas_arvore, total_dirs, total_files = self._gerar_arvore_ascii(caminho)
            for l in linhas_arvore:
                self.log(l)
            self.log(f"[TOTAL] {total_dirs} diretórios, {total_files} arquivos mapeados.")
            self.set_status("Pronto.")

        threading.Thread(target=_worker, daemon=True).start()

    # ==================================================================================
    # ABA 6: HARDWARE-Z (TELEMETRIA E AVALIAÇÃO DO COMPUTADOR)
    # ==================================================================================
    def _construir_aba_hardware_z(self):
        tab = ttk.Frame(self.notebook, padding=10)
        self.notebook.add(tab, text="💻 Hardware-Z")

        header_frame = ttk.LabelFrame(tab, text=" Painel de Avaliação de Hardware e Sistema Operacional (Estilo CPU-Z) ", padding=10)
        header_frame.pack(fill=tk.X, pady=(0, 10))

        btn_refresh = ttk.Button(
            header_frame,
            text="🔄 ATUALIZAR TELEMETRIA DE HARDWARE AGORA",
            style="RetroAction.TButton",
            command=self.exibir_diagnostico_hardware
        )
        btn_refresh.pack(side=tk.RIGHT, padx=5)

        ttk.Label(header_frame, text="Inspeciona o computador onde o Kanivet XP está sendo executado.", font=("Tahoma", 9, "bold")).pack(side=tk.LEFT)

        # Container dos Dados
        self.hw_container = ttk.LabelFrame(tab, text=" Especificações Técnicas da Máquina ", padding=10)
        self.hw_container.pack(fill=tk.BOTH, expand=True)

        self.lbl_hw_info = ttk.Label(self.hw_container, text="Clique em 'Atualizar Telemetria' para carregar.", font=("Consolas", 9), justify=tk.LEFT)
        self.lbl_hw_info.pack(anchor=tk.NW, fill=tk.BOTH, expand=True)

        # Executa uma leitura inicial
        self.root.after(500, self.exibir_diagnostico_hardware)

    def exibir_diagnostico_hardware(self):
        """Coleta e imprime telemetria na aba Hardware-Z e no console CRT."""
        def _worker():
            self.set_status("Coletando telemetria de hardware...")
            dados = obter_telemetria_hardware()

            linhas = [
                "================================================================================",
                "   KANIVET XP // HARDWARE-Z — DIAGNÓSTICO PROFUNDO DO COMPUTADOR",
                "================================================================================",
                f"  • Sistema Operacional : {dados['so']}",
                f"  • Arquitetura CPU     : {dados['arquitetura']}",
                f"  • Processador Host    : {dados['processador']}",
                f"  • Núcleos Lógicos     : {dados['cpus_logicas']} vCPUs",
                f"  • Núcleos Físicos     : {dados['cpus_fisicas']}",
                f"  • Nome da Máquina     : {dados['hostname']}",
                f"  • Versão do Python    : {dados['python_version']}",
                "--------------------------------------------------------------------------------",
                f"  • Memória RAM Total   : {dados['ram_total']}",
                f"  • Memória RAM Usada   : {dados['ram_usada']} ({dados['ram_percent']})",
                f"  • Memória RAM Livre   : {dados['ram_livre']}",
                "--------------------------------------------------------------------------------",
                f"  • Disco Raiz Total    : {dados['disco_total']}",
                f"  • Disco Raiz Usado    : {dados['disco_usado']} ({dados['disco_percent']})",
                f"  • Disco Raiz Livre    : {dados['disco_livre']}",
                "--------------------------------------------------------------------------------",
                f"  • Tempo de Atividade  : {dados['uptime']}",
                f"  • Biblioteca Psutil   : {'Disponível (Leitura Completa)' if PSUTIL_AVAILABLE else 'Ausente (Execute: pip install psutil)'}",
                "================================================================================"
            ]

            texto_formatado = "\n".join(linhas)

            self.root.after(0, lambda: self.lbl_hw_info.config(text=texto_formatado))
            self.log("\n" + texto_formatado)
            self.set_status("Pronto.")

        threading.Thread(target=_worker, daemon=True).start()

    # ==================================================================================
    # MANUAL DO USUÁRIO INTEGRADO (WINDOWS HELP RETRO) & DIÁLOGOS
    # ==================================================================================
    def abrir_manual_usuario(self):
        """Abre a janela de diálogo dedicada com o Manual do Usuário Integrado em abas."""
        help_win = tk.Toplevel(self.root)
        help_win.title("Kanivet XP — Manual do Usuário e Orientações Técnicas")
        help_win.geometry("820x640")
        help_win.minsize(740, 500)
        help_win.configure(bg=XP_BG_BASE)

        # Header Retro
        top_bar = ttk.Frame(help_win, padding=10)
        top_bar.pack(fill=tk.X)
        ttk.Label(top_bar, text="📖 Sistema de Ajuda & Manual Integrado", font=("Tahoma", 12, "bold"), foreground=XP_ACCENT).pack(anchor=tk.W)
        ttk.Label(top_bar, text="Instruções operacionais detalhadas para cada um dos núcleos do Kanivet XP.", font=("Tahoma", 9)).pack(anchor=tk.W)

        # Notebook de Ajuda
        help_notebook = ttk.Notebook(help_win, padding=6)
        help_notebook.pack(fill=tk.BOTH, expand=True, padx=8, pady=(0, 8))

        secoes_manual = [
            ("1. Sanitizador & Deploy",
             "COMO USAR O SANITIZADOR E EVITAR VAZAMENTO DE CREDENCIAIS:\n\n"
             "1. Selecione a pasta do seu código na barra superior do programa.\n"
             "2. O Sanitizador NÃO altera a sua pasta original. Ele cria uma pasta limpa ao lado chamada '<projeto>_clean_export'.\n"
             "3. Antes de enviar para o GitHub, o motor heurístico inspeciona cada arquivo de texto/código e substitui\n"
             "   qualquer token, senha ou chave privada por placeholders como 'SEU_TOKEN_AQUI'.\n"
             "4. Arquivos .env, chaves .pem/.key, bancos SQLite (.db) e temporários de compilação são bloqueados automaticamente.\n"
             "5. Um arquivo .gitignore universal e blindado é injetado na raiz do projeto exportado.\n"
             "6. O envio é feito diretamente para a branch configurada (padrão 'main') com ou sem a flag --force."),

            ("2. Incidentes de Token",
             "O QUE FAZER CASO UM TOKEN DO TELEGRAM OU CHAVE VAZE:\n\n"
             "1. TELEGRAM BOT TOKEN:\n"
             "   - Abra o Telegram e converse com o @BotFather.\n"
             "   - Envie o comando: /revoke e selecione o seu bot comprometido.\n"
             "   - O BotFather gerará um novo token imediatamente e invalidará o anterior.\n"
             "   - Atualize seu código local com o novo token.\n\n"
             "2. GITHUB ALERTAS (SECRET SCANNING):\n"
             "   - Acesse o repositório no GitHub -> Vá na aba 'Security' -> 'Secret scanning alerts'.\n"
             "   - Revogue a credencial no serviço de origem (ex: BotFather, OpenAI, AWS).\n"
             "   - No GitHub, feche o alerta marcando como 'Revoked' (Revogado)."),

            ("3. Geração de PAT",
             "COMO GERAR E UTILIZAR O PERSONAL ACCESS TOKEN (PAT) NO GITHUB:\n\n"
             "1. Acesse https://github.com/settings/tokens (ou Perfil -> Settings -> Developer Settings -> Personal access tokens).\n"
             "2. Escolha 'Tokens (classic)' -> 'Generate new token (classic)'.\n"
             "3. Dê um nome em 'Note' (ex: Kanivet-XP-Deploy) e defina a validade (Expiration).\n"
             "4. MARQUE OBRIGATORIAMENTE O ESCOPO: [X] repo (Acesso total para repositórios privados e públicos).\n"
             "5. Clique em 'Generate token' no final da página e copie o código gerado (ex: ghp_...).\n"
             "6. Cole este código no campo 'GitHub Token (PAT)' no Kanivet XP.\n"
             "   O programa usará esse token para autenticar o push sem você precisar digitar senhas no terminal!"),

            ("4. Central Git",
             "COMO UTILIZAR A CENTRAL DE OPERAÇÕES GIT SEM LINHA DE COMANDO:\n\n"
             "1. Todos os botões executam os comandos originais do Git Baremetal diretamente na pasta do projeto ativo.\n"
             "2. Para registrar alterações:\n"
             "   - Clique em 'git status' para inspecionar arquivos modificados.\n"
             "   - Clique em 'git add .' para adicionar tudo ao Stage.\n"
             "   - Preencha o campo 'Mensagem de Commit' na primeira aba e clique em 'git commit -m'.\n"
             "   - Clique em 'git push' para sincronizar com o repositório remoto.\n"
             "3. Para clonar repositórios externos, use o campo inferior 'Clonar Repositório Remoto', informando a URL e pasta destino."),

            ("5. MDnator v4.0",
             "COMO COMPILAR PROJETOS INTEIROS COM O MDNATOR PARA ALIMENTAR IAs:\n\n"
             "1. Selecione a pasta do seu projeto na barra superior.\n"
             "2. Vá até a aba 'Motor MDnator v4.0' e clique em 'Compilar Projeto Ativo em Markdown Único (.MD)'.\n"
             "3. Escolha o local para salvar o arquivo compilado.\n"
             "4. O MDnator gera um documento consolidado contendo:\n"
             "   - Cabeçalho oficial com métricas de data e linhas.\n"
             "   - Árvore de navegação ASCII de todas as pastas e arquivos.\n"
             "   - Todo o código-fonte de arquivos Python, C++, Arduino (.ino), PlatformIO (.io), Web e scripts com blocos sintáticos.\n"
             "5. Esse arquivo único pode ser anexado diretamente no ChatGPT, Claude, Gemini ou LLMs locais para contextualização total!"),

            ("6. InfoPlan",
             "COMO EXTRAIR A RADIOGRAFIA ESTRUTURAL DE PLANILHAS PELO INFOPLAN:\n\n"
             "1. Vá até a aba 'Módulo InfoPlan' e clique em 'Selecionar Planilha e Gerar Relatório Completo'.\n"
             "2. Escolha um arquivo .xlsx ou .xls.\n"
             "3. O InfoPlan inspeciona cada aba e gera um relatório detalhado com:\n"
             "   - Metadados e contagem total de células.\n"
             "   - Tipagem automática de colunas (inteiros, decimais, datas, textos).\n"
             "   - Estatísticas completas: Soma, Média, Mediana, Desvio Padrão, Mínimo e Máximo.\n"
             "   - Amostras de dados e células posicionais (ex: B2 = 150.0).\n"
             "4. O relatório é exportado em formato TXT/MD limpo para auditoria."),

            ("7. Listador & Tree",
             "COMO GERAR RELATÓRIOS DE ESTRUTURA E ÁRVORE DE DIRETÓRIOS:\n\n"
             "1. Vá até a aba 'Listador de Estruturas'.\n"
             "2. Clique em 'Gerar Arquivo de Estrutura (Dump TXT Datado)'.\n"
             "3. O software criará um arquivo nomeado no padrão 'estrutura_YYYY-MM-DD_HHhMMm.txt' na raiz do seu projeto ativo.\n"
             "4. Você também pode clicar em 'Exibir Árvore Diretamente no Console CRT' para inspecionar instantaneamente no terminal.")
        ]

        for titulo_aba, conteudo_aba in secoes_manual:
            tab_sec = ttk.Frame(help_notebook, padding=8)
            help_notebook.add(tab_sec, text=titulo_aba)

            txt = scrolledtext.ScrolledText(tab_sec, wrap=tk.WORD, bg="#FFFFFF", fg="#111111", font=("Tahoma", 9), relief="sunken", bd=1)
            txt.pack(fill=tk.BOTH, expand=True)
            txt.insert(tk.END, conteudo_aba)
            txt.config(state=tk.DISABLED)

        # Botão Fechar
        btn_close = ttk.Button(help_win, text="Fechar Manual", style="Retro.TButton", command=help_win.destroy)
        btn_close.pack(side=tk.RIGHT, padx=10, pady=8)

    def abrir_dialogo_sobre(self):
        """Abre janela de créditos e informações autorais."""
        about_win = tk.Toplevel(self.root)
        about_win.title("Sobre o Kanivet XP — Universal Suite")
        about_win.geometry("580x480")
        about_win.resizable(False, False)
        about_win.configure(bg=XP_BG_BASE)

        banner = tk.Label(about_win, text=KANIVET_ASCII_BANNER, font=("Courier", 7, "bold"), bg=CRT_BG, fg=CRT_FG, justify=tk.CENTER)
        banner.pack(fill=tk.X, padx=10, pady=10)

        info_box = ttk.LabelFrame(about_win, text=" Credenciais do Desenvolvedor ", padding=10)
        info_box.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))

        creditos = (
            "SISTEMA       : KANIVET XP (CYBER-GIT MDNATOR UNIVERSAL SUITE)\n"
            "VERSÃO        : 5.0 Enterprise Monolithic Standalone\n"
            "ARQUITETURA   : Python 3 + Tkinter / TTK Retro Windows XP Engine\n"
            "----------------------------------------------------------------------\n"
            "AUTOR         : Philipe Sampaio Lima (@OldBoy465)\n"
            "COLABORAÇÃO   : Engenharia de Prompts & Inteligência Artificial\n"
            "ANO           : 2026\n"
            "----------------------------------------------------------------------\n"
            "CONTATOS OFICIAIS:\n"
            "  • E-mail   : cienciaegestao@gmail.com\n"
            "  • WhatsApp : +55 98 98250-6920\n"
            "  • GitHub   : https://github.com/OldBoy465\n"
            "----------------------------------------------------------------------\n"
            "FINALIDADE    : Automação completa de Git, Sanitização de Dados Sensíveis,\n"
            "                Compilação Markdown para IAs e Radiografia de Planilhas."
        )
        lbl_cred = ttk.Label(info_box, text=creditos, justify=tk.LEFT, font=("Consolas", 9))
        lbl_cred.pack(anchor=tk.NW, fill=tk.BOTH, expand=True)

        btn_box = ttk.Frame(about_win, padding=5)
        btn_box.pack(fill=tk.X, padx=10, pady=5)

        btn_copy_email = ttk.Button(
            btn_box,
            text="Copiar E-mail",
            style="Retro.TButton",
            command=lambda: self._copiar_texto_clipboard("cienciaegestao@gmail.com")
        )
        btn_copy_email.pack(side=tk.LEFT, padx=(0, 5))

        btn_copy_zap = ttk.Button(
            btn_box,
            text="Copiar WhatsApp",
            style="Retro.TButton",
            command=lambda: self._copiar_texto_clipboard("+55 98 98250-6920")
        )
        btn_copy_zap.pack(side=tk.LEFT)

        btn_ok = ttk.Button(btn_box, text="Fechar", style="Retro.TButton", command=about_win.destroy)
        btn_ok.pack(side=tk.RIGHT)

    def _copiar_texto_clipboard(self, texto: str):
        self.root.clipboard_clear()
        self.root.clipboard_append(texto)
        self.log(f"[CLIPBOARD] Valor copiado para a área de transferência: {texto}")
        messagebox.showinfo("Copiado", f"Copiado para a área de transferência:\n{texto}")


# ======================================================================================
# PONTO DE ENTRADA PRINCIPAL
# ======================================================================================
def main():
    root = tk.Tk()
    app = KanivetXPApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
