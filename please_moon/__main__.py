"""CLI.

  python -m please_moon TICKER            # T1 재무 사실 시트(빠름, 무키)
  python -m please_moon --report TICKER   # 전체 파이프라인(사실 + Gemini 1차 조사 드래프트)
"""
from __future__ import annotations

import sys

from .sources import SECEdgar, YahooChart
from .report import fact_sheet


def _fact_sheet(ticker: str) -> int:
    try:
        data = SECEdgar().fundamentals(ticker)
    except Exception as e:  # noqa: BLE001
        print(f"오류: {e}", file=sys.stderr)
        return 1
    try:
        price = YahooChart().latest_price(ticker)
        if price:
            data["facts"].insert(0, price)
    except Exception:  # noqa: BLE001
        pass
    print(fact_sheet(data))
    return 0


def _report(ticker: str) -> int:
    from .pipeline import gather, delegate_research, assemble_draft
    try:
        data = gather(ticker)
    except Exception as e:  # noqa: BLE001
        print(f"오류: {e}", file=sys.stderr)
        return 1
    print("[clemini] Gemini 1차 조사 위임 중…", file=sys.stderr)
    research = delegate_research(data)
    print(assemble_draft(data, research))
    return 0


def main(argv: list[str]) -> int:
    if len(argv) == 1 and not argv[0].startswith("-"):
        return _fact_sheet(argv[0])
    if len(argv) == 2 and argv[0] == "--report":
        return _report(argv[1])
    print("사용:\n  python -m please_moon TICKER\n  python -m please_moon --report TICKER",
          file=sys.stderr)
    return 2


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
