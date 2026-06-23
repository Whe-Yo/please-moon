# Changelog

[Keep a Changelog] / [SemVer] 지향. 프로토타입이라 0.x.

## [Unreleased]
- **키 기반 어댑터 추가**: `TwelveData`·`Finnhub`(시세, T2)·`Fred`(거시, T1). clemini 병렬 팬아웃으로 3개 동시 프로토타입 → 격리 워크스페이스 → Claude 검토·적용. 무키 graceful(None) 검증, 회귀 없음. **런타임 검증은 키 발급 후.**

## [0.2.0] - 260622
### Added
- **분석 파이프라인** (`pipeline.py`): 코드 사실수집 → clemini(agy 최신 Pro) 1차조사 위임 → 드래프트 조립. CLI `python -m please_moon --report TICKER`.
- **시세 어댑터** (`YahooChart`, 무키·글로벌, T3 비공식).
- **실증**: [reports/NVDA.md](reports/NVDA.md) — 전체 루프(코드+Gemini+Claude) 산출물.
### Fixed
- 재무 태그 선택 버그: 첫 태그에서 멈춰 옛 구값(NVDA 2022)을 잡던 것 → **후보 태그 전체에서 최신 end** 선택.
### Notes
- Stooq 무키 CSV는 JS proof-of-work로 차단 확인. 신뢰 시세는 키 기반(Twelve Data/Finnhub) 어댑터 예정.

## [0.1.0] - 260622
### Added
- **데이터 레이어**: `SECEdgar`(T1 재무, 무키) + 소스 추상화(`Tier`/`Fact`) + 사실 시트(`report.py`). CLI `python -m please_moon TICKER`.
- **문서**: 아키텍처, 신뢰도 등급, 글로벌 수집 도구 벤치마크, SpaceX 3-way 비교·분석, 토스 API 조사.
