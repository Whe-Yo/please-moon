"""please-moon — 주식 분석·정보 에이전트 (정보형, 글로벌/US 우선).

데이터 수집(결정론적 코드) ↔ 분석·종합(clemini LLM) 분리.
"""
from .sources import SECEdgar, Tier, Fact
from .report import fact_sheet, DISCLAIMER

__version__ = "0.2.0"
__all__ = ["SECEdgar", "Tier", "Fact", "fact_sheet", "DISCLAIMER"]
