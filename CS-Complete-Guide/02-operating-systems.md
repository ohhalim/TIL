# 2️⃣ 운영체제 (Operating Systems) 완전 정복

> 이것만 보면 운영체제는 끝!

---

## 📚 목차

1. [운영체제 기본 개념](#운영체제-기본-개념)
2. [프로세스와 스레드](#프로세스와-스레드)
3. [CPU 스케줄링](#cpu-스케줄링)
4. [프로세스 동기화](#프로세스-동기화)
5. [데드락](#데드락)
6. [메모리 관리](#메모리-관리)
7. [가상 메모리](#가상-메모리)
8. [파일 시스템](#파일-시스템)
9. [면접 필수 질문](#면접-필수-질문)

---

## 운영체제 기본 개념

### 운영체제란?

**정의:** 하드웨어와 사용자 사이의 중재자 (인터페이스)

**주요 역할:**
1. **자원 관리**: CPU, 메모리, I/O 장치 효율적 관리
2. **프로그램 실행**: 프로세스 생성 및 관리
3. **사용자 인터페이스 제공**: CLI, GUI
4. **보안 및 보호**: 권한 관리, 파일 보호

### 운영체제 구조

```
┌─────────────────────────────────────┐
│        User Applications            │
├─────────────────────────────────────┤
│        System Programs              │
├─────────────────────────────────────┤
│        Operating System             │
│  ┌──────────┬──────────┬─────────┐ │
│  │ Process  │  Memory  │  File   │ │
│  │ Manager  │  Manager │ System  │ │
│  ├──────────┼──────────┼─────────┤ │
│  │   CPU    │   I/O    │ Security│ │
│  │Scheduler │  Manager │ Manager │ │
│  └──────────┴──────────┴─────────┘ │
├─────────────────────────────────────┤
│           Hardware                  │
│  CPU | Memory | Disk | I/O Devices │
└─────────────────────────────────────┘
```

### 커널 (Kernel)

**정의:** OS의 핵심 부분, 항상 메모리에 상주

**종류:**
1. **모놀리식 커널**: 모든 기능이 한 덩어리 (Linux, Unix)
2. **마이크로 커널**: 최소 기능만 커널에, 나머지는 사용자 공간
3. **하이브리드 커널**: 둘의 장점 결합 (Windows, macOS)

### 시스템 콜 (System Call)

**정의:** 사용자 프로그램이 OS 서비스를 요청하는 인터페이스

**주요 시스템 콜:**
- **프로세스 제어**: `fork()`, `exec()`, `exit()`, `wait()`
- **파일 관리**: `open()`, `read()`, `write()`, `close()`
- **장치 관리**: `ioctl()`, `read()`, `write()`
- **정보 유지**: `getpid()`, `alarm()`, `sleep()`
- **통신**: `pipe()`, `shmget()`, `mmap()`

```c
// 시스템 콜 예시 (C)
#include <unistd.h>
#include <fcntl.h>

int main() {
    // 파일 열기
    int fd = open("file.txt", O_RDONLY);  // 시스템 콜

    // 파일 읽기
    char buffer[100];
    read(fd, buffer, 100);  // 시스템 콜

    // 파일 닫기
    close(fd);  // 시스템 콜

    return 0;
}
```

---

## 프로세스와 스레드

### 프로세스 (Process)

**정의:** 실행 중인 프로그램

**프로세스 메모리 구조:**
```
┌──────────────┐  높은 주소
│    Stack     │  ← 함수 호출, 지역 변수 (아래로 성장)
├──────────────┤
│      ↓       │
│              │
│      ↑       │
├──────────────┤
│     Heap     │  ← 동적 할당 (위로 성장)
├──────────────┤
│     Data     │  ← 전역/정적 변수
├──────────────┤
│     Code     │  ← 프로그램 코드
└──────────────┘  낮은 주소
```

**프로세스 상태 (Process State):**
```
       ┌──────────┐
       │   NEW    │  생성
       └────┬─────┘
            ↓
       ┌────────────┐
  ┌───→│   READY    │←──┐ 준비
  │    └─────┬──────┘   │
  │          ↓          │
  │    ┌─────────────┐  │
  │    │   RUNNING   │──┘ 실행
  │    └─────┬───┬───┘
  │          │   │
  │          │   ↓
  │          │ ┌────────────┐
  │          │ │  WAITING   │  대기
  │          │ └──────┬─────┘
  │          │        │
  │          └────────┘
  │               ↓
  │          ┌──────────┐
  └──────────│TERMINATED│  종료
             └──────────┘
```

**프로세스 제어 블록 (PCB):**
```java
class PCB {
    int processId;           // PID
    ProcessState state;      // 상태
    int programCounter;      // 다음 명령어 주소
    int[] registers;         // CPU 레지스터 값
    int priority;            // 우선순위
    long memoryLimits;       // 메모리 범위
    List<File> openFiles;    // 열린 파일 목록
}
```

### 프로세스 생성

```c
// fork() 시스템 콜
#include <stdio.h>
#include <unistd.h>

int main() {
    pid_t pid = fork();  // 자식 프로세스 생성

    if (pid < 0) {
        // 에러
        printf("Fork failed\n");
    } else if (pid == 0) {
        // 자식 프로세스
        printf("Child: PID = %d\n", getpid());
    } else {
        // 부모 프로세스
        printf("Parent: PID = %d, Child PID = %d\n", getpid(), pid);
        wait(NULL);  // 자식 종료 대기
    }

    return 0;
}
```

### 스레드 (Thread)

**정의:** 프로세스 내의 실행 단위

**프로세스 vs 스레드:**
```
프로세스                     스레드
┌────────────────┐          ┌────────────────┐
│   Process A    │          │   Process A    │
│ ┌────────────┐ │          │ ┌────┬────┬───┐│
│ │   Code     │ │          │ │Code│Code│Cd │← 공유
│ ├────────────┤ │          │ ├────┴────┴───┤│
│ │   Data     │ │          │ │    Data     │← 공유
│ ├────────────┤ │          │ ├────┬────┬───┤│
│ │   Heap     │ │          │ │Heap│Heap│Hp │← 공유
│ ├────────────┤ │          │ ├────┼────┼───┤│
│ │   Stack    │ │          │ │Stk1│Stk2│St3│← 독립
│ └────────────┘ │          │ └────┴────┴───┘│
│                │          │  T1   T2   T3  │
└────────────────┘          └────────────────┘
```

**스레드 특징:**
- ✅ **공유**: Code, Data, Heap, 파일
- ❌ **독립**: Stack, 레지스터, PC (Program Counter)

**멀티스레딩 장점:**
1. **응답성 향상**: UI 블로킹 방지
2. **자원 공유**: 메모리 효율적
3. **경제성**: 생성/전환 비용 낮음
4. **확장성**: 멀티코어 활용

```java
// Java 스레드 예시
class MyThread extends Thread {
    @Override
    public void run() {
        System.out.println("Thread: " + Thread.currentThread().getId());
    }
}

public class Main {
    public static void main(String[] args) {
        // 스레드 생성
        MyThread t1 = new MyThread();
        MyThread t2 = new MyThread();

        // 시작
        t1.start();
        t2.start();

        // 대기
        try {
            t1.join();
            t2.join();
        } catch (InterruptedException e) {
            e.printStackTrace();
        }
    }
}
```

### 사용자 레벨 스레드 vs 커널 레벨 스레드

| 구분 | 사용자 레벨 | 커널 레벨 |
|------|-----------|----------|
| 관리 주체 | 사용자 라이브러리 | OS 커널 |
| 생성 속도 | 빠름 | 느림 |
| 컨텍스트 스위칭 | 빠름 | 느림 |
| 멀티코어 활용 | 불가 | 가능 |
| 하나 블로킹 시 | 전체 블로킹 | 다른 스레드 실행 |

---

## CPU 스케줄링

### 스케줄링 목표

1. **CPU 이용률 최대화**
2. **처리량(Throughput) 최대화**
3. **대기 시간 최소화**
4. **응답 시간 최소화**
5. **공정성 보장**

### 스케줄링 알고리즘

#### 1. FCFS (First-Come, First-Served)

**특징:** 먼저 온 순서대로 처리

```
프로세스:  P1(24ms)  P2(3ms)  P3(3ms)
도착 순서: P1 → P2 → P3

간트 차트:
0        24  27  30
|───P1───|P2|P3|

평균 대기 시간 = (0 + 24 + 27) / 3 = 17ms
```

**장점:** 구현 간단
**단점:** Convoy Effect (짧은 프로세스가 긴 프로세스를 기다림)

#### 2. SJF (Shortest Job First)

**특징:** 실행 시간이 짧은 프로세스 먼저

```
프로세스:  P1(24ms)  P2(3ms)  P3(3ms)
도착 순서: P1, P2, P3 (동시)

간트 차트:
0  3  6        30
|P2|P3|───P1───|

평균 대기 시간 = (6 + 0 + 3) / 3 = 3ms
```

**장점:** 평균 대기 시간 최소
**단점:**
- 실행 시간 예측 어려움
- Starvation (긴 프로세스가 계속 대기)

#### 3. Priority Scheduling

**특징:** 우선순위가 높은 프로세스 먼저

```
프로세스: P1(우선순위 3), P2(우선순위 1), P3(우선순위 2)

실행 순서: P2 → P3 → P1
```

**문제:** Starvation
**해결:** Aging (대기 시간에 따라 우선순위 증가)

#### 4. Round Robin (RR)

**특징:** 시간 할당량(Time Quantum)만큼 돌아가며 실행

```
프로세스:  P1(24ms)  P2(3ms)  P3(3ms)
시간 할당량: 4ms

간트 차트:
0  4  7  10 14 18 22 26 30
|P1|P2|P3|P1|P1|P1|P1|P1|

평균 대기 시간 = (10-4 + 4 + 7) / 3 = 5.66ms
```

**장점:** 공정, 응답 시간 좋음
**단점:**
- 시간 할당량 선택 중요
- 너무 작으면 context switch 비용 증가
- 너무 크면 FCFS와 유사

#### 5. Multilevel Queue

**특징:** 여러 큐를 우선순위별로 관리

```
┌──────────────────────┐
│  System Processes    │ ← 우선순위 최상
├──────────────────────┤
│  Interactive         │
├──────────────────────┤
│  Batch Processes     │ ← 우선순위 최하
└──────────────────────┘
```

### 컨텍스트 스위칭 (Context Switching)

**정의:** CPU를 다른 프로세스로 전환하는 과정

```
Process P1 실행 중
    ↓
1. P1 상태 저장 (PCB에)
    ↓
2. P2 상태 복원 (PCB에서)
    ↓
Process P2 실행
```

**오버헤드:**
- 레지스터 저장/복원
- 메모리 매핑 변경
- 캐시 무효화

---

## 프로세스 동기화

### Race Condition (경쟁 상태)

**문제:**
```java
// 공유 변수
int count = 0;

// Thread 1
count++;  // 1. 읽기: 0  2. 증가: 1  3. 쓰기: 1

// Thread 2 (동시 실행)
count++;  // 1. 읽기: 0  2. 증가: 1  3. 쓰기: 1

// 결과: count = 1 (예상: 2) ❌
```

### Critical Section (임계 영역)

**정의:** 공유 자원에 접근하는 코드 영역

**해결 조건:**
1. **Mutual Exclusion (상호 배제)**: 한 번에 하나만 실행
2. **Progress (진행)**: 대기 중인 프로세스 중 하나는 선택되어야 함
3. **Bounded Waiting (한정 대기)**: 무한 대기 방지

### Peterson's Algorithm

```java
boolean[] flag = new boolean[2];  // 진입 의사
int turn;  // 차례

// Process i
void enter(int i) {
    int j = 1 - i;
    flag[i] = true;  // 진입 의사 표시
    turn = j;  // 상대방 차례

    // 상대방이 원하고 상대방 차례면 대기
    while (flag[j] && turn == j);
}

void exit(int i) {
    flag[i] = false;
}

// 사용
enter(0);
// Critical Section
exit(0);
```

### Mutex Lock

**특징:** 이진 세마포어 (0 또는 1)

```java
class Mutex {
    private boolean locked = false;

    public synchronized void lock() {
        while (locked) {
            try {
                wait();  // 대기
            } catch (InterruptedException e) {}
        }
        locked = true;
    }

    public synchronized void unlock() {
        locked = false;
        notify();  // 대기 중인 스레드 깨움
    }
}

// 사용
Mutex mutex = new Mutex();

mutex.lock();
// Critical Section
count++;
mutex.unlock();
```

### Semaphore

**특징:** 정수형 카운터 (N개까지 허용)

```java
class Semaphore {
    private int value;

    public Semaphore(int value) {
        this.value = value;
    }

    public synchronized void wait() {  // P() 연산
        while (value <= 0) {
            try {
                wait();
            } catch (InterruptedException e) {}
        }
        value--;
    }

    public synchronized void signal() {  // V() 연산
        value++;
        notify();
    }
}

// 사용 예: Producer-Consumer
Semaphore empty = new Semaphore(BUFFER_SIZE);  // 빈 공간
Semaphore full = new Semaphore(0);             // 찬 공간

// Producer
empty.wait();
// produce item
full.signal();

// Consumer
full.wait();
// consume item
empty.signal();
```

### Monitor

**특징:** 고수준 동기화 도구

```java
class BoundedBuffer {
    private int[] buffer;
    private int count = 0;
    private int in = 0;
    private int out = 0;

    public synchronized void produce(int item) {
        while (count == buffer.length) {
            try {
                wait();  // 버퍼 가득 참
            } catch (InterruptedException e) {}
        }

        buffer[in] = item;
        in = (in + 1) % buffer.length;
        count++;

        notifyAll();  // Consumer 깨움
    }

    public synchronized int consume() {
        while (count == 0) {
            try {
                wait();  // 버퍼 비어 있음
            } catch (InterruptedException e) {}
        }

        int item = buffer[out];
        out = (out + 1) % buffer.length;
        count--;

        notifyAll();  // Producer 깨움
        return item;
    }
}
```

---

## 데드락

### 데드락 (Deadlock)이란?

**정의:** 두 개 이상의 프로세스가 서로의 자원을 기다리며 무한 대기하는 상태

```
Process P1:           Process P2:
1. Lock A             1. Lock B
2. Wait for B         2. Wait for A
   ↓                     ↓
   └─────── DEADLOCK ────┘
```

### 데드락 발생 조건 (4가지 모두 만족 시)

1. **Mutual Exclusion (상호 배제)**: 자원은 한 번에 하나만 사용
2. **Hold and Wait (점유 대기)**: 자원을 가진 채로 다른 자원 대기
3. **No Preemption (비선점)**: 강제로 자원 빼앗기 불가
4. **Circular Wait (순환 대기)**: 자원 대기 그래프에 사이클 존재

### 데드락 해결 방법

#### 1. 예방 (Prevention)

4가지 조건 중 하나를 거부

```java
// 순환 대기 예방: 자원에 순서 부여
class DeadlockPrevention {
    Lock lock1 = new ReentrantLock();
    Lock lock2 = new ReentrantLock();

    void transfer1() {
        lock1.lock();  // 항상 lock1 먼저
        lock2.lock();
        try {
            // critical section
        } finally {
            lock2.unlock();
            lock1.unlock();
        }
    }

    void transfer2() {
        lock1.lock();  // 같은 순서
        lock2.lock();
        try {
            // critical section
        } finally {
            lock2.unlock();
            lock1.unlock();
        }
    }
}
```

#### 2. 회피 (Avoidance)

**Banker's Algorithm:**
- 안전 상태(Safe State)인지 확인 후 자원 할당
- 불안전 상태로 가지 않도록 회피

```java
boolean isSafe(int[][] allocation, int[][] max, int[] available) {
    int n = allocation.length;  // 프로세스 수
    int m = available.length;   // 자원 종류 수

    boolean[] finish = new boolean[n];
    int[] work = available.clone();

    while (true) {
        boolean found = false;

        for (int i = 0; i < n; i++) {
            if (!finish[i]) {
                // Need[i] = Max[i] - Allocation[i]
                boolean canAllocate = true;
                for (int j = 0; j < m; j++) {
                    if (max[i][j] - allocation[i][j] > work[j]) {
                        canAllocate = false;
                        break;
                    }
                }

                if (canAllocate) {
                    // 자원 할당 가능
                    for (int j = 0; j < m; j++) {
                        work[j] += allocation[i][j];
                    }
                    finish[i] = true;
                    found = true;
                }
            }
        }

        if (!found) break;
    }

    // 모든 프로세스가 완료되면 안전
    for (boolean f : finish) {
        if (!f) return false;
    }
    return true;
}
```

#### 3. 탐지 및 회복 (Detection and Recovery)

**탐지:** 자원 할당 그래프에서 사이클 찾기
**회복:**
- 프로세스 종료
- 자원 선점

#### 4. 무시 (Ignore)

- 데드락 발생 확률이 낮다면 무시
- 대부분의 OS가 사용 (UNIX, Windows)

---

## 메모리 관리

### 메모리 계층 구조

```
┌─────────────┐  빠름, 비쌈, 작음
│  Register   │  ← 1 cycle
├─────────────┤
│    Cache    │  ← 수십 cycles
├─────────────┤
│     RAM     │  ← 수백 cycles
├─────────────┤
│    Disk     │  ← 수백만 cycles
└─────────────┘  느림, 싸, 큼
```

### 주소 바인딩

**논리 주소 (Logical Address):** CPU가 생성하는 주소
**물리 주소 (Physical Address):** 실제 메모리 주소

**MMU (Memory Management Unit):** 논리 → 물리 주소 변환

### 연속 메모리 할당

#### 1. 고정 분할 (Fixed Partitioning)

```
┌─────────┐
│ Partition 1 (100KB)
├─────────┤
│ Partition 2 (200KB)
├─────────┤
│ Partition 3 (300KB)
└─────────┘
```

**문제:** Internal Fragmentation (내부 단편화)

#### 2. 동적 분할 (Dynamic Partitioning)

**할당 전략:**

1. **First Fit:** 첫 번째 적합한 공간
```java
Block findFirstFit(int size, List<Block> freeBlocks) {
    for (Block block : freeBlocks) {
        if (block.size >= size) {
            return block;
        }
    }
    return null;
}
```

2. **Best Fit:** 가장 작은 적합한 공간
```java
Block findBestFit(int size, List<Block> freeBlocks) {
    Block best = null;
    int minWaste = Integer.MAX_VALUE;

    for (Block block : freeBlocks) {
        if (block.size >= size) {
            int waste = block.size - size;
            if (waste < minWaste) {
                minWaste = waste;
                best = block;
            }
        }
    }
    return best;
}
```

3. **Worst Fit:** 가장 큰 공간

**문제:** External Fragmentation (외부 단편화)

### 페이징 (Paging)

**개념:** 물리 메모리를 고정 크기(Page)로 분할

```
논리 주소                물리 메모리
┌─────────┐              ┌─────────┐
│ Page 0  │ ────┐   ┌──→ │ Frame 2 │
├─────────┤     │   │    ├─────────┤
│ Page 1  │ ──┐ └───┼──→ │ Frame 5 │
├─────────┤   └─────┼──→ ├─────────┤
│ Page 2  │ ────────┘    │ Frame 1 │
└─────────┘              ├─────────┤
                         │ Frame 3 │
    Page Table           └─────────┘
```

**주소 변환:**
```
논리 주소 = (페이지 번호, 오프셋)
물리 주소 = (프레임 번호, 오프셋)

페이지 테이블에서: 페이지 번호 → 프레임 번호
```

**장점:**
- External Fragmentation 없음
- 연속적 할당 불필요

**단점:**
- Internal Fragmentation (마지막 페이지)
- 페이지 테이블 공간 필요

### 세그먼테이션 (Segmentation)

**개념:** 논리적 단위(Segment)로 분할

```
┌──────────┐
│   Code   │ ─── Segment 0
├──────────┤
│   Data   │ ─── Segment 1
├──────────┤
│   Stack  │ ─── Segment 2
└──────────┘
```

**주소 변환:**
```
논리 주소 = (세그먼트 번호, 오프셋)

세그먼트 테이블:
┌────┬──────┬──────┐
│ 번호│ Base │Limit │
├────┼──────┼──────┤
│  0 │ 1000 │ 500  │
│  1 │ 2000 │ 800  │
└────┴──────┴──────┘

물리 주소 = Base + Offset (if Offset < Limit)
```

---

## 가상 메모리

### 가상 메모리란?

**개념:** 물리 메모리보다 큰 주소 공간 제공

```
논리 메모리 (4GB)         물리 메모리 (1GB)
┌─────────────┐          ┌─────────────┐
│   Process   │          │   일부만    │
│   전체      │  ──────→ │   상주      │
│   공간      │          │             │
└─────────────┘          └─────────────┘
     ↓                        ↑
디스크 (Swap)
```

### 요구 페이징 (Demand Paging)

**개념:** 필요할 때만 페이지를 메모리로 로드

```
1. CPU가 페이지 접근
2. 페이지 테이블 확인
3. Valid bit = 0 (메모리에 없음)
4. Page Fault 발생
5. 디스크에서 페이지 로드
6. 페이지 테이블 갱신
7. 명령어 재실행
```

### Page Fault 처리

```
┌─────────────────────┐
│   Page Fault 발생   │
└──────────┬──────────┘
           ↓
┌─────────────────────┐
│  빈 프레임 있는가?  │
└──────┬───────┬──────┘
       ↓ Yes   ↓ No
       │  ┌─────────────┐
       │  │ 페이지 교체 │
       │  └──────┬──────┘
       ↓         ↓
┌─────────────────────┐
│ 디스크에서 페이지 로드│
└──────────┬──────────┘
           ↓
┌─────────────────────┐
│  페이지 테이블 갱신 │
└──────────┬──────────┘
           ↓
┌─────────────────────┐
│   명령어 재실행     │
└─────────────────────┘
```

### 페이지 교체 알고리즘

#### 1. FIFO (First-In-First-Out)

```java
class FIFOPageReplacement {
    Queue<Integer> queue = new LinkedList<>();
    Set<Integer> pages = new HashSet<>();
    int capacity;

    int pageFault(int[] references) {
        int faults = 0;

        for (int page : references) {
            if (!pages.contains(page)) {
                faults++;

                if (queue.size() == capacity) {
                    int removed = queue.poll();
                    pages.remove(removed);
                }

                queue.offer(page);
                pages.add(page);
            }
        }

        return faults;
    }
}
```

#### 2. LRU (Least Recently Used)

```java
class LRUPageReplacement {
    LinkedHashMap<Integer, Integer> cache;
    int capacity;

    public LRUPageReplacement(int capacity) {
        this.capacity = capacity;
        this.cache = new LinkedHashMap<>(capacity, 0.75f, true) {
            @Override
            protected boolean removeEldestEntry(Map.Entry eldest) {
                return size() > capacity;
            }
        };
    }

    int pageFault(int[] references) {
        int faults = 0;

        for (int page : references) {
            if (!cache.containsKey(page)) {
                faults++;
            }
            cache.put(page, page);  // 접근 표시
        }

        return faults;
    }
}
```

#### 3. Optimal (이론적 최적)

```
미래에 가장 오래 사용되지 않을 페이지 교체
(실제 구현 불가능 - 미래를 알 수 없음)
```

#### 4. LFU (Least Frequently Used)

사용 빈도가 가장 낮은 페이지 교체

### Thrashing (스래싱)

**정의:** 페이지 교체가 너무 빈번해서 CPU 이용률 급격히 감소

```
페이지 부재율 ↑
      ↓
페이지 교체 증가
      ↓
CPU 이용률 ↓
      ↓
OS: 프로세스 더 추가 (멀티프로그래밍 증가)
      ↓
더 심한 스래싱!
```

**해결:**
- Working Set 모델
- Page Fault Frequency 제어
- 프로세스 수 감소

---

## 파일 시스템

### 파일 (File)

**정의:** 관련 정보의 집합

**파일 속성:**
- 이름, 식별자 (inode)
- 타입, 크기
- 위치 (디스크 주소)
- 보호 (권한)
- 시간 (생성, 수정, 접근)

### 디렉토리 구조

```
/ (루트)
├── home
│   ├── user1
│   │   ├── file1.txt
│   │   └── file2.txt
│   └── user2
├── etc
│   └── config.conf
└── var
    └── log
```

### 파일 할당 방법

#### 1. 연속 할당 (Contiguous Allocation)

```
파일 A: 블록 0-4
파일 B: 블록 5-7

┌───┬───┬───┬───┬───┬───┬───┬───┐
│ A │ A │ A │ A │ A │ B │ B │ B │
└───┴───┴───┴───┴───┴───┴───┴───┘
```

**장점:** 빠른 접근, 순차/직접 접근 모두 가능
**단점:** External Fragmentation, 파일 크기 변경 어려움

#### 2. 연결 할당 (Linked Allocation)

```
파일 A: 0 → 2 → 5 → 9
파일 B: 1 → 3 → 4

┌───┬───┬───┬───┬───┬───┐
│A,2│B,3│A,5│B,4│B,-│A,9│
└───┴───┴───┴───┴───┴───┘
```

**장점:** External Fragmentation 없음, 크기 제한 없음
**단점:** 직접 접근 느림, 포인터 공간 필요

#### 3. 인덱스 할당 (Indexed Allocation)

```
인덱스 블록
┌───┐     데이터 블록
│ 2 │ ──→ ┌───┐
│ 5 │     │   │ 2
│ 9 │ ──→ ├───┤
└───┘     │   │ 5
      ──→ ├───┤
          │   │ 9
          └───┘
```

**장점:** 직접 접근 가능, Fragmentation 없음
**단점:** 인덱스 블록 공간 필요

### FAT (File Allocation Table)

```
FAT
┌────┬────┬────┬────┬────┐
│ -1 │  2 │  3 │ -1 │ -1 │
└────┴────┴────┴────┴────┘
  0    1    2    3    4

파일 시작: 1
1 → 2 → 3 (EOF)
```

### inode (Unix/Linux)

```
inode
┌──────────────┐
│ 파일 메타데이터│
├──────────────┤
│ Direct (12)  │ ─→ 데이터 블록
├──────────────┤
│ Single (1)   │ ─→ 간접 블록
├──────────────┤
│ Double (1)   │ ─→ 이중 간접
├──────────────┤
│ Triple (1)   │ ─→ 삼중 간접
└──────────────┘
```

### 디스크 스케줄링

#### 1. FCFS

요청 순서대로 처리

#### 2. SSTF (Shortest Seek Time First)

현재 위치에서 가장 가까운 요청 처리

#### 3. SCAN (엘리베이터 알고리즘)

한 방향으로 끝까지 이동하며 처리, 끝에서 방향 전환

```
요청: 98, 183, 37, 122, 14, 124, 65, 67
현재 위치: 53

SCAN (오른쪽으로):
53 → 65 → 67 → 98 → 122 → 124 → 183 → 199 (끝)
    ← 37 ← 14
```

---

## 면접 필수 질문

### Q1: 프로세스와 스레드의 차이는?

**A:**
- **프로세스**: 독립적 메모리 공간, 무거움, 생성 비용 큼
- **스레드**: 메모리 공유 (Code, Data, Heap), 가벼움, 생성 비용 작음
- **실무 예시**: 크롬은 탭마다 프로세스, 워드는 백그라운드 저장 시 스레드

### Q2: 컨텍스트 스위칭이란?

**A:**
- CPU를 다른 프로세스/스레드로 전환하는 과정
- **오버헤드**: 레지스터 저장/복원, 캐시 무효화
- **최소화 방법**: 스레드 사용, 비동기 I/O

### Q3: 데드락 조건 4가지와 해결 방법은?

**A:**
- **4가지 조건**: 상호 배제, 점유 대기, 비선점, 순환 대기
- **해결**: 예방 (자원 순서화), 회피 (Banker's Algorithm), 탐지 및 회복, 무시

### Q4: 가상 메모리가 필요한 이유는?

**A:**
- **물리 메모리보다 큰 프로그램 실행 가능**
- **메모리 보호**: 프로세스 간 독립성
- **효율적 메모리 사용**: 필요한 부분만 로드

### Q5: 페이지 교체 알고리즘 중 가장 좋은 것은?

**A:**
- **이론적**: Optimal (미래 예측 필요 - 불가능)
- **실무**: LRU (Locality 원리 활용)
- **구현**: LRU Approximation (Clock Algorithm)

### Q6: Race Condition을 방지하려면?

**A:**
- **Mutex/Lock**: 상호 배제
- **Semaphore**: 카운팅 세마포어로 N개까지 허용
- **Monitor**: 고수준 동기화
- **Atomic 연산**: CAS (Compare-And-Swap)

### Q7: 멀티프로세싱 vs 멀티스레딩?

**A:**
| 구분 | 멀티프로세싱 | 멀티스레딩 |
|------|------------|-----------|
| 메모리 | 독립 | 공유 |
| 통신 | IPC (느림) | 공유 메모리 (빠름) |
| 안정성 | 높음 (독립) | 낮음 (공유) |
| 사용 사례 | 크롬 (탭) | 웹 서버 (요청 처리) |

---

**이것만 마스터하면 운영체제는 끝!** 🎯
