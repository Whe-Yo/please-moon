# 아키텍처 — please-moon

## 핵심 분리 (설계 철학)
**데이터 수집 = 결정론적 코드 / 분석·종합 = clemini(LLM).**
- 코드가 해야 할 것(검증 가능·반복): 시세·재무·공시 **수집**, 출처 **Tier 태깅**, 사실 시트 **조립**.
- LLM(clemini)이 해야 할 것(판단·서사): 밸류에이션·시나리오·반론·"지켜볼 신호" 종합. 시점민감 사실은 **Claude 라이브 검증**.

이 분리로 ① 사실은 틀리지 않고(코드+T1 공시) ② 분석은 유연하며 ③ LLM 토큰을 사실 재계산에 낭비하지 않는다.

## 파이프라인
```
TICKER/테마
  │
  ├─[코드] 수집: SourceAdapter들 → Fact(값·기간·source·Tier)   ← 결정론적
  │        (SEC EDGAR=T1 / Twelve Data·Finnhub=T2~3 / FRED 매크로)
  │
  ├─[코드] 조립: fact_sheet() — 출처 등급 표기 + 면책
  │
  ├─[clemini] 조사: Gemini가 넓은 정성 리서치(촉매·경쟁·서사)  ← 토큰 볼륨
  │
  ├─[Claude] 검증·종합: 시점민감 사실 라이브 대조 + 시나리오(Bull/Base/Bear)·반론·신호
  │
  └─ 리포트: 사실(코드) + 분석(clemini) + 면책
```

## 소스 추상화 (`please_moon/sources.py`)
- `Tier(IntEnum)`: T1 OFFICIAL → T4 SPECULATIVE.
- `Fact`: label·value·unit·period·source·tier·tag — 모든 수치는 등급·출처를 달고 다닌다.
- `SECEdgar`: **구현 완료**(무키, ticker→CIK→companyfacts, 연간 핵심 재무). T1.
- 확장 지점: `TwelveData`, `Finnhub`, `FRED`, `OpenBB`(집계 백본) 어댑터를 같은 인터페이스로 추가 → provider 교체에 코드 불변.

## 가드레일
- **매수·매도 권유 금지**(정보형). 출력 면책 고정([report.py](../please_moon/report.py)의 `DISCLAIMER`).
- 사실 충돌 시 **T1 우선**(덮어쓰기). 한국 K-IFRS는 글로벌 GAAP 스키마와 매핑 불일치 → 필요시 DART 별도(글로벌 우선이라 후순위).

## 현재 상태 / 로드맵
- [x] **v0.1**: 데이터 레이어 동작 — SEC EDGAR(T1)로 실제 재무 수집·사실 시트(AAPL/MSFT 검증).
- [ ] OpenBB 백본 + Twelve Data/Finnhub/FRED 어댑터(무료 글로벌 시세·뉴스·매크로).
- [ ] clemini 분석 레이어 자동화(Gemini API 조사 + Claude 검증) — 현재는 수동 clemini.
- [ ] 테마 스크리너(다종목 배치 = Gemini 토큰 볼륨).
