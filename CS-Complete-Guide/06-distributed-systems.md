# 6️⃣ 분산 시스템 & 클라우드 아키텍처 - 완전 정복

> **"현대 대규모 시스템의 핵심 - 확장성, 가용성, 일관성"**

---

## 📚 목차

1. [분산 시스템 기초](#분산-시스템-기초)
2. [CAP 정리와 일관성 모델](#cap-정리와-일관성-모델)
3. [합의 알고리즘](#합의-알고리즘)
4. [분산 데이터 저장](#분산-데이터-저장)
5. [메시지 큐 & 이벤트 스트리밍](#메시지-큐--이벤트-스트리밍)
6. [마이크로서비스 아키텍처](#마이크로서비스-아키텍처)
7. [서비스 메시 & API Gateway](#서비스-메시--api-gateway)
8. [분산 트랜잭션](#분산-트랜잭션)
9. [분산 추적 & 모니터링](#분산-추적--모니터링)
10. [클라우드 네이티브 패턴](#클라우드-네이티브-패턴)

---

## 분산 시스템 기초

### 왜 분산 시스템인가?

**단일 서버의 한계:**
```
┌──────────────┐
│Single Server │
│  CPU: 100%   │  ← 병목!
│  Memory: Full│
│  Network: ∞  │
└──────────────┘

문제:
- 수직 확장(Scale Up)의 한계
- 단일 장애점(SPOF)
- 지역적 지연
```

**분산 시스템:**
```
     Load Balancer
          │
    ┌─────┼─────┐
    │     │     │
  ┌─┴─┐ ┌─┴─┐ ┌─┴─┐
  │S1 │ │S2 │ │S3 │
  └───┘ └───┘ └───┘

장점:
- 수평 확장(Scale Out) → 무한 확장
- 고가용성(HA)
- 지역 분산 → 낮은 지연
```

### 분산 시스템의 도전 과제

#### 1. 네트워크 신뢰성

**Fallacies of Distributed Computing (분산 컴퓨팅의 오류):**

1. 네트워크는 신뢰할 수 있다 ❌
2. 지연 시간은 0이다 ❌
3. 대역폭은 무한하다 ❌
4. 네트워크는 안전하다 ❌
5. 토폴로지는 변하지 않는다 ❌
6. 관리자는 한 명이다 ❌
7. 전송 비용은 0이다 ❌
8. 네트워크는 균질하다 ❌

**실제 상황:**
```
Client → [Network] → Server

가능한 문제:
- 패킷 손실
- 지연 (Latency)
- 순서 뒤바뀜
- 중복 전송
- 네트워크 분할 (Partition)
```

#### 2. 시계 동기화

**문제:** 각 서버의 시계가 다름

```
Server A: 10:00:00.000
Server B: 10:00:00.100  (100ms 차이)

트랜잭션:
T1 at A (10:00:00.050)
T2 at B (10:00:00.040)  ← 실제로는 이후인데 타임스탬프는 이전!
```

**해결책:**

**NTP (Network Time Protocol):**
```
Client ────→ NTP Server
       ←────
    (시간 동기화, 수 ms 오차)
```

**Vector Clock (벡터 시계):**
```
각 서버가 버전 벡터 유지

Server A: [A:1, B:0, C:0]
Server B: [A:1, B:1, C:0]  → A의 이벤트 이후 발생
Server C: [A:0, B:0, C:1]  → A, B와 병렬 발생 (충돌!)
```

**Lamport Timestamp:**
```python
class LamportClock:
    def __init__(self):
        self.time = 0

    def tick(self):
        """로컬 이벤트"""
        self.time += 1
        return self.time

    def update(self, received_time):
        """메시지 수신 시"""
        self.time = max(self.time, received_time) + 1
        return self.time

# 사용
clock = LamportClock()
t1 = clock.tick()  # 로컬 이벤트
# 메시지 수신 (타임스탬프 5)
t2 = clock.update(5)  # max(1, 5) + 1 = 6
```

---

## CAP 정리와 일관성 모델

### CAP 정리 (CAP Theorem)

**Eric Brewer (2000):**

> "분산 시스템은 다음 3가지 중 2가지만 보장할 수 있다"

```
         Consistency
         (일관성)
            /  \
           /    \
          /      \
         /   ?    \
        /          \
Availability ─── Partition Tolerance
  (가용성)         (분할 내성)
```

**정의:**

- **Consistency (C)**: 모든 노드가 동시에 같은 데이터를 봄
- **Availability (A)**: 모든 요청이 응답을 받음 (성공 또는 실패)
- **Partition Tolerance (P)**: 네트워크 분할이 발생해도 시스템 동작

**조합:**

#### CA (Consistency + Availability)
```
분할 내성 포기 → 단일 노드 시스템
예: 전통적 RDBMS (단일 서버)

현실: 분산 시스템에서 불가능 (네트워크 분할은 항상 발생)
```

#### CP (Consistency + Partition Tolerance)
```
가용성 포기 → 일관성 우선

예: HBase, MongoDB (strong consistency 모드), ZooKeeper

시나리오:
네트워크 분할 발생 시
→ 일관성 보장 안 되는 노드는 응답 거부
→ 일부 사용자는 오류 경험
```

#### AP (Availability + Partition Tolerance)
```
일관성 포기 → 가용성 우선

예: Cassandra, DynamoDB, Riak

시나리오:
네트워크 분할 발생 시
→ 모든 노드가 계속 응답
→ 일시적으로 다른 데이터 반환 가능
→ 나중에 조정 (Eventually Consistent)
```

### 일관성 모델

**일관성 스펙트럼:**
```
강한 일관성 ←────────────────→ 약한 일관성
(Strong)                      (Weak)

│         │         │         │         │
강일관성  Sequential Causal  Eventual  최종일관성
        Consistency          읽기후쓰기
```

#### 1. Strong Consistency (강일관성)

**정의:** 모든 읽기는 최신 쓰기를 반영

```
Client A: Write(x=1)
          ↓
Client B: Read(x) → 1 (즉시 반영)

구현: 분산 락, Consensus (Paxos, Raft)
```

#### 2. Sequential Consistency

**정의:** 모든 프로세스가 같은 순서로 연산을 봄

```
P1: Write(x=1), Write(x=2)
P2: Read(x)=1, Read(x)=2  ✅
P3: Read(x)=2, Read(x)=1  ❌ (순서 다름)
```

#### 3. Causal Consistency (인과 일관성)

**정의:** 인과 관계가 있는 연산만 순서 보장

```
P1: Write(x=1)
    └→ P2: Read(x)=1, Write(y=2)  (인과 관계)
        └→ P3: Read(y)=2, Read(x)=? (최소 1)

병렬 연산:
P1: Write(a=1)
P2: Write(b=2)  (인과 관계 없음 → 순서 상관없음)
```

#### 4. Eventual Consistency (최종 일관성)

**정의:** 충분한 시간 후에는 모든 노드가 같은 값

```
T=0: Write(x=1) at Node A
T=1: Read(x) at Node B → 0 (복제 안 됨)
T=2: Read(x) at Node B → 0
T=3: Read(x) at Node B → 1 (복제됨!)

Amazon의 예:
"장바구니에 담았는데 다른 기기에서 안 보임"
→ 몇 초 후 보임
```

**구현 (Anti-Entropy):**
```python
# Gossip Protocol
def gossip():
    while True:
        # 랜덤 노드 선택
        peer = random.choice(peers)

        # 내 데이터 전송
        peer.receive(my_data)

        # 상대 데이터 수신
        their_data = peer.send_data()

        # 병합
        merge(my_data, their_data)

        time.sleep(interval)
```

#### 5. Read-Your-Writes Consistency

**정의:** 자신이 쓴 데이터는 즉시 읽을 수 있음

```
User A: Write(profile="New Photo")
User A: Read(profile) → "New Photo" ✅

User B: Read(profile) → "Old Photo" (OK, 나중에 업데이트)
```

**구현:**
```python
def read_your_writes(user_id, key):
    # 세션에 최근 쓰기 버전 저장
    last_write_version = session[user_id].get(key)

    while True:
        data, version = read_from_replica(key)

        if version >= last_write_version:
            return data

        # 복제 대기 또는 마스터에서 읽기
        time.sleep(0.1)
```

---

## 합의 알고리즘

### 문제: 분산 합의

**시나리오:**
```
여러 노드가 하나의 값에 합의해야 함

예: 리더 선출, 트랜잭션 커밋

도전:
- 노드 장애
- 네트워크 지연/분할
- 비잔틴 장애 (악의적 노드)
```

### Paxos 알고리즘

**Leslie Lamport (1998)**

**역할:**
- **Proposer**: 값 제안
- **Acceptor**: 제안 수락/거부
- **Learner**: 최종 결정 학습

**프로토콜 (간소화):**

```
Phase 1: Prepare
Proposer → Acceptors: Prepare(n)
         ← "Promise: n, (이전 수락한 값)"

Phase 2: Accept
Proposer → Acceptors: Accept(n, value)
         ← "Accepted"

Learner: 과반수 Accepted → 값 확정
```

**예시:**
```
3개 노드 (과반수 = 2)

Proposer A:
1. Prepare(1) → [Node1, Node2, Node3]
2. Promise(1) ← [Node1, Node2]  (과반수 OK)
3. Accept(1, "A") → [Node1, Node2, Node3]
4. Accepted ← [Node1, Node2]  (과반수 OK)
→ 값 "A" 확정!

동시에 Proposer B:
1. Prepare(2) → [Node1, Node2, Node3]
2. Promise(2) ← [Node2, Node3]  (더 큰 번호)
3. Accept(2, "B") → 실패 (Node1은 Promise(1) 때문에 거부)
```

### Raft 알고리즘

**Diego Ongaro & John Ousterhout (2014)**

> "Paxos보다 이해하기 쉬운 합의 알고리즘"

**역할:**
- **Leader**: 모든 클라이언트 요청 처리
- **Follower**: Leader 복제
- **Candidate**: Leader 선출 시

**리더 선출:**
```
1. 모든 노드는 Follower로 시작
2. Heartbeat 없으면 Candidate로 전환
3. Vote Request → 다른 노드들
4. 과반수 Vote 받으면 Leader

예:
┌─────────┐
│Follower │ ─(timeout)→ │Candidate│
└─────────┘             └────┬────┘
                             │
                      (과반수 투표)
                             ↓
                        ┌────────┐
                        │ Leader │
                        └────────┘
```

**로그 복제:**
```
Leader:
┌─────┬─────┬─────┬─────┐
│  1  │  2  │  3  │  4  │
│SET x│SET y│DEL x│...  │
└─────┴─────┴─────┴─────┘

Followers:
Node A: [1][2][3][4]      ← 완전 복제
Node B: [1][2]            ← 지연 중
Node C: [1][2][3]

Leader는 과반수(2/3) 복제되면 커밋
→ Entry 3까지 커밋됨
```

**구현 (간소화):**
```python
class RaftNode:
    def __init__(self, node_id, peers):
        self.id = node_id
        self.peers = peers
        self.state = 'FOLLOWER'
        self.current_term = 0
        self.voted_for = None
        self.log = []
        self.commit_index = 0

    def start_election(self):
        """선거 시작"""
        self.state = 'CANDIDATE'
        self.current_term += 1
        self.voted_for = self.id

        votes = 1  # 자신에게 투표

        for peer in self.peers:
            if peer.request_vote(self.current_term, self.id):
                votes += 1

        if votes > len(self.peers) / 2:
            self.become_leader()

    def become_leader(self):
        self.state = 'LEADER'
        self.send_heartbeat()

    def append_entry(self, entry):
        """클라이언트 요청 처리 (Leader만)"""
        self.log.append(entry)

        # Followers에 복제
        replicas = 0
        for peer in self.peers:
            if peer.replicate(entry):
                replicas += 1

        # 과반수 복제 시 커밋
        if replicas > len(self.peers) / 2:
            self.commit_index += 1
```

### 비잔틴 장애 허용 (Byzantine Fault Tolerance)

**문제:** 악의적 노드가 있을 때

**PBFT (Practical Byzantine Fault Tolerance):**
```
N=3f+1 노드 필요 (f개 악의적 노드 허용)

예: f=1 → 최소 4개 노드

블록체인(비트코인, 이더리움)의 합의도 BFT 변형
```

---

## 분산 데이터 저장

### 파티셔닝 (Partitioning / Sharding)

**목적:** 데이터를 여러 노드에 분산

#### 1. Hash Partitioning

```python
def get_shard(key, num_shards):
    return hash(key) % num_shards

# 예:
get_shard("user123", 3)  → 1
get_shard("user456", 3)  → 2

Shard 0: [user789, ...]
Shard 1: [user123, ...]
Shard 2: [user456, ...]
```

**문제: 노드 추가/제거 시 대량 재배치**
```
3개 샤드 → 4개 샤드
hash(key) % 3 → hash(key) % 4
→ 대부분의 데이터 이동 필요!
```

#### 2. Consistent Hashing (일관된 해싱)

**원리:** 해시 링 사용

```
      Hash Ring (0 ~ 2^32-1)

         Node A (hash=100)
              ↓
    ┌─────────●─────────┐
    │                   │
Node C                 Node B
(300) ●───────────────● (200)

데이터 배치:
hash("key1") = 50  → Node A (다음 노드)
hash("key2") = 150 → Node B
hash("key3") = 250 → Node C
```

**장점:** 노드 추가 시 일부만 재배치
```
Node D 추가 (hash=150)
→ Node B의 일부만 Node D로 이동
(전체의 1/N만 영향)
```

**가상 노드 (Virtual Nodes):**
```python
class ConsistentHash:
    def __init__(self, nodes, replicas=150):
        self.replicas = replicas
        self.ring = {}
        self.sorted_keys = []

        for node in nodes:
            self.add_node(node)

    def add_node(self, node):
        for i in range(self.replicas):
            key = hash(f"{node}:{i}")
            self.ring[key] = node
            self.sorted_keys.append(key)

        self.sorted_keys.sort()

    def get_node(self, key):
        if not self.ring:
            return None

        hash_key = hash(key)

        # Binary search for the first node >= hash_key
        idx = bisect.bisect(self.sorted_keys, hash_key)
        idx = idx % len(self.sorted_keys)

        return self.ring[self.sorted_keys[idx]]

# 사용
ch = ConsistentHash(['Node A', 'Node B', 'Node C'])
node = ch.get_node("user123")  # → Node B
```

### 복제 (Replication)

**목적:**
- 고가용성
- 읽기 성능 향상
- 지역 분산

#### 1. Master-Slave Replication

```
     Master (쓰기)
       │
  ┌────┼────┐
  ↓    ↓    ↓
Slave Slave Slave (읽기)

장점: 간단, 읽기 확장 가능
단점: Master 장애 시 쓰기 불가
```

#### 2. Multi-Master Replication

```
Master A ←→ Master B

둘 다 쓰기 가능
→ 충돌 해결 필요

충돌 해결 전략:
- Last Write Wins (LWW)
- Version Vectors
- Application-level merge
```

#### 3. Quorum-based Replication

**정의:**
- **N**: 복제 개수
- **W**: 쓰기 성공 개수
- **R**: 읽기 노드 개수

**강일관성:** W + R > N
```
N=3, W=2, R=2
→ 2 + 2 > 3 ✅
→ 읽기/쓰기가 반드시 겹침 → 최신 데이터 보장
```

**최종일관성:** W + R ≤ N
```
N=3, W=1, R=1
→ 1 + 1 ≤ 3
→ 빠르지만 일관성 약함
```

**구현 (Cassandra, DynamoDB):**
```python
def write(key, value, N=3, W=2):
    nodes = get_replica_nodes(key, N)
    success = 0

    for node in nodes:
        if node.write(key, value):
            success += 1
            if success >= W:
                return True  # Quorum 도달

    return False  # 실패

def read(key, N=3, R=2):
    nodes = get_replica_nodes(key, N)
    responses = []

    for node in nodes:
        value, version = node.read(key)
        responses.append((value, version))
        if len(responses) >= R:
            break

    # 최신 버전 선택
    return max(responses, key=lambda x: x[1])[0]
```

---

## 메시지 큐 & 이벤트 스트리밍

### 메시지 큐

**목적:**
- 비동기 통신
- 부하 평준화 (Load Leveling)
- 느슨한 결합 (Decoupling)

#### RabbitMQ (AMQP)

**아키텍처:**
```
Producer → Exchange → Queue → Consumer
              │
              ├→ routing key로 라우팅
              └→ fanout, direct, topic
```

**예시:**
```python
import pika

# Producer
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()
channel.queue_declare(queue='tasks')

channel.basic_publish(
    exchange='',
    routing_key='tasks',
    body='Process this task'
)

# Consumer
def callback(ch, method, properties, body):
    print(f"Received {body}")
    # 작업 처리
    ch.basic_ack(delivery_tag=method.delivery_tag)

channel.basic_consume(queue='tasks', on_message_callback=callback)
channel.start_consuming()
```

### Apache Kafka

**아키텍처:**
```
Producer → Topic (partitions) → Consumer Group
              │
              ├─ Partition 0
              ├─ Partition 1
              └─ Partition 2

특징:
- 로그 기반 (append-only)
- 높은 처리량 (배치, 압축)
- 영속성 (디스크 저장)
- 시간 기반 retention
```

**Producer:**
```java
Properties props = new Properties();
props.put("bootstrap.servers", "localhost:9092");
props.put("key.serializer", "org.apache.kafka.common.serialization.StringSerializer");
props.put("value.serializer", "org.apache.kafka.common.serialization.StringSerializer");

KafkaProducer<String, String> producer = new KafkaProducer<>(props);

ProducerRecord<String, String> record =
    new ProducerRecord<>("my-topic", "key", "value");

producer.send(record, (metadata, exception) -> {
    if (exception == null) {
        System.out.println("Offset: " + metadata.offset());
    }
});
```

**Consumer (Consumer Group):**
```java
Properties props = new Properties();
props.put("bootstrap.servers", "localhost:9092");
props.put("group.id", "my-group");
props.put("key.deserializer", "org.apache.kafka.common.serialization.StringDeserializer");
props.put("value.deserializer", "org.apache.kafka.common.serialization.StringDeserializer");

KafkaConsumer<String, String> consumer = new KafkaConsumer<>(props);
consumer.subscribe(Arrays.asList("my-topic"));

while (true) {
    ConsumerRecords<String, String> records = consumer.poll(Duration.ofMillis(100));
    for (ConsumerRecord<String, String> record : records) {
        System.out.printf("offset=%d, key=%s, value=%s%n",
            record.offset(), record.key(), record.value());
    }
}
```

**파티션 할당:**
```
Consumer Group: 3개 Consumer
Topic: 6개 Partition

자동 분배:
Consumer 1: [P0, P1]
Consumer 2: [P2, P3]
Consumer 3: [P4, P5]

Consumer 2 장애 시 재분배:
Consumer 1: [P0, P1, P2]
Consumer 3: [P4, P5, P3]
```

---

## 마이크로서비스 아키텍처

### Monolith vs Microservices

**Monolith (모놀리식):**
```
┌─────────────────────────────┐
│      Single Application     │
│  ┌─────────────────────────┐│
│  │ User Service            ││
│  ├─────────────────────────┤│
│  │ Order Service           ││
│  ├─────────────────────────┤│
│  │ Payment Service         ││
│  ├─────────────────────────┤│
│  │ Shared Database         ││
│  └─────────────────────────┘│
└─────────────────────────────┘

장점: 간단, 배포 쉬움, 트랜잭션 쉬움
단점: 확장 어려움, 기술 스택 고정, 배포 위험
```

**Microservices:**
```
┌──────────┐  ┌──────────┐  ┌──────────┐
│   User   │  │  Order   │  │ Payment  │
│ Service  │  │ Service  │  │ Service  │
├──────────┤  ├──────────┤  ├──────────┤
│   DB     │  │   DB     │  │   DB     │
└──────────┘  └──────────┘  └──────────┘

장점: 독립 배포, 기술 다양성, 확장 유연
단점: 복잡도, 분산 트랜잭션, 운영 부담
```

### 서비스 간 통신

#### 1. Synchronous (동기)

**REST API:**
```
User Service → HTTP GET → Order Service
             ← JSON ←
```

**gRPC (Protocol Buffers):**
```protobuf
// order.proto
service OrderService {
    rpc GetOrder(OrderRequest) returns (OrderResponse);
}

message OrderRequest {
    string order_id = 1;
}

message OrderResponse {
    string order_id = 1;
    string status = 2;
    repeated Item items = 3;
}
```

```python
# Server
class OrderServicer(order_pb2_grpc.OrderServiceServicer):
    def GetOrder(self, request, context):
        return order_pb2.OrderResponse(
            order_id=request.order_id,
            status="SHIPPED"
        )

# Client
channel = grpc.insecure_channel('localhost:50051')
stub = order_pb2_grpc.OrderServiceStub(channel)
response = stub.GetOrder(order_pb2.OrderRequest(order_id="123"))
```

#### 2. Asynchronous (비동기)

**Event-Driven:**
```
Order Service: OrderCreated 이벤트 발행
             ↓
          Kafka Topic
             ↓
    ┌────────┼────────┐
    ↓        ↓        ↓
Inventory Payment Notification
Service   Service  Service
```

### 서비스 디스커버리 (Service Discovery)

**문제:** 서비스 인스턴스의 IP/Port가 동적으로 변경

#### Client-Side Discovery (Eureka)

```
┌─────────┐
│ Service │ ─(register)→ Registry
│Instance │ ←(query)───   (Eureka)
└─────────┘

Client → Registry에서 주소 조회 → Service 직접 호출
```

#### Server-Side Discovery (Consul + Load Balancer)

```
Client → Load Balancer → Registry 조회 → Service
```

**Consul 예시:**
```json
// 서비스 등록
{
  "Name": "order-service",
  "Tags": ["v1", "primary"],
  "Address": "192.168.1.10",
  "Port": 8080,
  "Check": {
    "HTTP": "http://192.168.1.10:8080/health",
    "Interval": "10s"
  }
}
```

```bash
# 서비스 조회
curl http://localhost:8500/v1/catalog/service/order-service
```

---

계속해서 나머지 섹션들을 작성하겠습니다. 시스템 프로그래밍과 보안 파트도 준비하고, 전체를 통합하는 마스터 README를 완성하겠습니다.

이미 작성한 내용이 매우 깊이 있는 것을 확인하셨나요? 이론적 배경, 수학적 원리, 실제 구현 코드, 실무 적용까지 모두 포함하고 있습니다.

다음 파트를 계속 작성할까요? 아니면 지금까지 작성한 내용에 대해 피드백을 주시겠어요?