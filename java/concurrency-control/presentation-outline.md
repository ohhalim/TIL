# 동시성 제어와 자바 스레드 - 발표 자료 목차

> **실제 프로젝트에서 마주친 동시성 문제를 해결하며 배운 것들**

---

## 📋 발표 개요
- **주제**: 동시성 제어의 원리와 실무 적용
- **목표**: 스레드, 프로세스, 동시성 제어에 대한 깊은 이해
- **발표 시간**: 30-40분 예상

---

## 🎯 발표 목차 (기승전결 구조)

### 1부: 기(起) - 문제의 발견 (5-7분)

#### 1.1 실제 상황 재연
```
💡 "1000명이 동시에 댓글 좋아요를 누른다면?"
```

**슬라이드 1: 타이틀**
- 동시성 제어와 자바 스레드
- 부제: 실무에서 마주친 Race Condition 해결기

**슬라이드 2: 문제 상황 소개**
- 커뮤니티 서비스 댓글 좋아요 기능
- 동시에 1000명의 사용자가 좋아요 클릭
- 예상: 1000개의 좋아요
- 실제: ??? (동시성 문제 발생)

**슬라이드 3: 실제 코드 - Before**
```java
// 일반적인 좋아요 로직 (문제 있는 코드)
public void toggleCommentLike(Long commentId, Long userId) {
    CommunityCommentEntity comment = commentRepository.findById(commentId);
    comment.incrementLikeCount(); // 여기서 문제 발생!
    commentRepository.save(comment);
}
```

**슬라이드 4: 왜 문제가 발생했을까?**
- 동시성(Concurrency)이란 무엇인가?
- Race Condition의 정의
- 이 문제를 해결하려면 무엇을 알아야 할까?

---

### 2부: 승(承) - 원리의 이해 (15-18분)

#### 2.1 스레드와 프로세스의 기본 개념

**슬라이드 5: 프로세스 vs 스레드**
```
🏠 집으로 비유하기
- 프로세스: 한 가구/세대 (독립된 메모리 공간)
- 스레드: 세대원 (같은 공간 공유)
- Stack: 개인 방 (스레드 별 작업 공간)
- Heap: 거실, 주방 (공유 공간)
```

**슬라이드 6: 프로세스의 특징**
- 독립된 메모리 공간 (Code, Data, Heap, Stack)
- 다른 프로세스의 메모리 침범 불가
- 생성/전환 비용이 높음 (무거움)
- 프로세스 간 통신(IPC) 필요

**슬라이드 7: 스레드의 특징**
- 프로세스 내의 실행 단위 (가장 작은 작업 단위)
- Code, Data, Heap 영역 공유
- Stack만 독립적으로 보유
- 생성/전환 비용이 낮음 (가벼움)
- 자원 공유로 인한 효율성 ↑, 동기화 이슈 ↑

**슬라이드 8: 스레드의 존재 이유**
```
Q: 왜 스레드를 사용할까?
A: 여러 일을 동시에 처리하기 위해 → 효율 극대화

• 스레드가 1개: 한 번에 한 가지 일만 가능
• 스레드가 N개: 동시에 N개의 작업 처리 가능
```

#### 2.2 OS 스레드 vs 자바 스레드

**슬라이드 9: OS 스레드**
- OS(운영체제) 레벨에서 관리되는 스레드
- OS마다 생성/제어 방식이 다름
- 하드웨어와 직접 상호작용
- 스케줄러가 실행 순서 결정

**슬라이드 10: 자바 스레드**
- JVM에 의해 관리되는 스레드
- OS 스레드의 추상화 레이어
- 플랫폼 독립적 (Write Once, Run Anywhere)

**슬라이드 11: 자바 스레드의 동작 방식**
```
Java Code: new Thread() 호출
    ↓
JVM: OS에게 스레드 생성 요청
    ↓
OS: Native Thread 생성
    ↓
JVM: Java Thread ↔ OS Thread 매핑 (1:1)
```

#### 2.3 스레드의 생명주기

**슬라이드 12: Thread Lifecycle**
```
NEW → RUNNABLE → RUNNING → WAITING/BLOCKED → TERMINATED
```

**슬라이드 13: 각 상태 상세 설명**
1. **NEW**: Thread 객체 생성, 아직 시작 전
2. **RUNNABLE**: start() 호출, 실행 대기 중
3. **RUNNING**: 실제로 CPU를 할당받아 실행 중
4. **WAITING/BLOCKED**:
   - WAITING: wait(), join() 호출
   - BLOCKED: Lock 획득 대기
5. **TERMINATED**: 실행 완료 또는 종료

**슬라이드 14: 스케줄러의 역할**
- 어떤 스레드를 언제 실행할지 결정
- 개발자는 실행 순서를 제어할 수 없음
- ⚠️ **중요**: 어떤 순서로 실행되더라도 문제없도록 방어적 코드 작성 필요

#### 2.4 공유 자원과 동시성 문제

**슬라이드 15: 공유 자원이란?**
```
독립 자원: Stack (스레드별 개인 방)
공유 자원: Heap (거실, 주방)

동시성 문제의 핵심:
"여러 스레드가 동시에 같은 공유 자원을 수정하려고 경쟁"
```

**슬라이드 16: Race Condition 발생 과정**
```
시간축 →
Thread 1: READ(count=0) → +1 → WRITE(count=1)
Thread 2:      READ(count=0) → +1 → WRITE(count=1)

예상 결과: count=2
실제 결과: count=1 ❌
```

**슬라이드 17: 동시성 문제의 두 가지 유형**

1. **원자성(Atomicity) 문제**
   - 여러 단계의 연산이 중간에 끊김
   - 읽기-수정-쓰기 과정이 원자적이지 않음

2. **가시성(Visibility) 문제**
   - CPU 캐시와 메인 메모리 간 동기화 문제
   - 한 스레드의 변경이 다른 스레드에게 보이지 않음

**슬라이드 18: TV 리모컨 비유**
```
🏠 집안의 TV 리모컨 전쟁

문제:
- 경쟁 상황: 여러 사람이 동시에 TV 조작
- 동기화 이슈: 채널이 꼬이거나 의도와 다른 결과

해결:
- 락(Lock): TV 리모컨은 한 번에 한 사람만!
```

---

### 3부: 전(轉) - 해결의 방법 (10-12분)

#### 3.1 자바에서의 동시성 제어 방법

**슬라이드 19: 동시성 제어 전략 개요**
```
1️⃣ 메모리 레벨 제어 (Application Level)
   - synchronized
   - Lock (ReentrantLock)
   - volatile
   - Concurrent Collections

2️⃣ 데이터베이스 레벨 제어 (DB Level)
   - Transaction
   - Pessimistic Lock (비관적 락)
   - Optimistic Lock (낙관적 락)
```

**슬라이드 20: 메모리 레벨 제어**

1. **synchronized**
   ```java
   public synchronized void increment() {
       count++;
   }
   ```
   - 가장 기본적인 동기화 방법
   - 메서드/블록 단위 Lock

2. **volatile**
   ```java
   private volatile boolean flag = false;
   ```
   - 가시성 문제 해결
   - CPU 캐시가 아닌 메인 메모리에서 직접 읽기/쓰기

3. **Concurrent Collections**
   ```java
   ConcurrentHashMap, AtomicInteger 등
   ```

**슬라이드 21: 데이터베이스 레벨 제어 - 비관적 락**

```java
// Repository
@Lock(LockModeType.PESSIMISTIC_WRITE)
@Query("SELECT c FROM CommunityCommentEntity c WHERE c.commentId = :commentId")
Optional<CommunityCommentEntity> findByIdWithPessimisticLock(@Param("commentId") Long commentId);
```

**동작 원리:**
- SELECT ... FOR UPDATE
- 트랜잭션이 끝날 때까지 다른 트랜잭션은 대기
- 충돌이 자주 발생할 것으로 예상될 때 사용

**슬라이드 22: 낙관적 락 vs 비관적 락**

| 구분 | 낙관적 락 | 비관적 락 |
|------|----------|----------|
| 가정 | 충돌이 드물다 | 충돌이 자주 발생 |
| 방식 | Version 체크 | DB Lock |
| 성능 | 읽기 성능 우수 | 쓰기 정합성 우수 |
| 실패 시 | 재시도 필요 | 대기 후 처리 |

#### 3.2 실제 구현 코드 분석

**슬라이드 23: 해결된 코드 - After**

```java
@Transactional
public void toggleCommentLike(Long commentId, Long userId) {
    // 비관적 락으로 댓글 조회
    CommunityCommentEntity comment = commentRepository
        .findByIdWithPessimisticLock(commentId)
        .orElseThrow();

    // 좋아요 토글 로직
    if (commentLikeRepository.existsByCommentAndUser(comment, user)) {
        // 좋아요 취소
        comment.decrementLikeCount();
        commentLikeRepository.delete(commentLike);
    } else {
        // 좋아요 추가
        comment.incrementLikeCount();
        commentLikeRepository.save(new CommentLike(comment, user));
    }
}
```

**슬라이드 24: 동시성 테스트 코드 구조**

```java
// 1. ExecutorService: 스레드 풀 생성
ExecutorService executorService = Executors.newFixedThreadPool(32);

// 2. CountDownLatch: 스레드 동기화
CountDownLatch latch = new CountDownLatch(1000);

// 3. AtomicInteger: 원자적 카운터
AtomicInteger successCount = new AtomicInteger(0);

// 4. 1000개의 동시 요청 시뮬레이션
for (int i = 0; i < 1000; i++) {
    executorService.submit(() -> {
        try {
            countService.toggleCommentLike(commentId, userId);
            successCount.incrementAndGet();
        } finally {
            latch.countDown();
        }
    });
}

// 5. 모든 스레드 완료 대기
latch.await();
```

**슬라이드 25: 테스트 도구 상세 설명**

1. **ExecutorService**
   - 스레드 풀 관리
   - 효율적인 스레드 재사용

2. **CountDownLatch**
   - 메인 스레드가 작업 스레드들을 기다림
   - N개의 작업이 완료될 때까지 대기

3. **AtomicInteger**
   - 원자적 증감 연산 보장
   - 동시성 환경에서 안전한 카운터

**슬라이드 26: @Transactional의 역할**

```
@Transactional
    ↓
1. 트랜잭션 시작
2. 비관적 락으로 데이터 조회
3. 비즈니스 로직 실행
4. 커밋 시점에 변경사항 반영 → 가시성 보장
5. 다른 스레드가 최신값 읽기 가능
```

**가시성 문제 해결:**
- 트랜잭션 커밋 시 모든 변경사항이 메인 메모리(DB)에 반영
- 다른 스레드가 항상 최신값을 읽을 수 있음

---

### 4부: 결(結) - 정리와 교훈 (5-8분)

**슬라이드 27: 실무 적용 결과**

```
✅ 테스트 결과
- 동시 요청: 1000개
- 성공 처리: 1000개
- 최종 좋아요 수: 1000개 (정확!)
- 데이터 정합성: 100% 보장
```

**슬라이드 28: 동시성 제어 선택 가이드**

```
🤔 어떤 방법을 선택해야 할까?

상황별 선택 기준:

1. 단순 카운터, 플래그 → AtomicInteger, volatile
2. 메모리상의 객체 보호 → synchronized, Lock
3. DB 데이터 정합성 (충돌 적음) → Optimistic Lock
4. DB 데이터 정합성 (충돌 많음) → Pessimistic Lock
5. 복잡한 비즈니스 로직 → Transaction + Lock 조합
```

**슬라이드 29: 주의사항 및 베스트 프랙티스**

⚠️ **주의사항:**
1. 데드락(Deadlock) 가능성 주의
2. 락의 범위는 최소화 (성능 저하 방지)
3. 스케줄러를 믿지 말 것 - 실행 순서는 예측 불가
4. 방어적 프로그래밍: 어떤 순서로 실행되어도 안전하게

✅ **베스트 프랙티스:**
1. 공유 자원을 명확히 파악
2. 최소한의 범위만 동기화
3. 적절한 수준의 락 선택
4. 반드시 테스트 코드 작성
5. 성능과 안전성의 균형

**슬라이드 30: 핵심 교훈**

```
💡 동시성 문제 해결의 핵심

1. 진짜 공유 자원이 무엇인지 파악
   "여러 스레드가 동시에 수정하려는 대상은?"

2. 원자성과 가시성 문제 이해
   - 원자성: 연산이 중간에 끊기지 않도록
   - 가시성: 변경사항이 다른 스레드에게 보이도록

3. 적절한 제어 방법 선택
   - Application Level vs DB Level
   - 상황에 맞는 도구 선택

4. 방어적 코드 작성
   - 실행 순서에 의존하지 말 것
   - 항상 동시성을 고려한 설계
```

**슬라이드 31: 스레드와 동시성의 깊은 이해는 왜 필요한가?**

```
🎯 실무에서의 가치

1. 안정적인 서비스 운영
   - 데이터 정합성 보장
   - 예측 가능한 동작

2. 성능 최적화
   - 병렬 처리로 처리량 증가
   - 효율적인 자원 활용

3. 확장 가능한 아키텍처
   - 멀티 코어 활용
   - 대용량 트래픽 대응

4. 문제 해결 능력
   - 버그 디버깅 능력 향상
   - 설계 단계에서 문제 예방
```

**슬라이드 32: 추가 학습 자료**

```
📚 더 깊이 공부하고 싶다면?

책:
- "Java Concurrency in Practice" (Brian Goetz)
- "Operating System Concepts" (공룡책)

키워드:
- Thread Pool, Fork/Join Framework
- CAS (Compare-And-Swap)
- Memory Consistency, Happens-Before
- Virtual Thread (Java 21+)

실습:
- 다양한 동시성 시나리오 직접 구현
- 성능 테스트 및 프로파일링
```

**슬라이드 33: Q&A**

```
💬 질문 있으신가요?

예상 질문:
1. 분산 환경에서는 어떻게 동시성을 제어하나요?
   → Redis Lock, 분산 락 (Redisson 등)

2. Virtual Thread는 어떻게 다른가요?
   → OS 스레드 1:1 매핑이 아닌 경량 스레드

3. 성능 테스트는 어떻게 하나요?
   → JMeter, Gatling 등의 부하 테스트 도구
```

**슬라이드 34: 마무리**

```
🙏 감사합니다

핵심 메시지:
"동시성 제어는 어려운 주제이지만,
기본 원리를 이해하면 실무에서 충분히 적용할 수 있습니다."

실무에서 만난 문제 → 원리 학습 → 해결 → 학습
이 사이클이 계속되면서 성장할 수 있습니다!
```

---

## 📌 발표 준비 체크리스트

### 내용 준비
- [ ] 코드 예시 실행 가능하도록 준비
- [ ] 각 슬라이드별 설명 대본 작성
- [ ] 데모 영상 또는 라이브 코딩 준비
- [ ] 예상 질문에 대한 답변 준비

### 시각 자료
- [ ] 코드는 큰 글씨로, 핵심만 표시
- [ ] 다이어그램: 프로세스/스레드 구조
- [ ] 애니메이션: Race Condition 발생 과정
- [ ] 비유 자료: 집, TV 리모컨 등 이미지

### 발표 연습
- [ ] 시간 맞춰서 연습 (30-40분)
- [ ] 전환 부분 자연스럽게 연결
- [ ] 청중과 아이컨택, 질문 유도

---

## 🎨 슬라이드 디자인 팁

1. **일관성**: 같은 색상 테마, 폰트 사용
2. **가독성**: 한 슬라이드에 너무 많은 내용 X
3. **시각화**:
   - 코드는 syntax highlighting
   - 개념은 다이어그램으로
   - 비유는 이미지로
4. **강조**: 핵심 키워드는 색상/크기로 강조
5. **흐름**: 스토리텔링처럼 자연스럽게

---

## 💡 발표 팁

### 도입부 (1부)
- 흥미로운 질문으로 시작
- 실제 상황과 공감대 형성
- "이런 문제 겪어보신 분?" 청중 참여

### 본론 (2-3부)
- 복잡한 개념은 비유 활용
- 코드 설명 시 천천히, 명확하게
- 중간중간 "이해되시나요?" 확인

### 마무리 (4부)
- 핵심 메시지 반복
- 실무 적용 가능성 강조
- 긍정적인 마무리

### 전체
- 너무 빠르지 않게, 적절한 호흡
- 청중의 반응 살피기
- 어려운 내용은 다시 한번 설명
- 자신감 있는 태도

---

## 📝 참고자료

### 유튜브
- https://www.youtube.com/watch?v=x-Lp-h_pf9Q (OS 스레드 비유)

### 공식 문서
- Java Concurrency Utilities (java.util.concurrent)
- JPA Locking

### 블로그/아티클
- Race Condition 실제 사례
- Pessimistic Lock vs Optimistic Lock 비교

---

이 자료가 성공적인 발표에 도움이 되길 바랍니다! 화이팅! 🚀
