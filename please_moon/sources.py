"""데이터 소스 추상화 + 어댑터.

설계 원칙:
- 데이터 수집은 **결정론적 코드**(여기), 분석·종합은 clemini(LLM) 레이어가 맡는다.
- 모든 소스는 신뢰도 Tier를 달고 들어온다(출처 등급 표기·교차검증의 근거).
- 어댑터 교체로 provider를 갈아끼운다(OpenBB/Twelve Data/Finnhub 등 추가 지점).
"""
from __future__ import annotations

import json
import urllib.request
from dataclasses import dataclass, field
from enum import IntEnum
from typing import Optional

# SEC는 식별 가능한 User-Agent를 요구한다(없으면 403).
USER_AGENT = "please-moon research (contact: wnrwjs120@gmail.com)"


class Tier(IntEnum):
    """소스 신뢰도 등급 (data-sources.md)."""
    OFFICIAL = 1     # 공시·거래소 (절대)
    REPUTABLE = 2    # 평판 매체·브로커 API
    EVALUATIVE = 3   # 표준 데이터·리서치 (의견은 컨센서스 변수)
    SPECULATIVE = 4  # 커뮤니티·AI·블로그 (사실근거 불가)


@dataclass
class Fact:
    """하나의 검증 가능한 수치/사실."""
    label: str
    value: object
    unit: str = ""
    period: str = ""       # 기준일/기간 (예: 2025-09-28)
    source: str = ""       # 소스명
    tier: Tier = Tier.OFFICIAL
    tag: str = ""          # 원천 태그(예: us-gaap:Revenues)


def _get_json(url: str) -> dict:
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.load(resp)


# Yahoo 엔드포인트는 식별 가능한 브라우저 UA가 필요(기본 UA는 차단되기도 함).
_BROWSER_UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"


class YahooChart:
    """Yahoo Finance chart 엔드포인트 (무료·무키, 글로벌 시세). 집계 → T3.

    ⚠️ **비공식** — 가끔 깨지거나 차단됨(프로토타입용). 신뢰 시세는 키 기반
    어댑터(Twelve Data/Finnhub)로 교체. 글로벌 심볼은 접미사 사용(예: 005930.KS, 7203.T).
    """
    name = "Yahoo(비공식)"
    tier = Tier.EVALUATIVE

    def latest_price(self, ticker: str) -> Optional[Fact]:
        url = (f"https://query1.finance.yahoo.com/v8/finance/chart/{ticker}"
               "?interval=1d&range=1d")
        req = urllib.request.Request(url, headers={"User-Agent": _BROWSER_UA})
        with urllib.request.urlopen(req, timeout=30) as resp:
            d = json.load(resp)
        result = (d.get("chart", {}) or {}).get("result") or []
        if not result:
            return None
        meta = result[0].get("meta", {})
        price = meta.get("regularMarketPrice")
        if price is None:
            return None
        return Fact(label="Price", value=float(price), unit=meta.get("currency", ""),
                    period="실시간(근사)", source=self.name, tier=self.tier,
                    tag="yahoo:regularMarketPrice")


class SECEdgar:
    """SEC EDGAR (T1 공식, 무료, 키 불필요). 미국 상장사 재무.

    https://www.sec.gov/files/company_tickers.json  (ticker→CIK)
    https://data.sec.gov/api/xbrl/companyfacts/CIK{cik}.json
    """
    name = "SEC EDGAR"
    tier = Tier.OFFICIAL

    def __init__(self) -> None:
        self._ticker_map: Optional[dict] = None

    def resolve(self, ticker: str) -> tuple[str, str]:
        """ticker → (CIK 10자리, 회사명)."""
        if self._ticker_map is None:
            self._ticker_map = _get_json("https://www.sec.gov/files/company_tickers.json")
        for row in self._ticker_map.values():
            if row["ticker"].upper() == ticker.upper():
                return f'{int(row["cik_str"]):010d}', row["title"]
        raise ValueError(f"SEC EDGAR에 ticker 없음(미국 상장 아님일 수 있음): {ticker}")

    def _facts(self, cik: str) -> dict:
        return _get_json(f"https://data.sec.gov/api/xbrl/companyfacts/CIK{cik}.json")

    def _latest_annual(self, facts: dict, tags: list[str], unit: str = "USD") -> Optional[Fact]:
        """후보 태그 전체에서 가장 최신(end) 연간(10-K, FY) 값을 고른다.
        (첫 태그에서 멈추면 NVDA처럼 옛 태그의 구값을 잡는 버그가 생김.)"""
        gaap = facts.get("facts", {}).get("us-gaap", {})
        candidates: list[tuple[dict, str]] = []
        for tag in tags:
            units = gaap.get(tag, {}).get("units", {}).get(unit, [])
            for u in units:
                if u.get("form") == "10-K" and u.get("fp") == "FY":
                    candidates.append((u, tag))
        if not candidates:  # 폴백: 아무 10-K
            for tag in tags:
                units = gaap.get(tag, {}).get("units", {}).get(unit, [])
                for u in units:
                    if u.get("form") == "10-K":
                        candidates.append((u, tag))
        if not candidates:
            return None
        u, tag = max(candidates, key=lambda x: x[0].get("end", ""))
        return Fact(label=tag, value=u["val"], unit=unit, period=u.get("end", ""),
                    source=self.name, tier=self.tier, tag=f"us-gaap:{tag}")

    def fundamentals(self, ticker: str) -> dict:
        """핵심 연간 재무 사실 묶음 (T1)."""
        cik, name = self.resolve(ticker)
        facts = self._facts(cik)
        out = {"ticker": ticker.upper(), "company": name, "cik": cik, "facts": []}
        wanted = {
            "Revenue": ["RevenueFromContractWithCustomerExcludingAssessedTax", "Revenues", "SalesRevenueNet"],
            "NetIncome": ["NetIncomeLoss"],
            "Assets": ["Assets"],
            "StockholdersEquity": ["StockholdersEquity"],
        }
        for label, tags in wanted.items():
            f = self._latest_annual(facts, tags)
            if f:
                f.label = label
                out["facts"].append(f)
        return out
