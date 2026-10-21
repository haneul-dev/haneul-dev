### 안녕하세요, 강하늘입니다

단국대학교 소프트웨어학과에 다니고 있고(2027년 2월 졸업 예정), 백엔드와 LLM 서빙 쪽을 공부하고 있습니다.

저는 "빨라졌어요"보다 **"1.75초에서 1.30초가 됐어요"** 라고 말하는 쪽을 좋아합니다.
그래서 뭘 만들든 측정 코드부터 붙여놓고 시작하는 편이에요.
요즘은 RAG 파이프라인에서 근거를 꼼꼼하게 해석할수록 응답이 느려지는 문제를 붙잡고 있습니다.

<br>

### 지금 하고 있는 것

**멀티모달 RAG — 계층형 근거 해석 디코더** · 연구실 프로젝트 · [`Multimodal_specialization_LLM`](https://github.com/haneul-dev/Multimodal_specialization_LLM/tree/haneul)

검색된 텍스트·이미지·오디오 근거를 LLM에 통째로 넣지 않고, 모달별로 핵심만 뽑아서 합친 다음 최종 답변 모델에 넘기는 구조를 맡고 있습니다.
LLM 모델을 고를 때도 감으로 정하지 않고 직접 재봤습니다.

| 후보 | 평균 응답 | 지시 준수 |
|---|---|---|
| solar-mini | 5.89s | 출력 형식 위반 |
| solar-pro2 | 1.75s | O |
| **solar-pro3** | **1.30s** | O (json_schema strict 지원 → 파싱 재시도 0회) |

솔직히 아직 숙제가 남아 있습니다. LLM을 1번 부르는 베이스라인이 1,030ms인데, 제가 만든 구조는 4번 불러서 4,401ms(+327%)가 나옵니다.
이 격차를 줄이는 게 지금 제 연구 목표이고, `raw / no-integ / bypass / full` 4개 비교군으로 어디서 시간이 새는지 쪼개 보고 있어요.

**RECRAG 생성 모듈 (Step 8~9)** · [`recrag-generation-module`](https://github.com/haneul-dev/recrag-generation-module)

앞단에서 검색·재정렬된 문서를 받아 Qwen2.5-7B-Instruct로 근거 기반 설명을 만드는 모듈입니다.
답변마다 참조한 Chunk ID와 Groundedness Note를 같이 내보내고, 생성 latency를 `t0~t5` 구간으로 나눠서 JSONL/CSV로 남기도록 했습니다.
"어느 단계가 느린지"를 나중에 다시 묻지 않아도 되게 하는 게 목표였어요.

<br>

### 만든 것들

**🎪 단짠 (DANZZAN) — 대학 축제 통합 플랫폼** · 캡스톤 · 4인 · [`DKU-Dan-Zzan`](https://github.com/DKU-Dan-Zzan)

인스타, 에브리타임, 구글폼, 현장 명단으로 흩어져 있던 축제 정보를 하나로 모은 서비스입니다. 티켓팅 대기열, 부스맵, 공지 기능이 들어가 있어요.
`React` `Spring Boot` `Redis` `Kafka` `NHN Cloud` `AWS RDS/S3`

- PWA 설정과 안드로이드 아이콘·스플래시 이슈를 맡아서 고쳤습니다. 기기마다 다르게 보이는 문제라 몇 번 되돌리면서 잡았어요.
- 프론트 CI/CD에 카카오맵·Mapbox 환경변수가 빌드 때 주입되지 않던 문제를 해결했습니다.
- 휴식기 동안 AWS 자원을 전부 내렸다가 다시 개발을 시작할 때, 개발/운영 환경 구조와 세팅 순서를 문서로 정리해서 팀원들이 각자 로컬에서 바로 시작할 수 있게 했습니다.

**🛡️ npm Hallucination Detector** · 인공지능 보안 프로젝트 · [`repo`](https://github.com/haneul-dev/npm-hallucination-detector) · [라이브 데모](https://npm-hallucination-detector-gp9gffw4vvohhjqwj6gvbn.streamlit.app)

LLM이 존재하지 않는 패키지명을 그럴듯하게 추천하면, 공격자가 그 이름을 선점해서 악성 패키지를 올려두는 공격(슬롭스쿼팅)이 있습니다.
이걸 `npm install` 하기 **전에** 잡아내는 위험도 평가기를 만들었어요.

- 이름 유사도, 메타데이터 등 9개 요소로 0~100점 위험도를 계산하고, 점수마다 근거를 추적할 수 있게 했습니다.
- v1부터 v3c까지 5번 고쳐가며 **Precision 1.000 / False Positive Rate 0.000** 까지 끌어올렸습니다.
- AI 도구를 많이 썼는데, 제안을 그대로 받지 않고 검증 → 수정 → 기각한 사례를 README에 따로 기록해뒀습니다.

**🏠 RENTREE — 대학생 전용 안전 중고거래** · 백엔드 리드

같은 학교 학생끼리만 거래하는 위치 기반 중고거래 플랫폼입니다.
DB의 `CASCADE/RESTRICT` 제약 때문에 걸리던 락을 걷어내고 JPA 레벨에서 처리하도록 바꿔서 **API 응답 시간을 약 7배 줄였습니다.**

**그 외**

- **개인 일기 iOS 앱** — Flutter + Spring Boot로 만들어 App Store에 배포까지 했습니다. 디자인부터 사용자 피드백 반영까지 혼자 끝까지 가본 첫 경험이에요.
- **AI 카드 추천 앱** — 거래 내역을 분석해서 소비 패턴에 맞는 카드를 추천합니다.
- **RunPT** — TABA 팀 프로젝트 백엔드 ([`RunPT-BE`](https://github.com/haneul-dev/RunPT-BE))

<br>

### 제가 일하는 방식

- **숫자로 고르고, 숫자로 설명합니다.** 모델 하나, 쿼리 하나를 바꿔도 전후를 재서 남겨둡니다.
- **AI가 쓴 코드도 제 코드처럼 검증합니다.** 돌아가는 것과 맞는 것은 다르다고 생각해요.
- **남이 이어받을 수 있게 남깁니다.** 세팅 문서, 실험 config, README를 귀찮아도 씁니다. 다음 사람이 저한테 물어보지 않아도 되게요.
- **쉽게 설명할 수 있어야 제대로 아는 거라고 믿습니다.** CJ올리브네트웍스 교육 멘토로 2기 연속 활동하면서 코딩을 처음 접하는 학생들을 가르쳤고, 동아리에서는 코딩테스트 스터디를 이끌었습니다.

<br>

### 기술

```
주로 씁니다     Java · Spring Boot · JPA · Python
써봤습니다      React · Flutter · MySQL · Redis · Kafka · Docker · AWS(RDS, S3) · NHN Cloud
LLM / RAG       Qwen2.5 · Upstage Solar · Gemini API · Streamlit
```

<br>

### 그 밖의 경험

- CJ ENM 전략기획 인턴 — 사용자 반응 데이터를 분석해서 서비스 기획안으로 만드는 일을 했습니다.
- IT 동아리 운영진 2년 · 코딩테스트 스터디 리더
- 앱 개발 경진 우수상
- 베트남 다낭 해외 교육봉사
- 소프트웨어 전공과 함께 영문학 과목을 공부했습니다. 그래서 그런지 문서 쓰는 걸 꽤 좋아합니다.

<br>

<sub>금융 IT · 백엔드 · AI 엔지니어링 포지션을 찾고 있습니다. 이야기 나눠보고 싶으시면 편하게 연락 주세요.</sub>
