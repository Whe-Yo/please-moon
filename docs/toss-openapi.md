# 토스증권 Open API — 사전 조사 (260622, 공식 출처)

> 출처: 공식 [developers.tossinvest.com](https://developers.tossinvest.com/docs) + `/llms.txt`(AI 에이전트용 스펙). 시점민감 — Claude 라이브 검증.

## 상태
- **사전 신청 단계**(2026, [뉴스 05-21](https://v.daum.net/v/20260521073602305)). 정식 오픈일 미정. 신청자 순차 오픈 → **토스증권 PC 웹에서 API 키 발급**. 대상=토스 계좌 보유자. 국내주식 수수료 면제(~2026.6).

## 스펙 (핵심)
- **Base URL**: `https://openapi.tossinvest.com`
- **인증**: OAuth 2.0 **Client Credentials Grant** → `Authorization: Bearer {access_token}`. 계좌·자산·주문 API엔 `X-Tossinvest-Account` 헤더 추가.
- **카테고리**:
  1. **Auth** — OAuth2 토큰 발급, JWKS
  2. **Market Data** — orderbook · prices · trades · price limits · **candles** ← *우리 핵심*
  3. **Stock Info** — 종목 마스터, 종목 경고
  4. **Market Info** — 환율, KR/US 거래일 캘린더
  5. **Account & Asset** — 계좌·보유
  6. **Order** — 생성/정정/취소/조회/매수여력/매도가능/수수료 ← *우리 미사용(매매 안 함)*
- **시장**: KRX + US.
- **스펙 포맷**: OpenAPI JSON 3.0(authoritative) / OpenAPI **Markdown(LLM용, `/llms.txt`)** / 인터랙티브 레퍼런스. → 에이전트가 Markdown 스펙을 직접 파싱하기 좋음.
- **미확인(공식 발췌엔 없음)**: WebSocket 지원·rate limit·샌드박스 → OpenAPI JSON 원본에서 확인 필요. (블로그는 WebSocket 있다고 하나 공식 미확인.)

## 우리 please-moon 적용
- 필요한 건 **Market Data(prices·candles)** + Stock Info뿐. Order 불필요(정보형, 매매 안 함).
- **키 발급은 사용자**(사전 신청 + PC 웹). 나는 자격증명 입력 안 함 — 키 주면 환경변수로 주입.
- 대기 동안엔 무료 소스(FinanceDataReader 등)로 파이프라인 골격 → 키 나오면 토스 어댑터로 스왑(데이터소스 인터페이스 추상화).
