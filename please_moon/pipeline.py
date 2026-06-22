"""분석 파이프라인 — 코드(사실) → clemini(Gemini 1차 조사) → Claude 종합.

설계: 사실 수집은 결정론적 코드, 1차 정성 조사는 Gemini(agy, 최신 Pro)에 위임,
시점민감 검증·최종 종합은 Claude. 이 파일은 앞 두 단계를 자동화하고
'Claude 종합' 자리를 비워 드래프트로 내보낸다.
"""
from __future__ import annotations

import os
import subprocess

from .sources import SECEdgar, YahooChart
from .report import fact_sheet, DISCLAIMER

# clemini 위임 래퍼 경로 (환경변수로 override).
DELEGATE = os.environ.get(
    "CLEMINI_DELEGATE",
    "/Volumes/Wheyo/0_RESEARCH/please-work-clemini/bin/delegate.sh",
)


def gather(ticker: str) -> dict:
    """결정론적 사실 수집 (T1 재무 + 시세)."""
    data = SECEdgar().fundamentals(ticker)
    try:
        price = YahooChart().latest_price(ticker)
        if price:
            data["facts"].insert(0, price)
    except Exception:  # noqa: BLE001
        pass
    return data


def _facts_brief(data: dict) -> str:
    rows = [f"- {f.label}: {f.value} {f.unit} ({f.period}, {f.source})" for f in data["facts"]]
    return f"{data['company']} ({data['ticker']}, CIK {data['cik']}):\n" + "\n".join(rows)


def delegate_research(data: dict, timeout: int = 300) -> str | None:
    """clemini(delegate.sh → agy/Gemini 최신 Pro)에 1차 정성 조사 위임."""
    if not os.path.exists(DELEGATE):
        return None
    spec = (
        f"다음 '사실'을 바탕으로 {data['company']}({data['ticker']}) 투자 정보 분석을 구조화하라. "
        "매수·매도 권유 금지(정보 정리만). 불확실하면 '불확실'. 서론 없이 끝나면 멈춰라:\n"
        "1. 핵심 사업·경제적 해자 2~3개.\n"
        "2. Bull / Base / Bear 시나리오 드라이버 각 2개.\n"
        "3. 전문가가 지켜볼 KPI·선행지표 4개.\n"
        "4. 구조적 리스크 3개.\n\n"
        "[사실]\n" + _facts_brief(data)
    )
    try:
        proc = subprocess.run(
            [DELEGATE, "--mode", "plan", spec],
            capture_output=True, text=True, timeout=timeout,
        )
        return proc.stdout.strip() or None
    except Exception:  # noqa: BLE001
        return None


def assemble_draft(data: dict, research: str | None) -> str:
    """사실 시트 + Gemini 1차 조사 + Claude 종합 자리 → 드래프트 리포트."""
    return "\n".join([
        fact_sheet(data),
        "\n---\n## Gemini 1차 조사 (clemini · agy 최신 Pro)\n",
        research or "_(위임 불가/실패 — delegate.sh 경로·agy 확인)_",
        "\n---\n## Claude 종합 (검증·밸류에이션·시나리오·신호)\n",
        "> 시점민감 사실(가격·상장상태·실적·일정)은 Claude가 라이브 검증 후 종합한다. "
        "위 1차 조사를 검증·교정하고 Bull/Base/Bear·지켜볼 신호로 마무리.",
        "\n" + DISCLAIMER,
    ])
