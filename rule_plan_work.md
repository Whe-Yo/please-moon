# please-moon — RPW

## Rule
**Always do**: 시점민감 사실(가격·상장상태·실적·일정)은 Claude 라이브 검증. 출처 신뢰도 표기. clemini 분담(조사=Gemini, 검증·종합=Claude).
**Ask first**: 외부 데이터 API 연동(키 필요), 자동 실행/스케줄링 도입.
**Never do**: 매수·매도 등 개인화 투자 권유. 매매·송금 실행. Gemini 훈련지식만으로 시점민감 사실 단정.

## Plan
목표: clemini 기반 주식 정보·분석 에이전트(정보 정리형, 권유 아님).
- [x] 3-way 비교(SpaceX)로 구조 결정 — clemini 필수 확인 ([docs](docs/spacex-3way-comparison.md))
- [ ] 분석 파이프라인 정의: (1) Gemini 조사 뼈대 → (2) Claude 라이브 검증·교정 → (3) 정보 리포트(신호·시나리오·리스크+면책)
- [ ] 입력 형식(종목/주제) + 출력 템플릿 확정
- [ ] 데이터 소스 전략(공시·1차 우선, 라이브 검증 경로)

## Work
**260622 착수.** 3-way 비교 완료 — 핵심: 주식처럼 시점민감 도메인에선 Gemini 단독이 위험(SpaceX 2026 IPO 누락, 비상장으로 단정). clemini(Gemini breadth + Claude 라이브 검증)가 정답 구조, Claude-light로 최고 ROI. 다음: 파이프라인·출력 템플릿 정의.

### 결정 기록
- WHAT: 에이전트를 clemini 구조 + "정보 정리형(권유 아님)"으로. WHY: 시점민감 사실 검증 필수(실증) + 개인화 투자조언은 비면허 금지선. REJECTED: Gemini 단독(자신 있게 틀림), 매수/매도 추천형(규정 위반).
