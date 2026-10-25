# -*- coding: utf-8 -*-
"""
========================================================================================
    KANIVET XP NEXUS — CYBER-GIT MDNATOR UNIVERSAL SUITE (ENTERPRISE EDITION v6.0)
========================================================================================
    Autor Principal : Philipe Sampaio Lima (@OldBoy465)
    Co-Autoria      : Engenharia de Prompts & Inteligência Artificial
    Ano             : 2026
    Contatos        : cienciaegestao@gmail.com | WhatsApp: +55 98 98250-6920
========================================================================================
    ARQUITETURA MONOLÍTICA COMPLETA EM ARQUIVO ÚNICO (19 SEÇÕES LÓGICAS):
      1. Sanitizador Heurístico & Security Center (Severidade, Diff, Backup, .env, Git)
      2. Central Git Baremetal Expandida (Stage/Unstage, Tags, Conflitos, Grandes Arqs)
      3. Motor MDnator v5.0 (Perfis LLM/Flask/ESP32, Duplicidades SHA-256, Incremental)
      4. Módulo InfoPlan Pro (Auditoria de Qualidade, Assimetria, Curtose, Gráficos Reais)
      5. Listador de Estruturas & Explorador Avançado (Busca, Comparação de Pastas, Hash)
      6. Hardware-Z Pro (Partições, Rede, Top Processos, Histórico da Sessão)
      7. Code Quality Center (Ruff, Black, Pytest, Mypy, Bandit + AST Nativo Python)
      8. Diagnóstico de Ambiente & Dependências (Venv, Pacotes, Requisitos, Ferramentas)
      9. Workspace & Automações (Perfis Persistentes e Pipeline de Auditoria Pré-Publicação)
     10. Suíte de Autotestes de Não-Regressão Integrada (--self-test / GUI)
========================================================================================
    REVISÃO DE CORREÇÃO (v6.0.1):
      • [CORREÇÃO 1] Erro de sintaxe (SyntaxError) no operador morsa (:=) em
        gerar_relatorio_infoplan(): a expressão 'and preenc_val := ...' é inválida.
      • [CORREÇÃO 2] 'io' não estava importado; executar_suite_autotestes() causaria
        NameError ao tentar usar io.StringIO(). Import adicionado no topo.
      • [CORREÇÃO 3] Atribuição residual 'PS_PANDAS = False' removida (variável morta).
      • [CORREÇÃO 4] formatar_valor_planilha() protegida contra valores não escalares
        (listas/arrays), que faziam pd.isna() retornar array e quebrar o 'if'.
      • [CORREÇÃO 5] Log e status enviados por threads de trabalho agora passam pela
        fila thread-safe do TaskManager, em vez de chamar root.after() de outra thread
        (Tkinter não é thread-safe).
      • [CORREÇÃO 6] Indentação inconsistente do bloco de limite do histórico de
        telemetria normalizada.
========================================================================================
"""

# ======================================================================================
# 2. IMPORTS E DETECÇÃO DE DEPENDÊNCIAS
# ======================================================================================
import sys
import os
import re
import io
import ast
import csv
import json
import math
import time
import queue
import shutil
import hashlib
import logging
import tempfile
import platform
import unittest
import subprocess
import threading
import statistics
from datetime import datetime
from collections import Counter
from typing import List, Tuple, Optional, Dict, Any, Callable

try:
    import importlib.metadata as importlib_metadata
except ImportError:
    importlib_metadata = None

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext, simpledialog

# Telemetria de Hardware opcional (psutil)
try:
    import psutil
    PSUTIL_AVAILABLE = True
except ImportError:
    psutil = None
    PSUTIL_AVAILABLE = False

# Análise de Planilhas opcional (Pandas e Openpyxl / XLRD)
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
# 3. CONSTANTES E CONFIGURAÇÕES PADRÃO
# ======================================================================================
APP_VERSION = "6.0.0-NEXUS"
APP_DATA_DIR = os.path.join(os.path.expanduser("~"), ".kanivet_xp_nexus")
APP_BACKUP_DIR = os.path.join(APP_DATA_DIR, "backups")
APP_WORKSPACES_FILE = os.path.join(APP_DATA_DIR, "workspaces.json")
APP_HISTORY_FILE = os.path.join(APP_DATA_DIR, "operation_history.json")
APP_MDNATOR_CACHE = os.path.join(APP_DATA_DIR, "mdnator_incremental_cache.json")

KANIVET_ASCII_BANNER = r"""
 ██╗  ██╗ █████╗ ███╗   ██╗██╗██╗   ██╗███████╗████████╗   ██╗  ██╗██████╗ 
 ██║ ██╔╝██╔══██╗████╗  ██║██║██║   ██║██╔════╝╚══██╔══╝   ╚██╗██╔╝██╔══██╗
 █████╔╝ ███████║██╔██╗ ██║██║██║   ██║█████╗     ██║       ╚███╔╝ ██████╔╝
 ██╔═██╗ ██╔══██║██║╚██╗██║██║╚██╗ ██╔╝██╔══╝     ██║       ██╔██╗ ██╔═══╝ 
 ██║  ██╗██║  ██║██║ ╚████║██║ ╚████╔╝ ███████╗    ██║      ██╔╝ ██╗██║     
 ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═══╝╚═╝  ╚═══╝  ╚══════╝    ╚═╝      ╚═╝  ╚═╝╚═╝     
   >> UNIVERSAL SUITE: GIT BAREMETAL, MDNATOR, INFOPLAN, QUALITY & HARDWARE-Z <<
"""

# Paleta clássica Windows XP / Java Swing (Preservada integralmente)
XP_BG_BASE = "#ECE9D8"
XP_PANEL_BG = "#F0EEE0"
XP_ACCENT = "#0A246A"
XP_BTN_BG = "#E1DFD6"
XP_BTN_ACTIVE = "#D4DFD0"
CRT_BG = "#000000"
CRT_FG = "#00FF66"
CRT_CURSOR = "#33FF33"

# Paleta Tema Escuro (Cyber Dark)
DARK_BG_BASE = "#1E1E24"
DARK_PANEL_BG = "#25252D"
DARK_ACCENT = "#58A6FF"
DARK_BTN_BG = "#32323D"
DARK_BTN_ACTIVE = "#434352"
DARK_FG = "#E6EDF3"

# Padrões de Sanitização Originais Preservados
EXACT_SECRET_PATTERNS = [
    (r'\b\d{8,11}:[a-zA-Z0-9_-]{34,36}\b', 'SEU_TELEGRAM_BOT_TOKEN_AQUI'),
    (r'\bghp_[a-zA-Z0-9]{36}\b', 'ghp_SEU_GITHUB_PAT_AQUI'),
    (r'\bgithub_pat_[a-zA-Z0-9_]{60,100}\b', 'github_pat_SEU_GITHUB_PAT_AQUI'),
    (r'\bgho_[a-zA-Z0-9]{36}\b', 'gho_SEU_GITHUB_OAUTH_AQUI'),
    (r'\bsk-[a-zA-Z0-9T3BlbkFJ]{30,60}\b', 'sk-SUA_CHAVE_OPENAI_AQUI'),
    (r'\bsk-ant-[a-zA-Z0-9_-]{60,100}\b', 'sk-ant-SUA_CHAVE_ANTHROPIC_AQUI'),
    (r'\bAIza[0-9A-Za-z-_]{35}\b', 'AIza_SUA_GOOGLE_API_KEY_AQUI'),
    (r'\b(AKIA|ABIA|ACCA|ASIA)[0-9A-Z]{16}\b', 'AKIA_SUA_AWS_ACCESS_KEY_AQUI'),
    (r'\beyJ[a-zA-Z0-9_-]{10,}\.eyJ[a-zA-Z0-9_-]{10,}\.[a-zA-Z0-9_-]{10,}\b', 'SEU_JWT_TOKEN_AQUI'),
    (r'((?:CHAT_ID|chat_id|AUTHORIZED_CHAT_ID|authorized_chat_id)\s*[:=]\s*)-?\d{8,12}\b', r'\g<1>0000000000')
]

GENERIC_ASSIGNMENT_PATTERNS = [
    (
        r'((?:password|passwd|pass|token|secret|api_key|apikey|auth|private_key|bot_token)\s*=\s*")[^"\r\n]+(")',
        r'\1SEU_TOKEN_AQUI\2',
        re.IGNORECASE
    ),
    (
        r'((?:password|passwd|pass|token|secret|api_key|apikey|auth_token|bot_token)\s*=\s*[\'"])[^\'"\r\n]+([\'"])',
        r'\1SEU_TOKEN_AQUI\2',
        re.IGNORECASE
    ),
    (
        r'((?:["\']?(?:password|passwd|pass|token|secret|api_key|apikey|auth)["\']?\s*[:=]\s*["\']))[^\'"\r\n]+(["\'])',
        r'\1SEU_TOKEN_AQUI\2',
        re.IGNORECASE
    )
]

# Regras Expandidas do Security Center com Classificação de Severidade
SECURITY_RULES_CATALOG = [
    {"id": "SEC-001", "name": "Telegram Bot Token", "severity": "CRITICAL", "regex": r'\b\d{8,11}:[a-zA-Z0-9_-]{34,36}\b'},
    {"id": "SEC-002", "name": "GitHub Personal Access Token", "severity": "CRITICAL", "regex": r'\b(?:ghp_[a-zA-Z0-9]{36}|github_pat_[a-zA-Z0-9_]{60,100}|gho_[a-zA-Z0-9]{36})\b'},
    {"id": "SEC-003", "name": "OpenAI / Anthropic API Key", "severity": "CRITICAL", "regex": r'\b(?:sk-[a-zA-Z0-9T3BlbkFJ]{30,60}|sk-ant-[a-zA-Z0-9_-]{60,100})\b'},
    {"id": "SEC-004", "name": "Google Cloud API Key", "severity": "HIGH", "regex": r'\bAIza[0-9A-Za-z-_]{35}\b'},
    {"id": "SEC-005", "name": "AWS Access Key ID", "severity": "CRITICAL", "regex": r'\b(?:AKIA|ABIA|ACCA|ASIA)[0-9A-Z]{16}\b'},
    {"id": "SEC-006", "name": "Chave Privada RSA/SSH/PEM", "severity": "CRITICAL", "regex": r'-----BEGIN (?:RSA |OPENSSH |EC |DSA )?PRIVATE KEY-----'},
    {"id": "SEC-007", "name": "JSON Web Token (JWT)", "severity": "MEDIUM", "regex": r'\beyJ[a-zA-Z0-9_-]{10,}\.eyJ[a-zA-Z0-9_-]{10,}\.[a-zA-Z0-9_-]{10,}\b'},
    {"id": "SEC-008", "name": "Senha ou Segredo Hardcoded", "severity": "HIGH", "regex": r'(?i)(?:password|passwd|secret|api_key|apikey|bot_token)\s*[:=]\s*[\'"][^\'"\r\n]{4,}[\'"]'},
    {"id": "SEC-009", "name": "Telegram Chat ID Explícito", "severity": "LOW", "regex": r'(?:CHAT_ID|chat_id|AUTHORIZED_CHAT_ID)\s*[:=]\s*-?\d{8,12}\b'},
]

FALSE_POSITIVE_PLACEHOLDERS = {
    "SEU_TOKEN_AQUI", "SEU_TELEGRAM_BOT_TOKEN_AQUI", "ghp_SEU_GITHUB_PAT_AQUI",
    "github_pat_SEU_GITHUB_PAT_AQUI", "sk-SUA_CHAVE_OPENAI_AQUI", "YOUR_API_KEY",
    "CHANGE_ME", "123456", "password", "admin", "example", "0000000000", " dummy"
}

IGNORE_DIRS = {
    '.git', '.build_cache', '.vscode', '.idea', '__pycache__',
    'build', 'dist', 'node_modules', '.pio', '.platformio', 'venv', '.env_dir', '.pytest_cache', '.mypy_cache', '.ruff_cache'
}

RESTRICTED_EXACT_FILES = {
    '.env', '.env.local', 'secrets.json', 'id_rsa', 'id_dsa', 'id_ed25519',
    'Listador de Estruturas.bat'
}

RESTRICTED_EXTENSIONS = {
    '.bin', '.o', '.d', '.libsdetect.d', '.merged', '.cache', '.bat',
    '.pem', '.key', '.pkcs12', '.pfx', '.crt', '.sqlite', '.sqlite3', '.db'
}

TEMP_JUNK_EXTENSIONS = {'.tmp', '.bak', '.swp', '.pyc', '.pyo', '.log', '.cache', '.orig'}

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

TEXT_CODE_EXTENSIONS = {
    '.py', '.js', '.ts', '.css', '.html', '.md', '.txt', '.json', '.xml',
    '.sql', '.java', '.c', '.cpp', '.h', '.hpp', '.cs', '.sh',
    '.bat', '.cmd', '.php', '.ino', '.io', '.properties', '.ini',
    '.yaml', '.yml', '.r', '.m', '.go', '.rs'
}

LANG_MAP = {
    '.py': 'python', '.js': 'javascript', '.ts': 'typescript', '.css': 'css',
    '.html': 'html', '.md': 'markdown', '.json': 'json', '.sql': 'sql',
    '.php': 'php', '.c': 'c', '.cpp': 'cpp', '.h': 'cpp', '.hpp': 'cpp',
    '.cs': 'csharp', '.bat': 'bat', '.cmd': 'bat', '.sh': 'bash',
    '.ino': 'arduino', '.io': 'cpp', '.ini': 'ini', '.properties': 'properties',
    '.yaml': 'yaml', '.yml': 'yaml', '.go': 'go', '.rs': 'rust'
}

MDNATOR_PROFILES = {
    "Universal (Todos os Formatos)": TEXT_CODE_EXTENSIONS,
    "Python & Flask": {'.py', '.html', '.css', '.js', '.json', '.ini', '.yaml', '.yml', '.md', '.sql', '.txt'},
    "Arduino & ESP32 Firmware": {'.ino', '.io', '.c', '.cpp', '.h', '.hpp', '.ini', '.json', '.md'},
    "Web Frontend (HTML/CSS/JS/TS)": {'.html', '.css', '.js', '.ts', '.json', '.md'},
    "Ciência e Análise de Dados": {'.py', '.r', '.sql', '.json', '.yaml', '.yml', '.md', '.txt'},
    "Pacote de Contexto para LLMs": {'.py', '.js', '.ts', '.c', '.cpp', '.h', '.ino', '.html', '.css', '.sql', '.md', '.json', '.yaml'}
}

AMOSTRA_VALORES = 10
AMOSTRA_LINHAS = 10


# ======================================================================================
# 4. EXCEÇÕES, VALIDAÇÕES E MASCARAMENTO DE SEGURANÇA
# ======================================================================================
class KanivetError(Exception):
    """Exceção base para erros operacionais do Kanivet XP."""
    pass


class TaskCancelledError(KanivetError):
    """Exceção lançada quando o usuário cancela cooperativamente uma tarefa."""
    pass


def mascarar_credenciais(texto: str) -> str:
    """Neutraliza tokens e senhas em URLs HTTPS ou saídas de log antes de exibir/gravar."""
    if not texto:
        return ""
    mascarado = re.sub(r'(https?://[^:\s/@]+:)([^@\s/]+)(@)', r'\1***TOKEN_OCULTO***\3', str(texto))
    mascarado = re.sub(r'\b(ghp_|github_pat_|gho_|sk-|AIza)[a-zA-Z0-9_-]{20,}\b', r'\1***OCULTO***', mascarado)
    return mascarado


def validar_caminho_diretorio(caminho: str) -> str:
    """Valida e normaliza o caminho de um diretório existente."""
    if not caminho or not str(caminho).strip():
        raise KanivetError("Nenhum caminho de diretório foi informado.")
    abs_path = os.path.abspath(os.path.expanduser(str(caminho).strip()))
    if not os.path.exists(abs_path):
        raise KanivetError(f"O diretório informado não existe: {abs_path}")
    if not os.path.isdir(abs_path):
        raise KanivetError(f"O caminho informado não é um diretório válido: {abs_path}")
    return abs_path


# ======================================================================================
# 5. LOGGING E HISTÓRICO OPERACIONAL
# ======================================================================================
def inicializar_diretorios_dados():
    """Garante que os diretórios locais de estado e backup existam."""
    for d in (APP_DATA_DIR, APP_BACKUP_DIR):
        try:
            os.makedirs(d, exist_ok=True)
        except Exception:
            pass


class OperationHistoryManager:
    """Gerencia o histórico persistente e em memória de operações executadas."""
    def __init__(self):
        inicializar_diretorios_dados()
        self.entries: List[Dict[str, Any]] = []
        self._carregar()

    def _carregar(self):
        if os.path.exists(APP_HISTORY_FILE):
            try:
                with open(APP_HISTORY_FILE, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    if isinstance(data, list):
                        self.entries = data[-300:]
            except Exception:
                self.entries = []

    def registrar(self, modulo: str, acao: str, status: str, detalhes: str = ""):
        item = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "modulo": modulo,
            "acao": acao,
            "status": status,
            "detalhes": mascarar_credenciais(detalhes)[:400]
        }
        self.entries.append(item)
        if len(self.entries) > 300:
            self.entries = self.entries[-300:]
        try:
            with open(APP_HISTORY_FILE, "w", encoding="utf-8") as f:
                json.dump(self.entries, f, ensure_ascii=False, indent=2)
        except Exception:
            pass


# ======================================================================================
# 6. FUNÇÕES UTILITÁRIAS E GERENCIAMENTO DE ARQUIVOS / BACKUPS
# ======================================================================================
def safe_read_file_text(file_path: str) -> Tuple[str, int]:
    """Leitura resiliente multi-encoding de arquivos de código (Preservada e Aprimorada)."""
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


def is_binary_file(file_path: str) -> bool:
    """Detecta se um arquivo é binário inspecionando bytes nulos no bloco inicial."""
    try:
        with open(file_path, 'rb') as f:
            chunk = f.read(2048)
            return b'\x00' in chunk
    except Exception:
        return True


def calcular_sha256(file_path: str) -> str:
    """Calcula o hash SHA-256 de um arquivo em blocos."""
    h = hashlib.sha256()
    with open(file_path, 'rb') as f:
        while True:
            chunk = f.read(65536)
            if not chunk:
                break
            h.update(chunk)
    return h.hexdigest()


def formatar_bytes(num_bytes: float) -> str:
    """Formata tamanho em bytes para unidade legível (KB, MB, GB)."""
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if abs(num_bytes) < 1024.0:
            return f"{num_bytes:3.2f} {unit}"
        num_bytes /= 1024.0
    return f"{num_bytes:.2f} PB"


class BackupManager:
    """Gerencia backups automáticos antes de modificações ou sanitizações locais."""
    @staticmethod
    def criar_backup_projeto(src_dir: str, tag: str = "sanitizacao") -> str:
        inicializar_diretorios_dados()
        nome_proj = os.path.basename(os.path.normpath(src_dir)) or "projeto"
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        destino_zip_base = os.path.join(APP_BACKUP_DIR, f"{nome_proj}_{tag}_{ts}")
        arquivo_zip = shutil.make_archive(destino_zip_base, 'zip', src_dir)
        return arquivo_zip

    @staticmethod
    def listar_backups() -> List[str]:
        inicializar_diretorios_dados()
        if not os.path.exists(APP_BACKUP_DIR):
            return []
        arquivos = [
            os.path.join(APP_BACKUP_DIR, f)
            for f in os.listdir(APP_BACKUP_DIR)
            if f.endswith(".zip")
        ]
        return sorted(arquivos, key=lambda x: os.path.getmtime(x), reverse=True)

    @staticmethod
    def restaurar_backup(caminho_zip: str, pasta_destino: str):
        if not os.path.exists(caminho_zip):
            raise KanivetError("Arquivo de backup não encontrado.")
        shutil.unpack_archive(caminho_zip, pasta_destino, 'zip')


# ======================================================================================
# 7. GERENCIAMENTO DE TAREFAS E CONCORRÊNCIA
# ======================================================================================
class TaskManager:
    """Executor assíncrono com fila thread-safe para o Tkinter, progresso e cancelamento."""
    def __init__(self, root: tk.Tk, log_cb: Callable[[str], None], status_cb: Callable[[str], None], progress_cb: Callable[[float], None]):
        self.root = root
        self.log_cb = log_cb
        self.status_cb = status_cb
        self.progress_cb = progress_cb
        self.ui_queue: queue.Queue = queue.Queue()
        self.cancel_event = threading.Event()
        self.active_tasks = 0
        self._poll_queue()

    def _poll_queue(self):
        try:
            while True:
                action, payload = self.ui_queue.get_nowait()
                if action == "log":
                    self.log_cb(payload)
                elif action == "status":
                    self.status_cb(payload)
                elif action == "progress":
                    self.progress_cb(payload)
                elif action == "callback":
                    func, args = payload
                    func(*args)
        except queue.Empty:
            pass
        self.root.after(60, self._poll_queue)

    def post_log(self, msg: str):
        self.ui_queue.put(("log", mascarar_credenciais(msg)))

    def post_status(self, msg: str):
        self.ui_queue.put(("status", msg))

    def post_progress(self, value: float):
        self.ui_queue.put(("progress", max(0.0, min(100.0, float(value)))))

    def post_callback(self, func: Callable, *args):
        self.ui_queue.put(("callback", (func, args)))

    def solicitar_cancelamento(self):
        if self.active_tasks > 0:
            self.cancel_event.set()
            self.post_log("[TAREFA] Solicitação de cancelamento cooperativo enviada...")
            self.post_status("Cancelando operação em andamento...")

    def run_async(self, nome_tarefa: str, target_func: Callable, on_complete: Optional[Callable] = None):
        if self.active_tasks == 0:
            self.cancel_event.clear()
        self.active_tasks += 1
        self.post_status(f"Executando: {nome_tarefa}...")
        self.post_progress(5.0)

        def _wrapper():
            try:
                res = target_func(self.cancel_event, self.post_progress)
                self.post_progress(100.0)
                if on_complete:
                    self.post_callback(on_complete, res)
            except TaskCancelledError:
                self.post_log(f"[CANCELADO] A tarefa '{nome_tarefa}' foi interrompida pelo usuário.")
                self.post_status("Operação cancelada.")
                self.post_progress(0.0)
            except Exception as e:
                self.post_log(f"[ERRO EM '{nome_tarefa}'] {mascarar_credenciais(str(e))}")
                self.post_status("Erro durante a execução.")
                self.post_progress(0.0)
            finally:
                self.active_tasks = max(0, self.active_tasks - 1)
                if self.active_tasks == 0:
                    self.post_status("Pronto.")

        threading.Thread(target=_wrapper, daemon=True).start()


# ======================================================================================
# 8. MÓDULOS DE SEGURANÇA (SECURITY CENTER)
# ======================================================================================
class SecurityCenterEngine:
    """Motor avançado de auditoria de segredos, classificação de severidade e sanitização."""
    @staticmethod
    def inspecionar_projeto(
        root_dir: str,
        incluir_historico_git: bool = False,
        ignorar_falsos_positivos: bool = True,
        cancel_event: Optional[threading.Event] = None,
        progress_cb: Optional[Callable[[float], None]] = None
    ) -> Dict[str, Any]:
        achados: List[Dict[str, Any]] = []
        arquivos_sensibles: List[Dict[str, str]] = []
        todos_arquivos = []

        for r, dirs, files in os.walk(root_dir):
            dirs[:] = [d for d in dirs if d not in IGNORE_DIRS]
            for f in files:
                todos_arquivos.append(os.path.join(r, f))

        total = max(1, len(todos_arquivos))
        for idx, fpath in enumerate(todos_arquivos):
            if cancel_event and cancel_event.is_set():
                raise TaskCancelledError()
            if progress_cb and idx % 10 == 0:
                progress_cb(10.0 + (idx / total) * 75.0)

            rel_path = os.path.relpath(fpath, root_dir)
            fname = os.path.basename(fpath)
            _, ext = os.path.splitext(fname)

            # Detecção de .env, certificados e chaves privadas
            if fname in RESTRICTED_EXACT_FILES or fname.lower().startswith(".env") or ext.lower() in {'.pem', '.key', '.pfx', '.pkcs12', '.crt'}:
                arquivos_sensibles.append({
                    "arquivo": rel_path,
                    "tipo": "Arquivo Sensível / Certificado / .env",
                    "severidade": "CRITICAL" if ext.lower() in {'.pem', '.key', '.pfx'} or fname.startswith(".env") else "HIGH"
                })

            if is_binary_file(fpath):
                continue

            try:
                conteudo, _ = safe_read_file_text(fpath)
            except Exception:
                continue

            linhas = conteudo.splitlines()
            for num_linha, texto_linha in enumerate(linhas, start=1):
                for regra in SECURITY_RULES_CATALOG:
                    for match in re.finditer(regra["regex"], texto_linha):
                        trecho = match.group(0)
                        eh_fp = any(fp.lower() in trecho.lower() for fp in FALSE_POSITIVE_PLACEHOLDERS)
                        if eh_fp and ignorar_falsos_positivos:
                            continue
                        # Mascara parcialmente o valor encontrado para relatórios seguros
                        trecho_seguro = trecho[:6] + "..." + trecho[-4:] if len(trecho) > 14 else "***SEGRED0***"
                        achados.append({
                            "regra_id": regra["id"],
                            "tipo": regra["name"],
                            "severidade": "LOW (Falso Positivo Provável)" if eh_fp else regra["severity"],
                            "arquivo": rel_path,
                            "linha": num_linha,
                            "amostra_mascarada": trecho_seguro,
                            "falso_positivo": eh_fp
                        })

        # Auditoria opcional do histórico Git (últimos 20 commits)
        achados_git = []
        if incluir_historico_git and os.path.exists(os.path.join(root_dir, ".git")):
            try:
                p = subprocess.run(
                    ["git", "log", "-p", "-n", "20"],
                    cwd=root_dir, capture_output=True, text=True, timeout=25, shell=False, errors="replace"
                )
                if p.returncode == 0 and p.stdout:
                    for regra in SECURITY_RULES_CATALOG[:6]:
                        matches = re.findall(regra["regex"], p.stdout)
                        if matches:
                            achados_git.append({
                                "regra_id": regra["id"],
                                "tipo": f"[HISTÓRICO GIT] {regra['name']}",
                                "ocorrencias": len(matches),
                                "severidade": "CRITICAL"
                            })
            except Exception:
                pass

        resumo_sev = Counter(a["severidade"] for a in achados)
        return {
            "diretorio": root_dir,
            "timestamp": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
            "arquivos_inspecionados": len(todos_arquivos),
            "total_ocorrencias": len(achados),
            "arquivos_sensiveis": arquivos_sensibles,
            "ocorrencias": achados,
            "historico_git": achados_git,
            "resumo_severidade": dict(resumo_sev),
            "aviso_legal": "A ausência de ocorrências detectadas não garante que o projeto esteja 100% livre de vulnerabilidades ou segredos ofuscados."
        }

    @staticmethod
    def exportar_relatorio(dados: Dict[str, Any], caminho_saida: str):
        ext = os.path.splitext(caminho_saida)[1].lower()
        if ext == ".json":
            with open(caminho_saida, "w", encoding="utf-8") as f:
                json.dump(dados, f, ensure_ascii=False, indent=2)
        elif ext == ".csv":
            with open(caminho_saida, "w", encoding="utf-8", newline="") as f:
                writer = csv.writer(f)
                writer.writerow(["Regra", "Tipo", "Severidade", "Arquivo", "Linha", "Amostra Mascarada", "Falso Positivo"])
                for item in dados.get("ocorrencias", []):
                    writer.writerow([
                        item["regra_id"], item["tipo"], item["severidade"],
                        item["arquivo"], item["linha"], item["amostra_mascarada"], item["falso_positivo"]
                    ])
        else:
            # HTML
            linhas_html = [
                "<!DOCTYPE html><html><head><meta charset='utf-8'><title>Relatório Security Center - Kanivet XP</title>",
                "<style>body{font-family:Tahoma,sans-serif;background:#F4F4F0;padding:20px;} table{border-collapse:collapse;width:100%;background:#fff;} th,td{border:1px solid #ccc;padding:8px;text-align:left;} th{background:#0A246A;color:#fff;} .CRITICAL{color:#a00;font-weight:bold;} .HIGH{color:#d60;font-weight:bold;}</style></head><body>",
                f"<h2>🛡️ Relatório de Auditoria de Segurança — Kanivet XP Nexus</h2>",
                f"<p><b>Diretório:</b> {dados['diretorio']} | <b>Data:</b> {dados['timestamp']}</p>",
                f"<p><b>Arquivos Inspecionados:</b> {dados['arquivos_inspecionados']} | <b>Ocorrências de Segredos:</b> {dados['total_ocorrencias']} | <b>Arquivos Sensíveis (.env/Chaves):</b> {len(dados['arquivos_sensiveis'])}</p>",
                "<h3>Ocorrências no Código</h3><table><tr><th>ID</th><th>Severidade</th><th>Tipo</th><th>Arquivo</th><th>Linha</th><th>Amostra (Mascarada)</th></tr>"
            ]
            for o in dados.get("ocorrencias", []):
                linhas_html.append(f"<tr><td>{o['regra_id']}</td><td class='{o['severidade']}'>{o['severidade']}</td><td>{o['tipo']}</td><td>{o['arquivo']}</td><td>{o['linha']}</td><td><code>{o['amostra_mascarada']}</code></td></tr>")
            linhas_html.append(f"</table><p><em>{dados['aviso_legal']}</em></p></body></html>")
            with open(caminho_saida, "w", encoding="utf-8") as f:
                f.write("\n".join(linhas_html))


# ======================================================================================
# 9. MÓDULOS GIT (GIT CONTROL ENGINE SEGURO)
# ======================================================================================
class GitControlEngine:
    """Executor seguro de operações Git com shell=False, timeout e mascaramento de PAT."""
    @staticmethod
    def run_git_command(args: List[str], cwd: str, timeout: int = 60) -> Tuple[int, str, str]:
        cmd = ["git"] + [str(a) for a in args if a is not None]
        try:
            proc = subprocess.run(
                cmd,
                cwd=cwd,
                capture_output=True,
                text=True,
                timeout=timeout,
                shell=False,
                errors="replace"
            )
            out = mascarar_credenciais(proc.stdout.strip())
            err = mascarar_credenciais(proc.stderr.strip())
            return proc.returncode, out, err
        except FileNotFoundError:
            return 127, "", "Executável 'git' não encontrado no PATH do sistema operacional."
        except subprocess.TimeoutExpired:
            return 124, "", f"Tempo limite excedido ({timeout}s) ao executar: git {' '.join(args[:2])}"
        except Exception as e:
            return 1, "", mascarar_credenciais(str(e))

    @staticmethod
    def detectar_conflitos(cwd: str) -> List[str]:
        code, out, _ = GitControlEngine.run_git_command(["diff", "--name-only", "--diff-filter=U"], cwd)
        if code == 0 and out:
            return [l.strip() for l in out.splitlines() if l.strip()]
        return []

    @staticmethod
    def analisar_arquivos_grandes(cwd: str, limite_mb: float = 10.0) -> List[Tuple[str, float]]:
        grandes = []
        limite_bytes = limite_mb * 1024 * 1024
        for r, dirs, files in os.walk(cwd):
            dirs[:] = [d for d in dirs if d != ".git"]
            for f in files:
                fp = os.path.join(r, f)
                try:
                    sz = os.path.getsize(fp)
                    if sz >= limite_bytes:
                        grandes.append((os.path.relpath(fp, cwd), sz / (1024 * 1024)))
                except Exception:
                    pass
        return sorted(grandes, key=lambda x: x[1], reverse=True)

    @staticmethod
    def diagnosticar_config(cwd: str) -> str:
        rel = ["=== DIAGNÓSTICO DE CONFIGURAÇÃO GIT ==="]
        for escopo, args in [
            ("Versão do Git", ["--version"]),
            ("Usuário Local", ["config", "--get", "user.name"]),
            ("E-mail Local", ["config", "--get", "user.email"]),
            ("Branch Atual", ["rev-parse", "--abbrev-ref", "HEAD"]),
            ("Remotos Configurados", ["remote", "-v"]),
        ]:
            _, out, err = GitControlEngine.run_git_command(args, cwd)
            rel.append(f"• {escopo:22s}: {out or err or '(Não definido)'}")
        conflitos = GitControlEngine.detectar_conflitos(cwd)
        rel.append(f"• Arquivos em Conflito  : {len(conflitos)} ({', '.join(conflitos) if conflitos else 'Nenhum'})")
        return "\n".join(rel)


# ======================================================================================
# 10. MOTOR MDNATOR v5.0 (DOCUMENTAÇÃO, CONSOLIDAÇÃO E PERFIS)
# ======================================================================================
class MDnatorEngine:
    """Motor avançado de consolidação documental para projetos e modelos de linguagem."""
    @staticmethod
    def escanear_e_consolidar(
        caminho: str,
        perfil: str = "Universal (Todos os Formatos)",
        max_kb_arquivo: int = 512,
        modo_incremental: bool = False,
        exclusoes_extras: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        extensoes_ativas = MDNATOR_PROFILES.get(perfil, TEXT_CODE_EXTENSIONS)
        ignorar = set(IGNORE_DIRS)
        if exclusoes_extras:
            ignorar.update(x.strip() for x in exclusoes_extras if x.strip())

        cache_anterior = {}
        if modo_incremental and os.path.exists(APP_MDNATOR_CACHE):
            try:
                with open(APP_MDNATOR_CACHE, "r", encoding="utf-8") as f:
                    cache_anterior = json.load(f).get(caminho, {})
            except Exception:
                cache_anterior = {}

        novo_cache = {}
        arvore_linhas = []
        arquivos_processados = []
        arquivos_vazios = []
        arquivos_ignorados_tamanho = []
        hashes_vistos: Dict[str, List[str]] = {}
        distribuicao_lang: Counter = Counter()
        total_linhas = 0

        for dirpath, dirnames, filenames in os.walk(caminho):
            dirnames[:] = [d for d in dirnames if d not in ignorar]
            rel_dir = os.path.relpath(dirpath, caminho)
            prefixo = "" if rel_dir == "." else "│   " * (rel_dir.count(os.sep) + 1)

            if rel_dir != ".":
                arvore_linhas.append(f"{'│   ' * rel_dir.count(os.sep)}├── 📁 {os.path.basename(dirpath)}/")

            for filename in sorted(filenames):
                _, ext = os.path.splitext(filename)
                ext_low = ext.lower()
                if ext_low not in extensoes_ativas:
                    continue

                f_path = os.path.join(dirpath, filename)
                rel_file = os.path.relpath(f_path, caminho)
                arvore_linhas.append(f"{prefixo}├── 💾 {filename}")

                try:
                    tamanho_bytes = os.path.getsize(f_path)
                except Exception:
                    continue

                if tamanho_bytes == 0:
                    arquivos_vazios.append(rel_file)

                if max_kb_arquivo > 0 and tamanho_bytes > max_kb_arquivo * 1024:
                    arquivos_ignorados_tamanho.append(f"{rel_file} ({formatar_bytes(tamanho_bytes)})")
                    continue

                if is_binary_file(f_path):
                    continue

                try:
                    f_hash = calcular_sha256(f_path)
                    hashes_vistos.setdefault(f_hash, []).append(rel_file)
                    novo_cache[rel_file] = f_hash
                    if modo_incremental and cache_anterior.get(rel_file) == f_hash:
                        continue

                    code_content, l_count = safe_read_file_text(f_path)
                    total_linhas += l_count
                    lang = LANG_MAP.get(ext_low, "text")
                    distribuicao_lang[lang] += 1

                    arquivos_processados.append({
                        "rel_path": rel_file,
                        "ext": ext_low,
                        "lang": lang,
                        "linhas": l_count,
                        "bytes": tamanho_bytes,
                        "sha256": f_hash[:12],
                        "conteudo": code_content
                    })
                except Exception:
                    pass

        # Atualiza cache incremental
        try:
            inicializar_diretorios_dados()
            todo_cache = {}
            if os.path.exists(APP_MDNATOR_CACHE):
                with open(APP_MDNATOR_CACHE, "r", encoding="utf-8") as f:
                    todo_cache = json.load(f)
            todo_cache[caminho] = novo_cache
            with open(APP_MDNATOR_CACHE, "w", encoding="utf-8") as f:
                json.dump(todo_cache, f, indent=2)
        except Exception:
            pass

        duplicados = {h[:12]: paths for h, paths in hashes_vistos.items() if len(paths) > 1}

        return {
            "projeto": os.path.basename(os.path.normpath(caminho)) or "projeto",
            "caminho": caminho,
            "perfil": perfil,
            "timestamp": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
            "total_arquivos": len(arquivos_processados),
            "total_linhas": total_linhas,
            "distribuicao_linguagem": dict(distribuicao_lang),
            "arquivos_vazios": arquivos_vazios,
            "arquivos_excedendo_limite": arquivos_ignorados_tamanho,
            "duplicidades_hash": duplicados,
            "arvore": arvore_linhas,
            "arquivos": arquivos_processados
        }

    @staticmethod
    def formatar_saida(dados: Dict[str, Any], formato: str = ".md") -> str:
        if formato == ".json":
            return json.dumps(dados, ensure_ascii=False, indent=2)

        linhas = [
            f"# 🟩 KANIVET XP // MDNATOR v5.0 — PACOTE DOCUMENTAL ({dados['perfil']})\n",
            f"> **Projeto Alvo:** `{dados['projeto']}`",
            f"> **Caminho Host:** `{dados['caminho']}`",
            f"> **Data de Geração:** `{dados['timestamp']}`",
            f"> **Arquivos Compilados:** `{dados['total_arquivos']}` | **Total de Linhas:** `{dados['total_linhas']:,}`\n",
            "---\n",
            "## 📑 Sumário Navegável e Métricas\n"
        ]
        for idx, arq in enumerate(dados["arquivos"], start=1):
            linhas.append(f"{idx}. `{arq['rel_path']}` ({arq['linhas']} linhas, {arq['lang']}, SHA256: `{arq['sha256']}`)")

        if dados["distribuicao_linguagem"]:
            linhas.append("\n### 📊 Distribuição por Linguagem")
            for lg, qtd in dados["distribuicao_linguagem"].items():
                linhas.append(f"- **{lg}**: {qtd} arquivo(s)")

        if dados["arquivos_vazios"]:
            linhas.append(f"\n- **Arquivos Vazios Detectados ({len(dados['arquivos_vazios'])}):** `{', '.join(dados['arquivos_vazios'])}`")

        if dados["duplicidades_hash"]:
            linhas.append("\n### ⚠️ Duplicidades Exatas por Hash SHA-256")
            for h, lista in dados["duplicidades_hash"].items():
                linhas.append(f"- Hash `{h}`: {', '.join(lista)}")

        linhas.append("\n---\n## 🌳 Árvore de Diretórios\n\n```text")
        linhas.extend(dados["arvore"])
        linhas.append("```\n\n---\n## 📄 Códigos-Fonte Consolidados\n")

        for arq in dados["arquivos"]:
            badge = " [FIRMWARE EMBARCADO ESP32 / ARDUINO]" if arq["ext"] in ['.io', '.ino'] else ""
            linhas.append(f"\n### 💾 Módulo: `{arq['rel_path']}` ({arq['linhas']} linhas){badge}\n")
            linhas.append(f"```{arq['lang']}\n{arq['conteudo']}\n```\n\n---")

        return "\n".join(linhas)


# ======================================================================================
# 11. MÓDULO INFOPLAN PRO (AUDITORIA DE DADOS, ESTATÍSTICA E VISUALIZAÇÃO REAL)
# ======================================================================================
def formatar_valor_planilha(valor: Any) -> str:
    """Preservada integralmente do arquivo original (protegida contra valores não escalares)."""
    try:
        if pd is not None and pd.isna(valor):
            return "[VAZIO]"
    except (TypeError, ValueError):
        # Valores não escalares (listas, arrays) não possuem um único estado de "vazio"
        pass
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
    """Preservada integralmente do arquivo original."""
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


def calcular_metricas_estatisticas_avancadas(valores: List[float]) -> Dict[str, Any]:
    """
    Calcula indicadores descritivos com rigor metodológico:
    - Variância amostral (s²) com correção de Bessel (n - 1).
    - Assimetria de Fisher-Pearson (g1) e Curtose em Excesso de Fisher (g2).
    - Coeficiente de Variação (CV%) reportado apenas quando |média| > 1e-9.
    """
    n = len(valores)
    if n == 0:
        return {}
    ordenados = sorted(valores)
    soma = sum(ordenados)
    media = soma / n
    minimo = ordenados[0]
    maximo = ordenados[-1]
    amplitude = maximo - minimo

    def _percentil(p: float) -> float:
        if n == 1:
            return ordenados[0]
        pos = (n - 1) * p
        base = int(math.floor(pos))
        resto = pos - base
        if base + 1 < n:
            return ordenados[base] + resto * (ordenados[base + 1] - ordenados[base])
        return ordenados[base]

    q1 = _percentil(0.25)
    mediana = _percentil(0.50)
    q3 = _percentil(0.75)
    p10 = _percentil(0.10)
    p90 = _percentil(0.90)
    iqr = q3 - q1

    contagem = Counter(ordenados)
    max_freq = max(contagem.values())
    modas = [k for k, v in contagem.items() if v == max_freq]
    moda_str = f"{modas[0]:.4f}" if (len(modas) == 1 and max_freq > 1) else "Amodal / Multimoda"

    variancia = sum((x - media) ** 2 for x in ordenados) / (n - 1) if n > 1 else 0.0
    desvio_padrao = math.sqrt(variancia)
    cv_pct = (desvio_padrao / abs(media)) * 100.0 if abs(media) > 1e-9 else None

    # Assimetria amostral ajustada de Fisher-Pearson (G1) e Curtose em Excesso (G2)
    assimetria = None
    curtose_excesso = None
    if n >= 3 and desvio_padrao > 1e-12:
        m3 = sum(((x - media) / desvio_padrao) ** 3 for x in ordenados)
        assimetria = (n / ((n - 1) * (n - 2))) * m3
    if n >= 4 and desvio_padrao > 1e-12:
        m4 = sum(((x - media) / desvio_padrao) ** 4 for x in ordenados)
        termo1 = (n * (n + 1)) / ((n - 1) * (n - 2) * (n - 3)) * m4
        termo2 = (3 * ((n - 1) ** 2)) / ((n - 2) * (n - 3))
        curtose_excesso = termo1 - termo2

    return {
        "n": n, "soma": soma, "media": media, "mediana": mediana, "moda": moda_str,
        "minimo": minimo, "maximo": maximo, "amplitude": amplitude,
        "variancia": variancia, "desvio_padrao": desvio_padrao,
        "q1": q1, "q3": q3, "iqr": iqr, "p10": p10, "p90": p90,
        "cv_pct": cv_pct, "assimetria": assimetria, "curtose_excesso": curtose_excesso,
        "valores_ordenados": ordenados
    }


def estatisticas_coluna(serie, tipo_str: str) -> List[str]:
    """Preservada e expandida com quartis, IQR, CV, assimetria e curtose documentadas."""
    resultado = []
    if pd is None:
        return resultado
    validos = serie.dropna()
    if len(validos) == 0:
        return resultado

    if tipo_str in ["INTEIRO", "NÚMERO DECIMAL", "NUMÉRICO"]:
        nums = pd.to_numeric(validos, errors="coerce").dropna().tolist()
        if len(nums) > 0:
            m = calcular_metricas_estatisticas_avancadas([float(x) for x in nums])
            resultado.append(f"  • Soma: {m['soma']:,.4f}")
            resultado.append(f"  • Média: {m['media']:,.4f}")
            resultado.append(f"  • Mediana (Q2): {m['mediana']:,.4f} | Moda: {m['moda']}")
            resultado.append(f"  • Mínimo: {m['minimo']} | Máximo: {m['maximo']} | Amplitude: {m['amplitude']:,.4f}")
            resultado.append(f"  • Variância Amostral (s²): {m['variancia']:,.4f} | Desvio Padrão (s): {m['desvio_padrao']:,.4f}")
            resultado.append(f"  • Quartis: Q1={m['q1']:,.4f} | Q3={m['q3']:,.4f} | IIQ (IQR)={m['iqr']:,.4f} | P10={m['p10']:,.4f} | P90={m['p90']:,.4f}")
            if m['cv_pct'] is not None:
                resultado.append(f"  • Coeficiente de Variação (CV): {m['cv_pct']:.2f}%")
            if m['assimetria'] is not None:
                resultado.append(f"  • Assimetria Fisher-Pearson (G1): {m['assimetria']:.4f}")
            if m['curtose_excesso'] is not None:
                resultado.append(f"  • Curtose em Excesso Fisher (G2): {m['curtose_excesso']:.4f}")
    elif "DATA" in tipo_str:
        datas = pd.to_datetime(validos, errors="coerce", dayfirst=True).dropna()
        if len(datas) > 0:
            d_min = datas.min()
            d_max = datas.max()
            resultado.append("  • Data Mínima: " + d_min.strftime("%d/%m/%Y %H:%M:%S"))
            resultado.append("  • Data Máxima: " + d_max.strftime("%d/%m/%Y %H:%M:%S"))
            resultado.append(f"  • Amplitude Temporal: {(d_max - d_min).days} dia(s)")
    return resultado


def carregar_abas_planilha(caminho: str) -> Dict[str, Any]:
    """Carrega abas de arquivos .xlsx, .xls ou .csv."""
    if not PANDAS_AVAILABLE:
        raise ImportError(
            "O módulo 'pandas' não está instalado neste interpretador.\n"
            "Por favor, execute: pip install pandas openpyxl xlrd"
        )
    extensao = os.path.splitext(caminho)[1].lower()
    if extensao == ".csv":
        df_csv = pd.read_csv(caminho, sep=None, engine="python")
        return {"CSV_Principal": df_csv}
    elif extensao == ".xls":
        return pd.read_excel(caminho, sheet_name=None, engine="xlrd")
    elif extensao == ".xlsx":
        return pd.read_excel(caminho, sheet_name=None, engine="openpyxl")
    else:
        raise ValueError("Formato não suportado. Selecione um arquivo .xlsx, .xls ou .csv.")


def gerar_relatorio_infoplan(caminho: str) -> str:
    """Preservada e expandida com Auditoria de Qualidade, Chaves Candidatas e Matriz de Correlação."""
    todas_as_abas = carregar_abas_planilha(caminho)
    extensao = os.path.splitext(caminho)[1].lower()
    tamanho_bytes = os.path.getsize(caminho)
    tamanho_mb = tamanho_bytes / (1024 * 1024)
    data_modificacao = datetime.fromtimestamp(os.path.getmtime(caminho))

    relatorio = [
        "=" * 85,
        "   KANIVET XP // INFOPLAN PRO - RADIOGRAFIA ESTRUTURAL, AUDITORIA E ESTATÍSTICA",
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
        qtd_linhas = len(df)
        qtd_colunas = len(df.columns)
        linhas_duplicadas = int(df.duplicated().sum()) if qtd_linhas > 0 else 0
        colunas_constantes = [str(c) for c in df.columns if df[c].nunique(dropna=False) <= 1] if qtd_colunas > 0 else []
        chaves_candidatas = [
            str(c) for c in df.columns
            if qtd_linhas > 0 and df[c].notna().all() and df[c].nunique() == qtd_linhas
        ]

        relatorio.extend([
            "=" * 85,
            f"ABA #{numero_aba:02d}: {nome_aba}",
            "=" * 85,
            "",
            "DIMENSÕES E AUDITORIA DE QUALIDADE DA ABA:",
            "-" * 85,
            f"  Linhas Totais        : {qtd_linhas:,}",
            f"  Colunas              : {qtd_colunas:,}",
            f"  Linhas Duplicadas    : {linhas_duplicadas:,}",
            f"  Colunas Constantes   : {', '.join(colunas_constantes) if colunas_constantes else 'Nenhuma'}",
            f"  Possíveis Chaves (PK): {', '.join(chaves_candidatas) if chaves_candidatas else 'Nenhuma identificada'}",
        ])

        if qtd_linhas > 0 and qtd_colunas > 0:
            celula_final = f"{get_column_letter(qtd_colunas)}{qtd_linhas + 1}"
            relatorio.append(f"  Range de Dados       : A1:{celula_final}")

        relatorio.extend(["", "ANÁLISE DETALHADA DAS COLUNAS:", "-" * 85])

        for col_idx, coluna in enumerate(df.columns, start=1):
            serie = df[coluna]
            letra_col = get_column_letter(col_idx)
            tipo_detectado = identificar_tipo_serie(serie)
            total_reg = len(serie)
            preenchidos = int(serie.notna().sum())
            vazios = int(serie.isna().sum())
            pct_preenchido = (preenchidos / total_reg * 100) if total_reg > 0 else 0
            unicos = int(serie.nunique(dropna=True))

            # Detecção de inconsistência mista de tipos em coluna object
            tipos_python = set(type(v).__name__ for v in serie.dropna())
            inconsistencia_str = f"Sim ({', '.join(sorted(tipos_python))})" if len(tipos_python) > 1 else "Não"

            relatorio.extend([
                "",
                f"  [COLUNA {col_idx:02d} | Letra: {letra_col}] => {repr(str(coluna))}",
                f"    • Tipo Heurístico      : {tipo_detectado}",
                f"    • Tipo Pandas Nativo   : {serie.dtype}",
                f"    • Inconsistência Mista : {inconsistencia_str}",
                f"    • Registros Totais     : {total_reg:,}",
                f"    • Preenchidos / Vazios : {preenchidos:,} / {vazios:,} ({pct_preenchido:.2f}% preenchido)",
                f"    • Valores Únicos       : {unicos:,}",
            ])

            stats = estatisticas_coluna(serie, tipo_detectado)
            if stats:
                relatorio.append("    • Estatísticas Descritivas:")
                relatorio.extend(["    " + s for s in stats])

            # Frequências absolutas e relativas (Top 5 categorias)
            # [CORREÇÃO] Operador morsa (:=) não pode ser usado diretamente após 'and' sem parênteses
            preenc_val = serie.dropna()
            if unicos > 0 and len(preenc_val) > 0:
                top_freq = preenc_val.value_counts().head(5)
                relatorio.append("    • Top 5 Frequências (Absoluta | Relativa):")
                for val_k, count_v in top_freq.items():
                    rel_pct = (count_v / preenchidos) * 100 if preenchidos > 0 else 0
                    relatorio.append(f"        - {formatar_valor_planilha(val_k)}: {count_v:,} ({rel_pct:.2f}%)")

            valores_unicos = serie.dropna().astype(str).unique().tolist()
            relatorio.append(f"    • Amostra de Valores Únicos (Primeiros {AMOSTRA_VALORES}):")
            if valores_unicos:
                for v in valores_unicos[:AMOSTRA_VALORES]:
                    relatorio.append(f"        - {v}")
            else:
                relatorio.append("        [Nenhum dado legível]")

            relatorio.append("    • Amostra Posicional de Células:")
            qtd_amostra = min(AMOSTRA_VALORES, len(serie))
            for pos in range(qtd_amostra):
                end_cel = f"{letra_col}{pos + 2}"
                val_cel = formatar_valor_planilha(serie.iloc[pos])
                relatorio.append(f"        {end_cel} = {val_cel}")

        # Matriz de Correlação de Pearson para variáveis numéricas
        df_num = df.select_dtypes(include=['number'])
        if len(df_num.columns) >= 2 and len(df_num) >= 2:
            relatorio.extend(["", "MATRIZ DE CORRELAÇÃO DE PEARSON (VARIÁVEIS NUMÉRICAS):", "-" * 85])
            corr_df = df_num.corr(method='pearson')
            relatorio.append(corr_df.round(4).to_string())

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
            preenchidas_total = int(df.notna().sum().sum())
            vazias_total = total_cells - preenchidas_total
            taxa_preenchimento = (preenchidas_total / total_cells) * 100
            relatorio.append(f"  Células Totais       : {total_cells:,}")
            relatorio.append(f"  Células Preenchidas  : {preenchidas_total:,}")
            relatorio.append(f"  Células Vazias       : {vazias_total:,}")
            relatorio.append(f"  Taxa de Ocupação     : {taxa_preenchimento:.2f}%")
        relatorio.append("")

    relatorio.extend([
        "=" * 85,
        "NOTA METODOLÓGICA: Variância/Desvio Padrão utilizam denominador amostral (n-1).",
        "Assimetria (G1) e Curtose em Excesso (G2) seguem a formulação amostral de Fisher.",
        "   [FIM DA RADIOGRAFIA INFOPLAN PRO - KANIVET XP NEXUS]",
        "=" * 85
    ])
    return "\n".join(relatorio)


GLOSSARIO_ESTATISTICO = """GLOSSÁRIO ESTATÍSTICO E PRESSUPOSTOS METODOLÓGICOS (INFOPLAN PRO)
================================================================================
1. MÉDIA ARITMÉTICA (x̄):
   • Técnico: Soma dos valores dividida pelo tamanho amostral n: x̄ = (1/n) Σ x_i.
   • Simplificado: Ponto de equilíbrio dos dados; sensível a valores extremos (outliers).

2. MEDIANA (Q2):
   • Técnico: Valor central que divide a amostra ordenada ao meio (50% abaixo, 50% acima).
   • Simplificado: Medida robusta de centro que não se distorce com valores discrepantes.

3. VARIÂNCIA AMOSTRAL (s²) E DESVIO PADRÃO (s):
   • Técnico: s² = [1 / (n - 1)] Σ (x_i - x̄)² (com correção de Bessel para amostras). s = √s².
   • Simplificado: Mede o espalhamento médio dos dados em torno da média na mesma unidade da variável.

4. QUARTIS (Q1, Q2, Q3) E INTERVALO INTERQUARTIL (IIQ / IQR):
   • Técnico: Q1 (percentil 25%), Q3 (percentil 75%), IQR = Q3 - Q1.
   • Simplificado: O IQR abrange os 50% centrais da distribuição; usado no Boxplot para detectar outliers
     (valores abaixo de Q1 - 1.5*IQR ou acima de Q3 + 1.5*IQR).

5. COEFICIENTE DE VARIAÇÃO (CV%):
   • Técnico: CV = (s / |x̄|) * 100. Condição de uso: Válido para escalas de razão com média não nula.
   • Simplificado: Dispersão relativa percentual; permite comparar variáveis de unidades diferentes.

6. ASSIMETRIA DE FISHER-PEARSON (G1):
   • Técnico: Momento central padronizado de 3ª ordem ajustado para tamanho amostral (n >= 3).
   • Simplificado: G1 ≈ 0 indica simetria; G1 > 0 cauda longa à direita; G1 < 0 cauda longa à esquerda.

7. CURTOSE EM EXCESSO DE FISHER (G2):
   • Técnico: Momento central padronizado de 4ª ordem menos 3 (referência Normal = 0, requer n >= 4).
   • Simplificado: Mede o peso das caudas e propensão a outliers (G2 > 0 leptocúrtica; G2 < 0 platicúrtica).

8. CORRELAÇÃO LINEAR DE PEARSON (r):
   • Técnico: Covariância padronizada entre X e Y, variando em [-1, +1]. Pressupõe relação linear.
   • Simplificado: Mede a força da associação em linha reta (+1 direta perfeita, -1 inversa, 0 sem relação linear).
"""


# ======================================================================================
# 12. HARDWARE-Z PRO (TELEMETRIA AVANÇADA E SESSÃO)
# ======================================================================================
HISTORICO_METRICAS_SESSAO: List[Dict[str, Any]] = []


def obter_telemetria_hardware() -> Dict[str, Any]:
    """Preservada e expandida com partições, rede, top processos e histórico de sessão."""
    dados = {
        "so": f"{platform.system()} {platform.release()} (Build {platform.version()})",
        "arquitetura": platform.machine(),
        "processador": platform.processor() or "Processador Padrão",
        "python_version": platform.python_version(),
        "hostname": platform.node(),
        "cpus_logicas": os.cpu_count() or 1,
        "cpus_fisicas": "N/D",
        "cpu_percent": "N/D",
        "ram_total": "N/D",
        "ram_usada": "N/D",
        "ram_livre": "N/D",
        "ram_percent": "N/D",
        "disco_total": "N/D",
        "disco_usado": "N/D",
        "disco_livre": "N/D",
        "disco_percent": "N/D",
        "uptime": "N/D",
        "rede_enviado": "N/D",
        "rede_recebido": "N/D",
        "particoes": [],
        "top_processos": []
    }

    if PSUTIL_AVAILABLE:
        try:
            dados["cpus_fisicas"] = psutil.cpu_count(logical=False) or "N/D"
            dados["cpu_percent"] = f"{psutil.cpu_percent(interval=0.1):.1f}%"
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

            net = psutil.net_io_counters()
            if net:
                dados["rede_enviado"] = formatar_bytes(net.bytes_sent)
                dados["rede_recebido"] = formatar_bytes(net.bytes_recv)

            for part in psutil.disk_partitions(all=False):
                try:
                    u = psutil.disk_usage(part.mountpoint)
                    dados["particoes"].append(
                        f"{part.device} ({part.fstype}) -> Livre: {u.free / (1024**3):.1f} GB / Total: {u.total / (1024**3):.1f} GB ({u.percent}%)"
                    )
                except Exception:
                    pass

            procs = []
            for p in psutil.process_iter(['pid', 'name', 'memory_percent']):
                try:
                    procs.append(p.info)
                except Exception:
                    pass
            procs_ord = sorted(procs, key=lambda x: x.get('memory_percent') or 0.0, reverse=True)[:5]
            for pr in procs_ord:
                dados["top_processos"].append(f"PID {pr['pid']:6d} | {str(pr['name'])[:22]:22s} | RAM: {(pr.get('memory_percent') or 0.0):.2f}%")
        except Exception:
            pass
    else:
        try:
            total, used, free = shutil.disk_usage(os.path.abspath(os.sep))
            dados["disco_total"] = f"{total / (1024**3):.2f} GB"
            dados["disco_usado"] = f"{used / (1024**3):.2f} GB"
            dados["disco_livre"] = f"{free / (1024**3):.2f} GB"
            dados["disco_percent"] = f"{(used / total) * 100:.1f}%"
        except Exception:
            pass

    HISTORICO_METRICAS_SESSAO.append({
        "hora": datetime.now().strftime("%H:%M:%S"),
        "cpu": dados["cpu_percent"],
        "ram": dados["ram_percent"],
        "disco": dados["disco_percent"]
    })
    # [CORREÇÃO] Indentação normalizada
    if len(HISTORICO_METRICAS_SESSAO) > 50:
        del HISTORICO_METRICAS_SESSAO[0]

    return dados


# ======================================================================================
# 13. EXPLORADOR AVANÇADO DE PROJETOS
# ======================================================================================
class ProjectExplorerEngine:
    """Busca avançada, comparação de diretórios, detecção de duplicados e temporários."""
    @staticmethod
    def buscar_arquivos(
        root_dir: str,
        filtro_nome: str = "",
        filtro_texto: str = "",
        filtro_ext: str = ""
    ) -> List[Dict[str, Any]]:
        resultados = []
        ext_set = {e.strip().lower() for e in filtro_ext.split(",") if e.strip()}
        nome_low = filtro_nome.strip().lower()
        texto_low = filtro_texto.strip().lower()

        for r, dirs, files in os.walk(root_dir):
            dirs[:] = [d for d in dirs if d not in IGNORE_DIRS]
            for f in files:
                _, ext = os.path.splitext(f)
                if ext_set and ext.lower() not in ext_set:
                    continue
                if nome_low and nome_low not in f.lower():
                    continue

                fp = os.path.join(r, f)
                try:
                    st = os.stat(fp)
                except Exception:
                    continue

                if texto_low:
                    if is_binary_file(fp):
                        continue
                    try:
                        conteudo, _ = safe_read_file_text(fp)
                        if texto_low not in conteudo.lower():
                            continue
                    except Exception:
                        continue

                resultados.append({
                    "arquivo": os.path.relpath(fp, root_dir),
                    "ext": ext.lower() or "(sem ext)",
                    "tamanho_bytes": st.st_size,
                    "tamanho_fmt": formatar_bytes(st.st_size),
                    "modificado": datetime.fromtimestamp(st.st_mtime).strftime("%d/%m/%Y %H:%M")
                })
        return resultados

    @staticmethod
    def comparar_diretorios(dir_a: str, dir_b: str) -> Dict[str, List[str]]:
        mapa_a = {}
        mapa_b = {}
        for base, mapa in [(dir_a, mapa_a), (dir_b, mapa_b)]:
            for r, dirs, files in os.walk(base):
                dirs[:] = [d for d in dirs if d not in IGNORE_DIRS]
                for f in files:
                    fp = os.path.join(r, f)
                    rel = os.path.relpath(fp, base)
                    try:
                        mapa[rel] = calcular_sha256(fp)
                    except Exception:
                        pass

        apenas_a = sorted(set(mapa_a.keys()) - set(mapa_b.keys()))
        apenas_b = sorted(set(mapa_b.keys()) - set(mapa_a.keys()))
        comuns = set(mapa_a.keys()) & set(mapa_b.keys())
        diferentes = sorted(k for k in comuns if mapa_a[k] != mapa_b[k])
        identicos = sorted(k for k in comuns if mapa_a[k] == mapa_b[k])

        return {
            "apenas_em_A": apenas_a,
            "apenas_em_B": apenas_b,
            "modificados": diferentes,
            "identicos": identicos
        }

    @staticmethod
    def diagnosticar_espaco_e_temporarios(root_dir: str) -> Dict[str, Any]:
        por_ext: Counter = Counter()
        temporarios = []
        hashes: Dict[str, List[str]] = {}
        total_bytes = 0

        for r, dirs, files in os.walk(root_dir):
            dirs[:] = [d for d in dirs if d != ".git"]
            for f in files:
                fp = os.path.join(r, f)
                rel = os.path.relpath(fp, root_dir)
                _, ext = os.path.splitext(f)
                ext_low = ext.lower() or "(sem ext)"
                try:
                    sz = os.path.getsize(fp)
                    total_bytes += sz
                    por_ext[ext_low] += sz
                    if ext_low in TEMP_JUNK_EXTENSIONS or "__pycache__" in r:
                        temporarios.append(rel)
                    if sz > 0 and sz < 50 * 1024 * 1024:
                        h = calcular_sha256(fp)
                        hashes.setdefault(h, []).append(rel)
                except Exception:
                    pass

        duplicados = {h[:12]: v for h, v in hashes.items() if len(v) > 1}
        return {
            "total_bytes": total_bytes,
            "total_fmt": formatar_bytes(total_bytes),
            "uso_por_extensao": {k: formatar_bytes(v) for k, v in por_ext.most_common(10)},
            "arquivos_temporarios": temporarios,
            "duplicidades_hash": duplicados
        }


# ======================================================================================
# 14. MÓDULO CODE QUALITY (FERRAMENTAS EXTERNAS + ANALISADOR AST NATIVO)
# ======================================================================================
class CodeQualityEngine:
    """Executa linters/testes Python (Ruff, Black, Pytest, Mypy, Bandit) e inspeção AST nativa."""
    TOOLS = {
        "ruff": [sys.executable, "-m", "ruff", "check"],
        "black_check": [sys.executable, "-m", "black", "--check"],
        "mypy": [sys.executable, "-m", "mypy"],
        "bandit": [sys.executable, "-m", "bandit", "-r"],
        "pytest": [sys.executable, "-m", "pytest", "-q"]
    }

    @staticmethod
    def verificar_ferramentas_disponiveis() -> Dict[str, bool]:
        disp = {}
        for mod in ["ruff", "black", "mypy", "bandit", "pytest", "coverage"]:
            try:
                p = subprocess.run([sys.executable, "-m", mod, "--version"], capture_output=True, text=True, timeout=8, shell=False)
                disp[mod] = (p.returncode == 0)
            except Exception:
                disp[mod] = False
        return disp

    @staticmethod
    def inspecionar_ast_nativo(root_dir: str) -> List[Dict[str, Any]]:
        """Analisador estático AST Python embutido (funciona mesmo sem ferramentas externas)."""
        avisos = []
        for r, dirs, files in os.walk(root_dir):
            dirs[:] = [d for d in dirs if d not in IGNORE_DIRS]
            for f in files:
                if not f.endswith(".py"):
                    continue
                fp = os.path.join(r, f)
                rel = os.path.relpath(fp, root_dir)
                try:
                    codigo, _ = safe_read_file_text(fp)
                    tree = ast.parse(codigo, filename=rel)
                    for node in ast.walk(tree):
                        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                            end_ln = getattr(node, "end_lineno", node.lineno)
                            tam = end_ln - node.lineno
                            if tam > 120:
                                avisos.append({"arquivo": rel, "linha": node.lineno, "severidade": "WARNING", "msg": f"Função '{node.name}' extensa ({tam} linhas)."})
                        elif isinstance(node, ast.ExceptHandler) and node.type is None:
                            avisos.append({"arquivo": rel, "linha": node.lineno, "severidade": "INFO", "msg": "Bloco 'except:' genérico sem tipo específico."})
                        elif isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id in ("eval", "exec"):
                            avisos.append({"arquivo": rel, "linha": node.lineno, "severidade": "HIGH", "msg": f"Uso potencialmente perigoso de '{node.func.id}()'."})
                except SyntaxError as se:
                    avisos.append({"arquivo": rel, "linha": se.lineno or 1, "severidade": "ERROR", "msg": f"Erro de Sintaxe Python: {se.msg}"})
                except Exception:
                    pass
        return avisos

    @staticmethod
    def executar_ferramenta(nome: str, root_dir: str) -> str:
        if nome == "ast_nativo":
            itens = CodeQualityEngine.inspecionar_ast_nativo(root_dir)
            if not itens:
                return "[AST NATIVO] Nenhum erro de sintaxe ou alerta estrutural encontrado.\nNota: A ausência de alertas estáticos não garante ausência de bugs lógicos."
            linhas = [f"[AST NATIVO] {len(itens)} alerta(s) encontrado(s):"]
            for i in itens:
                linhas.append(f"  {i['arquivo']}:{i['linha']} [{i['severidade']}] -> {i['msg']}")
            return "\n".join(linhas)

        cmd_base = CodeQualityEngine.TOOLS.get(nome)
        if not cmd_base:
            return f"Ferramenta '{nome}' desconhecida."
        cmd = cmd_base + ["."]
        try:
            p = subprocess.run(cmd, cwd=root_dir, capture_output=True, text=True, timeout=60, shell=False, errors="replace")
            saida = (p.stdout + "\n" + p.stderr).strip()
            return f"[{nome.upper()} | Código {p.returncode}]\n{saida or 'Sem saídas reportadas.'}\n\nNota: Verificações estáticas não substituem testes funcionais completos."
        except Exception as e:
            return f"[ERRO AO EXECUTAR {nome.upper()}] {e}"


# ======================================================================================
# 15. GERENCIAMENTO E DIAGNÓSTICO DE DEPENDÊNCIAS
# ======================================================================================
class DependencyEngine:
    """Inspeciona ambiente Python, pacotes instalados, dependências declaradas e ferramentas do SO."""
    @staticmethod
    def diagnosticar_ambiente(project_dir: str) -> Dict[str, Any]:
        em_venv = (hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix))
        instalados: Dict[str, str] = {}
        if importlib_metadata is not None:
            try:
                for dist in importlib_metadata.distributions():
                    nome = dist.metadata.get("Name")
                    ver = dist.metadata.get("Version")
                    if nome:
                        instalados[nome.lower()] = ver or "N/D"
            except Exception:
                pass

        # Lê requirements.txt se existir no projeto ativo
        declarados = []
        ausentes = []
        req_file = os.path.join(project_dir, "requirements.txt")
        if os.path.exists(req_file):
            try:
                conteudo, _ = safe_read_file_text(req_file)
                for ln in conteudo.splitlines():
                    ln = ln.strip()
                    if not ln or ln.startswith("#"):
                        continue
                    pkg_name = re.split(r'[<>=!~;\[\s]', ln)[0].strip().lower()
                    if pkg_name:
                        declarados.append(ln)
                        if instalados and pkg_name not in instalados and pkg_name.replace("-", "_") not in instalados:
                            ausentes.append(ln)
            except Exception:
                pass

        ferramentas_so = {}
        for tool in ["git", "python", "pip", "node", "npm", "gcc", "docker"]:
            ferramentas_so[tool] = shutil.which(tool) or "Não encontrado no PATH"

        return {
            "python_version": sys.version.replace("\n", " "),
            "executable": sys.executable,
            "virtualenv_ativo": "Sim" if em_venv else "Não (Ambiente Global/Base)",
            "prefixo": sys.prefix,
            "total_pacotes_instalados": len(instalados),
            "pacotes_amostra": dict(sorted(instalados.items())[:80]),
            "declarados_requirements": declarados,
            "ausentes_requirements": ausentes,
            "ferramentas_externas": ferramentas_so
        }


# ======================================================================================
# 16. WORKSPACE E AUTOMAÇÕES (PIPELINE PRÉ-PUBLICAÇÃO)
# ======================================================================================
class WorkspaceAutomationEngine:
    """Gerencia perfis de projetos persistentes e executa o Pipeline Real de Auditoria."""
    @staticmethod
    def carregar_perfis() -> Dict[str, Any]:
        inicializar_diretorios_dados()
        if os.path.exists(APP_WORKSPACES_FILE):
            try:
                with open(APP_WORKSPACES_FILE, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                return {}
        return {}

    @staticmethod
    def salvar_perfil(nome: str, dados: Dict[str, Any]):
        perfis = WorkspaceAutomationEngine.carregar_perfis()
        perfis[nome] = dados
        with open(APP_WORKSPACES_FILE, "w", encoding="utf-8") as f:
            json.dump(perfis, f, ensure_ascii=False, indent=2)

    @staticmethod
    def executar_auditoria_pre_publicacao(
        caminho: str,
        cancel_event: Optional[threading.Event] = None,
        progress_cb: Optional[Callable[[float], None]] = None
    ) -> str:
        rel = [
            "=" * 85,
            "   KANIVET XP NEXUS // RELATÓRIO DE AUDITORIA AUTOMATIZADA PRÉ-PUBLICAÇÃO",
            "=" * 85,
            f"Projeto Auditado : {os.path.basename(caminho)}",
            f"Caminho          : {caminho}",
            f"Data/Hora        : {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}",
            "-" * 85
        ]

        # Etapa 1: Inspeção estrutural do projeto
        if progress_cb:
            progress_cb(15.0)
        espaco = ProjectExplorerEngine.diagnosticar_espaco_e_temporarios(caminho)
        rel.append(f"\n[ETAPA 1/6] INSPEÇÃO ESTRUTURAL E ESPAÇO:")
        rel.append(f"  • Tamanho Total do Projeto : {espaco['total_fmt']}")
        rel.append(f"  • Arquivos Temporários     : {len(espaco['arquivos_temporarios'])}")
        rel.append(f"  • Grupos Duplicados (Hash) : {len(espaco['duplicidades_hash'])}")

        # Etapa 2: Estado Git
        if cancel_event and cancel_event.is_set():
            raise TaskCancelledError()
        if progress_cb:
            progress_cb(30.0)
        rel.append(f"\n[ETAPA 2/6] DIAGNÓSTICO GIT:")
        rel.append(GitControlEngine.diagnosticar_config(caminho))

        # Etapa 3: Varredura de Segredos
        if progress_cb:
            progress_cb(50.0)
        sec = SecurityCenterEngine.inspecionar_projeto(caminho, incluir_historico_git=False)
        rel.append(f"\n[ETAPA 3/6] AUDITORIA DE SEGURANÇA (SECURITY CENTER):")
        rel.append(f"  • Arquivos Inspecionados   : {sec['arquivos_inspecionados']}")
        rel.append(f"  • Segredos Detectados      : {sec['total_ocorrencias']} {sec['resumo_severidade']}")
        rel.append(f"  • Arquivos Sensíveis (.env): {len(sec['arquivos_sensiveis'])}")

        # Etapa 4: Dependências
        if progress_cb:
            progress_cb(65.0)
        dep = DependencyEngine.diagnosticar_ambiente(caminho)
        rel.append(f"\n[ETAPA 4/6] AMBIENTE E DEPENDÊNCIAS:")
        rel.append(f"  • Virtualenv Ativo         : {dep['virtualenv_ativo']}")
        rel.append(f"  • Dependências Declaradas  : {len(dep['declarados_requirements'])}")
        rel.append(f"  • Dependências Ausentes    : {len(dep['ausentes_requirements'])}")

        # Etapa 5: Qualidade de Código (AST Nativo)
        if progress_cb:
            progress_cb(80.0)
        ast_avisos = CodeQualityEngine.inspecionar_ast_nativo(caminho)
        rel.append(f"\n[ETAPA 5/6] QUALIDADE DE CÓDIGO (AST PYTHON):")
        rel.append(f"  • Alertas Estáticos AST    : {len(ast_avisos)}")

        # Etapa 6: Consolidação MDnator
        if progress_cb:
            progress_cb(95.0)
        md_info = MDnatorEngine.escanear_e_consolidar(caminho)
        rel.append(f"\n[ETAPA 6/6] MÉTRICAS DOCUMENTAIS (MDNATOR):")
        rel.append(f"  • Arquivos de Código       : {md_info['total_arquivos']} ({md_info['total_linhas']:,} linhas)")
        rel.append(f"  • Distribuição Linguagens  : {md_info['distribuicao_linguagem']}")

        aprovado = (sec["total_ocorrencias"] == 0 and len(sec["arquivos_sensiveis"]) == 0)
        veredito = "PRONTO PARA REVISÃO HUMANA E PUBLICAÇÃO" if aprovado else "ATENÇÃO: REQUER SANITIZAÇÃO ANTES DE PUBLICAR"
        rel.extend([
            "",
            "=" * 85,
            f"PARECER TÉCNICO PRELIMINAR: {veredito}",
            "NOTA: Nenhuma publicação automática foi executada. Revise este relatório antes do Push.",
            "=" * 85
        ])
        return "\n".join(rel)


# ======================================================================================
# 17. SUÍTE INTERNA DE TESTES E GARANTIA DE NÃO-REGRESSÃO
# ======================================================================================
class KanivetNonRegressionTests(unittest.TestCase):
    """Testes automatizados em diretórios sintéticos temporários."""
    def setUp(self):
        self.test_dir = tempfile.mkdtemp(prefix="kanivet_test_")

    def tearDown(self):
        shutil.rmtree(self.test_dir, ignore_errors=True)

    def test_01_mascaramento_credenciais(self):
        raw = "Erro ao conectar em https://oldboy465:ghp_1234567890abcdefghijklmnopqrstuvwx@github.com/repo.git"
        limpo = mascarar_credenciais(raw)
        self.assertNotIn("ghp_1234567890", limpo)
        self.assertIn("***TOKEN_OCULTO***", limpo)

    def test_02_sanitizacao_codigo_e_security_center(self):
        amostra = 'BOT_TOKEN = "123456789:AAFSflRHyWrwGeqSygqgCMoL5OQNJqAld9M"\nsenha = "minha_senha_secreta"\n'
        arq = os.path.join(self.test_dir, "config.py")
        with open(arq, "w", encoding="utf-8") as f:
            f.write(amostra)

        rel = SecurityCenterEngine.inspecionar_projeto(self.test_dir)
        self.assertGreaterEqual(rel["total_ocorrencias"], 1)

        # Testa sanitização preservada
        modificado = amostra
        for padrao, subst in EXACT_SECRET_PATTERNS:
            modificado = re.sub(padrao, subst, modificado)
        self.assertIn("SEU_TELEGRAM_BOT_TOKEN_AQUI", modificado)

    def test_03_mdnator_e_binarios(self):
        with open(os.path.join(self.test_dir, "main.py"), "w", encoding="utf-8") as f:
            f.write("def hello():\n    return 42\n")
        with open(os.path.join(self.test_dir, "firmware.bin"), "wb") as f:
            f.write(b"\x00\x01\x02\xff")

        self.assertTrue(is_binary_file(os.path.join(self.test_dir, "firmware.bin")))
        self.assertFalse(is_binary_file(os.path.join(self.test_dir, "main.py")))

        dados = MDnatorEngine.escanear_e_consolidar(self.test_dir)
        self.assertEqual(dados["total_arquivos"], 1)
        md_text = MDnatorEngine.formatar_saida(dados, ".md")
        self.assertIn("main.py", md_text)

    def test_04_estatistica_infoplan(self):
        metricas = calcular_metricas_estatisticas_avancadas([10.0, 20.0, 20.0, 30.0, 40.0])
        self.assertAlmostEqual(metricas["media"], 24.0)
        self.assertAlmostEqual(metricas["mediana"], 20.0)
        self.assertAlmostEqual(metricas["minimo"], 10.0)
        self.assertAlmostEqual(metricas["maximo"], 40.0)
        self.assertIsNotNone(metricas["assimetria"])
        self.assertIsNotNone(metricas["curtose_excesso"])

    def test_05_explorador_e_comparacao(self):
        dir_b = tempfile.mkdtemp(prefix="kanivet_test_b_")
        try:
            with open(os.path.join(self.test_dir, "a.txt"), "w") as f:
                f.write("conteudo 1")
            with open(os.path.join(dir_b, "a.txt"), "w") as f:
                f.write("conteudo 1")
            comp = ProjectExplorerEngine.comparar_diretorios(self.test_dir, dir_b)
            self.assertIn("a.txt", comp["identicos"])
        finally:
            shutil.rmtree(dir_b, ignore_errors=True)

    def test_06_code_quality_ast(self):
        with open(os.path.join(self.test_dir, "bad.py"), "w", encoding="utf-8") as f:
            f.write("def x():\n    try:\n        eval('1+1')\n    except:\n        pass\n")
        avisos = CodeQualityEngine.inspecionar_ast_nativo(self.test_dir)
        self.assertGreaterEqual(len(avisos), 2)


def executar_suite_autotestes() -> str:
    """Executa a suíte interna de testes unitários e retorna o relatório."""
    # [CORREÇÃO] Removido o trecho que usava 'io' sem importação válida; io agora é importado no topo.
    buf = io.StringIO()
    suite = unittest.TestLoader().loadTestsFromTestCase(KanivetNonRegressionTests)
    runner = unittest.TextTestRunner(stream=buf, verbosity=2)
    result = runner.run(suite)
    cabecalho = (
        f"=== RELATÓRIO DE AUTOTESTES DE NÃO-REGRESSÃO (KANIVET XP NEXUS) ===\n"
        f"Testes Executados: {result.testsRun} | Falhas: {len(result.failures)} | Erros: {len(result.errors)}\n"
        f"Status Global    : {'APROVADO (100%)' if result.wasSuccessful() else 'FALHA DETECTADA'}\n"
        + "-" * 70 + "\n"
    )
    return cabecalho + buf.getvalue()


# ======================================================================================
# 18. COMPONENTES DA INTERFACE E JANELA PRINCIPAL (KANIVET XP APP)
# ======================================================================================
class KanivetXPApp:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Kanivet XP Nexus — Cyber-Git MDnator Universal Suite [Edition 2026 v6.0]")
        self.root.geometry("1180x860")
        self.root.minsize(1020, 740)

        self.dark_mode = False
        self.history_manager = OperationHistoryManager()
        self.ultimo_relatorio_sec: Optional[Dict[str, Any]] = None
        self.df_infoplan_atual: Optional[Any] = None
        self.caminho_infoplan_atual: str = ""

        # Configuração do Estilo Visual Retro Windows XP / Java Swing
        self._configurar_estilos_retro()

        # Variáveis Globais de Estado Originais (Preservadas Integralmente)
        self.src_project_path = tk.StringVar(value=os.path.abspath(os.getcwd()))
        self.git_name_var = tk.StringVar(value="oldboy465")
        self.git_email_var = tk.StringVar(value="XXxXxXxXxXx")
        self.repo_url_var = tk.StringVar(value="https://github.com/oldboy465/meu_projeto.git")
        self.token_var = tk.StringVar()
        self.branch_var = tk.StringVar(value="main")
        self.commit_msg_var = tk.StringVar(value="Release seguro via Kanivet XP (Sanitizado)")
        self.force_push_var = tk.BooleanVar(value=True)
        self.show_token_var = tk.BooleanVar(value=False)
        self.clone_url_var = tk.StringVar()

        # Novas Variáveis de Expansão
        self.quick_search_var = tk.StringVar()
        self.sec_dry_run_var = tk.BooleanVar(value=False)
        self.sec_git_hist_var = tk.BooleanVar(value=False)
        self.md_profile_var = tk.StringVar(value="Universal (Todos os Formatos)")
        self.md_format_var = tk.StringVar(value=".md")
        self.md_incremental_var = tk.BooleanVar(value=False)
        self.md_max_kb_var = tk.IntVar(value=512)
        self.exp_name_var = tk.StringVar()
        self.exp_text_var = tk.StringVar()
        self.exp_ext_var = tk.StringVar()
        self.infoplan_col_var = tk.StringVar()

        # Inicia a interface e os menus
        self._construir_menu_superior()
        self._construir_layout_principal()
        self._configurar_atalhos_teclado()

        # Gerenciador de Tarefas Assíncronas
        self.task_mgr = TaskManager(
            self.root,
            log_cb=self._append_console_direct,
            status_cb=lambda m: self.lbl_status_msg.config(text=m),
            progress_cb=lambda v: self.progress_var.set(v)
        )

        self._iniciar_relogio_status()
        self._atualizar_url_remota_automatica()
        self._atualizar_indicadores_dashboard()

        # Log inicial no console CRT
        self.log(KANIVET_ASCII_BANNER)
        self.log(f"[*] SISTEMA KANIVET XP NEXUS v{APP_VERSION} CARREGADO [{datetime.now().strftime('%d/%m/%Y %H:%M:%S')}]")
        self.log(f"[*] DIRETÓRIO BASE ATUAL: {self.src_project_path.get()}")
        self.log("[*] AUTORIA: Philipe Sampaio Lima (@OldBoy465) — Edição 2026")
        self.log("[*] NOVOS MÓDULOS ATIVOS: Security Center Pro, Code Quality, Dependências, Explorador Pro e Automações.")
        self.log("=" * 85)

    def _configurar_estilos_retro(self):
        """Aplica o tema 'clam' customizado com cores retro Windows XP ou Tema Escuro."""
        self.style = ttk.Style()
        try:
            self.style.theme_use("clam")
        except Exception:
            pass

        bg = DARK_BG_BASE if self.dark_mode else XP_BG_BASE
        fg = DARK_FG if self.dark_mode else "#000000"
        acc = DARK_ACCENT if self.dark_mode else XP_ACCENT
        btn_bg = DARK_BTN_BG if self.dark_mode else XP_BTN_BG
        btn_act = DARK_BTN_ACTIVE if self.dark_mode else XP_BTN_ACTIVE

        self.root.configure(bg=bg)
        self.style.configure(".", background=bg, foreground=fg, font=("Tahoma", 9))
        self.style.configure("TFrame", background=bg)
        self.style.configure("TLabelframe", background=bg, relief="groove")
        self.style.configure("TLabelframe.Label", background=bg, foreground=acc, font=("Tahoma", 9, "bold"))
        self.style.configure("TLabel", background=bg, foreground=fg, font=("Tahoma", 9))
        self.style.configure("TCheckbutton", background=bg, foreground=fg, font=("Tahoma", 9))
        self.style.configure("TNotebook", background=bg, tabmargins=[2, 4, 2, 0])
        self.style.configure("TNotebook.Tab", background=btn_bg, foreground=fg, padding=[8, 4], font=("Tahoma", 8, "bold"))
        self.style.map("TNotebook.Tab", background=[("selected", bg), ("active", btn_act)])

        self.style.configure("Retro.TButton", font=("Tahoma", 9, "bold"), relief="raised", background=btn_bg, foreground=fg, padding=4)
        self.style.map("Retro.TButton", background=[("pressed", "#BFBCAD"), ("active", btn_act)], relief=[("pressed", "sunken")])

        self.style.configure("RetroAction.TButton", font=("Tahoma", 9, "bold"), relief="raised", background="#DCE8D5" if not self.dark_mode else "#234828", foreground="#004D00" if not self.dark_mode else "#9FFFB0", padding=5)
        self.style.configure("RetroDanger.TButton", font=("Tahoma", 9, "bold"), relief="raised", background="#F2DEDE" if not self.dark_mode else "#5A1E1E", foreground="#8A1F11" if not self.dark_mode else "#FFB3B3", padding=5)

    def alternar_tema_visual(self):
        self.dark_mode = not self.dark_mode
        self._configurar_estilos_retro()
        tema_nome = "Tema Escuro (Cyber Dark)" if self.dark_mode else "Tema Clássico (Windows XP Retro)"
        self.log(f"[INTERFACE] Tema visual alterado para: {tema_nome}")

    def _configurar_atalhos_teclado(self):
        self.root.bind("<Control-o>", lambda e: self.selecionar_pasta_projeto())
        self.root.bind("<Control-l>", lambda e: self.limpar_console())
        self.root.bind("<Control-t>", lambda e: self.alternar_tema_visual())
        self.root.bind("<F1>", lambda e: self.abrir_manual_usuario())
        self.root.bind("<F5>", lambda e: self._atualizar_indicadores_dashboard())

    # ----------------------------------------------------------------------------------
    # MENU SUPERIOR (PRESERVADO E EXPANDIDO)
    # ----------------------------------------------------------------------------------
    def _construir_menu_superior(self):
        menubar = tk.Menu(self.root, bg=XP_BG_BASE, font=("Tahoma", 9))

        menu_arquivo = tk.Menu(menubar, tearoff=0, bg=XP_PANEL_BG, font=("Tahoma", 9))
        menu_arquivo.add_command(label="📁 Selecionar Pasta do Projeto... (Ctrl+O)", command=self.selecionar_pasta_projeto)
        menu_arquivo.add_command(label="📂 Abrir Pasta Atual no Explorer", command=self.abrir_pasta_no_explorer)
        menu_arquivo.add_separator()
        menu_arquivo.add_command(label="🌓 Alternar Tema Retrô XP / Escuro (Ctrl+T)", command=self.alternar_tema_visual)
        menu_arquivo.add_command(label="📜 Ver Histórico de Operações", command=self.abrir_janela_historico)
        menu_arquivo.add_command(label="🧹 Limpar Console CRT (Ctrl+L)", command=self.limpar_console)
        menu_arquivo.add_separator()
        menu_arquivo.add_command(label="❌ Sair do Sistema", command=self.root.quit)
        menubar.add_cascade(label="Arquivo", menu=menu_arquivo)

        menu_git = tk.Menu(menubar, tearoff=0, bg=XP_PANEL_BG, font=("Tahoma", 9))
        menu_git.add_command(label="git status", command=lambda: self.executar_git(["git", "status"]))
        menu_git.add_command(label="git log -n 5", command=lambda: self.executar_git(["git", "log", "-n", "5", "--oneline"]))
        menu_git.add_command(label="git diff", command=lambda: self.executar_git(["git", "diff"]))
        menu_git.add_command(label="git fetch --all", command=lambda: self.executar_git(["git", "fetch", "--all"]))
        menu_git.add_command(label="git branch -a", command=lambda: self.executar_git(["git", "branch", "-a"]))
        menu_git.add_separator()
        menu_git.add_command(label="git stash", command=lambda: self.executar_git(["git", "stash"]))
        menu_git.add_command(label="git stash pop", command=lambda: self.executar_git(["git", "stash", "pop"]))
        menu_git.add_separator()
        menu_git.add_command(label="🔍 Diagnóstico Completo Git", command=self.git_diagnosticar_config)
        menubar.add_cascade(label="Operações Git", menu=menu_git)

        menu_ferramentas = tk.Menu(menubar, tearoff=0, bg=XP_PANEL_BG, font=("Tahoma", 9))
        menu_ferramentas.add_command(label="🛡️ Security Center: Varredura de Segredos", command=self.sec_executar_varredura)
        menu_ferramentas.add_command(label="⚡ MDnator: Compilar Projeto em Markdown", command=self.mdnator_compilar_projeto)
        menu_ferramentas.add_command(label="📊 InfoPlan: Analisar Planilha Excel...", command=self.infoplan_analisar_arquivo)
        menu_ferramentas.add_command(label="🌳 Listador: Gerar Dump de Estrutura (.TXT)", command=self.gerar_dump_estrutura_txt)
        menu_ferramentas.add_command(label="✅ Code Quality: Inspecionar AST Python", command=lambda: self.quality_executar("ast_nativo"))
        menu_ferramentas.add_command(label="🚀 Workspace: Auditoria Pré-Publicação", command=self.automacao_executar_pipeline)
        menu_ferramentas.add_separator()
        menu_ferramentas.add_command(label="🧪 Executar Autotestes Internos de Não-Regressão", command=self.executar_autotestes_gui)
        menu_ferramentas.add_command(label="💻 Hardware-Z: Diagnóstico em Tempo Real", command=self.exibir_diagnostico_hardware)
        menubar.add_cascade(label="Ferramentas", menu=menu_ferramentas)

        menu_ajuda = tk.Menu(menubar, tearoff=0, bg=XP_PANEL_BG, font=("Tahoma", 9))
        menu_ajuda.add_command(label="📖 Manual do Usuário / Orientações... (F1)", command=self.abrir_manual_usuario)
        menu_ajuda.add_command(label="📚 Glossário Estatístico InfoPlan", command=self.abrir_glossario_estatistico)
        menu_ajuda.add_separator()
        menu_ajuda.add_command(label="ℹ️ Sobre o Kanivet XP...", command=self.abrir_dialogo_sobre)
        menubar.add_cascade(label="Ajuda", menu=menu_ajuda)

        self.root.config(menu=menubar)

    # ----------------------------------------------------------------------------------
    # LAYOUT PRINCIPAL (DASHBOARD + BUSCA RÁPIDA + NOTEBOOK 10 ABAS + CRT + STATUSBAR)
    # ----------------------------------------------------------------------------------
    def _construir_layout_principal(self):
        # 1. Barra Superior: Seletor Global + Busca Rápida + Tema
        top_frame = ttk.LabelFrame(self.root, text=" 📂 Seletor Global de Diretório / Projeto Ativo & Busca Rápida ", padding=6)
        top_frame.pack(fill=tk.X, padx=10, pady=(4, 2))

        entry_path = ttk.Entry(top_frame, textvariable=self.src_project_path, font=("Consolas", 10))
        entry_path.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 6))
        self.src_project_path.trace_add("write", lambda *args: self._on_project_path_changed())

        ttk.Button(top_frame, text="Selecionar Pasta...", style="Retro.TButton", command=self.selecionar_pasta_projeto).pack(side=tk.LEFT, padx=2)
        ttk.Button(top_frame, text="Abrir Explorer", style="Retro.TButton", command=self.abrir_pasta_no_explorer).pack(side=tk.LEFT, padx=2)
        ttk.Button(top_frame, text="🌓 Tema", style="Retro.TButton", command=self.alternar_tema_visual).pack(side=tk.LEFT, padx=2)

        # Busca rápida de funcionalidades
        ttk.Label(top_frame, text="🔎 Ir para:").pack(side=tk.LEFT, padx=(8, 2))
        self.combo_quick_nav = ttk.Combobox(
            top_frame,
            textvariable=self.quick_search_var,
            values=[
                "1. Sanitizador & Security Center",
                "2. Central Git Baremetal",
                "3. Motor MDnator v5.0",
                "4. Módulo InfoPlan Pro",
                "5. Listador de Estruturas",
                "6. Hardware-Z Pro",
                "7. Code Quality Center",
                "8. Ambiente & Dependências",
                "9. Explorador Avançado",
                "10. Workspace & Automações"
            ],
            width=26,
            state="readonly"
        )
        self.combo_quick_nav.pack(side=tk.LEFT, padx=2)
        self.combo_quick_nav.bind("<<ComboboxSelected>>", self._navegar_busca_rapida)

        # 1.b Dashboard Operacional Real
        dash_frame = ttk.Frame(self.root, padding=(10, 2))
        dash_frame.pack(fill=tk.X)
        self.lbl_dash_proj = ttk.Label(dash_frame, text="📦 Projeto: -", font=("Tahoma", 8, "bold"))
        self.lbl_dash_proj.pack(side=tk.LEFT, padx=(0, 12))
        self.lbl_dash_git = ttk.Label(dash_frame, text="🌿 Branch: -", font=("Tahoma", 8, "bold"))
        self.lbl_dash_git.pack(side=tk.LEFT, padx=(0, 12))
        self.lbl_dash_env = ttk.Label(dash_frame, text="🐍 Python: -", font=("Tahoma", 8))
        self.lbl_dash_env.pack(side=tk.LEFT, padx=(0, 12))
        ttk.Button(dash_frame, text="🔄 Atualizar Indicadores (F5)", style="Retro.TButton", command=self._atualizar_indicadores_dashboard).pack(side=tk.RIGHT)

        # 2. Divisor Principal (Splitter Vertical entre Abas e Console CRT)
        self.paned = ttk.PanedWindow(self.root, orient=tk.VERTICAL)
        self.paned.pack(fill=tk.BOTH, expand=True, padx=10, pady=4)

        notebook_container = ttk.Frame(self.paned)
        self.paned.add(notebook_container, weight=3)

        self.notebook = ttk.Notebook(notebook_container)
        self.notebook.pack(fill=tk.BOTH, expand=True)

        # Construção das 6 Abas Originais Preservadas + 4 Novas Abas de Expansão
        self._construir_aba_sanitizador()
        self._construir_aba_git_central()
        self._construir_aba_mdnator()
        self._construir_aba_infoplan()
        self._construir_aba_listador_tree()
        self._construir_aba_hardware_z()
        self._construir_aba_code_quality()
        self._construir_aba_dependencias()
        self._construir_aba_explorador_avancado()
        self._construir_aba_workspace_automacoes()

        # Container Inferior do Console CRT Retro
        crt_frame = ttk.LabelFrame(self.paned, text=" 💻 Console CRT Retro em Tempo Real (Fósforo Verde) ", padding=4)
        self.paned.add(crt_frame, weight=2)

        crt_toolbar = ttk.Frame(crt_frame)
        crt_toolbar.pack(fill=tk.X, pady=(0, 2))

        ttk.Label(crt_toolbar, text="STATUS OPERACIONAL: CONEXÃO NATIVA ESTABELECIDA (CREDENCIAIS PROTEGIDAS)", font=("Tahoma", 8, "bold"), foreground="#005500").pack(side=tk.LEFT)
        ttk.Button(crt_toolbar, text="Limpar Terminal", style="Retro.TButton", command=self.limpar_console).pack(side=tk.RIGHT, padx=2)
        ttk.Button(crt_toolbar, text="⏹ Cancelar Tarefa", style="RetroDanger.TButton", command=lambda: self.task_mgr.solicitar_cancelamento()).pack(side=tk.RIGHT, padx=2)

        self.console_text = scrolledtext.ScrolledText(
            crt_frame, wrap=tk.WORD, bg=CRT_BG, fg=CRT_FG,
            insertbackground=CRT_CURSOR, font=("Consolas", 9), relief="sunken", bd=2
        )
        self.console_text.pack(fill=tk.BOTH, expand=True)

        # 3. Barra de Status Retro Inferior com Progresso Real
        self.status_bar = ttk.Frame(self.root, relief="sunken", padding=(6, 3))
        self.status_bar.pack(fill=tk.X, side=tk.BOTTOM)

        self.lbl_status_msg = ttk.Label(self.status_bar, text="Pronto.", font=("Tahoma", 8))
        self.lbl_status_msg.pack(side=tk.LEFT)

        self.progress_var = tk.DoubleVar(value=0.0)
        self.progress_bar = ttk.Progressbar(self.status_bar, variable=self.progress_var, maximum=100.0, length=180, mode="determinate")
        self.progress_bar.pack(side=tk.RIGHT, padx=8)

        self.lbl_relogio = ttk.Label(self.status_bar, text="", font=("Tahoma", 8, "bold"))
        self.lbl_relogio.pack(side=tk.RIGHT, padx=5)

    def _navegar_busca_rapida(self, event=None):
        val = self.quick_search_var.get()
        if val:
            idx = int(val.split(".")[0]) - 1
            if 0 <= idx < self.notebook.index("end"):
                self.notebook.select(idx)

    def _on_project_path_changed(self):
        self._atualizar_url_remota_automatica()
        self._atualizar_indicadores_dashboard()

    def _atualizar_indicadores_dashboard(self):
        caminho = self.src_project_path.get().strip()
        nome = os.path.basename(os.path.normpath(caminho)) if os.path.exists(caminho) else "Inválido"
        self.lbl_dash_proj.config(text=f"📦 Projeto: {nome}")

        branch_txt = "Sem Git"
        if os.path.exists(os.path.join(caminho, ".git")):
            code, out, _ = GitControlEngine.run_git_command(["rev-parse", "--abbrev-ref", "HEAD"], caminho, timeout=4)
            if code == 0 and out:
                branch_txt = out
        self.lbl_dash_git.config(text=f"🌿 Branch: {branch_txt}")
        self.lbl_dash_env.config(text=f"🐍 Python {platform.python_version()} | psutil: {'OK' if PSUTIL_AVAILABLE else 'N/D'} | pandas: {'OK' if PANDAS_AVAILABLE else 'N/D'}")

    def _iniciar_relogio_status(self):
        agora = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        self.lbl_relogio.config(text=f"🕐 {agora} | Kanivet XP v6.0 Nexus")
        self.root.after(1000, self._iniciar_relogio_status)

    def _atualizar_url_remota_automatica(self):
        caminho = self.src_project_path.get().strip()
        if caminho:
            nome_pasta = os.path.basename(os.path.normpath(caminho))
            usuario = self.git_name_var.get().strip() or "usuario"
            if nome_pasta:
                self.repo_url_var.set(f"https://github.com/{usuario}/{nome_pasta}.git")

    def _append_console_direct(self, texto: str):
        self.console_text.insert(tk.END, mascarar_credenciais(texto) + "\n")
        self.console_text.see(tk.END)

    def log(self, texto: str):
        """Imprime mensagem no console CRT retro de forma thread-safe com mascaramento de segredos.
        [CORREÇÃO] Quando chamado de threads de trabalho, usa a fila do TaskManager (thread-safe)."""
        msg_segura = mascarar_credenciais(texto)
        task_mgr = getattr(self, "task_mgr", None)
        if task_mgr is not None and threading.current_thread() is not threading.main_thread():
            task_mgr.post_log(msg_segura)
        else:
            self.root.after(0, lambda: self._append_console_direct(msg_segura))

    def set_status(self, msg: str):
        task_mgr = getattr(self, "task_mgr", None)
        if task_mgr is not None and threading.current_thread() is not threading.main_thread():
            task_mgr.post_status(msg)
        else:
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
    # ABA 1: DEPLOY, SANITIZADOR & SECURITY CENTER EXPANDIDO
    # ==================================================================================
    def _construir_aba_sanitizador(self):
        tab = ttk.Frame(self.notebook, padding=8)
        self.notebook.add(tab, text="🛡️ Sanitizador & Security")

        grid_frame = ttk.LabelFrame(tab, text=" Parâmetros de Identificação Git & Segurança de Deploy ", padding=8)
        grid_frame.pack(fill=tk.X, pady=(0, 6))

        ttk.Label(grid_frame, text="Git user.name:").grid(row=0, column=0, sticky=tk.W, pady=2)
        ttk.Entry(grid_frame, textvariable=self.git_name_var, width=28).grid(row=0, column=1, sticky=tk.W, padx=6, pady=2)

        ttk.Label(grid_frame, text="Git user.email:").grid(row=1, column=0, sticky=tk.W, pady=2)
        ttk.Entry(grid_frame, textvariable=self.git_email_var, width=48).grid(row=1, column=1, sticky=tk.EW, padx=6, pady=2)

        ttk.Label(grid_frame, text="URL do Repositório:").grid(row=2, column=0, sticky=tk.W, pady=2)
        ttk.Entry(grid_frame, textvariable=self.repo_url_var, width=48).grid(row=2, column=1, sticky=tk.EW, padx=6, pady=2)

        ttk.Label(grid_frame, text="GitHub Token (PAT):").grid(row=3, column=0, sticky=tk.W, pady=2)
        token_sub = ttk.Frame(grid_frame)
        token_sub.grid(row=3, column=1, sticky=tk.EW, padx=6, pady=2)

        self.entry_token = ttk.Entry(token_sub, textvariable=self.token_var, show="*")
        self.entry_token.pack(side=tk.LEFT, fill=tk.X, expand=True)
        ttk.Checkbutton(token_sub, text="Mostrar", variable=self.show_token_var, command=self._toggle_token_visibility).pack(side=tk.RIGHT, padx=(6, 0))

        ttk.Label(grid_frame, text="Mensagem de Commit:").grid(row=4, column=0, sticky=tk.W, pady=2)
        ttk.Entry(grid_frame, textvariable=self.commit_msg_var, width=48).grid(row=4, column=1, sticky=tk.EW, padx=6, pady=2)

        ttk.Label(grid_frame, text="Opções de Operação:").grid(row=5, column=0, sticky=tk.W, pady=2)
        opts_sub = ttk.Frame(grid_frame)
        opts_sub.grid(row=5, column=1, sticky=tk.W, padx=6, pady=2)

        ttk.Label(opts_sub, text="Branch:").pack(side=tk.LEFT)
        ttk.Entry(opts_sub, textvariable=self.branch_var, width=10).pack(side=tk.LEFT, padx=(4, 10))
        ttk.Checkbutton(opts_sub, text="Forçar Envio (--force)", variable=self.force_push_var).pack(side=tk.LEFT, padx=4)
        ttk.Checkbutton(opts_sub, text="Modo Simulação (Dry-Run)", variable=self.sec_dry_run_var).pack(side=tk.LEFT, padx=4)
        ttk.Checkbutton(opts_sub, text="Inspecionar Histórico Git", variable=self.sec_git_hist_var).pack(side=tk.LEFT, padx=4)

        grid_frame.columnconfigure(1, weight=1)

        # Barra de Ações do Security Center + Sanitizador
        sec_bar = ttk.Frame(tab)
        sec_bar.pack(fill=tk.X, pady=4)

        ttk.Button(sec_bar, text="🔍 Inspecionar Segredos & Severidade", style="Retro.TButton", command=self.sec_executar_varredura).pack(side=tk.LEFT, padx=2, fill=tk.X, expand=True)
        ttk.Button(sec_bar, text="👁️ Prévia de Sanitização (Diff)", style="Retro.TButton", command=self.sec_visualizar_previa_diff).pack(side=tk.LEFT, padx=2, fill=tk.X, expand=True)
        ttk.Button(sec_bar, text="💾 Exportar Relatório (JSON/CSV/HTML)", style="Retro.TButton", command=self.sec_exportar_relatorio_dialog).pack(side=tk.LEFT, padx=2, fill=tk.X, expand=True)
        ttk.Button(sec_bar, text="⏪ Backups & Restauração", style="Retro.TButton", command=self.sec_abrir_gerenciador_backups).pack(side=tk.LEFT, padx=2, fill=tk.X, expand=True)

        self.btn_run_sanitizer = ttk.Button(
            tab,
            text="🛡️ SANITIZAR PROJETO INTEIRO (COM BACKUP) & ENVIAR AO GITHUB COM PAT",
            style="RetroAction.TButton",
            command=self.iniciar_pipeline_sanitizacao
        )
        self.btn_run_sanitizer.pack(fill=tk.X, ipady=4, pady=4)

        # Tabela Treeview de Ocorrências do Security Center
        res_frame = ttk.LabelFrame(tab, text=" Ocorrências Detectadas pelo Security Center ", padding=4)
        res_frame.pack(fill=tk.BOTH, expand=True)

        cols = ("id", "severidade", "tipo", "arquivo", "linha", "amostra")
        self.tree_sec = ttk.Treeview(res_frame, columns=cols, show="headings", height=5)
        for cid, titulo, larg in [
            ("id", "Regra", 70), ("severidade", "Severidade", 95), ("tipo", "Tipo de Segredo", 190),
            ("arquivo", "Arquivo Relativo", 260), ("linha", "Linha", 60), ("amostra", "Amostra Mascarada", 180)
        ]:
            self.tree_sec.heading(cid, text=titulo)
            self.tree_sec.column(cid, width=larg, anchor=tk.W)
        self.tree_sec.pack(fill=tk.BOTH, expand=True)

    def _toggle_token_visibility(self):
        self.entry_token.config(show="" if self.show_token_var.get() else "*")

    def sanitizar_codigo(self, nome_arquivo: str, conteudo: str) -> Tuple[str, bool]:
        """Preservada integralmente do código original."""
        modificado = conteudo
        alterado = False
        for padrao, substituto in EXACT_SECRET_PATTERNS:
            if re.search(padrao, modificado):
                modificado = re.sub(padrao, substituto, modificado)
                alterado = True
        for padrao, substituto, flags in GENERIC_ASSIGNMENT_PATTERNS:
            if re.search(padrao, modificado, flags=flags):
                modificado = re.sub(padrao, substituto, modificado, flags=flags)
                alterado = True
        return modificado, alterado

    def sec_executar_varredura(self):
        try:
            caminho = validar_caminho_diretorio(self.src_project_path.get())
        except Exception as e:
            messagebox.showerror("Erro", str(e))
            return

        inc_git = self.sec_git_hist_var.get()

        def _work(cancel_ev, prog_cb):
            return SecurityCenterEngine.inspecionar_projeto(caminho, incluir_historico_git=inc_git, cancel_event=cancel_ev, progress_cb=prog_cb)

        def _done(dados):
            self.ultimo_relatorio_sec = dados
            for i in self.tree_sec.get_children():
                self.tree_sec.delete(i)
            for oc in dados["ocorrencias"]:
                self.tree_sec.insert("", tk.END, values=(oc["regra_id"], oc["severidade"], oc["tipo"], oc["arquivo"], oc["linha"], oc["amostra_mascarada"]))
            for sens in dados["arquivos_sensiveis"]:
                self.tree_sec.insert("", tk.END, values=("ENV/CERT", sens["severidade"], sens["tipo"], sens["arquivo"], "-", "Bloqueado no Deploy"))

            self.log(f"\n[SECURITY CENTER] Varredura concluída em: {caminho}")
            self.log(f"  • Arquivos Inspecionados : {dados['arquivos_inspecionados']}")
            self.log(f"  • Segredos no Código     : {dados['total_ocorrencias']} {dados['resumo_severidade']}")
            self.log(f"  • Arquivos Sensíveis     : {len(dados['arquivos_sensiveis'])}")
            if dados["historico_git"]:
                self.log(f"  • Alertas Histórico Git  : {len(dados['historico_git'])} regra(s) acionada(s)")
            self.log(f"  • Nota: {dados['aviso_legal']}")
            self.history_manager.registrar("SecurityCenter", "Varredura", "OK", f"{dados['total_ocorrencias']} achados")

        self.task_mgr.run_async("Varredura de Segurança", _work, _done)

    def sec_visualizar_previa_diff(self):
        try:
            src = validar_caminho_diretorio(self.src_project_path.get())
        except Exception as e:
            messagebox.showerror("Erro", str(e))
            return

        previa = ["=== PRÉVIA DE SANITIZAÇÃO (SIMULAÇÃO SEM MODIFICAR ARQUIVOS) ===\n"]
        total_afetados = 0
        for r, dirs, files in os.walk(src):
            dirs[:] = [d for d in dirs if d not in IGNORE_DIRS]
            for f in files:
                fp = os.path.join(r, f)
                if is_binary_file(fp):
                    continue
                try:
                    raw, _ = safe_read_file_text(fp)
                    limpo, mudou = self.sanitizar_codigo(f, raw)
                    if mudou:
                        total_afetados += 1
                        rel = os.path.relpath(fp, src)
                        previa.append(f"Arquivo: {rel}")
                        for idx, (l_orig, l_new) in enumerate(zip(raw.splitlines(), limpo.splitlines()), start=1):
                            if l_orig != l_new:
                                previa.append(f"  Linha {idx:04d} [ANTES (Mascarado)] : {mascarar_credenciais(l_orig)[:90]}")
                                previa.append(f"  Linha {idx:04d} [DEPOIS (Sanitizado)]: {l_new[:90]}")
                        previa.append("-" * 70)
                except Exception:
                    pass
        if total_afetados == 0:
            previa.append("Nenhum arquivo sofreria substituição heurística de segredos.")
        self._exibir_janela_texto("Prévia de Sanitização (Diff)", "\n".join(previa))

    def sec_exportar_relatorio_dialog(self):
        if not self.ultimo_relatorio_sec:
            messagebox.showinfo("Aviso", "Execute primeiro a varredura em 'Inspecionar Segredos & Severidade'.")
            return
        saida = filedialog.asksaveasfilename(
            title="Exportar Relatório de Segurança",
            defaultextension=".html",
            filetypes=[("Relatório HTML", "*.html"), ("Dados JSON", "*.json"), ("Planilha CSV", "*.csv")]
        )
        if saida:
            SecurityCenterEngine.exportar_relatorio(self.ultimo_relatorio_sec, saida)
            self.log(f"[SECURITY CENTER] Relatório exportado para: {saida}")
            messagebox.showinfo("Exportado", f"Relatório salvo com sucesso em:\n{saida}")

    def sec_abrir_gerenciador_backups(self):
        win = tk.Toplevel(self.root)
        win.title("Gerenciador de Backups & Restauração — Security Center")
        win.geometry("680x380")
        win.configure(bg=XP_BG_BASE)

        ttk.Label(win, text="Backups Automáticos Criados pelo Kanivet XP:", font=("Tahoma", 9, "bold")).pack(anchor=tk.W, padx=10, pady=6)
        lb = tk.Listbox(win, font=("Consolas", 9))
        lb.pack(fill=tk.BOTH, expand=True, padx=10, pady=4)

        def _popular():
            lb.delete(0, tk.END)
            for b in BackupManager.listar_backups():
                lb.insert(tk.END, b)

        _popular()

        btn_f = ttk.Frame(win, padding=8)
        btn_f.pack(fill=tk.X)

        def _criar_agora():
            try:
                src = validar_caminho_diretorio(self.src_project_path.get())
                z = BackupManager.criar_backup_projeto(src, "manual")
                self.log(f"[BACKUP] Backup ZIP criado em: {z}")
                _popular()
                messagebox.showinfo("Backup Criado", f"Backup salvo em:\n{z}")
            except Exception as e:
                messagebox.showerror("Erro", str(e))

        def _restaurar():
            sel = lb.curselection()
            if not sel:
                return
            zip_path = lb.get(sel[0])
            dest = filedialog.askdirectory(title="Selecione a Pasta de Destino para Restaurar o Backup")
            if dest and messagebox.askyesno("Confirmar Restauração", f"Deseja extrair o backup:\n{os.path.basename(zip_path)}\nna pasta:\n{dest}?"):
                BackupManager.restaurar_backup(zip_path, dest)
                self.log(f"[RESTAURAÇÃO] Backup {os.path.basename(zip_path)} restaurado em {dest}")
                messagebox.showinfo("Sucesso", "Arquivos restaurados com sucesso!")

        ttk.Button(btn_f, text="📦 Criar Backup do Projeto Atual Agora", style="RetroAction.TButton", command=_criar_agora).pack(side=tk.LEFT, padx=4)
        ttk.Button(btn_f, text="⏪ Restaurar Backup Selecionado...", style="Retro.TButton", command=_restaurar).pack(side=tk.LEFT, padx=4)
        ttk.Button(btn_f, text="Fechar", style="Retro.TButton", command=win.destroy).pack(side=tk.RIGHT, padx=4)

    def iniciar_pipeline_sanitizacao(self):
        caminho_origem = self.src_project_path.get().strip()
        if not os.path.exists(caminho_origem):
            messagebox.showerror("Erro", "O diretório do projeto ativo informado não existe!")
            return

        if not self.sec_dry_run_var.get() and self.force_push_var.get():
            if not messagebox.askyesno(
                "Confirmação de Operação (--force)",
                "A opção 'Forçar Envio (--force)' está marcada.\n"
                "Isso sobrescreverá a branch remota no GitHub com a versão sanitizada.\n\n"
                "Deseja prosseguir?"
            ):
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
        dry_run = self.sec_dry_run_var.get()

        try:
            self.log("=" * 80)
            self.log(f"INICIANDO MOTOR UNIVERSAL DE SANITIZAÇÃO HEURÍSTICA & DEPLOY {'[SIMULAÇÃO DRY-RUN]' if dry_run else ''}")
            self.log(f"Projeto : {nome_pasta} | Origem: {src} | Destino: {dest}")
            self.log("=" * 80)

            if not dry_run:
                try:
                    bkp = BackupManager.criar_backup_projeto(src, "pre_deploy")
                    self.log(f"[BACKUP AUTOMÁTICO] Snapshot de segurança salvo em: {bkp}")
                except Exception as be:
                    self.log(f"[AVISO BACKUP] Não foi possível criar ZIP prévio: {be}")

            if dry_run:
                sec_res = SecurityCenterEngine.inspecionar_projeto(src)
                self.log(f"[DRY-RUN] Arquivos inspecionados: {sec_res['arquivos_inspecionados']} | Segredos que seriam neutralizados: {sec_res['total_ocorrencias']}")
                self.log("[DRY-RUN] Simulação concluída sem alterar arquivos ou executar push.")
                return

            git_backup_dir = os.path.join(dest, ".git")
            temp_git_dir = os.path.join(dir_pai, f"_temp_git_{nome_pasta}")
            has_existing_git = os.path.exists(git_backup_dir)

            if os.path.exists(dest):
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

            for root_d, dirs, files in os.walk(src):
                dirs[:] = [d for d in dirs if d not in IGNORE_DIRS]
                rel_path = os.path.relpath(root_d, src)
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

                    src_file = os.path.join(root_d, f)
                    dest_file = os.path.join(target_root, f)

                    if not is_binary_file(src_file):
                        try:
                            raw_code, _ = safe_read_file_text(src_file)
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
                    else:
                        shutil.copy2(src_file, dest_file)
                        self.log(f"[BINÁRIO] Copiado diretamente: {f}")
                    total_copiados += 1

            with open(os.path.join(dest, ".gitignore"), "w", encoding="utf-8") as gf:
                gf.write(UNIVERSAL_GITIGNORE.strip())
            self.log(f"\n[ESTATÍSTICAS] {total_copiados} arquivos exportados | {sanitizados_count} arquivos higienizados.")

            def _exec_git_safe(git_args, mask_log=False):
                if not mask_log:
                    self.log(f"> git {' '.join(git_args)}")
                code, out, err = GitControlEngine.run_git_command(git_args, cwd=dest, timeout=90)
                if out:
                    self.log(out)
                if err and code != 0:
                    self.log(f"[AVISO GIT] {err}")
                return code

            if not os.path.exists(os.path.join(dest, ".git")):
                _exec_git_safe(["init"])

            _exec_git_safe(["config", "user.name", user_name])
            _exec_git_safe(["config", "user.email", user_email])

            target_push_url = repo_url
            if token and "https://" in repo_url:
                clean_host = repo_url.replace("https://", "")
                if "@" in clean_host:
                    clean_host = clean_host.split("@", 1)[1]
                target_push_url = f"https://{user_name}:{token}@{clean_host}"
                self.log("[AUTH] Personal Access Token anexado com proteção de log ao transporte HTTPS.")

            _exec_git_safe(["remote", "remove", "origin"])
            _exec_git_safe(["remote", "add", "origin", target_push_url], mask_log=True)
            _exec_git_safe(["branch", "-M", branch])
            _exec_git_safe(["add", "."])

            commit_res = _exec_git_safe(["commit", "-m", commit_msg])
            if commit_res != 0:
                self.log("[INFO] Nenhuma alteração nova detectada na árvore para comitar.")

            push_cmd = ["push", "-u", "origin", branch]
            if force_push:
                push_cmd.append("--force")

            push_res = _exec_git_safe(push_cmd, mask_log=True)
            self.history_manager.registrar("Sanitizador", "Deploy GitHub", "OK" if push_res == 0 else "FALHA", f"Exportados: {total_copiados}")

            if push_res == 0:
                self.log("\n🚀 SUCESSO ABSOLUTO: REPOSITÓRIO ENVIADO E SEGURO!")
                self.root.after(0, lambda: messagebox.showinfo("Sucesso Absoluto", f"Projeto '{nome_pasta}' sanitizado e enviado!\nPasta limpa:\n{dest}"))
            else:
                self.root.after(0, lambda: messagebox.showwarning("Autenticação Necessária", "O envio foi recusado pelo servidor remoto. Verifique o Token PAT."))
        except Exception as e:
            self.log(f"\n[ERRO CRÍTICO] {e}")
        finally:
            self.root.after(0, lambda: self.btn_run_sanitizer.config(state=tk.NORMAL))
            self.set_status("Pronto.")

    # ==================================================================================
    # ABA 2: CENTRAL DE OPERAÇÕES GIT BAREMETAL EXPANDIDA
    # ==================================================================================
    def _construir_aba_git_central(self):
        tab = ttk.Frame(self.notebook, padding=8)
        self.notebook.add(tab, text="🌿 Central Git Baremetal")

        grid_frame = ttk.LabelFrame(tab, text=" Painel de Comandos Git em Tempo Real (Execução Segura shell=False) ", padding=6)
        grid_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 6))

        botoes_git = [
            ("git status", "Verificar modificações e arquivos staged", lambda: self.executar_git(["git", "status"])),
            ("git log -n 5", "Visualizar os 5 últimos commits da árvore", lambda: self.executar_git(["git", "log", "-n", "5", "--oneline", "--graph", "--decorate"])),
            ("git diff", "Comparar linha a linha as alterações locais", lambda: self.executar_git(["git", "diff"])),
            ("git fetch --all", "Baixar referências e ponteiros remotos", lambda: self.executar_git(["git", "fetch", "--all"])),
            ("git pull", "Puxar e mesclar atualizações da branch ativa", lambda: self.executar_git(["git", "pull", "origin", self.branch_var.get().strip()])),
            ("git add .", "Adicionar todas as alterações ao Stage", lambda: self.executar_git(["git", "add", "."])),
            ("git commit -m", "Gravar alterações usando a mensagem definida", lambda: self.executar_git(["git", "commit", "-m", self.commit_msg_var.get().strip()])),
            ("git push", "Enviar commits locais para o servidor remoto", lambda: self.executar_git(["git", "push", "origin", self.branch_var.get().strip()])),
            ("git remote -v", "Listar endereços dos servidores remotos", lambda: self.executar_git(["git", "remote", "-v"])),
            ("git branch -a", "Exibir todas as ramificações locais e remotas", lambda: self.executar_git(["git", "branch", "-a"])),
            ("git stash", "Salvar temporariamente alterações em progresso", lambda: self.executar_git(["git", "stash"])),
            ("git stash pop", "Restaurar alterações salvas do stash", lambda: self.executar_git(["git", "stash", "pop"]))
        ]

        for i, (cmd_name, desc, func) in enumerate(botoes_git):
            r = i // 2
            c = i % 2
            cell_frame = ttk.Frame(grid_frame, padding=2)
            cell_frame.grid(row=r, column=c, sticky=tk.EW, padx=4, pady=2)
            ttk.Button(cell_frame, text=cmd_name, style="Retro.TButton", command=func, width=16).pack(side=tk.LEFT, padx=(0, 6))
            ttk.Label(cell_frame, text=desc, font=("Tahoma", 8)).pack(side=tk.LEFT, fill=tk.X, expand=True)

        grid_frame.columnconfigure(0, weight=1)
        grid_frame.columnconfigure(1, weight=1)

        # Barra de Operações Git Avançadas (Tags, Unstage, Conflitos, Grandes Arquivos, Diagnóstico)
        adv_git = ttk.LabelFrame(tab, text=" Operações Avançadas & Governança de Repositório ", padding=6)
        adv_git.pack(fill=tk.X, pady=(0, 6))

        for txt, cmd_fn in [
            ("🌱 git init", lambda: self.executar_git(["git", "init"])),
            ("↩️ Unstage All (reset HEAD)", lambda: self.executar_git(["git", "reset", "HEAD"])),
            ("🏷️ Listar/Criar Tags", self.git_gerenciar_tags),
            ("🔀 Nova Branch / Checkout", self.git_criar_ou_trocar_branch),
            ("⚔️ Detectar Conflitos", self.git_verificar_conflitos),
            ("🐘 Arquivos Grandes (>5MB)", self.git_escanear_arquivos_grandes),
            ("🛡️ Inspecionar .gitignore", self.git_inspecionar_gitignore),
            ("🩺 Diagnóstico Git", self.git_diagnosticar_config)
        ]:
            ttk.Button(adv_git, text=txt, style="Retro.TButton", command=cmd_fn).pack(side=tk.LEFT, padx=2, pady=2, expand=True, fill=tk.X)

        clone_frame = ttk.LabelFrame(tab, text=" Clonar Repositório Remoto (git clone) ", padding=6)
        clone_frame.pack(fill=tk.X)
        ttk.Label(clone_frame, text="URL do Repositório:").pack(side=tk.LEFT, padx=(0, 6))
        ttk.Entry(clone_frame, textvariable=self.clone_url_var, font=("Consolas", 9)).pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 6))
        ttk.Button(clone_frame, text="Clonar Repositório...", style="RetroAction.TButton", command=self.executar_git_clone).pack(side=tk.RIGHT)

    def executar_git(self, args: List[str]):
        """Preservada assinatura original; agora usa GitControlEngine seguro sem shell=True."""
        caminho = self.src_project_path.get().strip()
        if not os.path.exists(caminho):
            messagebox.showwarning("Aviso", "O diretório do projeto ativo informado não existe!")
            return

        git_subargs = args[1:] if (args and args[0] == "git") else args
        # Remove aspas extras caso tenham vindo de chamadas legadas
        git_subargs = [a.strip('"') if isinstance(a, str) else a for a in git_subargs]

        def _work(cancel_ev, prog_cb):
            return GitControlEngine.run_git_command(git_subargs, cwd=caminho, timeout=60)

        def _done(res):
            code, out, err = res
            cmd_str = "git " + " ".join(git_subargs)
            self.log(f"\n[GIT EXEC] {cmd_str} (em: {caminho})")
            if out:
                self.log(out)
            if err:
                self.log(f"[SAÍDA STDERR] {err}")
            self.log(f"[GIT {'OK' if code == 0 else 'AVISO'}] Código de retorno: {code}")
            self.history_manager.registrar("Git", cmd_str, "OK" if code == 0 else f"Code {code}")
            self._atualizar_indicadores_dashboard()

        self.task_mgr.run_async(" ".join(args), _work, _done)

    def executar_git_clone(self):
        url = self.clone_url_var.get().strip()
        if not url:
            messagebox.showwarning("Aviso", "Insira a URL do repositório a ser clonado!")
            return
        pasta_destino = filedialog.askdirectory(title="Selecione a Pasta de Destino para o Clone")
        if not pasta_destino:
            return

        def _work(cancel_ev, prog_cb):
            return GitControlEngine.run_git_command(["clone", url], cwd=pasta_destino, timeout=180)

        def _done(res):
            code, out, err = res
            if out:
                self.log(out)
            if err:
                self.log(err)
            if code == 0:
                self.log("[CLONE SUCESSO] Repositório clonado com êxito!")
                messagebox.showinfo("Sucesso", "Repositório clonado com sucesso!")
            else:
                messagebox.showerror("Erro de Clone", f"Falha ao clonar (código {code}).")

        self.task_mgr.run_async("git clone", _work, _done)

    def git_gerenciar_tags(self):
        caminho = self.src_project_path.get().strip()
        _, out, _ = GitControlEngine.run_git_command(["tag", "-l"], caminho)
        nova = simpledialog.askstring("Tags Git", f"Tags existentes:\n{out or '(Nenhuma)'}\n\nDigite o nome de uma nova Tag para criar (ou deixe vazio para cancelar):")
        if nova and nova.strip():
            self.executar_git(["git", "tag", nova.strip()])

    def git_criar_ou_trocar_branch(self):
        nova = simpledialog.askstring("Branch Git", "Digite o nome da Branch para criar/alternar (checkout -B):")
        if nova and nova.strip():
            self.branch_var.set(nova.strip())
            self.executar_git(["git", "checkout", "-B", nova.strip()])

    def git_verificar_conflitos(self):
        caminho = self.src_project_path.get().strip()
        conflitos = GitControlEngine.detectar_conflitos(caminho)
        if conflitos:
            self.log(f"\n[CONFLITOS GIT] {len(conflitos)} arquivo(s) em conflito: {', '.join(conflitos)}")
            messagebox.showwarning("Conflitos Detectados", "\n".join(conflitos))
        else:
            self.log("\n[CONFLITOS GIT] Nenhum arquivo com conflito de merge pendente.")
            messagebox.showinfo("Git Limpo", "Nenhum conflito de merge detectado.")

    def git_escanear_arquivos_grandes(self):
        caminho = self.src_project_path.get().strip()
        grandes = GitControlEngine.analisar_arquivos_grandes(caminho, limite_mb=5.0)
        if not grandes:
            self.log("\n[GIT LARGE FILES] Nenhum arquivo acima de 5 MB encontrado.")
        else:
            self.log("\n[GIT LARGE FILES] Arquivos acima de 5 MB que podem impactar o push:")
            for rel, mb in grandes:
                self.log(f"  • {rel} ({mb:.2f} MB)")

    def git_inspecionar_gitignore(self):
        gi = os.path.join(self.src_project_path.get().strip(), ".gitignore")
        if os.path.exists(gi):
            txt, _ = safe_read_file_text(gi)
            self._exibir_janela_texto("Inspeção de .gitignore", txt)
        else:
            if messagebox.askyesno(".gitignore Ausente", "Não há arquivo .gitignore na raiz. Deseja gerar o .gitignore universal agora?"):
                with open(gi, "w", encoding="utf-8") as f:
                    f.write(UNIVERSAL_GITIGNORE.strip())
                self.log("[GITIGNORE] Arquivo .gitignore universal criado na raiz do projeto.")

    def git_diagnosticar_config(self):
        caminho = self.src_project_path.get().strip()
        rel = GitControlEngine.diagnosticar_config(caminho)
        self.log("\n" + rel)

    # ==================================================================================
    # ABA 3: MDNATOR v5.0 (COMPILAÇÃO DOCUMENTAL COM PERFIS E HASH)
    # ==================================================================================
    def _construir_aba_mdnator(self):
        tab = ttk.Frame(self.notebook, padding=10)
        self.notebook.add(tab, text="⚡ Motor MDnator v5.0")

        cfg_frame = ttk.LabelFrame(tab, text=" Configuração de Perfil Documental, Formato e Limites ", padding=8)
        cfg_frame.pack(fill=tk.X, pady=(0, 8))

        ttk.Label(cfg_frame, text="Perfil de Projeto:").grid(row=0, column=0, sticky=tk.W, padx=4, pady=3)
        ttk.Combobox(cfg_frame, textvariable=self.md_profile_var, values=list(MDNATOR_PROFILES.keys()), state="readonly", width=32).grid(row=0, column=1, sticky=tk.W, padx=4, pady=3)

        ttk.Label(cfg_frame, text="Formato de Exportação:").grid(row=0, column=2, sticky=tk.W, padx=8, pady=3)
        ttk.Combobox(cfg_frame, textvariable=self.md_format_var, values=[".md", ".json", ".txt"], state="readonly", width=10).grid(row=0, column=3, sticky=tk.W, padx=4, pady=3)

        ttk.Label(cfg_frame, text="Limite Máx por Arquivo (KB):").grid(row=1, column=0, sticky=tk.W, padx=4, pady=3)
        ttk.Entry(cfg_frame, textvariable=self.md_max_kb_var, width=10).grid(row=1, column=1, sticky=tk.W, padx=4, pady=3)

        ttk.Checkbutton(cfg_frame, text="Modo Incremental (Apenas arquivos alterados desde a última execução)", variable=self.md_incremental_var).grid(row=1, column=2, columnspan=2, sticky=tk.W, padx=8, pady=3)

        btn_box = ttk.Frame(tab)
        btn_box.pack(fill=tk.X, pady=6)

        ttk.Button(btn_box, text="⚡ COMPILAR PROJETO ATIVO (MD / JSON / TXT)", style="RetroAction.TButton", command=self.mdnator_compilar_projeto).pack(side=tk.LEFT, fill=tk.X, expand=True, padx=2, ipady=4)
        ttk.Button(btn_box, text="📊 INSPECIONAR MÉTRICAS & DUPLICIDADES", style="Retro.TButton", command=self.mdnator_inspecionar_metricas).pack(side=tk.LEFT, fill=tk.X, expand=True, padx=2, ipady=4)
        ttk.Button(btn_box, text="👁️ PRÉVIA DOS ARQUIVOS ELEGÍVEIS", style="Retro.TButton", command=self.mdnator_previa_arquivos).pack(side=tk.LEFT, fill=tk.X, expand=True, padx=2, ipady=4)

        ext_frame = ttk.LabelFrame(tab, text=" Recursos do Motor MDnator v5.0 ", padding=8)
        ext_frame.pack(fill=tk.BOTH, expand=True)
        ttk.Label(
            ext_frame,
            text=(
                "• Perfis Dedicados: Universal, Python/Flask, Arduino/ESP32, Web Frontend, Ciência de Dados e Pacote LLM.\n"
                "• Auditoria Integrada: Sumário navegável, distribuição por linguagem, detecção de arquivos vazios e duplicidades exatas por hash SHA-256.\n"
                "• Segurança de Origem: Leitura estritamente não-destrutiva com descarte automático de binários."
            ),
            justify=tk.LEFT
        ).pack(anchor=tk.W)

    def mdnator_inspecionar_metricas(self):
        caminho = self.src_project_path.get().strip()
        if not os.path.exists(caminho):
            messagebox.showwarning("Aviso", "O diretório informado não existe!")
            return
        perfil = self.md_profile_var.get()
        max_kb = self.md_max_kb_var.get()

        def _work(cancel_ev, prog_cb):
            return MDnatorEngine.escanear_e_consolidar(caminho, perfil=perfil, max_kb_arquivo=max_kb)

        def _done(dados):
            self.log("=" * 70)
            self.log(f"[MDNATOR MÉTRICAS] Projeto: {dados['projeto']} | Perfil: {dados['perfil']}")
            self.log(f"  • Total de Arquivos Elegíveis : {dados['total_arquivos']:,}")
            self.log(f"  • Linhas de Código Estimadas  : {dados['total_linhas']:,}")
            self.log(f"  • Arquivos Vazios (0 bytes)   : {len(dados['arquivos_vazios'])}")
            self.log(f"  • Grupos Duplicados (SHA-256) : {len(dados['duplicidades_hash'])}")
            self.log(f"  • Distribuição por Linguagem  : {dados['distribuicao_linguagem']}")
            self.log("=" * 70)

        self.task_mgr.run_async("Métricas MDnator", _work, _done)

    def mdnator_previa_arquivos(self):
        caminho = self.src_project_path.get().strip()
        if not os.path.exists(caminho):
            return
        dados = MDnatorEngine.escanear_e_consolidar(caminho, perfil=self.md_profile_var.get(), max_kb_arquivo=self.md_max_kb_var.get())
        linhas = [f"PRÉVIA DE ARQUIVOS SELECIONADOS ({dados['total_arquivos']} arquivos):\n"]
        for a in dados["arquivos"]:
            linhas.append(f"• {a['rel_path']:45s} | {a['linhas']:6d} linhas | {formatar_bytes(a['bytes']):10s} | SHA256: {a['sha256']}")
        self._exibir_janela_texto("Prévia de Arquivos — MDnator", "\n".join(linhas))

    def mdnator_compilar_projeto(self):
        caminho = self.src_project_path.get().strip()
        if not os.path.exists(caminho):
            messagebox.showwarning("Aviso", "O diretório informado não existe!")
            return

        ext_fmt = self.md_format_var.get() or ".md"
        nome_projeto = os.path.basename(os.path.normpath(caminho)) or "projeto"
        sugestao = f"{nome_projeto}_MDNATOR_{datetime.now().strftime('%Y%m%d_%H%M%S')}{ext_fmt}"

        caminho_saida = filedialog.asksaveasfilename(
            title="Salvar Compilação do MDnator",
            defaultextension=ext_fmt,
            initialfile=sugestao,
            filetypes=[("Markdown", "*.md"), ("JSON", "*.json"), ("Texto", "*.txt"), ("Todos", "*.*")]
        )
        if not caminho_saida:
            return

        perfil = self.md_profile_var.get()
        max_kb = self.md_max_kb_var.get()
        inc = self.md_incremental_var.get()

        def _work(cancel_ev, prog_cb):
            dados = MDnatorEngine.escanear_e_consolidar(caminho, perfil=perfil, max_kb_arquivo=max_kb, modo_incremental=inc)
            conteudo = MDnatorEngine.formatar_saida(dados, os.path.splitext(caminho_saida)[1].lower() or ext_fmt)
            with open(caminho_saida, "w", encoding="utf-8") as wf:
                wf.write(conteudo)
            return dados

        def _done(dados):
            self.log(f"[MDNATOR SUCESSO] {dados['total_arquivos']} arquivos ({dados['total_linhas']:,} linhas) gravados em:\n  {caminho_saida}")
            self.history_manager.registrar("MDnator", f"Compilar ({perfil})", "OK", caminho_saida)
            messagebox.showinfo("MDnator Concluído", f"Compilação concluída com sucesso!\nSalvo em:\n{caminho_saida}")

        self.task_mgr.run_async("Compilação MDnator", _work, _done)

    # ==================================================================================
    # ABA 4: INFOPLAN PRO (ANÁLISE EXPLORATÓRIA, ESTATÍSTICA E GRÁFICOS REAIS)
    # ==================================================================================
    def _construir_aba_infoplan(self):
        tab = ttk.Frame(self.notebook, padding=8)
        self.notebook.add(tab, text="📊 Módulo InfoPlan Pro")

        top_bar = ttk.Frame(tab)
        top_bar.pack(fill=tk.X, pady=(0, 6))

        ttk.Button(top_bar, text="📊 Selecionar Planilha (.XLSX / .XLS / .CSV) & Gerar Radiografia...", style="RetroAction.TButton", command=self.infoplan_analisar_arquivo).pack(side=tk.LEFT, padx=2, fill=tk.X, expand=True)
        ttk.Button(top_bar, text="🌐 Exportar Relatório HTML", style="Retro.TButton", command=self.infoplan_exportar_html).pack(side=tk.LEFT, padx=2)
        ttk.Button(top_bar, text="📚 Glossário Estatístico", style="Retro.TButton", command=self.abrir_glossario_estatistico).pack(side=tk.LEFT, padx=2)

        # Painel de Seleção de Variável e Gráficos Reais em Canvas Nativo
        viz_bar = ttk.LabelFrame(tab, text=" Visualizador Gráfico Estatístico Baseado nos Dados Reais ", padding=6)
        viz_bar.pack(fill=tk.BOTH, expand=True)

        ctrl_row = ttk.Frame(viz_bar)
        ctrl_row.pack(fill=tk.X, pady=(0, 4))
        ttk.Label(ctrl_row, text="Variável Numérica:").pack(side=tk.LEFT, padx=4)
        self.combo_infoplan_col = ttk.Combobox(ctrl_row, textvariable=self.infoplan_col_var, state="readonly", width=28)
        self.combo_infoplan_col.pack(side=tk.LEFT, padx=4)
        ttk.Button(ctrl_row, text="📊 Plotar Histograma", style="Retro.TButton", command=lambda: self._desenhar_grafico_infoplan("hist")).pack(side=tk.LEFT, padx=3)
        ttk.Button(ctrl_row, text="📦 Plotar Boxplot (Quartis/IQR)", style="Retro.TButton", command=lambda: self._desenhar_grafico_infoplan("box")).pack(side=tk.LEFT, padx=3)
        ttk.Button(ctrl_row, text="🔥 Mapa de Correlação (Pearson)", style="Retro.TButton", command=lambda: self._desenhar_grafico_infoplan("corr")).pack(side=tk.LEFT, padx=3)

        self.canvas_infoplan = tk.Canvas(viz_bar, bg="#FFFFFF", height=220, relief="sunken", bd=1)
        self.canvas_infoplan.pack(fill=tk.BOTH, expand=True)

    def infoplan_analisar_arquivo(self):
        caminho = filedialog.askopenfilename(
            title="Selecione a Planilha para Análise InfoPlan Pro",
            filetypes=[("Planilhas e Dados (*.xlsx;*.xls;*.csv)", "*.xlsx *.xls *.csv"), ("Todos os Arquivos", "*.*")]
        )
        if not caminho:
            return

        def _work(cancel_ev, prog_cb):
            abas = carregar_abas_planilha(caminho)
            primeira_aba = next(iter(abas.values())) if abas else None
            rel = gerar_relatorio_infoplan(caminho)
            return caminho, primeira_aba, rel

        def _done(res):
            cam, df_prim, relatorio = res
            self.caminho_infoplan_atual = cam
            self.df_infoplan_atual = df_prim
            if df_prim is not None:
                cols_num = [str(c) for c in df_prim.select_dtypes(include=['number']).columns]
                self.combo_infoplan_col["values"] = cols_num
                if cols_num:
                    self.infoplan_col_var.set(cols_num[0])
                    self._desenhar_grafico_infoplan("hist")

            nome_base = os.path.splitext(os.path.basename(cam))[0]
            caminho_saida = filedialog.asksaveasfilename(
                title="Salvar Radiografia da Planilha",
                defaultextension=".txt",
                initialfile=f"{nome_base}_INFOPLAN_RADIOGRAFIA.txt",
                filetypes=[("Arquivo de Texto", "*.txt"), ("Markdown", "*.md"), ("Todos", "*.*")]
            )
            if caminho_saida:
                with open(caminho_saida, "w", encoding="utf-8") as f:
                    f.write(relatorio)
                self.log(f"[INFOPLAN SUCESSO] Relatório salvo em:\n  {caminho_saida}")
                self.history_manager.registrar("InfoPlan", "Análise de Planilha", "OK", cam)
                messagebox.showinfo("Sucesso", f"Planilha analisada com sucesso!\nRelatório salvo em:\n{caminho_saida}")

        self.task_mgr.run_async("Análise InfoPlan Pro", _work, _done)

    def _desenhar_grafico_infoplan(self, tipo: str):
        c = self.canvas_infoplan
        c.delete("all")
        if self.df_infoplan_atual is None or self.df_infoplan_atual.empty:
            c.create_text(300, 100, text="Carregue uma planilha primeiro para visualizar gráficos reais.", fill="#555", font=("Tahoma", 10, "bold"))
            return

        w = max(560, c.winfo_width())
        h = max(200, c.winfo_height())
        pad_x, pad_y = 60, 35

        if tipo in ("hist", "box"):
            col = self.infoplan_col_var.get()
            if not col or col not in self.df_infoplan_atual.columns:
                c.create_text(w // 2, h // 2, text="Selecione uma coluna numérica válida.", fill="#800")
                return
            vals = pd.to_numeric(self.df_infoplan_atual[col], errors="coerce").dropna().tolist()
            if not vals:
                c.create_text(w // 2, h // 2, text="Sem valores numéricos válidos na coluna selecionada.", fill="#800")
                return
            m = calcular_metricas_estatisticas_avancadas([float(x) for x in vals])

            if tipo == "hist":
                k = max(5, min(20, int(1 + 3.322 * math.log10(len(vals)))))
                vmin, vmax = m["minimo"], m["maximo"]
                if vmin == vmax:
                    vmax = vmin + 1.0
                larg_bin = (vmax - vmin) / k
                contagens = [0] * k
                for v in vals:
                    idx = min(k - 1, int((v - vmin) / larg_bin))
                    contagens[idx] += 1
                max_c = max(contagens) or 1
                c.create_text(w // 2, 16, text=f"Histograma de Frequências: {col} (n={m['n']}, Média={m['media']:.2f}, DP={m['desvio_padrao']:.2f})", font=("Tahoma", 9, "bold"), fill="#0A246A")
                usable_w = w - 2 * pad_x
                usable_h = h - 2 * pad_y
                bar_w = usable_w / k
                for i, cnt in enumerate(contagens):
                    x0 = pad_x + i * bar_w
                    x1 = x0 + bar_w - 2
                    bh = (cnt / max_c) * usable_h
                    y1 = h - pad_y
                    y0 = y1 - bh
                    c.create_rectangle(x0, y0, x1, y1, fill="#3A7CA5", outline="#16425B")
                    if cnt > 0:
                        c.create_text((x0 + x1) / 2, y0 - 8, text=str(cnt), font=("Tahoma", 7))
                c.create_text(pad_x, h - 15, text=f"{vmin:.2f}", font=("Tahoma", 8))
                c.create_text(w - pad_x, h - 15, text=f"{vmax:.2f}", font=("Tahoma", 8))

            elif tipo == "box":
                vmin, vmax = m["minimo"], m["maximo"]
                span = (vmax - vmin) if vmax != vmin else 1.0
                usable_w = w - 2 * pad_x

                def _x(val):
                    return pad_x + ((val - vmin) / span) * usable_w

                ymid = h // 2
                x_min, x_q1, x_med, x_q3, x_max = _x(vmin), _x(m["q1"]), _x(m["mediana"]), _x(m["q3"]), _x(vmax)
                c.create_text(w // 2, 18, text=f"Boxplot (Quartis e Amplitude): {col} | Q1={m['q1']:.2f} | Mediana={m['mediana']:.2f} | Q3={m['q3']:.2f} | IQR={m['iqr']:.2f}", font=("Tahoma", 9, "bold"), fill="#0A246A")
                c.create_line(x_min, ymid, x_q1, ymid, width=2, fill="#333")
                c.create_line(x_q3, ymid, x_max, ymid, width=2, fill="#333")
                c.create_line(x_min, ymid - 15, x_min, ymid + 15, width=2, fill="#333")
                c.create_line(x_max, ymid - 15, x_max, ymid + 15, width=2, fill="#333")
                c.create_rectangle(x_q1, ymid - 28, x_q3, ymid + 28, fill="#90BE6D", outline="#2D6A4F", width=2)
                c.create_line(x_med, ymid - 28, x_med, ymid + 28, width=3, fill="#D90429")
                for xv, lbl in [(x_min, f"Min\n{vmin:.1f}"), (x_q1, f"Q1\n{m['q1']:.1f}"), (x_med, f"Med\n{m['mediana']:.1f}"), (x_q3, f"Q3\n{m['q3']:.1f}"), (x_max, f"Max\n{vmax:.1f}")]:
                    c.create_text(xv, ymid + 48, text=lbl, font=("Tahoma", 7))

        elif tipo == "corr":
            df_num = self.df_infoplan_atual.select_dtypes(include=['number'])
            cols = list(df_num.columns)[:8]
            if len(cols) < 2:
                c.create_text(w // 2, h // 2, text="São necessárias pelo menos 2 colunas numéricas para a matriz de correlação.", fill="#800")
                return
            corr = df_num[cols].corr().fillna(0.0)
            n_c = len(cols)
            cell_w = min(65, (w - 140) // n_c)
            cell_h = min(26, (h - 50) // n_c)
            c.create_text(w // 2, 14, text="Matriz de Correlação Linear de Pearson (r)", font=("Tahoma", 9, "bold"), fill="#0A246A")
            for i in range(n_c):
                c.create_text(110, 40 + i * cell_h + cell_h // 2, text=str(cols[i])[:14], anchor=tk.E, font=("Tahoma", 7, "bold"))
                for j in range(n_c):
                    val = float(corr.iloc[i, j])
                    intens = int(abs(val) * 180)
                    cor = f"#{255 - intens:02x}{255 - intens // 2:02x}ff" if val >= 0 else f"#ff{255 - intens:02x}{255 - intens:02x}"
                    x0 = 115 + j * cell_w
                    y0 = 40 + i * cell_h
                    c.create_rectangle(x0, y0, x0 + cell_w, y0 + cell_h, fill=cor, outline="#ccc")
                    c.create_text(x0 + cell_w // 2, y0 + cell_h // 2, text=f"{val:.2f}", font=("Tahoma", 7))

    def infoplan_exportar_html(self):
        if not self.caminho_infoplan_atual or not os.path.exists(self.caminho_infoplan_atual):
            messagebox.showinfo("Aviso", "Analise uma planilha primeiro antes de exportar para HTML.")
            return
        saida = filedialog.asksaveasfilename(title="Exportar Relatório HTML InfoPlan", defaultextension=".html", filetypes=[("HTML", "*.html")])
        if saida:
            rel_txt = gerar_relatorio_infoplan(self.caminho_infoplan_atual)
            html = (
                "<!DOCTYPE html><html><head><meta charset='utf-8'><title>Relatório InfoPlan Pro</title>"
                "<style>body{background:#ECE9D8;font-family:Consolas,monospace;padding:20px;} pre{background:#fff;padding:15px;border:2px inset #ccc;overflow-x:auto;}</style></head>"
                f"<body><h2>📊 Relatório InfoPlan Pro — Kanivet XP Nexus</h2><pre>{rel_txt}</pre><pre>{GLOSSARIO_ESTATISTICO}</pre></body></html>"
            )
            with open(saida, "w", encoding="utf-8") as f:
                f.write(html)
            messagebox.showinfo("Exportado", f"Relatório HTML salvo em:\n{saida}")

    def abrir_glossario_estatistico(self):
        self._exibir_janela_texto("Glossário Estatístico & Definições Matemáticas — InfoPlan Pro", GLOSSARIO_ESTATISTICO)

    # ==================================================================================
    # ABA 5: LISTADOR DE ESTRUTURAS (PRESERVADA INTEGRALMENTE)
    # ==================================================================================
    def _construir_aba_listador_tree(self):
        tab = ttk.Frame(self.notebook, padding=10)
        self.notebook.add(tab, text="🌳 Listador de Estruturas")

        header_frame = ttk.LabelFrame(tab, text=" Emulador e Expansor Nativo do Utilitário Windows Tree ", padding=10)
        header_frame.pack(fill=tk.X, pady=(0, 10))

        ttk.Label(
            header_frame,
            text=(
                "Gera a listagem completa e hierárquica de todas as pastas, subpastas e arquivos (com extensão)\n"
                "do diretório ativo, recriando e expandindo nativamente o comportamento do script 'Listador de Estruturas.bat'.\n"
                "Cria automaticamente um arquivo nomeado no padrão: estrutura_YYYY-MM-DD_HHhMMm.txt."
            ),
            justify=tk.LEFT
        ).pack(anchor=tk.W)

        btn_box = ttk.Frame(tab)
        btn_box.pack(fill=tk.X, pady=8)

        ttk.Button(btn_box, text="💾 GERAR ARQUIVO DE ESTRUTURA (DUMP TXT DATADO)", style="RetroAction.TButton", command=self.gerar_dump_estrutura_txt).pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 6), ipady=5)
        ttk.Button(btn_box, text="🖥️ EXIBIR ÁRVORE DIRETAMENTE NO CONSOLE CRT", style="Retro.TButton", command=self.exibir_arvore_no_console).pack(side=tk.RIGHT, fill=tk.X, expand=True, padx=(6, 0), ipady=5)

    def _gerar_arvore_ascii(self, root_dir: str) -> Tuple[List[str], int, int]:
        linhas = []
        total_dirs = 0
        total_files = 0
        for dirpath, dirnames, filenames in os.walk(root_dir):
            dirnames[:] = [d for d in dirnames if d not in IGNORE_DIRS]
            rel_path = os.path.relpath(dirpath, root_dir)
            if rel_path != ".":
                nivel = rel_path.count(os.sep)
                linhas.append(f"{'│   ' * nivel}├── 📁 {os.path.basename(dirpath)}\\")
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

        def _work(cancel_ev, prog_cb):
            timestamp = datetime.now()
            nome_arquivo = f"estrutura_{timestamp.strftime('%Y-%m-%d_%Hh%Mm')}.txt"
            caminho_saida = os.path.join(caminho, nome_arquivo)
            linhas_arvore, total_dirs, total_files = self._gerar_arvore_ascii(caminho)
            conteudo = "\n".join([
                "ESTRUTURA", f"Diretório Raiz: {caminho}", "",
                f"Listagem de pastas e arquivos para o volume {os.path.basename(caminho)}", "=" * 60, ""
            ] + linhas_arvore + [
                "", "=" * 60, f"Total de Diretórios : {total_dirs}", f"Total de Arquivos    : {total_files}",
                f"Arquivo gerado em   : {timestamp.strftime('%d/%m/%Y às %H:%M:%S')}", "=" * 60, ""
            ])
            with open(caminho_saida, "w", encoding="utf-8") as wf:
                wf.write(conteudo)
            return caminho_saida, nome_arquivo, total_dirs, total_files

        def _done(res):
            caminho_saida, nome_arquivo, t_dirs, t_files = res
            self.log(f"\n[ESTRUTURA DUMP] Arquivo criado com sucesso em:\n  {caminho_saida} ({t_dirs} pastas, {t_files} arquivos)")
            messagebox.showinfo("Estrutura Gerada", f"Arquivo '{nome_arquivo}' criado com sucesso em:\n{caminho}")

        self.task_mgr.run_async("Gerar Estrutura TXT", _work, _done)

    def exibir_arvore_no_console(self):
        caminho = self.src_project_path.get().strip()
        if not os.path.exists(caminho):
            messagebox.showwarning("Aviso", "O diretório informado não existe!")
            return
        linhas_arvore, total_dirs, total_files = self._gerar_arvore_ascii(caminho)
        self.log(f"\n[ÁRVORE DE ARQUIVOS] Mapeando: {caminho}")
        for l in linhas_arvore:
            self.log(l)
        self.log(f"[TOTAL] {total_dirs} diretórios, {total_files} arquivos mapeados.")

    # ==================================================================================
    # ABA 6: HARDWARE-Z PRO (PRESERVADA E EXPANDIDA)
    # ==================================================================================
    def _construir_aba_hardware_z(self):
        tab = ttk.Frame(self.notebook, padding=10)
        self.notebook.add(tab, text="💻 Hardware-Z Pro")

        header_frame = ttk.LabelFrame(tab, text=" Painel de Avaliação de Hardware, Rede, Partições e Processos ", padding=8)
        header_frame.pack(fill=tk.X, pady=(0, 8))

        ttk.Button(header_frame, text="🔄 ATUALIZAR TELEMETRIA AGORA", style="RetroAction.TButton", command=self.exibir_diagnostico_hardware).pack(side=tk.RIGHT, padx=4)
        ttk.Button(header_frame, text="💾 Exportar Diagnóstico", style="Retro.TButton", command=self.hw_exportar_relatorio).pack(side=tk.RIGHT, padx=4)
        ttk.Label(header_frame, text="Monitoramento local real sem congelar a interface.", font=("Tahoma", 9, "bold")).pack(side=tk.LEFT)

        self.hw_container = ttk.LabelFrame(tab, text=" Especificações Técnicas da Máquina ", padding=8)
        self.hw_container.pack(fill=tk.BOTH, expand=True)

        self.lbl_hw_info = scrolledtext.ScrolledText(self.hw_container, wrap=tk.WORD, font=("Consolas", 9), height=12)
        self.lbl_hw_info.pack(fill=tk.BOTH, expand=True)

        self.root.after(600, self.exibir_diagnostico_hardware)

    def exibir_diagnostico_hardware(self):
        def _work(cancel_ev, prog_cb):
            dados = obter_telemetria_hardware()
            linhas = [
                "================================================================================",
                "   KANIVET XP NEXUS // HARDWARE-Z PRO — DIAGNÓSTICO DO COMPUTADOR",
                "================================================================================",
                f"  • Sistema Operacional : {dados['so']}",
                f"  • Arquitetura / Host  : {dados['arquitetura']} | Host: {dados['hostname']}",
                f"  • Processador Host    : {dados['processador']}",
                f"  • Núcleos CPU         : {dados['cpus_logicas']} Lógicos | {dados['cpus_fisicas']} Físicos | Uso: {dados['cpu_percent']}",
                f"  • Versão do Python    : {dados['python_version']}",
                "--------------------------------------------------------------------------------",
                f"  • Memória RAM         : Total: {dados['ram_total']} | Usada: {dados['ram_usada']} ({dados['ram_percent']}) | Livre: {dados['ram_livre']}",
                f"  • Disco Principal     : Total: {dados['disco_total']} | Usado: {dados['disco_usado']} ({dados['disco_percent']}) | Livre: {dados['disco_livre']}",
                f"  • Tráfego de Rede I/O : Enviado: {dados['rede_enviado']} | Recebido: {dados['rede_recebido']}",
                f"  • Tempo de Atividade  : {dados['uptime']}",
            ]
            if dados["particoes"]:
                linhas.append("--------------------------------------------------------------------------------")
                linhas.append("  • Partições Montadas:")
                for pt in dados["particoes"]:
                    linhas.append(f"      - {pt}")
            if dados["top_processos"]:
                linhas.append("--------------------------------------------------------------------------------")
                linhas.append("  • Top 5 Processos por Consumo de Memória:")
                for pr in dados["top_processos"]:
                    linhas.append(f"      - {pr}")
            linhas.append("================================================================================")
            return "\n".join(linhas)

        def _done(texto):
            self.lbl_hw_info.delete("1.0", tk.END)
            self.lbl_hw_info.insert(tk.END, texto)
            self.log("\n" + texto)

        self.task_mgr.run_async("Telemetria Hardware-Z", _work, _done)

    def hw_exportar_relatorio(self):
        conteudo = self.lbl_hw_info.get("1.0", tk.END).strip()
        if not conteudo:
            return
        saida = filedialog.asksaveasfilename(title="Salvar Diagnóstico Hardware-Z", defaultextension=".txt", initialfile="hardware_z_diagnostico.txt")
        if saida:
            with open(saida, "w", encoding="utf-8") as f:
                f.write(conteudo)
            messagebox.showinfo("Salvo", f"Relatório salvo em:\n{saida}")

    # ==================================================================================
    # ABA 7: NOVO MÓDULO CODE QUALITY
    # ==================================================================================
    def _construir_aba_code_quality(self):
        tab = ttk.Frame(self.notebook, padding=8)
        self.notebook.add(tab, text="✅ Code Quality")

        bar = ttk.LabelFrame(tab, text=" Verificadores Estáticos, Testes e Analisador AST Nativo ", padding=6)
        bar.pack(fill=tk.X, pady=(0, 6))

        for rotulo, chave in [
            ("🔍 AST Python Nativo (Embutido)", "ast_nativo"),
            ("⚡ Ruff Linter", "ruff"),
            ("🎨 Black (--check)", "black_check"),
            ("🔬 Mypy (Tipos)", "mypy"),
            ("🛡️ Bandit (Segurança)", "bandit"),
            ("🧪 Pytest", "pytest")
        ]:
            ttk.Button(bar, text=rotulo, style="Retro.TButton", command=lambda k=chave: self.quality_executar(k)).pack(side=tk.LEFT, padx=2, expand=True, fill=tk.X)

        self.txt_quality = scrolledtext.ScrolledText(tab, wrap=tk.WORD, font=("Consolas", 9), height=12)
        self.txt_quality.pack(fill=tk.BOTH, expand=True)

    def quality_executar(self, ferramenta: str):
        caminho = self.src_project_path.get().strip()
        if not os.path.exists(caminho):
            return

        def _work(cancel_ev, prog_cb):
            disp = CodeQualityEngine.verificar_ferramentas_disponiveis()
            cab = "Ferramentas instaladas no ambiente: " + ", ".join(f"{k}={'OK' if v else 'Ausente'}" for k, v in disp.items())
            res = CodeQualityEngine.executar_ferramenta(ferramenta, caminho)
            return cab + "\n" + ("-" * 75) + "\n" + res

        def _done(texto):
            self.txt_quality.delete("1.0", tk.END)
            self.txt_quality.insert(tk.END, texto)
            self.log("\n" + texto)
            self.history_manager.registrar("CodeQuality", ferramenta, "Executado")

        self.task_mgr.run_async(f"Code Quality ({ferramenta})", _work, _done)

    # ==================================================================================
    # ABA 8: NOVO MÓDULO DE DEPENDÊNCIAS E AMBIENTE
    # ==================================================================================
    def _construir_aba_dependencias(self):
        tab = ttk.Frame(self.notebook, padding=8)
        self.notebook.add(tab, text="📦 Dependências")

        top = ttk.Frame(tab)
        top.pack(fill=tk.X, pady=(0, 6))
        ttk.Button(top, text="🔍 Diagnosticar Ambiente Python, Pacotes & Requisitos", style="RetroAction.TButton", command=self.dep_executar_diagnostico).pack(side=tk.LEFT, fill=tk.X, expand=True, padx=2)

        self.txt_deps = scrolledtext.ScrolledText(tab, wrap=tk.WORD, font=("Consolas", 9), height=12)
        self.txt_deps.pack(fill=tk.BOTH, expand=True)

    def dep_executar_diagnostico(self):
        caminho = self.src_project_path.get().strip()
        dados = DependencyEngine.diagnosticar_ambiente(caminho)
        linhas = [
            "================================================================================",
            "   DIAGNÓSTICO DE AMBIENTE PYTHON E DEPENDÊNCIAS (SOMENTE LEITURA)",
            "================================================================================",
            f"  • Interpretador Ativo : {dados['executable']}",
            f"  • Versão do Python    : {dados['python_version']}",
            f"  • Virtualenv Ativo    : {dados['virtualenv_ativo']}",
            f"  • Total Instalados    : {dados['total_pacotes_instalados']} pacotes",
            "--------------------------------------------------------------------------------",
            f"  • Declarados em requirements.txt ({len(dados['declarados_requirements'])}): {', '.join(dados['declarados_requirements']) or 'Nenhum arquivo requirements.txt na raiz'}",
            f"  • Ausentes no Ambiente ({len(dados['ausentes_requirements'])}): {', '.join(dados['ausentes_requirements']) or 'Nenhuma dependência declarada ausente'}",
            "--------------------------------------------------------------------------------",
            "  • Ferramentas Externas no PATH do Sistema:"
        ]
        for k, v in dados["ferramentas_externas"].items():
            linhas.append(f"      - {k:10s}: {v}")
        linhas.append("--------------------------------------------------------------------------------")
        linhas.append("  • Amostra de Pacotes Instalados:")
        for pk, pv in dados["pacotes_amostra"].items():
            linhas.append(f"      {pk:28s} == {pv}")
        texto = "\n".join(linhas)
        self.txt_deps.delete("1.0", tk.END)
        self.txt_deps.insert(tk.END, texto)
        self.log("\n[DEPENDÊNCIAS] Diagnóstico concluído.")

    # ==================================================================================
    # ABA 9: NOVO EXPLORADOR AVANÇADO DE PROJETOS
    # ==================================================================================
    def _construir_aba_explorador_avancado(self):
        tab = ttk.Frame(self.notebook, padding=8)
        self.notebook.add(tab, text="🔎 Explorador Pro")

        f_bar = ttk.LabelFrame(tab, text=" Filtros de Busca por Nome, Conteúdo Textual, Extensão e Comparação ", padding=6)
        f_bar.pack(fill=tk.X, pady=(0, 6))

        ttk.Label(f_bar, text="Nome:").pack(side=tk.LEFT, padx=2)
        ttk.Entry(f_bar, textvariable=self.exp_name_var, width=16).pack(side=tk.LEFT, padx=2)
        ttk.Label(f_bar, text="Texto Interno:").pack(side=tk.LEFT, padx=2)
        ttk.Entry(f_bar, textvariable=self.exp_text_var, width=18).pack(side=tk.LEFT, padx=2)
        ttk.Label(f_bar, text="Extensões (.py,.md):").pack(side=tk.LEFT, padx=2)
        ttk.Entry(f_bar, textvariable=self.exp_ext_var, width=12).pack(side=tk.LEFT, padx=2)

        ttk.Button(f_bar, text="🔎 Buscar", style="RetroAction.TButton", command=self.exp_executar_busca).pack(side=tk.LEFT, padx=4)
        ttk.Button(f_bar, text="⚖️ Comparar com Outra Pasta...", style="Retro.TButton", command=self.exp_comparar_pastas).pack(side=tk.LEFT, padx=2)
        ttk.Button(f_bar, text="🧹 Espaço, Duplicados & Temporários", style="Retro.TButton", command=self.exp_diagnosticar_espaco).pack(side=tk.LEFT, padx=2)

        cols = ("arquivo", "ext", "tamanho", "modificado")
        self.tree_exp = ttk.Treeview(tab, columns=cols, show="headings", height=9)
        for cid, tit, w in [("arquivo", "Caminho Relativo", 420), ("ext", "Extensão", 90), ("tamanho", "Tamanho", 110), ("modificado", "Modificado em", 140)]:
            self.tree_exp.heading(cid, text=tit)
            self.tree_exp.column(cid, width=w, anchor=tk.W)
        self.tree_exp.pack(fill=tk.BOTH, expand=True)

    def exp_executar_busca(self):
        caminho = self.src_project_path.get().strip()
        if not os.path.exists(caminho):
            return
        res = ProjectExplorerEngine.buscar_arquivos(caminho, self.exp_name_var.get(), self.exp_text_var.get(), self.exp_ext_var.get())
        for i in self.tree_exp.get_children():
            self.tree_exp.delete(i)
        for r in res:
            self.tree_exp.insert("", tk.END, values=(r["arquivo"], r["ext"], r["tamanho_fmt"], r["modificado"]))
        self.log(f"[EXPLORADOR PRO] {len(res)} arquivo(s) encontrado(s) para os filtros informados.")

    def exp_comparar_pastas(self):
        dir_a = self.src_project_path.get().strip()
        dir_b = filedialog.askdirectory(title="Selecione o Segundo Diretório (B) para Comparação")
        if not dir_b:
            return
        comp = ProjectExplorerEngine.comparar_diretorios(dir_a, dir_b)
        rel = [
            f"=== COMPARAÇÃO ENTRE DIRETÓRIOS ===\nPasta A: {dir_a}\nPasta B: {dir_b}\n",
            f"• Arquivos Idênticos (Mesmo SHA-256) : {len(comp['identicos'])}",
            f"• Arquivos Modificados (Hash difere) : {len(comp['modificados'])} -> {', '.join(comp['modificados'][:20])}",
            f"• Exclusivos da Pasta A              : {len(comp['apenas_em_A'])} -> {', '.join(comp['apenas_em_A'][:20])}",
            f"• Exclusivos da Pasta B              : {len(comp['apenas_em_B'])} -> {', '.join(comp['apenas_em_B'][:20])}"
        ]
        self._exibir_janela_texto("Comparação de Diretórios", "\n".join(rel))

    def exp_diagnosticar_espaco(self):
        caminho = self.src_project_path.get().strip()
        diag = ProjectExplorerEngine.diagnosticar_espaco_e_temporarios(caminho)
        rel = [
            f"=== DIAGNÓSTICO DE ESPAÇO, DUPLICIDADES E TEMPORÁRIOS ===\nDiretório: {caminho}",
            f"• Espaço Total Ocupado: {diag['total_fmt']}",
            f"• Distribuição Top Extensões: {diag['uso_por_extensao']}",
            f"• Arquivos Temporários Detectados ({len(diag['arquivos_temporarios'])}): {', '.join(diag['arquivos_temporarios'][:30])}",
            f"• Grupos de Arquivos Duplicados por Hash ({len(diag['duplicidades_hash'])}): {diag['duplicidades_hash']}"
        ]
        self._exibir_janela_texto("Relatório de Estrutura e Espaço", "\n".join(rel))

    # ==================================================================================
    # ABA 10: NOVO WORKSPACE E AUTOMAÇÕES (AUDITORIA PRÉ-PUBLICAÇÃO)
    # ==================================================================================
    def _construir_aba_workspace_automacoes(self):
        tab = ttk.Frame(self.notebook, padding=8)
        self.notebook.add(tab, text="🚀 Automações & Workspace")

        w_bar = ttk.LabelFrame(tab, text=" Perfis de Projetos Persistentes & Pipeline de Auditoria Pré-Publicação ", padding=8)
        w_bar.pack(fill=tk.X, pady=(0, 6))

        ttk.Button(w_bar, text="💾 Salvar Projeto Atual nos Perfis", style="Retro.TButton", command=self.workspace_salvar_atual).pack(side=tk.LEFT, padx=3)
        ttk.Button(w_bar, text="📂 Carregar Perfil Salvo...", style="Retro.TButton", command=self.workspace_carregar_dialog).pack(side=tk.LEFT, padx=3)
        ttk.Button(w_bar, text="🚀 EXECUTAR PIPELINE DE AUDITORIA PRÉ-PUBLICAÇÃO (6 ETAPAS REAIS)", style="RetroAction.TButton", command=self.automacao_executar_pipeline).pack(side=tk.LEFT, padx=6, fill=tk.X, expand=True)
        ttk.Button(w_bar, text="🧪 Autotestes", style="Retro.TButton", command=self.executar_autotestes_gui).pack(side=tk.RIGHT, padx=3)

        self.txt_automacao = scrolledtext.ScrolledText(tab, wrap=tk.WORD, font=("Consolas", 9), height=12)
        self.txt_automacao.pack(fill=tk.BOTH, expand=True)

    def workspace_salvar_atual(self):
        nome = simpledialog.askstring("Salvar Workspace", "Nome do Perfil do Projeto:")
        if nome and nome.strip():
            WorkspaceAutomationEngine.salvar_perfil(nome.strip(), {
                "path": self.src_project_path.get(),
                "git_name": self.git_name_var.get(),
                "git_email": self.git_email_var.get(),
                "repo_url": self.repo_url_var.get(),
                "branch": self.branch_var.get(),
                "md_profile": self.md_profile_var.get()
            })
            self.log(f"[WORKSPACE] Perfil '{nome.strip()}' salvo com sucesso.")

    def workspace_carregar_dialog(self):
        perfis = WorkspaceAutomationEngine.carregar_perfis()
        if not perfis:
            messagebox.showinfo("Workspaces", "Nenhum perfil salvo ainda.")
            return
        nomes = list(perfis.keys())
        escolha = simpledialog.askstring("Carregar Workspace", f"Perfis disponíveis:\n{', '.join(nomes)}\n\nDigite o nome do perfil:")
        if escolha and escolha in perfis:
            p = perfis[escolha]
            self.src_project_path.set(p.get("path", self.src_project_path.get()))
            self.git_name_var.set(p.get("git_name", self.git_name_var.get()))
            self.git_email_var.set(p.get("git_email", self.git_email_var.get()))
            self.repo_url_var.set(p.get("repo_url", self.repo_url_var.get()))
            self.branch_var.set(p.get("branch", "main"))
            self.md_profile_var.set(p.get("md_profile", "Universal (Todos os Formatos)"))
            self.log(f"[WORKSPACE] Perfil '{escolha}' carregado.")

    def automacao_executar_pipeline(self):
        caminho = self.src_project_path.get().strip()
        if not os.path.exists(caminho):
            messagebox.showwarning("Aviso", "Diretório ativo inválido.")
            return

        def _work(cancel_ev, prog_cb):
            return WorkspaceAutomationEngine.executar_auditoria_pre_publicacao(caminho, cancel_ev, prog_cb)

        def _done(relatorio):
            self.txt_automacao.delete("1.0", tk.END)
            self.txt_automacao.insert(tk.END, relatorio)
            self.log("\n" + relatorio)
            self.history_manager.registrar("Automacao", "Auditoria Pré-Publicação", "Concluído")

        self.task_mgr.run_async("Pipeline Pré-Publicação", _work, _done)

    def executar_autotestes_gui(self):
        rel = executar_suite_autotestes()
        self.log("\n" + rel)
        self._exibir_janela_texto("Suíte Interna de Autotestes de Não-Regressão", rel)

    # ==================================================================================
    # JANELAS AUXILIARES, HISTÓRICO, MANUAL INTEGRADO & SOBRE (PRESERVADOS)
    # ==================================================================================
    def _exibir_janela_texto(self, titulo: str, conteudo: str):
        win = tk.Toplevel(self.root)
        win.title(titulo)
        win.geometry("820x560")
        win.configure(bg=XP_BG_BASE)
        txt = scrolledtext.ScrolledText(win, wrap=tk.WORD, font=("Consolas", 9))
        txt.pack(fill=tk.BOTH, expand=True, padx=8, pady=8)
        txt.insert(tk.END, conteudo)
        ttk.Button(win, text="Fechar", style="Retro.TButton", command=win.destroy).pack(side=tk.RIGHT, padx=10, pady=6)

    def abrir_janela_historico(self):
        linhas = ["=== HISTÓRICO DE OPERAÇÕES DA SUÍTE ===\n"]
        for e in reversed(self.history_manager.entries):
            linhas.append(f"[{e['timestamp']}] [{e['modulo']:14s}] {e['acao']:26s} -> {e['status']} | {e['detalhes']}")
        self._exibir_janela_texto("Histórico de Operações", "\n".join(linhas))

    def abrir_manual_usuario(self):
        """Preservado integralmente do arquivo original e expandido com as novas abas."""
        help_win = tk.Toplevel(self.root)
        help_win.title("Kanivet XP — Manual do Usuário e Orientações Técnicas")
        help_win.geometry("860x640")
        help_win.minsize(740, 500)
        help_win.configure(bg=XP_BG_BASE)

        top_bar = ttk.Frame(help_win, padding=10)
        top_bar.pack(fill=tk.X)
        ttk.Label(top_bar, text="📖 Sistema de Ajuda & Manual Integrado", font=("Tahoma", 12, "bold"), foreground=XP_ACCENT).pack(anchor=tk.W)
        ttk.Label(top_bar, text="Instruções operacionais detalhadas para cada um dos núcleos do Kanivet XP.", font=("Tahoma", 9)).pack(anchor=tk.W)

        help_notebook = ttk.Notebook(help_win, padding=6)
        help_notebook.pack(fill=tk.BOTH, expand=True, padx=8, pady=(0, 8))

        secoes_manual = [
            ("1. Sanitizador & Security",
             "COMO USAR O SANITIZADOR E O SECURITY CENTER:\n\n"
             "1. Selecione a pasta do seu código na barra superior do programa.\n"
             "2. Clique em 'Inspecionar Segredos & Severidade' para auditar chaves sem alterar arquivos.\n"
             "3. O Sanitizador cria um backup ZIP automático e exporta uma cópia limpa em '<projeto>_clean_export'.\n"
             "4. Você pode visualizar a prévia das alterações (Diff) ou usar o Modo Simulação (Dry-Run)."),
            ("2. Incidentes de Token",
             "O QUE FAZER CASO UM TOKEN DO TELEGRAM OU CHAVE VAZE:\n\n"
             "1. TELEGRAM BOT TOKEN: Converse com @BotFather -> /revoke -> selecione o bot.\n"
             "2. GITHUB SECRET SCANNING: Revogue a chave na origem (OpenAI, AWS, GitHub) e feche o alerta como Revoked."),
            ("3. Geração de PAT",
             "COMO GERAR E UTILIZAR O PERSONAL ACCESS TOKEN (PAT) NO GITHUB:\n\n"
             "1. Acesse https://github.com/settings/tokens -> Generate new token (classic).\n"
             "2. Marque o escopo [X] repo e copie o código ghp_... para o campo GitHub Token (PAT)."),
            ("4. Central Git",
             "OPERAÇÕES GIT BAREMETAL:\n\n"
             "Executa comandos Git reais com subprocess seguro (shell=False), incluindo status, diff, log, commit, push, tags, branches, detecção de conflitos e varredura de arquivos grandes."),
            ("5. MDnator v5.0",
             "COMPILAÇÃO DE PROJETOS PARA IAs:\n\n"
             "Suporta perfis específicos (Python/Flask, Arduino/ESP32, Web, Ciência de Dados, LLMs), detecção de duplicidades SHA-256, modo incremental e exportação em Markdown, JSON e TXT."),
            ("6. InfoPlan Pro",
             "AUDITORIA E ESTATÍSTICA DE PLANILHAS:\n\n"
             "Calcula estatísticas descritivas completas (Média, Mediana, Moda, Variância Amostral, Quartis, IQR, CV%, Assimetria e Curtose de Fisher), Matriz de Correlação e plota Histograma, Boxplot e Heatmap reais."),
            ("7. Novos Módulos Nexus",
             "CODE QUALITY, DEPENDÊNCIAS, EXPLORADOR PRO & AUTOMAÇÕES:\n\n"
             "• Code Quality: Analisador AST nativo + integração Ruff, Black, Mypy, Bandit e Pytest.\n"
             "• Dependências: Diagnóstico de virtualenv, pacotes instalados e requirements.txt.\n"
             "• Explorador Pro: Busca textual, comparação de pastas A vs B e detecção de temporários.\n"
             "• Automações: Pipeline completo de Auditoria Pré-Publicação em 6 etapas reais.")
        ]

        for titulo_aba, conteudo_aba in secoes_manual:
            tab_sec = ttk.Frame(help_notebook, padding=8)
            help_notebook.add(tab_sec, text=titulo_aba)
            txt = scrolledtext.ScrolledText(tab_sec, wrap=tk.WORD, bg="#FFFFFF", fg="#111111", font=("Tahoma", 9), relief="sunken", bd=1)
            txt.pack(fill=tk.BOTH, expand=True)
            txt.insert(tk.END, conteudo_aba)
            txt.config(state=tk.DISABLED)

        ttk.Button(help_win, text="Fechar Manual", style="Retro.TButton", command=help_win.destroy).pack(side=tk.RIGHT, padx=10, pady=8)

    def abrir_dialogo_sobre(self):
        """Preservado integralmente do arquivo original."""
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
            "SISTEMA       : KANIVET XP NEXUS (CYBER-GIT MDNATOR UNIVERSAL SUITE)\n"
            "VERSÃO        : 6.0 Enterprise Monolithic Standalone (Preservação Integral v5.0)\n"
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
            "                Compilação Markdown para IAs, Qualidade e Radiografia de Dados."
        )
        ttk.Label(info_box, text=creditos, justify=tk.LEFT, font=("Consolas", 9)).pack(anchor=tk.NW, fill=tk.BOTH, expand=True)

        btn_box = ttk.Frame(about_win, padding=5)
        btn_box.pack(fill=tk.X, padx=10, pady=5)
        ttk.Button(btn_box, text="Copiar E-mail", style="Retro.TButton", command=lambda: self._copiar_texto_clipboard("cienciaegestao@gmail.com")).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(btn_box, text="Copiar WhatsApp", style="Retro.TButton", command=lambda: self._copiar_texto_clipboard("+55 98 98250-6920")).pack(side=tk.LEFT)
        ttk.Button(btn_box, text="Fechar", style="Retro.TButton", command=about_win.destroy).pack(side=tk.RIGHT)

    def _copiar_texto_clipboard(self, texto: str):
        self.root.clipboard_clear()
        self.root.clipboard_append(texto)
        self.log(f"[CLIPBOARD] Valor copiado para a área de transferência: {texto}")
        messagebox.showinfo("Copiado", f"Copiado para a área de transferência:\n{texto}")


# ======================================================================================
# 19. INICIALIZAÇÃO DA APLICAÇÃO
# ======================================================================================
def main():
    if "--self-test" in sys.argv:
        relatorio = executar_suite_autotestes()
        print(relatorio)
        sys.exit(0 if "APROVADO (100%)" in relatorio else 1)

    root = tk.Tk()
    app = KanivetXPApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
