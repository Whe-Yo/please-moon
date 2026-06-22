# please-moon 🚀 — 주식 분석·정보 에이전트

> 이름: "제발 올라라(to the moon)". [please-work](https://github.com/Whe-Yo/please-work-claude) 가족의 애원 톤을 잇는 **앱**(하네스가 아니라 그 위에서 도는 응용).

조사·분석을 정리하고 **"지켜볼 다음 신호"를 정보 관점에서** 제시하는 에이전트. clemini(Claude×Gemini) 구조 위에서 동작.

> please-work-clemini 개선의 연장 — 조사 비중이 큰 도메인에서 clemini ROI를 검증하는 벤치마크.

## 원칙 (중요)
- **매수·매도 권유 안 함.** 개인화된 투자 조언(비면허)이 아니라 **정보·시나리오·리스크 정리** + 면책.
- **시점민감 사실(가격·상장상태·실적·일정)은 항상 라이브 검증** — Gemini 훈련지식만으론 틀린다(아래 실증).
- 출처 신뢰도 표기(공시·1차 vs 집계·블로그).

## clemini 분담
- **Gemini(agy)**: 넓은 조사 — 사업/밸류에이션 뼈대, 노출 경로, 촉매·리스크·시나리오. 싸고 빠름.
- **Claude**: 시점민감 사실 라이브 검증·교정, 출처 신뢰도 판정, 최종 종합. (매수권유 금지선도 Claude가 지킴.)

## 구조
**데이터 수집 = 결정론적 코드 / 분석·종합 = clemini(LLM).** 설계: [docs/architecture.md](docs/architecture.md).
데이터 소스/도구 벤치마크(글로벌): [docs/data-sources.md](docs/data-sources.md)(신뢰도 등급)·[docs/data-pulling.md](docs/data-pulling.md)(수집 도구).

## 실행 (무키, T1 SEC EDGAR)
```sh
python3 -m please_moon AAPL            # 사실 시트(재무 T1 + 시세)
python3 -m please_moon --report NVDA   # 전체 파이프라인: 사실 + Gemini 1차조사 드래프트
```
키 불필요(EDGAR/Yahoo). 글로벌/US 우선. 실증 산출물 예: [reports/NVDA.md](reports/NVDA.md). 버전: [CHANGELOG.md](CHANGELOG.md).

## 실증
[docs/spacex-3way-comparison.md](docs/spacex-3way-comparison.md) — Claude단독 vs Gemini단독 vs clemini. 결론: **Gemini 단독은 시점민감 사실에 자신 있게 틀린다(SpaceX 2026 IPO 누락). clemini가 정답 구조.**
