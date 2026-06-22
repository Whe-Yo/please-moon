# API 키 발급·설정 (사용자가 직접)

> 키 발급은 계정 가입이 필요해 **사용자가 직접** 한다(에이전트는 계정 생성·자격증명 입력 안 함). 다 **무료 티어**(카드 불필요).

## 보안
- 이 키들은 **읽기 전용 시세·데이터** 키 — 돈·매매·개인정보 접근 없음. 유출 위험 낮음(최악=무료 쿼터 소모).
- **채팅에 붙이지 말 것.** `.env`에만 넣는다(`GITHUB_PAT`과 동일 패턴). `.env`는 gitignore됨 → 커밋 안 됨. 에이전트는 `source`만 하고 값은 보지·출력하지 않음.

## 발급 (각 ~2분)
| 소스 | 사이트 | 용도 |
|---|---|---|
| **Twelve Data** | twelvedata.com | 글로벌 시세(무료 800콜/일) |
| **Finnhub** | finnhub.io | 뉴스·감성·내부자(무료 60콜/분) |
| **FRED** | fred.stlouisfed.org → API Keys | 매크로(금리·CPI 등, 무료) |

## 설정
`.env`(예: `/Volumes/Wheyo/.env`)에 이 변수명 그대로 추가:
```
TWELVEDATA_API_KEY=...
FINNHUB_API_KEY=...
FRED_API_KEY=...
```
그 후 "됐어" → 에이전트가 어댑터 작성·테스트(값 노출 없이) 후 please-moon에 연동.

## 코드 측 (참고)
어댑터는 `os.environ["TWELVEDATA_API_KEY"]` 식으로 읽고, 키 없으면 graceful skip(무키 EDGAR/Yahoo로 동작 유지).
