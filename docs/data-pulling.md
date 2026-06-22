# 글로벌 주식 데이터 수집 도구 벤치마크 (실전)

> 글로벌/US 우선. 방법: Gemini 지형 오프로드 + Claude 시점민감 specs 라이브 검증(폐지·무료한도 변경 포함). reliability 등급은 [data-sources.md](data-sources.md).

## 추천 한 줄
**OpenBB Platform(집계 백본) + Twelve Data/Finnhub(무료 글로벌 시세·뉴스) + FRED(매크로) + SEC EDGAR(US 재무) + OpenBB MCP(에이전트)**. 신뢰 글로벌 보강이 필요하면 EODHD(~$20/mo) 추가.

## 무료/저가 글로벌 API (검증된 2026 현황)
| API | 무료 한도 | 커버리지 | 데이터 | 메모 |
|---|---|---|---|---|
| **Twelve Data** | **800콜/일**(최관대) | 50+ 글로벌 거래소 | 시세·130+ 지표 | 무료 글로벌 breadth 1순위 |
| **Finnhub** | 60콜/분 | 글로벌 | 시세(무료=20분지연)·**뉴스·감성·내부자·의원거래** | 뉴스/대체데이터 강함 |
| **Polygon** | 1년 히스토리만 | US 중심 | 시세·재무 | 실시간·장기=유료 |
| **Alpha Vantage** | **25콜/일**(과거 500→축소) | 글로벌(US중심) | 시세·재무·지표 | 너무 빡빡, 백업용 |
| **FMP** | 제한적 무료 | US 최적 | SEC 파싱 표준 재무제표 | US 펀더멘털 |
| **EODHD** | ~$20/mo(저가 유료) | **글로벌 EOD 광범위** | 시세·재무 | 신뢰 글로벌 보강의 가성비 |

## 집계기·라이브러리
- **OpenBB Platform (오픈소스)** — 다수 provider를 **표준 스키마**로 래핑. provider 교체해도 코드 거의 안 바뀜. 에이전트 백본으로 최적. **추천.**
- **yfinance** — 무료·간편하나 ⚠️ Yahoo 공식 API는 폐지됐고 **비공식 엔드포인트는 자주 깨짐**(프로덕션 부적합). 빠른 개발/프로토타입용만.
- (pykrx/FinanceDataReader — 한국 보조용.)

## LLM 에이전트 친화
- **OpenBB MCP Server** — 위 수집 파이프라인을 그대로 자연어 질의로. please-moon 에이전트에 직결.
- **표준 스키마(OpenBB)** — LLM이 일관된 필드로 받아 토큰·매핑 비용↓.

## 뉴스·대체데이터 (글로벌)
- **FRED** — 연준 80만+ 거시지표(금리·CPI·실업·장단기차). **완전 무료**, 매크로 필수.
- **Finnhub** — 뉴스+감성+내부자.
- **Stocktwits** — 리테일 소셜 버즈/심리(밈주 쏠림). *심리지표로만*(T4, 사실 아님).

## ⚠️ 검증된 정정 (시점민감)
- **IEX Cloud = 2024-08-31 폐지.** 쓰지 말 것.
- **Yahoo 공식 API 폐지** → yfinance 비공식은 불안정.
- **Alpha Vantage 무료 = 25콜/일** (대폭 축소).
- 2026년 "완벽한 무료 글로벌 API는 없음" — 신뢰 글로벌 프로덕션은 결국 저가 유료(EODHD/Twelve Data/Polygon 유료).

## please-moon 적용
- **백본**: OpenBB Platform — provider 자유 교체 + MCP로 에이전트화.
- **무료 시작**: Twelve Data(글로벌 시세) + Finnhub(뉴스·감성) + FRED(매크로) + SEC EDGAR(US 재무).
- **유료 보강**: EODHD(글로벌 EOD 신뢰).
- 사실은 **항상 Claude 라이브 검증**(T1 공시 대조). 한국은 보조(필요시 DART 별도).
