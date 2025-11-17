# 4️⃣ 데이터베이스 (Databases) 완전 정복

> 이것만 보면 데이터베이스는 끝!

---

## 📚 목차

1. [데이터베이스 기본 개념](#데이터베이스-기본-개념)
2. [SQL 기초](#sql-기초)
3. [정규화](#정규화)
4. [인덱스](#인덱스)
5. [트랜잭션](#트랜잭션)
6. [격리 수준](#격리-수준)
7. [데이터베이스 설계](#데이터베이스-설계)
8. [NoSQL](#nosql)
9. [면접 필수 질문](#면접-필수-질문)

---

## 데이터베이스 기본 개념

### 데이터베이스란?

**정의:** 구조화된 데이터의 집합

**DBMS (Database Management System):**
- MySQL, PostgreSQL, Oracle
- MongoDB, Redis, Cassandra

### 관계형 데이터베이스 (RDBMS)

**특징:**
- **테이블 (Table)**: 행(Row)과 열(Column)
- **관계 (Relation)**: 테이블 간 연결
- **SQL**: 표준 쿼리 언어

**예시:**
```
Users 테이블
┌────┬─────────┬─────────┬─────┐
│ ID │  Name   │  Email  │ Age │
├────┼─────────┼─────────┼─────┤
│  1 │  John   │ j@...   │  25 │
│  2 │  Jane   │ ja@...  │  30 │
└────┴─────────┴─────────┴─────┘

Orders 테이블
┌────┬─────────┬────────┬────────┐
│ ID │ User_ID │Product │ Price  │
├────┼─────────┼────────┼────────┤
│  1 │    1    │  Book  │  10.00 │
│  2 │    1    │  Pen   │   2.00 │
│  3 │    2    │  Book  │  10.00 │
└────┴─────────┴────────┴────────┘
```

### 키 (Key)

#### 1. Primary Key (기본키)

**특징:**
- 유일성 (Unique)
- NULL 불가
- 테이블당 1개

```sql
CREATE TABLE users (
    id INT PRIMARY KEY,  -- 기본키
    email VARCHAR(100) UNIQUE,
    name VARCHAR(50)
);
```

#### 2. Foreign Key (외래키)

**특징:**
- 다른 테이블의 Primary Key 참조
- 관계 설정

```sql
CREATE TABLE orders (
    id INT PRIMARY KEY,
    user_id INT,
    product VARCHAR(100),
    FOREIGN KEY (user_id) REFERENCES users(id)
);
```

#### 3. Candidate Key (후보키)

기본키가 될 수 있는 속성들

#### 4. Super Key (슈퍼키)

유일성을 만족하는 속성 집합

---

## SQL 기초

### DDL (Data Definition Language)

#### CREATE
```sql
-- 테이블 생성
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    email VARCHAR(100) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

#### ALTER
```sql
-- 컬럼 추가
ALTER TABLE users ADD COLUMN age INT;

-- 컬럼 수정
ALTER TABLE users MODIFY COLUMN age TINYINT;

-- 컬럼 삭제
ALTER TABLE users DROP COLUMN age;
```

#### DROP
```sql
-- 테이블 삭제
DROP TABLE users;

-- 데이터베이스 삭제
DROP DATABASE mydb;
```

### DML (Data Manipulation Language)

#### SELECT
```sql
-- 전체 조회
SELECT * FROM users;

-- 특정 컬럼
SELECT username, email FROM users;

-- 조건
SELECT * FROM users WHERE age >= 18;

-- 정렬
SELECT * FROM users ORDER BY created_at DESC;

-- 제한
SELECT * FROM users LIMIT 10;

-- DISTINCT (중복 제거)
SELECT DISTINCT city FROM users;
```

#### INSERT
```sql
-- 단일 삽입
INSERT INTO users (username, email, age)
VALUES ('john', 'john@example.com', 25);

-- 다중 삽입
INSERT INTO users (username, email, age) VALUES
    ('jane', 'jane@example.com', 30),
    ('bob', 'bob@example.com', 28);
```

#### UPDATE
```sql
-- 업데이트
UPDATE users
SET age = 26, email = 'newemail@example.com'
WHERE id = 1;

-- ⚠️ WHERE 없으면 모든 행 업데이트!
```

#### DELETE
```sql
-- 삭제
DELETE FROM users WHERE id = 1;

-- 전체 삭제
TRUNCATE TABLE users;  -- 빠름, 롤백 불가
DELETE FROM users;      -- 느림, 롤백 가능
```

### 조건절 (WHERE)

```sql
-- 비교 연산자
SELECT * FROM users WHERE age = 25;
SELECT * FROM users WHERE age > 18;
SELECT * FROM users WHERE age BETWEEN 20 AND 30;

-- 논리 연산자
SELECT * FROM users WHERE age > 18 AND city = 'Seoul';
SELECT * FROM users WHERE city = 'Seoul' OR city = 'Busan';
SELECT * FROM users WHERE NOT city = 'Seoul';

-- IN
SELECT * FROM users WHERE city IN ('Seoul', 'Busan', 'Daegu');

-- LIKE (패턴 매칭)
SELECT * FROM users WHERE name LIKE 'J%';     -- J로 시작
SELECT * FROM users WHERE name LIKE '%n';     -- n으로 끝남
SELECT * FROM users WHERE name LIKE '%oh%';   -- oh 포함

-- NULL 체크
SELECT * FROM users WHERE email IS NULL;
SELECT * FROM users WHERE email IS NOT NULL;
```

### JOIN

#### INNER JOIN
```sql
-- 양쪽 모두 매칭되는 행만
SELECT u.username, o.product, o.price
FROM users u
INNER JOIN orders o ON u.id = o.user_id;

┌────────┐     ┌────────┐
│ Users  │     │ Orders │
│   1    │────→│   1    │  결과: 포함
│   2    │  ×  │        │  결과: 제외
└────────┘     └────────┘
```

#### LEFT JOIN
```sql
-- 왼쪽 테이블의 모든 행 + 매칭되는 오른쪽 행
SELECT u.username, o.product
FROM users u
LEFT JOIN orders o ON u.id = o.user_id;

┌────────┐     ┌────────┐
│ Users  │     │ Orders │
│   1    │────→│   1    │  결과: username + product
│   2    │  ×  │        │  결과: username + NULL
└────────┘     └────────┘
```

#### RIGHT JOIN
```sql
-- 오른쪽 테이블의 모든 행 + 매칭되는 왼쪽 행
SELECT u.username, o.product
FROM users u
RIGHT JOIN orders o ON u.id = o.user_id;
```

#### FULL OUTER JOIN
```sql
-- 양쪽 모두 포함 (MySQL은 지원 안 함)
SELECT u.username, o.product
FROM users u
FULL OUTER JOIN orders o ON u.id = o.user_id;

-- MySQL 대안: UNION
SELECT u.username, o.product FROM users u LEFT JOIN orders o ON u.id = o.user_id
UNION
SELECT u.username, o.product FROM users u RIGHT JOIN orders o ON u.id = o.user_id;
```

### 집계 함수 (Aggregate Functions)

```sql
-- COUNT
SELECT COUNT(*) FROM users;
SELECT COUNT(DISTINCT city) FROM users;

-- SUM
SELECT SUM(price) FROM orders;

-- AVG
SELECT AVG(age) FROM users;

-- MIN, MAX
SELECT MIN(age), MAX(age) FROM users;

-- GROUP BY
SELECT city, COUNT(*) as user_count
FROM users
GROUP BY city;

-- HAVING (그룹 조건)
SELECT city, COUNT(*) as user_count
FROM users
GROUP BY city
HAVING COUNT(*) > 10;
```

### 서브쿼리 (Subquery)

```sql
-- WHERE 절 서브쿼리
SELECT * FROM users
WHERE id IN (SELECT user_id FROM orders WHERE price > 100);

-- FROM 절 서브쿼리
SELECT city, avg_age FROM (
    SELECT city, AVG(age) as avg_age
    FROM users
    GROUP BY city
) AS city_stats
WHERE avg_age > 30;

-- SELECT 절 서브쿼리 (스칼라 서브쿼리)
SELECT username,
       (SELECT COUNT(*) FROM orders WHERE orders.user_id = users.id) as order_count
FROM users;
```

---

## 정규화

### 정규화란?

**목적:**
- 데이터 중복 최소화
- 이상 현상 (Anomaly) 방지
- 데이터 무결성 향상

### 이상 현상

#### 1. 삽입 이상 (Insertion Anomaly)
```
┌────┬─────────┬───────┬──────────┐
│ ID │  Name   │Course │Professor │
├────┼─────────┼───────┼──────────┤
│  1 │  John   │  DB   │   Kim    │
│  2 │  Jane   │  OS   │   Lee    │
└────┴─────────┴───────┴──────────┘

문제: 수강생 없는 과목은 저장 불가
```

#### 2. 갱신 이상 (Update Anomaly)
```
┌────┬─────────┬───────┬──────────┐
│  1 │  John   │  DB   │   Kim    │
│  2 │  Jane   │  DB   │   Kim    │  ← 교수 변경 시 모두 수정
└────┴─────────┴───────┴──────────┘

문제: 일부만 수정 시 불일치
```

#### 3. 삭제 이상 (Deletion Anomaly)
```
문제: 마지막 수강생 삭제 시 과목 정보도 삭제됨
```

### 정규화 단계

#### 제1정규형 (1NF)

**조건:** 모든 속성이 원자값 (Atomic)

**Before (비정규형):**
```
┌────┬─────────┬──────────────┐
│ ID │  Name   │   Phones     │
├────┼─────────┼──────────────┤
│  1 │  John   │010-1111,     │
│    │         │010-2222      │  ← 다중값!
└────┴─────────┴──────────────┘
```

**After (1NF):**
```
┌────┬─────────┬────────────┐
│ ID │  Name   │   Phone    │
├────┼─────────┼────────────┤
│  1 │  John   │ 010-1111   │
│  1 │  John   │ 010-2222   │
└────┴─────────┴────────────┘
```

#### 제2정규형 (2NF)

**조건:** 1NF + 부분 함수 종속 제거

**함수 종속:**
```
학생ID, 과목ID → 성적  (완전 함수 종속)
학생ID, 과목ID → 과목명  (부분 함수 종속, 과목ID만으로 결정)
```

**Before (1NF):**
```
┌─────────┬────────┬──────┬──────────┐
│Student  │Course  │Grade │CourseName│
├─────────┼────────┼──────┼──────────┤
│   1     │  101   │  A   │   DB     │
│   1     │  102   │  B   │   OS     │
└─────────┴────────┴──────┴──────────┘
         복합키              ↑ 부분 종속
```

**After (2NF):**
```
Enrollment (수강)          Course (과목)
┌─────────┬────────┬──────┐  ┌────────┬──────────┐
│Student  │Course  │Grade │  │Course  │CourseName│
├─────────┼────────┼──────┤  ├────────┼──────────┤
│   1     │  101   │  A   │  │  101   │   DB     │
│   1     │  102   │  B   │  │  102   │   OS     │
└─────────┴────────┴──────┘  └────────┴──────────┘
```

#### 제3정규형 (3NF)

**조건:** 2NF + 이행 함수 종속 제거

**이행 종속:**
```
학생ID → 학과  → 학과위치
(학생ID → 학과위치는 이행 종속)
```

**Before (2NF):**
```
┌─────────┬──────┬──────────┐
│Student  │Dept  │DeptLoc   │
├─────────┼──────┼──────────┤
│   1     │  CS  │  A동     │
│   2     │  CS  │  A동     │  ← 중복!
└─────────┴──────┴──────────┘
         ↓        ↑
         이행 종속
```

**After (3NF):**
```
Student (학생)            Department (학과)
┌─────────┬──────┐        ┌──────┬──────────┐
│Student  │Dept  │        │Dept  │DeptLoc   │
├─────────┼──────┤        ├──────┼──────────┤
│   1     │  CS  │        │  CS  │  A동     │
│   2     │  CS  │        │  EE  │  B동     │
└─────────┴──────┘        └──────┴──────────┘
```

#### BCNF (Boyce-Codd Normal Form)

**조건:** 모든 결정자가 후보키

**예시:**
```
Before:
┌───────┬──────┬─────────┐
│Student│Course│Professor│
├───────┼──────┼─────────┤
│  John │  DB  │   Kim   │
│  Jane │  OS  │   Lee   │
└───────┴──────┴─────────┘

문제: Professor → Course (교수가 과목 결정)
      but Professor는 후보키가 아님!

After:
┌───────┬─────────┐      ┌─────────┬──────┐
│Student│Professor│      │Professor│Course│
├───────┼─────────┤      ├─────────┼──────┤
│  John │   Kim   │      │   Kim   │  DB  │
│  Jane │   Lee   │      │   Lee   │  OS  │
└───────┴─────────┘      └─────────┴──────┘
```

---

## 인덱스

### 인덱스란?

**정의:** 데이터 검색 속도를 높이는 자료구조

**비유:** 책의 색인 (Index)

### 인덱스 동작 원리

**Without Index:**
```
SELECT * FROM users WHERE id = 100;

Full Table Scan
┌────┐
│  1 │ ← 확인
│  2 │ ← 확인
│  3 │ ← 확인
│ ...│
│100 │ ← 찾음! (100번 확인)
└────┘
```

**With Index:**
```
B-Tree Index
      [50]
      /  \
  [25]    [75]
   / \    /  \
[10][40][60][100] ← 3-4번만에 찾음!
```

### B-Tree 인덱스

**구조:**
```
         Root
       [30, 60]
       /   |   \
     /     |     \
 [10,20] [40,50] [70,80]
   |        |        |
  Data     Data     Data
```

**특징:**
- 균형 트리
- 정렬된 상태 유지
- 범위 검색 효율적

### 인덱스 생성

```sql
-- 단일 컬럼 인덱스
CREATE INDEX idx_username ON users(username);

-- 복합 인덱스
CREATE INDEX idx_name_age ON users(name, age);

-- 유니크 인덱스
CREATE UNIQUE INDEX idx_email ON users(email);

-- 인덱스 삭제
DROP INDEX idx_username ON users;

-- 인덱스 조회
SHOW INDEX FROM users;
```

### 인덱스 사용 예시

```sql
-- ✅ 인덱스 사용
SELECT * FROM users WHERE username = 'john';

-- ✅ 복합 인덱스 (name, age) 사용
SELECT * FROM users WHERE name = 'John' AND age = 25;

-- ⚠️ 인덱스 일부만 사용
SELECT * FROM users WHERE name = 'John';  -- OK
SELECT * FROM users WHERE age = 25;       -- 인덱스 미사용 (뒤쪽 컬럼)

-- ❌ 인덱스 미사용
SELECT * FROM users WHERE YEAR(created_at) = 2023;  -- 함수 사용
SELECT * FROM users WHERE username LIKE '%john%';   -- 앞 와일드카드
```

### 클러스터 인덱스 vs 논클러스터 인덱스

#### 클러스터 인덱스 (Clustered Index)

**특징:**
- 물리적으로 데이터 정렬
- 테이블당 1개만
- 기본키에 자동 생성

```
실제 데이터가 인덱스 순서대로 저장됨
┌────┬─────────┬───────┐
│ 1  │  Alice  │  ...  │
│ 2  │  Bob    │  ...  │
│ 3  │  Charlie│  ...  │
└────┴─────────┴───────┘
```

#### 논클러스터 인덱스 (Non-Clustered Index)

**특징:**
- 별도의 인덱스 테이블
- 여러 개 생성 가능
- 인덱스 → 데이터 포인터

```
Index               Data
┌───────┬───┐      ┌────┬─────────┐
│ Alice │ →─┼─────→│ 1  │  Alice  │
│ Bob   │ →─┼─┐    │ 3  │ Charlie │
│Charlie│ →─┼─┘    │ 2  │  Bob    │
└───────┴───┘      └────┴─────────┘
```

### 인덱스 최적화

**장점:**
- 검색 속도 향상 (특히 WHERE, JOIN, ORDER BY)
- 유니크 제약으로 데이터 무결성

**단점:**
- 추가 저장 공간
- INSERT, UPDATE, DELETE 느려짐 (인덱스도 갱신)
- 너무 많으면 옵티마이저 혼란

**Best Practice:**
1. **선택도(Selectivity) 높은 컬럼**: 중복 값 적음
   ```sql
   -- Good: email (유니크)
   CREATE INDEX idx_email ON users(email);

   -- Bad: gender (M/F 2개뿐)
   ```

2. **WHERE, JOIN 자주 사용하는 컬럼**

3. **복합 인덱스 순서**: 선택도 높은 것부터
   ```sql
   -- 쿼리: WHERE city = 'Seoul' AND age > 20
   -- Good
   CREATE INDEX idx_city_age ON users(city, age);
   ```

4. **커버링 인덱스**: SELECT 컬럼도 인덱스에 포함
   ```sql
   CREATE INDEX idx_cover ON users(username, email);
   SELECT username, email FROM users WHERE username = 'john';
   -- → 인덱스만으로 해결 (데이터 테이블 접근 불필요)
   ```

### 실행 계획 (EXPLAIN)

```sql
EXPLAIN SELECT * FROM users WHERE username = 'john';

┌────┬────────┬───────┬──────┬─────────┬──────┬─────┬────────┐
│ id │  type  │ key   │ rows │filtered │ Extra│     │        │
├────┼────────┼───────┼──────┼─────────┼──────┼─────┼────────┤
│ 1  │  ref   │idx_un │  1   │  100.00 │ ...  │     │        │
└────┴────────┴───────┴──────┴─────────┴──────┴─────┴────────┘

type:
- ALL: Full Table Scan (느림)
- index: Index Scan
- range: 범위 검색
- ref: 인덱스 사용 (빠름)
- const: Primary Key/Unique (가장 빠름)
```

---

## 트랜잭션

### 트랜잭션이란?

**정의:** 하나의 논리적 작업 단위

**예시:** 계좌 이체
```sql
START TRANSACTION;

UPDATE accounts SET balance = balance - 100 WHERE id = 1;  -- A 출금
UPDATE accounts SET balance = balance + 100 WHERE id = 2;  -- B 입금

COMMIT;  -- 성공 시 확정
-- 또는
ROLLBACK;  -- 실패 시 취소
```

### ACID 속성

#### A - Atomicity (원자성)

**All or Nothing**: 모두 성공 또는 모두 실패

```sql
BEGIN;
UPDATE accounts SET balance = balance - 100 WHERE id = 1;
-- ❌ 오류 발생!
UPDATE accounts SET balance = balance + 100 WHERE id = 2;
ROLLBACK;  -- 모두 취소됨
```

#### C - Consistency (일관성)

**무결성 유지**: 트랜잭션 전후 일관된 상태

```sql
-- 제약: balance >= 0
UPDATE accounts SET balance = balance - 1000 WHERE id = 1;
-- ❌ balance < 0 → 롤백!
```

#### I - Isolation (격리성)

**동시 실행 시 간섭 없음**

```sql
-- Transaction 1
UPDATE accounts SET balance = balance - 100 WHERE id = 1;

-- Transaction 2 (동시 실행)
SELECT balance FROM accounts WHERE id = 1;
-- → 격리 수준에 따라 다른 결과
```

#### D - Durability (지속성)

**커밋 후 영구 저장**

```sql
COMMIT;
-- → 서버 다운되어도 데이터 유지 (로그 기반)
```

### 트랜잭션 상태

```
┌─────────┐
│  Active │  활성 (실행 중)
└────┬────┘
     │
     ├─→ ┌───────────────┐
     │   │Partially      │
     │   │Committed      │
     │   └───────┬───────┘
     │           │
     │           ↓
     │       ┌────────┐
     └──────→│Committed│  커밋 (완료)
     │       └────────┘
     │
     └─→ ┌────────┐
         │ Failed │  실패
         └────┬───┘
              │
              ↓
         ┌────────┐
         │ Aborted│  중단 (롤백)
         └────────┘
```

### 동시성 제어 문제

#### 1. Dirty Read (오손 읽기)

```
T1: UPDATE balance = 100
T2: SELECT balance → 100  ❌ (T1 미커밋)
T1: ROLLBACK
→ T2가 존재하지 않는 데이터 읽음
```

#### 2. Non-Repeatable Read (반복 불가능 읽기)

```
T1: SELECT balance → 100
T2: UPDATE balance = 200
T2: COMMIT
T1: SELECT balance → 200  ❌ (값이 변함)
```

#### 3. Phantom Read (유령 읽기)

```
T1: SELECT COUNT(*) WHERE age > 20 → 10
T2: INSERT age=25
T2: COMMIT
T1: SELECT COUNT(*) WHERE age > 20 → 11  ❌ (행이 추가됨)
```

---

## 격리 수준

### Isolation Level

| 격리 수준 | Dirty Read | Non-Repeatable | Phantom Read | 성능 |
|----------|------------|----------------|--------------|------|
| READ UNCOMMITTED | O | O | O | 최고 |
| READ COMMITTED | X | O | O | 높음 |
| REPEATABLE READ | X | X | O | 보통 |
| SERIALIZABLE | X | X | X | 낮음 |

### 1. READ UNCOMMITTED

**특징:** 커밋 안 된 데이터도 읽음

```sql
SET TRANSACTION ISOLATION LEVEL READ UNCOMMITTED;

-- T1
UPDATE accounts SET balance = 100 WHERE id = 1;

-- T2
SELECT balance FROM accounts WHERE id = 1;
-- → 100 (커밋 전인데 읽음!)
```

**문제:** Dirty Read 발생

### 2. READ COMMITTED

**특징:** 커밋된 데이터만 읽음 (대부분 DBMS 기본값)

```sql
SET TRANSACTION ISOLATION LEVEL READ COMMITTED;

-- T1
UPDATE accounts SET balance = 100 WHERE id = 1;

-- T2
SELECT balance FROM accounts WHERE id = 1;
-- → 50 (커밋 전이라 이전 값)

-- T1
COMMIT;

-- T2
SELECT balance FROM accounts WHERE id = 1;
-- → 100 (커밋 후 새 값)
```

**해결:** Dirty Read 방지
**문제:** Non-Repeatable Read 발생

### 3. REPEATABLE READ

**특징:** 트랜잭션 시작 시점의 스냅샷 읽음 (MySQL InnoDB 기본값)

```sql
SET TRANSACTION ISOLATION LEVEL REPEATABLE READ;

-- T1
BEGIN;
SELECT balance FROM accounts WHERE id = 1;  -- → 50

-- T2
UPDATE accounts SET balance = 100 WHERE id = 1;
COMMIT;

-- T1
SELECT balance FROM accounts WHERE id = 1;  -- → 50 (변경 안 됨!)
COMMIT;
```

**해결:** Non-Repeatable Read 방지
**문제:** Phantom Read 발생 (일부 DBMS)

### 4. SERIALIZABLE

**특징:** 완전히 직렬화 (순차 실행과 동일)

```sql
SET TRANSACTION ISOLATION LEVEL SERIALIZABLE;

-- T1
BEGIN;
SELECT * FROM accounts WHERE age > 20;

-- T2
INSERT INTO accounts (age) VALUES (25);
-- ⏸️ 대기 (T1이 끝날 때까지)

-- T1
COMMIT;

-- T2
-- → 이제 실행됨
```

**해결:** 모든 문제 방지
**문제:** 성능 저하, 데드락 가능성

### 실무 선택 기준

```
일반적인 웹 애플리케이션 → READ COMMITTED
금융, 재고 관리 → REPEATABLE READ
극도로 정확성 필요 → SERIALIZABLE
```

---

## 데이터베이스 설계

### ER 다이어그램 (Entity-Relationship Diagram)

**구성 요소:**
- **Entity (개체)**: 사각형
- **Attribute (속성)**: 타원
- **Relationship (관계)**: 마름모

```
┌─────────┐              ┌─────────┐
│  User   │──<  writes  >──│  Post   │
└─────────┘              └─────────┘
    │                        │
 ┌──┴──┐                 ┌──┴──┐
 │ ID  │                 │ ID  │
 │Name │                 │Title│
 └─────┘                 └─────┘
```

### 관계 유형

#### 1:1 (One-to-One)

```sql
-- 사용자 : 프로필 = 1:1
Users                   Profiles
┌────┬──────┐          ┌────┬────────┬─────┐
│ id │ name │          │ id │user_id │ bio │
├────┼──────┤          ├────┼────────┼─────┤
│  1 │John  │────1:1───│  1 │   1    │ ... │
└────┴──────┘          └────┴────────┴─────┘
```

#### 1:N (One-to-Many)

```sql
-- 사용자 : 게시글 = 1:N
Users                   Posts
┌────┬──────┐          ┌────┬────────┬───────┐
│ id │ name │          │ id │user_id │ title │
├────┼──────┤          ├────┼────────┼───────┤
│  1 │John  │────1:N───│  1 │   1    │  ...  │
└────┴──────┘       ├──│  2 │   1    │  ...  │
                    └──│  3 │   1    │  ...  │
                       └────┴────────┴───────┘
```

#### N:M (Many-to-Many)

```sql
-- 학생 : 수업 = N:M → 중간 테이블 필요
Students        Enrollments      Courses
┌────┬──────┐  ┌────┬────┬────┐ ┌────┬──────┐
│ id │ name │  │sid │cid │grade│ │ id │ name │
├────┼──────┤  ├────┼────┼────┤ ├────┼──────┤
│  1 │John  │──│ 1  │101 │  A  │──│101 │  DB  │
│  2 │Jane  │──│ 1  │102 │  B  │  │102 │  OS  │
└────┴──────┘  │ 2  │101 │  A  │──└────┴──────┘
               └────┴────┴────┘
```

### 데이터 타입 선택

#### 숫자
```sql
TINYINT      -- 1바이트 (-128 ~ 127)
SMALLINT     -- 2바이트
INT          -- 4바이트
BIGINT       -- 8바이트
DECIMAL(10,2)-- 고정 소수점 (금액)
FLOAT, DOUBLE-- 부동 소수점
```

#### 문자열
```sql
CHAR(10)     -- 고정 길이 (패딩)
VARCHAR(100) -- 가변 길이
TEXT         -- 긴 텍스트 (65,535)
MEDIUMTEXT   -- 16MB
LONGTEXT     -- 4GB
```

#### 날짜/시간
```sql
DATE         -- 날짜 (YYYY-MM-DD)
TIME         -- 시간 (HH:MM:SS)
DATETIME     -- 날짜+시간
TIMESTAMP    -- Unix timestamp
YEAR         -- 연도
```

#### 이진 데이터
```sql
BINARY(16)   -- 고정 길이
VARBINARY(100)-- 가변 길이
BLOB         -- 이진 데이터
```

### Best Practice

```sql
CREATE TABLE users (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,  -- 충분히 큰 ID
    uuid CHAR(36) UNIQUE NOT NULL,                  -- UUID (외부 노출용)
    email VARCHAR(255) UNIQUE NOT NULL,
    username VARCHAR(50) NOT NULL,
    password_hash CHAR(60) NOT NULL,                -- bcrypt
    age TINYINT UNSIGNED,                           -- 0-255
    balance DECIMAL(10,2) DEFAULT 0.00,             -- 금액
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

    INDEX idx_email (email),
    INDEX idx_username (username),
    INDEX idx_created_at (created_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
```

---

## NoSQL

### NoSQL이란?

**Not Only SQL**: 관계형 DB가 아닌 다양한 데이터베이스

**특징:**
- 유연한 스키마
- 수평 확장 (Sharding)
- 높은 성능
- 분산 시스템

### NoSQL 유형

#### 1. Key-Value Store

**예시:** Redis, DynamoDB

```
┌──────────┬────────────┐
│   Key    │   Value    │
├──────────┼────────────┤
│ user:1   │ {json...}  │
│ session:│ "abc123"   │
└──────────┴────────────┘
```

**사용 사례:**
- 캐싱
- 세션 저장
- 실시간 랭킹

```python
# Redis 예시
import redis

r = redis.Redis()
r.set('user:1:name', 'John')
r.get('user:1:name')  # → 'John'

# Expiration
r.setex('session:abc', 3600, 'user_data')  # 1시간 후 삭제
```

#### 2. Document Store

**예시:** MongoDB, Couchbase

```json
{
  "_id": "507f1f77bcf86cd799439011",
  "name": "John",
  "email": "john@example.com",
  "posts": [
    {
      "title": "First Post",
      "content": "...",
      "tags": ["tech", "db"]
    }
  ]
}
```

**사용 사례:**
- 콘텐츠 관리
- 사용자 프로필
- 카탈로그

```javascript
// MongoDB 예시
db.users.insertOne({
  name: "John",
  email: "john@example.com",
  posts: []
});

db.users.find({ name: "John" });

db.users.updateOne(
  { _id: ObjectId("...") },
  { $push: { posts: { title: "New Post", content: "..." } } }
);
```

#### 3. Column-Family Store

**예시:** Cassandra, HBase

```
Row Key: user:1
┌───────────┬───────────┬───────────┐
│  Column   │  Column   │  Column   │
│  Family   │  Family   │  Family   │
├───────────┼───────────┼───────────┤
│ profile:  │ posts:    │ friends:  │
│  name     │  post1    │  friend1  │
│  email    │  post2    │  friend2  │
└───────────┴───────────┴───────────┘
```

**사용 사례:**
- 시계열 데이터
- IoT 센서 데이터
- 로그 분석

#### 4. Graph Database

**예시:** Neo4j, Amazon Neptune

```
(John)-[:FRIEND]->(Jane)
(John)-[:LIKES]->(Post1)
(Jane)-[:WROTE]->(Post1)
```

**사용 사례:**
- 소셜 네트워크
- 추천 시스템
- 지식 그래프

```cypher
// Neo4j (Cypher 쿼리)
CREATE (john:Person {name: 'John'})
CREATE (jane:Person {name: 'Jane'})
CREATE (john)-[:FRIEND]->(jane)

// 친구의 친구 찾기
MATCH (me:Person {name: 'John'})-[:FRIEND]->(friend)-[:FRIEND]->(fof)
WHERE NOT (me)-[:FRIEND]->(fof)
RETURN fof.name
```

### SQL vs NoSQL

| 항목 | SQL | NoSQL |
|------|-----|-------|
| 스키마 | 고정 | 유연 |
| 확장 | 수직 (Scale Up) | 수평 (Scale Out) |
| 트랜잭션 | ACID 보장 | 최종 일관성 |
| JOIN | 지원 | 제한적 |
| 사용 사례 | 금융, ERP | SNS, IoT, 캐싱 |

### CAP 정리

**분산 시스템은 3가지 중 2가지만 보장 가능**

- **C (Consistency)**: 일관성
- **A (Availability)**: 가용성
- **P (Partition Tolerance)**: 분할 내성

```
       C
      / \
     /   \
    /  ?  \
   /       \
  A ────── P

CP: 일관성 + 분할 내성 (MongoDB, HBase)
AP: 가용성 + 분할 내성 (Cassandra, DynamoDB)
CA: 일관성 + 가용성 (RDBMS) - 분산 환경에서 불가능
```

---

## 면접 필수 질문

### Q1: 정규화가 필요한 이유는?

**A:**
- **데이터 중복 최소화**: 저장 공간 절약
- **이상 현상 방지**: 삽입/갱신/삭제 이상
- **데이터 무결성 향상**: 일관성 유지

### Q2: 인덱스의 장단점은?

**A:**
**장점:**
- 검색 속도 향상 (O(log n))
- 정렬, 그룹핑 효율적

**단점:**
- 추가 저장 공간
- INSERT, UPDATE, DELETE 느려짐
- 잘못 사용 시 오히려 성능 저하

### Q3: 트랜잭션의 ACID 속성을 설명하시오.

**A:**
- **Atomicity**: All or Nothing (원자성)
- **Consistency**: 무결성 유지 (일관성)
- **Isolation**: 동시 실행 시 간섭 없음 (격리성)
- **Durability**: 커밋 후 영구 저장 (지속성)

### Q4: 격리 수준에 따른 문제는?

**A:**
| 격리 수준 | Dirty Read | Non-Repeatable | Phantom Read |
|----------|------------|----------------|--------------|
| READ UNCOMMITTED | O | O | O |
| READ COMMITTED | X | O | O |
| REPEATABLE READ | X | X | O |
| SERIALIZABLE | X | X | X |

### Q5: 클러스터 인덱스와 논클러스터 인덱스의 차이는?

**A:**
- **클러스터**: 물리적 정렬, 테이블당 1개, 빠름
- **논클러스터**: 별도 테이블, 여러 개 가능, 상대적으로 느림

### Q6: JOIN 종류를 설명하시오.

**A:**
- **INNER JOIN**: 양쪽 모두 매칭되는 행만
- **LEFT JOIN**: 왼쪽 테이블 전체 + 매칭되는 오른쪽
- **RIGHT JOIN**: 오른쪽 테이블 전체 + 매칭되는 왼쪽
- **FULL OUTER JOIN**: 양쪽 모두 포함

### Q7: NoSQL을 사용하는 이유는?

**A:**
- **유연한 스키마**: 빠른 개발
- **수평 확장**: 대용량 데이터
- **높은 성능**: 읽기/쓰기 속도
- **특화된 사용 사례**: 캐싱, 실시간, 그래프 등

### Q8: 데이터베이스 성능 최적화 방법은?

**A:**
1. **인덱스 최적화**: 적절한 인덱스 생성
2. **쿼리 최적화**: EXPLAIN으로 분석
3. **정규화/비정규화**: 상황에 맞게
4. **파티셔닝**: 테이블 분할
5. **캐싱**: Redis, Memcached
6. **Connection Pooling**: 연결 재사용
7. **읽기 전용 복제본**: 읽기 부하 분산

---

**이것만 마스터하면 데이터베이스는 끝!** 💾
