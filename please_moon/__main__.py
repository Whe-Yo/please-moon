"""CLI: python -m please_moon TICKER

미국 상장사의 T1(SEC EDGAR) 핵심 재무 사실 시트를 출력한다.
분석(시나리오·밸류에이션)은 clemini 레이어가 이 사실 위에 얹는다.
"""
from __future__ import annotations

import sys

from .sources import SECEdgar
from .report import fact_sheet


def main(argv: list[str]) -> int:
    if len(argv) != 1:
        print("사용: python -m please_moon TICKER   (예: AAPL)", file=sys.stderr)
        return 2
    ticker = argv[0]
    try:
        data = SECEdgar().fundamentals(ticker)
    except Exception as e:  # noqa: BLE001
        print(f"오류: {e}", file=sys.stderr)
        return 1
    print(fact_sheet(data))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
