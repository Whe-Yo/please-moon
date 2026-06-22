"""출력 포맷 — 사실 시트 + 출처 등급 + 면책.

분석(시나리오·밸류에이션·반론)은 clemini(LLM) 레이어가 채운다.
여기 코드는 **결정론적 사실 시트**만 렌더한다(검증 가능한 부분).
"""
from __future__ import annotations

from .sources import Fact, Tier

DISCLAIMER = (
    "※ 정보·사실 정리이며 투자 권유·개인화 조언이 아님(비면허). "
    "수치는 표기된 출처/기간 기준, 시점민감하니 의사결정 전 1차 출처 재확인."
)

_TIER_LABEL = {
    Tier.OFFICIAL: "T1 공식",
    Tier.REPUTABLE: "T2 평판",
    Tier.EVALUATIVE: "T3 평가",
    Tier.SPECULATIVE: "T4 추정",
}


def _human(n) -> str:
    try:
        n = float(n)
    except (TypeError, ValueError):
        return str(n)
    for div, suf in ((1e12, "T"), (1e9, "B"), (1e6, "M")):
        if abs(n) >= div:
            return f"{n/div:,.2f}{suf}"
    return f"{n:,.0f}"


def fact_sheet(data: dict) -> str:
    """SECEdgar.fundamentals() 결과 → 마크다운 사실 시트."""
    lines = [
        f"# {data['company']} ({data['ticker']}) — 사실 시트",
        "",
        f"CIK {data['cik']} · 출처: SEC EDGAR (T1 공식, 무료)",
        "",
        "| 항목 | 값 | 기간 | 출처(등급) |",
        "|---|---|---|---|",
    ]
    for f in data["facts"]:
        assert isinstance(f, Fact)
        lines.append(
            f"| {f.label} | {_human(f.value)} {f.unit} | {f.period} | {f.source}({_TIER_LABEL[f.tier]}) |"
        )
    if not data["facts"]:
        lines.append("| (us-gaap 표준 태그에서 추출 실패) | — | — | — |")
    lines += ["", DISCLAIMER]
    return "\n".join(lines)
