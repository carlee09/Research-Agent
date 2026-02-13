# Product Requirements Document (PRD)
## Research Agent

---

## 1. Executive Summary

### Product Name
**Research Agent** - AI-powered research automation and analysis tool

### Vision Statement
리서처들이 자료 수집에 시간을 낭비하지 않고, 핵심 인사이트 도출에 집중할 수 있도록 돕는 CLI 기반 자동화 도구

### Target Users
- 시장 조사 리서처
- 트렌드 분석가
- 학술 연구자
- 콘텐츠 기획자
- 스타트업 창업자 (시장 분석용)

### Key Problem
리서처들은 자료를 많이 수집하지만, 정작 읽고 분석할 시간이 부족하여 수집한 자료가 활용되지 못하는 문제가 있음

### Solution
X(Twitter) 스크래핑과 웹 검색으로 자료를 자동 수집하고, Claude AI가 상세 분석 및 요약을 수행하여 구조화된 Markdown 리포트를 자동 생성

---

## 2. Product Goals

### Primary Goals
1. **자동화된 데이터 수집**: X와 웹에서 관련 정보를 자동으로 수집
2. **상세한 AI 분석**: Claude를 활용한 깊이 있는 분석 및 인사이트 추출
3. **즉시 활용 가능한 결과물**: 읽기 쉬운 Markdown 리포트 생성

### Success Metrics
- 리서치 시간 50% 이상 단축
- 사용자당 주 3회 이상 활용
- GitHub Stars 100+ 달성 (오픈소스 커뮤니티 기여)
- 월 Active Users 500+ (6개월 내)

---

## 3. Technical Specifications

### 3.1 Technology Stack

#### Core
- **Language**: Python 3.9+
- **CLI Framework**: Click
- **AI**: Anthropic Claude API
- **Environment**: python-dotenv

#### Data Collection
- **X Scraping**: 사용자 제공 X API
- **Web Search**: 사용자 제공 웹 서치 API
- **HTTP Client**: requests / httpx

#### Output
- **Format**: Markdown
- **Storage**: Local file system

### 3.2 Project Structure

```
research-agent/
├── README.md                    # 프로젝트 소개 및 사용법
├── LICENSE                      # 오픈소스 라이선스
├── requirements.txt             # Python 의존성
├── setup.py                     # 패키지 설치 스크립트
├── .env.example                 # 환경 변수 템플릿
├── .gitignore
│
├── src/
│   ├── __init__.py
│   ├── main.py                  # CLI 진입점
│   ├── config.py                # 설정 관리
│   │
│   ├── collectors/              # 데이터 수집
│   │   ├── __init__.py
│   │   ├── x_collector.py       # X API 연동
│   │   ├── web_collector.py     # 웹 서치 API 연동
│   │   └── base.py              # Base collector class
│   │
│   ├── analyzers/               # AI 분석
│   │   ├── __init__.py
│   │   ├── claude_analyzer.py   # Claude API 연동
│   │   └── prompt_templates.py  # 프롬프트 템플릿
│   │
│   ├── generators/              # 리포트 생성
│   │   ├── __init__.py
│   │   └── markdown_generator.py
│   │
│   └── utils/                   # 유틸리티
│       ├── __init__.py
│       ├── logger.py            # 로깅
│       └── validators.py        # 입력 검증
│
├── tests/                       # 테스트 코드
│   ├── __init__.py
│   ├── test_collectors.py
│   ├── test_analyzers.py
│   └── test_generators.py
│
└── examples/                    # 예제 및 샘플
    ├── sample_report.md
    └── sample_config.env
```

### 3.3 API Integration

#### Required APIs
1. **AI Models** (최소 1개 필수)
   - **Anthropic Claude API**
     - Model: claude-sonnet-4-20250514
     - Purpose: 텍스트 분석 및 요약
   - **Google Gemini API** (권장)
     - Model: gemini-2.0-flash-exp
     - Purpose: 텍스트 분석 및 요약

2. **Sela Network API** (필수)
   - Purpose: X (Twitter) 및 웹 검색 데이터 수집
   - Endpoint: `https://api.selanetwork.io/api/rpc/scrapeUrl`
   - Supported Scrape Types:
     - `GOOGLE_SEARCH`: Google 검색 결과
     - `TWITTER_PROFILE`: Twitter 프로필 포스트
     - `TWITTER_POST`: 개별 트윗
   - Rate Limit 및 타임아웃 고려 필요
   - 상세 문서: [SELA_API.md](SELA_API.md)

#### Environment Variables
```bash
# AI Models (at least one required)
ANTHROPIC_API_KEY=sk-ant-...
GEMINI_API_KEY=...
DEFAULT_MODEL=gemini

# Sela Network API (required)
SELA_API_KEY=...
SELA_API_ENDPOINT=https://api.selanetwork.io/api/rpc/scrapeUrl
SELA_TIMEOUT_MS=60000
```

---

## 4. Feature Specifications

### 4.1 Core Features (MVP)

#### Feature 1: CLI Interface
```bash
research-agent --topic "주제명" [옵션]
```

**Options:**
- `--topic` (required): 리서치 주제
- `--sources`: 데이터 소스 선택 (x, web, all) [default: all]
- `--max-items`: 수집할 최대 항목 수 [default: 20]
- `--output`: 출력 파일명 [default: research_YYYYMMDD_HHMMSS.md]
- `--depth`: 분석 깊이 (quick, detailed) [default: detailed]

**Examples:**
```bash
# 기본 사용
research-agent --topic "AI agents 2024"

# 상세 옵션
research-agent \
  --topic "Anthropic Claude updates" \
  --sources x,web \
  --max-items 30 \
  --output claude-research.md \
  --depth detailed
```

#### Feature 2: Data Collection

**X Collection:**
- Twitter 프로필 기반 포스트 수집 (TWITTER_PROFILE)
- 주제별 계정 매핑 (예: "uniswap" → @Uniswap)
- 메타데이터 포함 (작성자, 날짜, 좋아요 수 등)
- **참고**: Twitter Search 기능은 없음 - 프로필 스크래핑 사용

**Web Collection:**
- 관련 기사 및 블로그 검색
- 제목, URL, 발췌문 수집
- 출처 신뢰도 고려

#### Feature 3: AI Analysis

**Claude가 수행하는 분석:**
1. **데이터 정제**: 중복 제거, 노이즈 필터링
2. **주제 분류**: 자동 주제별 그룹핑
3. **핵심 인사이트 추출**: 
   - 주요 트렌드 파악
   - 공통 의견/반대 의견 분석
   - 중요 통계/데이터 포인트 식별
4. **맥락화**: 전체적인 흐름과 맥락 설명
5. **종합 요약**: Executive summary 생성

#### Feature 4: Report Generation

**Markdown 리포트 구조:**

```markdown
# [주제명] 리서치 리포트

**생성일시**: YYYY-MM-DD HH:MM:SS
**데이터 소스**: X (15개), Web (12개)
**분석 모델**: Claude Sonnet 4

---

## Executive Summary

[3-5문장으로 핵심 요약]

---

## 주요 인사이트

### 1. [주요 트렌드 1]
- **발견 내용**: ...
- **근거**: ...
- **의미**: ...

### 2. [주요 트렌드 2]
...

---

## 상세 분석

### [주제 카테고리 1]

#### 핵심 내용
[상세 분석 내용]

#### 주요 출처
- [출처 1]: [요약]
- [출처 2]: [요약]

### [주제 카테고리 2]
...

---

## 의견 분석

### 주류 의견
[분석 내용]

### 반대 의견
[분석 내용]

---

## 데이터 출처

### X (Twitter)
1. [@사용자명] - [트윗 내용] - [날짜] - [링크]
2. ...

### Web
1. [제목] - [출처] - [날짜] - [URL]
2. ...

---

## 결론 및 제언

[종합 결론 및 다음 단계 제안]
```

### 4.2 Future Features (Post-MVP)

#### Phase 2 (3개월 내)
- **정기 실행 스케줄러**: cron 통합으로 자동화
- **변화 추적**: 이전 리포트와 비교 분석
- **다중 포맷 지원**: PDF, HTML 출력

#### Phase 3 (6개월 내)
- **대화형 모드**: 추가 질문으로 심화 분석
- **시각화**: 차트 및 그래프 자동 생성
- **협업 기능**: 팀 공유 및 댓글

---

## 5. User Experience

### 5.1 User Journey

1. **설치**
   ```bash
   pip install research-agent
   # 또는
   git clone https://github.com/[username]/research-agent
   cd research-agent
   pip install -e .
   ```

2. **설정**
   ```bash
   cp .env.example .env
   # .env 파일에 API 키 입력
   ```

3. **실행**
   ```bash
   research-agent --topic "관심 주제"
   ```

4. **결과 확인**
   - 터미널에 진행 상황 표시
   - 완료 후 파일 경로 출력
   - Markdown 뷰어로 리포트 열람

### 5.2 Expected User Flow

```
사용자 → 주제 입력 → [수집 중...] → [분석 중...] → [리포트 생성 중...] → 완료 ✓
         (5초)        (30초)         (60초)           (10초)              
```

**진행 상황 표시:**
```
🔍 Collecting data from X... (15/20)
🌐 Collecting data from Web... (12/20)
🤖 Analyzing with Claude AI... (Processing 27 items)
📝 Generating report...
✅ Report saved: research_20250212_143022.md
```

---

## 6. Technical Requirements

### 6.1 Performance Requirements
- **수집 속도**: 20개 항목 기준 < 1분
- **분석 속도**: 20개 항목 기준 < 2분
- **총 실행 시간**: < 5분 (일반적인 케이스)
- **메모리 사용**: < 500MB

### 6.2 Reliability Requirements
- **API 오류 처리**: Retry 로직 (최대 3회)
- **부분 실패 허용**: 일부 소스 실패 시에도 진행
- **Rate Limit 관리**: 자동 백오프
- **로깅**: 모든 오류 및 경고 기록

### 6.3 Scalability Requirements
- **동시 실행**: 5개 프로세스까지 지원
- **데이터 크기**: 최대 100개 항목 처리 가능
- **출력 파일**: 최대 10MB

---

## 7. Quality Assurance

### 7.1 Testing Strategy

#### Unit Tests
- 각 collector 모듈
- Claude analyzer
- Report generator
- Utility functions

#### Integration Tests
- End-to-end 워크플로우
- API 연동 테스트 (mocking)

#### Manual Tests
- 다양한 주제로 실제 실행
- 리포트 품질 평가
- 오류 시나리오 테스트

### 7.2 Code Quality
- **Linting**: flake8, black
- **Type Hints**: mypy
- **Documentation**: Docstrings for all public functions
- **Coverage**: > 80%

---

## 8. Documentation

### 8.1 User Documentation
- **README.md**: 
  - 프로젝트 소개
  - 빠른 시작 가이드
  - 사용 예제
  - FAQ
- **CONTRIBUTING.md**: 기여 가이드라인
- **CHANGELOG.md**: 버전별 변경 사항

### 8.2 Developer Documentation
- **API Documentation**: 각 모듈 및 함수 설명
- **Architecture Guide**: 시스템 아키텍처 다이어그램
- **Setup Guide**: 개발 환경 구축

---

## 9. Deployment & Distribution

### 9.1 Release Strategy

#### v0.1.0 (MVP)
- 기본 CLI 기능
- X + Web 수집
- Claude 분석
- Markdown 리포트

#### v0.2.0
- 오류 처리 개선
- 설정 파일 지원
- 진행 상황 표시 개선

#### v0.3.0
- 테스트 커버리지 80%+
- 성능 최적화
- 문서화 완성

#### v1.0.0
- Production-ready
- PyPI 배포

### 9.2 Distribution Channels
1. **GitHub Repository**: 소스 코드 공개
2. **PyPI**: `pip install research-agent`
3. **Docker Hub**: 컨테이너 이미지 (선택)

---

## 10. Risks & Mitigation

### Risk 1: API Rate Limits
- **Risk**: X/Web API 호출 제한으로 데이터 수집 실패
- **Mitigation**: 
  - Rate limit 모니터링
  - 자동 백오프 구현
  - 사용자에게 제한 안내

### Risk 2: API 비용
- **Risk**: Claude API 비용 과다
- **Mitigation**:
  - 효율적인 프롬프트 설계
  - 토큰 사용량 모니터링
  - 사용자에게 비용 안내

### Risk 3: 데이터 품질
- **Risk**: 수집된 데이터가 저품질이거나 관련 없음
- **Mitigation**:
  - 필터링 로직 강화
  - Claude의 관련성 평가
  - 사용자 피드백 반영

### Risk 4: 법적 이슈
- **Risk**: 웹 스크래핑 관련 저작권/이용약관 문제
- **Mitigation**:
  - 공식 API만 사용
  - 출처 명시
  - Fair Use 준수

---

## 11. Success Criteria

### Launch Criteria (v1.0.0)
- [ ] 모든 핵심 기능 구현 완료
- [ ] 테스트 커버리지 80% 이상
- [ ] 문서화 완성
- [ ] 5명 이상의 베타 테스터 피드백 반영
- [ ] 주요 버그 0건

### 6개월 목표
- [ ] GitHub Stars 100+
- [ ] Monthly Active Users 500+
- [ ] 커뮤니티 컨트리뷰터 10+
- [ ] 사용자 만족도 4.5/5.0 이상

---

## 12. Timeline

### Phase 1: Development (4주)
- Week 1: 프로젝트 셋업, 기본 구조
- Week 2: Data collectors 구현
- Week 3: Claude analyzer 구현
- Week 4: Report generator, CLI 완성

### Phase 2: Testing & Refinement (2주)
- Week 5: 테스트 작성, 버그 수정
- Week 6: 문서화, 코드 정리

### Phase 3: Beta Release (1주)
- Week 7: 베타 테스터 모집 및 피드백 수집

### Phase 4: Public Release (1주)
- Week 8: v1.0.0 릴리스, GitHub 공개, 커뮤니티 홍보

**총 소요 기간**: 8주

---

## 13. Appendix

### A. Example Use Cases

#### Use Case 1: 스타트업 시장 조사
```bash
research-agent --topic "AI coding assistants market 2024" \
  --sources all \
  --max-items 30
```
**결과**: 시장 트렌드, 경쟁사 분석, 사용자 반응 종합 리포트

#### Use Case 2: 학술 연구
```bash
research-agent --topic "Large Language Models safety" \
  --sources web \
  --max-items 50 \
  --depth detailed
```
**결과**: 최신 논문, 연구 동향, 핵심 발견 요약

#### Use Case 3: 트렌드 분석
```bash
research-agent --topic "sustainable fashion trends" \
  --sources x \
  --max-items 40
```
**결과**: 소셜 미디어 반응, 인플루언서 의견, 소비자 트렌드

### B. Glossary

- **Research Agent**: 본 프로젝트의 명칭
- **Collector**: 데이터 수집 모듈
- **Analyzer**: AI 분석 모듈
- **Generator**: 리포트 생성 모듈
- **CLI**: Command Line Interface
- **MVP**: Minimum Viable Product

### C. References

- Anthropic Claude API Documentation: https://docs.anthropic.com
- Click Documentation: https://click.palletsprojects.com/
- Markdown Guide: https://www.markdownguide.org/

---

## Document History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2025-02-12 | [Your Name] | Initial PRD creation |

---

**Last Updated**: 2025-02-12
**Status**: Draft - Ready for Review
**Next Review**: 2025-02-19
