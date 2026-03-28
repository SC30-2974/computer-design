from __future__ import annotations

import os
import sqlite3
from pathlib import Path
from typing import Any

BASE_DIR = Path(__file__).resolve().parents[2]
DATA_DIR = BASE_DIR / 'data'
RAW_DIR = DATA_DIR / 'raw'
CHROMA_DIR = DATA_DIR / 'chroma_db'
PDF_PATH = RAW_DIR / '各企业2025年财报数据.pdf'
DB_PATH = DATA_DIR / 'finance_app.db'


def load_pdf_documents(pdf_path: Path = PDF_PATH) -> list[Any]:
    try:
        import pdfplumber
        from langchain_core.documents import Document
    except ModuleNotFoundError:
        return []

    documents: list[Any] = []
    if not pdf_path.exists():
        return documents

    with pdfplumber.open(pdf_path) as pdf:
        for page_no, page in enumerate(pdf.pages, start=1):
            text = page.extract_text() or ''
            if not text.strip():
                continue
            documents.append(
                Document(
                    page_content=text,
                    metadata={'source': pdf_path.name, 'page': page_no},
                )
            )
    return documents


def build_vector_store() -> Any:
    try:
        from langchain_chroma import Chroma
        from langchain_openai import OpenAIEmbeddings
        from langchain_text_splitters import RecursiveCharacterTextSplitter
    except ModuleNotFoundError as exc:
        raise RuntimeError('缺少 RAG 依赖，请安装 langchain/chroma/openai 相关库。') from exc

    documents = load_pdf_documents(PDF_PATH)
    if not documents:
        raise FileNotFoundError(f'未找到可切块的 PDF 文档：{PDF_PATH}')

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=120,
        separators=['\n\n', '\n', '。', '，', ' ', ''],
    )
    split_docs = splitter.split_documents(documents)

    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        raise RuntimeError('未配置 OPENAI_API_KEY，无法构建在线向量索引。')

    embeddings = OpenAIEmbeddings(
        model=os.getenv('EMBEDDING_MODEL', 'text-embedding-3-small'),
        api_key=api_key,
        base_url=os.getenv('OPENAI_BASE_URL'),
    )

    CHROMA_DIR.mkdir(parents=True, exist_ok=True)
    return Chroma.from_documents(
        documents=split_docs,
        embedding=embeddings,
        persist_directory=str(CHROMA_DIR),
        collection_name='finance_reports_2025',
    )


def ask_financial_question(question: str, top_k: int = 5) -> dict[str, Any]:
    if os.getenv('ENABLE_ONLINE_RAG', '0') != '1':
        return build_local_fallback_answer(question, '未开启在线 RAG（ENABLE_ONLINE_RAG!=1）。')

    try:
        from langchain_chroma import Chroma
        from langchain_openai import ChatOpenAI, OpenAIEmbeddings
    except ModuleNotFoundError as exc:
        return build_local_fallback_answer(question, f'RAG 依赖未安装：{exc}')

    try:
        api_key = os.getenv('OPENAI_API_KEY')
        if not api_key:
            raise RuntimeError('未配置 OPENAI_API_KEY，无法执行在线 RAG 推理。')

        embeddings = OpenAIEmbeddings(
            model=os.getenv('EMBEDDING_MODEL', 'text-embedding-3-small'),
            api_key=api_key,
            base_url=os.getenv('OPENAI_BASE_URL'),
        )

        vector_store = Chroma(
            persist_directory=str(CHROMA_DIR),
            embedding_function=embeddings,
            collection_name='finance_reports_2025',
        )
        retriever = vector_store.as_retriever(search_kwargs={'k': top_k})
        docs = retriever.invoke(question)
        if not docs:
            raise RuntimeError('向量检索未命中有效片段。')

        context_blocks: list[str] = []
        citations: list[dict[str, Any]] = []
        for doc in docs:
            page = doc.metadata.get('page', '未知页')
            source = doc.metadata.get('source', '未知来源')
            context_blocks.append(f'[来源:{source}-第{page}页]\n{doc.page_content}')
            citations.append({'source': source, 'page': page})

        context_text = '\n\n'.join(context_blocks)
        prompt = f"""
你是新能源财报分析助手，请严格仅基于给定资料回答，不得编造数据。
如果资料不足，请明确说明“根据当前检索结果无法确认”。

用户问题：
{question}

检索资料：
{context_text}

请按以下结构回答：
1. 结论摘要
2. 核心依据
3. 风险或不确定性
4. 引用来源
"""

        llm = ChatOpenAI(
            model=os.getenv('LLM_MODEL', 'gpt-4o-mini'),
            temperature=0.1,
            api_key=api_key,
            base_url=os.getenv('OPENAI_BASE_URL'),
        )
        response = llm.invoke(prompt)

        return {
            'question': question,
            'answer': response.content,
            'citations': citations,
            'mode': 'rag',
            'retrieved_chunks': [
                {
                    'source': doc.metadata.get('source'),
                    'page': doc.metadata.get('page'),
                    'preview': doc.page_content[:180],
                }
                for doc in docs
            ],
        }
    except Exception as exc:
        return build_local_fallback_answer(question, str(exc))


def build_local_fallback_answer(question: str, reason: str) -> dict[str, Any]:
    rows = load_company_rows()
    if not rows:
        return {
            'question': question,
            'answer': '当前未读取到企业财报数据，请先执行数据库初始化脚本。',
            'citations': [],
            'mode': 'fallback',
            'fallback_reason': reason,
        }

    mentioned = [row for row in rows if row['company_name'] in question]
    selected = mentioned if mentioned else rows[:2]

    lines = ['1. 结论摘要']
    if len(selected) == 1:
        one = selected[0]
        lines.append(
            f"{one['company_name']}前三季度营收 {one['revenue']} 亿元，净利润 {one['profit']} 亿元，毛利率 {one['margin']}%，整体表现为{judge_company(one)}。"
        )
    else:
        a = selected[0]
        b = selected[1]
        lines.append(
            f"{a['company_name']}与{b['company_name']}对比看，营收规模分别为 {a['revenue']} / {b['revenue']} 亿元，净利润分别为 {a['profit']} / {b['profit']} 亿元，毛利率分别为 {a['margin']}% / {b['margin']}%。"
        )

    lines.append('2. 核心依据')
    for item in selected:
        lines.append(f"- {item['company_name']}：营收 {item['revenue']} 亿元，净利润 {item['profit']} 亿元，毛利率 {item['margin']}%。")
        lines.append(f"  经营摘要：{item.get('business_summary') or '暂无'}")

    lines.append('3. 风险或不确定性')
    for item in selected:
        lines.append(f"- {item['company_name']}：{item.get('risk_opportunity') or '暂无'}")

    lines.append('4. 引用来源')
    lines.append('- finance_app.db / company_metrics（本地结构化财报数据表）')
    lines.append('')
    lines.append(f'注：当前回答使用本地回退模式，原因：{reason}')

    citations = [
        {
            'source': 'finance_app.db',
            'page': (item.get('source_page') or '结构化数据'),
        }
        for item in selected
    ]

    return {
        'question': question,
        'answer': '\n'.join(lines),
        'citations': citations,
        'mode': 'fallback',
        'fallback_reason': reason,
    }


def load_company_rows() -> list[dict[str, Any]]:
    if not DB_PATH.exists():
        return []
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    try:
        rows = conn.execute(
            """
            SELECT company_name, revenue, profit, margin, business_summary, risk_opportunity, source_page
            FROM company_metrics
            WHERE period = '前三季度'
            ORDER BY revenue DESC
            """
        ).fetchall()
        return [dict(row) for row in rows]
    except sqlite3.OperationalError:
        return []
    finally:
        conn.close()


def judge_company(row: dict[str, Any]) -> str:
    margin = float(row.get('margin') or 0)
    profit = float(row.get('profit') or 0)
    if margin >= 20 and profit > 0:
        return '盈利能力较强'
    if margin >= 10 and profit > 0:
        return '盈利能力中性偏稳'
    if profit <= 0:
        return '盈利承压'
    return '盈利能力一般'
