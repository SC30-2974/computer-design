# AI辅助生成：DeepSeek-V3, 2026-03-30
from pathlib import Path
import sqlite3
from typing import Generator

BASE_DIR = Path(__file__).resolve().parents[2]
DATA_DIR = BASE_DIR / "data"
DB_PATH = DATA_DIR / "finance_app.db"


def get_db() -> Generator[sqlite3.Connection, None, None]:
    DATA_DIR.mkdir(exist_ok=True)
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    # 和初始化脚本保持一致，避免 Windows 本地环境出现 SQLite disk I/O error。
    conn.execute("PRAGMA journal_mode=MEMORY")
    conn.execute("PRAGMA synchronous=NORMAL")
    try:
        yield conn
    finally:
        conn.close()
