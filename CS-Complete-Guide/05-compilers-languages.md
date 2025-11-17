# 5️⃣ 컴파일러 & 프로그래밍 언어 이론 - 완전 정복

> **"코드가 어떻게 실행되는가? - 컴파일러부터 런타임까지"**

---

## 📚 목차

1. [프로그래밍 언어의 역사와 분류](#프로그래밍-언어의-역사와-분류)
2. [컴파일러 구조](#컴파일러-구조)
3. [어휘 분석 (Lexical Analysis)](#어휘-분석)
4. [구문 분석 (Syntax Analysis)](#구문-분석)
5. [의미 분석 (Semantic Analysis)](#의미-분석)
6. [중간 코드 생성 & 최적화](#중간-코드-생성--최적화)
7. [코드 생성](#코드-생성)
8. [런타임 환경](#런타임-환경)
9. [가비지 컬렉션](#가비지-컬렉션)
10. [JIT 컴파일](#jit-컴파일)
11. [타입 시스템](#타입-시스템)
12. [동시성 모델](#동시성-모델)

---

## 프로그래밍 언어의 역사와 분류

### 언어의 진화

```
1950s: Assembly, FORTRAN
        ↓
1960s: COBOL, LISP, ALGOL
        ↓  (구조화 프로그래밍)
1970s: C, Pascal, Prolog
        ↓  (객체지향)
1980s: C++, Objective-C, Perl
        ↓  (웹, 스크립팅)
1990s: Python, Java, JavaScript, PHP
        ↓  (함수형, 현대 언어)
2000s: C#, Scala, Go
        ↓  (시스템 안전성, 동시성)
2010s~: Rust, Kotlin, Swift, TypeScript
```

### 언어 분류

#### 1. 구현 방식

**컴파일 언어 (C, C++, Rust, Go)**
```
Source Code → Compiler → Machine Code → Execution
              (컴파일 시간)      (실행 시간)

장점: 빠른 실행 속도, 최적화
단점: 플랫폼 의존적, 컴파일 시간
```

**인터프리터 언어 (Python, Ruby, JavaScript)**
```
Source Code → Interpreter → Execution
              (한 줄씩 해석하며 실행)

장점: 플랫폼 독립적, 동적 타이핑
단점: 느린 실행 속도
```

**하이브리드 (Java, C#)**
```
Source Code → Compiler → Bytecode → VM → Execution
              (javac)     (.class)   (JVM)

장점: 이식성 + 최적화(JIT)
단점: VM 오버헤드
```

#### 2. 패러다임

**명령형 (Imperative)**
```c
int sum = 0;
for (int i = 0; i < 10; i++) {
    sum += i;
}
// "어떻게(How)" - 상태 변경
```

**선언형 (Declarative)**
```sql
SELECT SUM(i) FROM numbers WHERE i < 10;
-- "무엇을(What)" - 결과만 기술
```

**객체지향 (OOP)**
```java
class Shape {
    abstract double area();
}
class Circle extends Shape {
    double radius;
    double area() { return Math.PI * radius * radius; }
}
// 캡슐화, 상속, 다형성
```

**함수형 (Functional)**
```haskell
sum = foldl (+) 0 [0..9]
-- 순수 함수, 불변성, 고차 함수
```

---

## 컴파일러 구조

### 전체 파이프라인

```
Source Code (hello.c)
    ↓
┌─────────────────────────────┐
│  Frontend (언어 의존적)     │
├─────────────────────────────┤
│  1. Lexical Analysis        │ → Tokens
│     (어휘 분석)             │
├─────────────────────────────┤
│  2. Syntax Analysis         │ → AST
│     (구문 분석)             │
├─────────────────────────────┤
│  3. Semantic Analysis       │ → Annotated AST
│     (의미 분석)             │
└─────────────────────────────┘
    ↓
┌─────────────────────────────┐
│  Optimizer (중간 단계)      │
├─────────────────────────────┤
│  4. Intermediate Code Gen   │ → IR (LLVM IR)
│     (중간 코드 생성)        │
├─────────────────────────────┤
│  5. Optimization            │ → Optimized IR
│     (최적화)                │
└─────────────────────────────┘
    ↓
┌─────────────────────────────┐
│  Backend (플랫폼 의존적)    │
├─────────────────────────────┤
│  6. Code Generation         │ → Assembly
│     (코드 생성)             │
├─────────────────────────────┤
│  7. Register Allocation     │
│     (레지스터 할당)         │
└─────────────────────────────┘
    ↓
Machine Code (hello.exe)
```

---

## 어휘 분석

### Tokenization (토큰화)

**입력 코드:**
```c
int sum = a + b * 2;
```

**토큰 스트림:**
```
<KEYWORD, "int">
<IDENTIFIER, "sum">
<OPERATOR, "=">
<IDENTIFIER, "a">
<OPERATOR, "+">
<IDENTIFIER, "b">
<OPERATOR, "*">
<NUMBER, 2>
<SEMICOLON, ";">
```

### Lexer 구현 (간단한 버전)

```python
import re

class Token:
    def __init__(self, type, value):
        self.type = type
        self.value = value

    def __repr__(self):
        return f'<{self.type}, {self.value}>'

class Lexer:
    # 토큰 정의 (정규표현식)
    TOKEN_SPEC = [
        ('NUMBER',   r'\d+(\.\d*)?'),      # 정수, 실수
        ('KEYWORD',  r'\b(int|if|else|while|return)\b'),  # 키워드
        ('ID',       r'[A-Za-z_]\w*'),     # 식별자
        ('OP',       r'[+\-*/=<>!]+'),     # 연산자
        ('LPAREN',   r'\('),               # (
        ('RPAREN',   r'\)'),               # )
        ('LBRACE',   r'\{'),               # {
        ('RBRACE',   r'\}'),               # }
        ('SEMI',     r';'),                # ;
        ('COMMA',    r','),                # ,
        ('SKIP',     r'[ \t\n]+'),         # 공백
        ('COMMENT',  r'//.*'),             # 주석
        ('MISMATCH', r'.'),                # 에러
    ]

    def __init__(self, code):
        self.code = code
        self.tokens = []

    def tokenize(self):
        # 모든 패턴을 하나로 합침
        tok_regex = '|'.join(f'(?P<{name}>{pattern})'
                             for name, pattern in self.TOKEN_SPEC)

        for mo in re.finditer(tok_regex, self.code):
            kind = mo.lastgroup
            value = mo.group()

            if kind == 'SKIP' or kind == 'COMMENT':
                continue
            elif kind == 'MISMATCH':
                raise SyntaxError(f'Unexpected character: {value}')
            else:
                self.tokens.append(Token(kind, value))

        return self.tokens

# 사용 예시
code = """
int sum = a + b * 2;
if (sum > 10) {
    return sum;
}
"""

lexer = Lexer(code)
tokens = lexer.tokenize()
for tok in tokens:
    print(tok)
```

### 유한 오토마타 (Finite Automaton)

**식별자 인식 (영문자 or _ 시작, 이후 영문/숫자/_)**

```
States: {START, ID, ERROR}

    [a-zA-Z_]
START ────────→ ID
  │             │ ↺ [a-zA-Z0-9_]
  │             │
  └─[0-9]───→ ERROR
```

**구현:**
```python
def is_identifier(s):
    state = 'START'

    for char in s:
        if state == 'START':
            if char.isalpha() or char == '_':
                state = 'ID'
            else:
                return False
        elif state == 'ID':
            if not (char.isalnum() or char == '_'):
                return False

    return state == 'ID'

print(is_identifier("var123"))   # True
print(is_identifier("123var"))   # False
print(is_identifier("_temp"))    # True
```

---

## 구문 분석

### 문맥 자유 문법 (Context-Free Grammar)

**BNF 표기법:**
```
<expr>   ::= <term> (('+' | '-') <term>)*
<term>   ::= <factor> (('*' | '/') <factor>)*
<factor> ::= <number> | '(' <expr> ')'
```

**예시: `2 + 3 * 4` 파싱**

```
        expr
       /  |  \
    term  +  term
     |       /  |  \
   factor factor * factor
     |       |       |
     2       3       4
```

### 파싱 알고리즘

#### 1. Recursive Descent Parser (재귀 하강 파서)

**Top-Down 방식**

```python
class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    def current_token(self):
        if self.pos < len(self.tokens):
            return self.tokens[self.pos]
        return None

    def eat(self, type):
        """현재 토큰이 예상한 타입이면 소비"""
        token = self.current_token()
        if token and token.type == type:
            self.pos += 1
            return token
        raise SyntaxError(f'Expected {type}, got {token}')

    # expr ::= term (('+' | '-') term)*
    def expr(self):
        node = self.term()

        while self.current_token() and \
              self.current_token().value in ['+', '-']:
            op = self.eat('OP')
            right = self.term()
            node = BinOp(node, op, right)

        return node

    # term ::= factor (('*' | '/') factor)*
    def term(self):
        node = self.factor()

        while self.current_token() and \
              self.current_token().value in ['*', '/']:
            op = self.eat('OP')
            right = self.factor()
            node = BinOp(node, op, right)

        return node

    # factor ::= NUMBER | '(' expr ')'
    def factor(self):
        token = self.current_token()

        if token.type == 'NUMBER':
            self.eat('NUMBER')
            return Num(token.value)
        elif token.type == 'LPAREN':
            self.eat('LPAREN')
            node = self.expr()
            self.eat('RPAREN')
            return node

        raise SyntaxError(f'Unexpected token: {token}')

# AST 노드
class Num:
    def __init__(self, value):
        self.value = int(value)

class BinOp:
    def __init__(self, left, op, right):
        self.left = left
        self.op = op.value
        self.right = right

# 사용
tokens = lexer.tokenize("2 + 3 * 4")
parser = Parser(tokens)
ast = parser.expr()
```

#### 2. LR Parser (Bottom-Up)

**Shift-Reduce 방식**

```
Input: 2 + 3
Stack: []

1. Shift 2    → Stack: [2]
2. Reduce     → Stack: [expr]
3. Shift +    → Stack: [expr, +]
4. Shift 3    → Stack: [expr, +, 3]
5. Reduce     → Stack: [expr, +, expr]
6. Reduce     → Stack: [expr]
```

---

## 의미 분석

### 타입 체킹

**예시:**
```c
int a = 5;
float b = 3.14;
a = b;  // ❌ Type Error (int ← float)
```

**구현:**
```python
class TypeChecker:
    def __init__(self):
        self.symbol_table = {}  # 변수명 → 타입

    def visit_Assignment(self, node):
        # 우변 타입 체크
        right_type = self.visit(node.right)

        # 변수 선언 확인
        if node.left.name in self.symbol_table:
            left_type = self.symbol_table[node.left.name]

            # 타입 호환성 체크
            if left_type != right_type:
                raise TypeError(
                    f'Cannot assign {right_type} to {left_type}'
                )
        else:
            # 새 변수 등록
            self.symbol_table[node.left.name] = right_type

    def visit_BinOp(self, node):
        left_type = self.visit(node.left)
        right_type = self.visit(node.right)

        # 타입 호환성
        if left_type != right_type:
            raise TypeError(
                f'Type mismatch: {left_type} {node.op} {right_type}'
            )

        return left_type
```

### Symbol Table (심볼 테이블)

**역할:**
- 변수, 함수, 클래스 정보 저장
- 스코프 관리
- 타입 정보

**구조:**
```python
class SymbolTable:
    def __init__(self, parent=None):
        self.symbols = {}
        self.parent = parent  # 상위 스코프

    def define(self, name, type, value=None):
        """심볼 정의"""
        if name in self.symbols:
            raise Exception(f'{name} already defined')
        self.symbols[name] = {
            'type': type,
            'value': value
        }

    def lookup(self, name):
        """심볼 조회 (현재 스코프 → 상위 스코프)"""
        if name in self.symbols:
            return self.symbols[name]
        elif self.parent:
            return self.parent.lookup(name)
        else:
            raise Exception(f'{name} not defined')

# 사용 예시
global_scope = SymbolTable()
global_scope.define('x', 'int', 10)

function_scope = SymbolTable(parent=global_scope)
function_scope.define('y', 'int', 20)

print(function_scope.lookup('x'))  # 상위 스코프에서 찾음
print(function_scope.lookup('y'))  # 현재 스코프
```

---

## 중간 코드 생성 & 최적화

### Three-Address Code (3-주소 코드)

**원본:**
```c
int a = b + c * d;
```

**3-주소 코드:**
```
t1 = c * d
t2 = b + t1
a = t2
```

**특징:**
- 각 명령어마다 최대 3개의 주소 (피연산자 2개, 결과 1개)
- 최적화하기 쉬움
- 플랫폼 독립적

### LLVM IR (Intermediate Representation)

**LLVM IR 예시:**
```llvm
define i32 @add(i32 %a, i32 %b) {
entry:
  %sum = add i32 %a, %b
  ret i32 %sum
}
```

**SSA (Static Single Assignment) 형식:**
- 각 변수는 정확히 한 번만 할당됨
- φ (phi) 함수로 분기 합류 지점 처리

```llvm
if (x > 0)
  y = 1;
else
  y = 2;
z = y;

→

if.then:
  br label %if.end

if.else:
  br label %if.end

if.end:
  %y = phi i32 [1, %if.then], [2, %if.else]  ; φ 함수
  %z = %y
```

### 최적화 기법

#### 1. Constant Folding (상수 접기)

```c
int x = 2 + 3;  →  int x = 5;
int y = 4 * 5;  →  int y = 20;
```

#### 2. Dead Code Elimination (죽은 코드 제거)

```c
int x = 10;
x = 20;  // 이전 할당은 사용 안 됨
return x;

→

int x = 20;
return x;
```

#### 3. Common Subexpression Elimination (공통 부분식 제거)

```c
a = b + c;
d = b + c;  // 중복 계산

→

temp = b + c;
a = temp;
d = temp;
```

#### 4. Loop Optimization (루프 최적화)

**Loop Unrolling:**
```c
for (int i = 0; i < 4; i++) {
    a[i] = i;
}

→

a[0] = 0;
a[1] = 1;
a[2] = 2;
a[3] = 3;
```

**Loop Invariant Code Motion:**
```c
for (int i = 0; i < n; i++) {
    x = y + z;  // 루프 불변식
    a[i] = x;
}

→

x = y + z;  // 루프 밖으로 이동
for (int i = 0; i < n; i++) {
    a[i] = x;
}
```

---

## 코드 생성

### 레지스터 할당

**문제:** 무한한 가상 레지스터 → 제한된 물리 레지스터

**그래프 착색 (Graph Coloring) 알고리즘:**

```
변수들의 간섭 그래프 생성
→ 그래프 착색 (k-색칠 문제)
→ 같은 색 = 같은 레지스터

a = 1
b = 2
c = a + b  // a, b 동시 사용 → 간섭
d = c + 1

간섭 그래프:
a ─── c
│     │
b ─── d

착색:
a → R1
b → R2
c → R3 (또는 R1, a 끝났으므로)
d → R1 (또는 R2)
```

### 명령어 선택

**CISC (x86) vs RISC (ARM)**

**CISC:**
```asm
; x86: 복잡한 명령어
MOV eax, [memory]      ; 메모리 → 레지스터
ADD eax, [memory + 4]  ; 메모리 직접 연산
```

**RISC:**
```asm
; ARM: 단순한 명령어
LDR r0, [memory]       ; 메모리 → 레지스터
LDR r1, [memory + 4]   ; 메모리 → 레지스터
ADD r0, r0, r1         ; 레지스터끼리만 연산
```

---

## 런타임 환경

### 메모리 레이아웃

```
┌────────────────┐  높은 주소
│  Command Args  │
│  Environment   │
├────────────────┤
│     Stack      │  지역 변수, 함수 호출
│       ↓        │  (아래로 성장)
│                │
│       ↑        │
│     Heap       │  동적 할당
│                │  (위로 성장)
├────────────────┤
│  BSS (unin..)  │  초기화 안 된 전역 변수
├────────────────┤
│  Data (init.)  │  초기화된 전역 변수
├────────────────┤
│     Text       │  코드 (읽기 전용)
└────────────────┘  낮은 주소
```

### 함수 호출 규약 (Calling Convention)

**Stack Frame 구조:**

```
main()
  └─→ foo(a, b)
        └─→ bar(x, y)

Stack:
┌──────────────┐
│  bar의 지역변수│  ← SP (Stack Pointer)
├──────────────┤
│  Return Addr │  (bar에서 foo로 돌아갈 주소)
├──────────────┤
│  Saved FP    │
├──────────────┤  ← FP (Frame Pointer)
│  Parameters  │  (x, y)
├──────────────┤
│  foo의 지역변수│
├──────────────┤
│  Return Addr │  (foo에서 main으로)
├──────────────┤
│  Saved FP    │
├──────────────┤
│  Parameters  │  (a, b)
├──────────────┤
│  main 지역변수│
└──────────────┘
```

**cdecl (C Calling Convention):**
1. 인자를 오른쪽부터 스택에 push
2. `call` 명령어 (return address를 스택에 push하고 점프)
3. 피호출자가 frame pointer 저장
4. 피호출자가 지역 변수 공간 확보
5. 함수 실행
6. 반환값을 EAX 레지스터에
7. 스택 정리 (caller가 정리)
8. `ret` 명령어

```asm
; foo(10, 20) 호출
push 20        ; 두 번째 인자
push 10        ; 첫 번째 인자
call foo
add esp, 8     ; 스택 정리 (caller)

foo:
    push ebp           ; 이전 frame pointer 저장
    mov ebp, esp       ; 새 frame pointer 설정
    sub esp, 16        ; 지역 변수 공간 확보

    ; 함수 본문
    mov eax, [ebp+8]   ; 첫 번째 인자
    add eax, [ebp+12]  ; 두 번째 인자

    mov esp, ebp       ; 스택 복구
    pop ebp
    ret
```

---

## 가비지 컬렉션

### 필요성

**수동 메모리 관리 (C):**
```c
int* p = malloc(sizeof(int) * 100);
// ...
free(p);  // 까먹으면 메모리 누수!
```

**자동 메모리 관리 (Java, Python, JavaScript):**
```java
int[] arr = new int[100];
// 사용 후 자동으로 회수됨
```

### GC 알고리즘

#### 1. Reference Counting

**원리:** 객체를 가리키는 참조 개수를 세고, 0이 되면 회수

```python
class RefCountGC:
    def __init__(self, value):
        self.value = value
        self.ref_count = 1  # 초기 참조 1

    def add_ref(self):
        self.ref_count += 1

    def release(self):
        self.ref_count -= 1
        if self.ref_count == 0:
            print(f"Freeing {self.value}")
            del self
```

**문제: 순환 참조 (Circular Reference)**
```python
a = Node()
b = Node()
a.next = b
b.next = a  # 순환!
del a
del b
# 둘 다 ref_count > 0이라 회수 안 됨!
```

#### 2. Mark-and-Sweep

**원리:**
1. **Mark**: Root부터 도달 가능한 객체 표시
2. **Sweep**: 표시 안 된 객체 회수

```
Root
 │
 ├→ A → B
 │     ↓
 └→ C   D (unreachable)

Mark: {A, B, C}
Sweep: D 회수
```

**구현 (간단화):**
```python
class MarkSweepGC:
    def __init__(self):
        self.objects = []
        self.roots = []

    def allocate(self, obj):
        obj.marked = False
        self.objects.append(obj)
        return obj

    def mark(self):
        """Root부터 DFS로 도달 가능한 객체 마킹"""
        for root in self.roots:
            self._mark_recursive(root)

    def _mark_recursive(self, obj):
        if obj.marked:
            return
        obj.marked = True
        for child in obj.children:
            self._mark_recursive(child)

    def sweep(self):
        """마킹 안 된 객체 회수"""
        alive = []
        for obj in self.objects:
            if obj.marked:
                obj.marked = False  # 다음 GC를 위해 초기화
                alive.append(obj)
            else:
                print(f"Collecting {obj}")
                del obj
        self.objects = alive

    def collect(self):
        self.mark()
        self.sweep()
```

#### 3. Copying GC (Generational GC의 기본)

**원리:** 메모리를 두 영역으로 나누고, 살아있는 객체만 복사

```
From Space          To Space
┌─────────┐        ┌─────────┐
│ A (live)│   →    │    A    │
│ B (dead)│        │    C    │
│ C (live)│        │         │
│ D (dead)│        │         │
└─────────┘        └─────────┘
     ↓                  ↓
  압축됨             (From ↔ To 교체)
```

#### 4. Generational GC (Java, Python)

**가설:** 대부분의 객체는 금방 죽는다 (Weak Generational Hypothesis)

```
┌──────────────────────────────────┐
│       Old Generation             │  오래 살아남은 객체
│  (Major GC - 느림, 드물게)       │
├──────────────────────────────────┤
│       Young Generation           │
│  ┌─────────┬──────────┬─────────┐│
│  │  Eden   │ Survivor │Survivor ││
│  │         │    S0    │   S1    ││
│  └─────────┴──────────┴─────────┘│
│  (Minor GC - 빠름, 자주)         │
└──────────────────────────────────┘

1. 객체는 Eden에 할당
2. Eden 가득 차면 Minor GC
3. 살아남은 객체는 Survivor로
4. 여러 번 살아남으면 Old로 승격
```

**Java GC 로깅:**
```bash
java -XX:+PrintGCDetails -XX:+PrintGCTimeStamps \
     -Xloggc:gc.log MyApp

# gc.log:
# [GC (Allocation Failure) [PSYoungGen: 2048K->512K(2560K)] ...
# [Full GC (Ergonomics) [PSYoungGen: 512K->0K(2560K)] ...
```

---

## JIT 컴파일

### Tiered Compilation (계층적 컴파일)

```
Code Execution Path:

1. Interpreted (인터프리터)
   - 빠른 시작
   - 느린 실행
   ↓
2. C1 Compiler (Client Compiler)
   - 빠른 컴파일
   - 기본 최적화
   ↓
3. C2 Compiler (Server Compiler)
   - 느린 컴파일
   - 고급 최적화 (인라이닝, 루프 언롤링 등)
```

**Hotspot Detection (핫스팟 탐지):**

```java
// 이 메서드가 자주 호출됨 (Hot Method)
public int sum(int a, int b) {
    return a + b;
}

// JVM이 감지:
// "이 메서드 10,000번 호출됨 → JIT 컴파일하자!"

→ 네이티브 코드로 컴파일
```

### 인라이닝 (Inlining)

```java
// Before
public int square(int x) {
    return x * x;
}

public int sumOfSquares(int a, int b) {
    return square(a) + square(b);  // 함수 호출 오버헤드
}

// After (JIT 최적화)
public int sumOfSquares(int a, int b) {
    return (a * a) + (b * b);  // 인라인됨
}
```

### 탈최적화 (Deoptimization)

```java
interface Animal {
    void speak();
}

class Dog implements Animal {
    public void speak() { System.out.println("Woof"); }
}

// JIT: "지금까지 Dog만 봤으니 Dog.speak()로 최적화!"
for (Animal animal : animals) {
    animal.speak();  // Dog.speak()로 인라인
}

// 갑자기 Cat 등장!
animals.add(new Cat());

// JIT: "앗, 가정이 틀렸다! 탈최적화!"
// → 인터프리터 모드로 되돌아감
```

---

## 타입 시스템

### 타입 분류

#### 1. 정적 타입 vs 동적 타입

**정적 타입 (Static Typing)**: 컴파일 시간에 타입 체크
```java
// Java
int x = 10;
x = "hello";  // ❌ 컴파일 에러
```

**동적 타입 (Dynamic Typing)**: 런타임에 타입 체크
```python
# Python
x = 10
x = "hello"  # ✅ OK
```

#### 2. 강타입 vs 약타입

**강타입 (Strong Typing)**: 암묵적 변환 제한
```python
# Python (강타입)
"3" + 5  # ❌ TypeError
```

**약타입 (Weak Typing)**: 암묵적 변환 허용
```javascript
// JavaScript (약타입)
"3" + 5  // "35" (문자열)
"3" - 2  // 1 (숫자)
```

### 타입 추론 (Type Inference)

**Hindley-Milner 타입 시스템 (Haskell, ML):**

```haskell
-- 타입 명시 안 해도 추론됨
id x = x
-- 추론: id :: a -> a (모든 타입 a에 대해)

map f [] = []
map f (x:xs) = f x : map f xs
-- 추론: map :: (a -> b) -> [a] -> [b]
```

**Java 10+ `var`:**
```java
var list = new ArrayList<String>();  // ArrayList<String> 추론
var x = 10;  // int 추론
```

### 제네릭 (Generics)

**Java:**
```java
// 타입 파라미터
class Box<T> {
    private T value;

    public void set(T value) {
        this.value = value;
    }

    public T get() {
        return value;
    }
}

Box<Integer> intBox = new Box<>();
intBox.set(10);
int value = intBox.get();  // 타입 안전

// 타입 소거 (Type Erasure)
// 컴파일 후: Box → Box<Object>
```

**C++ Templates:**
```cpp
template<typename T>
class Box {
    T value;
public:
    void set(T v) { value = v; }
    T get() { return value; }
};

Box<int> intBox;
intBox.set(10);

// 각 타입마다 코드 생성됨 (Code Generation)
```

---

## 동시성 모델

### 1. 스레드 기반 (Java, C++)

**공유 메모리 + Lock:**
```java
class Counter {
    private int count = 0;
    private final Object lock = new Object();

    public void increment() {
        synchronized(lock) {
            count++;
        }
    }
}
```

### 2. 액터 모델 (Erlang, Akka)

**메시지 전달, 상태 공유 없음:**
```erlang
% Erlang
-module(counter).

loop(Count) ->
    receive
        {increment, From} ->
            From ! {value, Count + 1},
            loop(Count + 1);
        {get, From} ->
            From ! {value, Count},
            loop(Count)
    end.
```

### 3. CSP (Communicating Sequential Processes) - Go

**채널 기반 통신:**
```go
func worker(ch chan int) {
    for num := range ch {
        fmt.Println("Processing", num)
    }
}

ch := make(chan int)
go worker(ch)  // 고루틴 생성

ch <- 1
ch <- 2
close(ch)
```

### 4. Async/Await (JavaScript, Python, C#)

**비동기 프로그래밍:**
```javascript
// JavaScript
async function fetchData() {
    const response = await fetch('/api/data');
    const data = await response.json();
    return data;
}

// 내부적으로 Promise/이벤트 루프 사용
```

### 5. Software Transactional Memory (Haskell, Clojure)

**트랜잭션 메모리:**
```haskell
-- Haskell STM
transfer :: TVar Int -> TVar Int -> Int -> STM ()
transfer from to amount = do
    fromBalance <- readTVar from
    toBalance <- readTVar to
    writeTVar from (fromBalance - amount)
    writeTVar to (toBalance + amount)

-- atomically로 원자적 실행
atomically $ transfer account1 account2 100
```

---

## 실무 적용

### 컴파일러 최적화 활용

**1. Profile-Guided Optimization (PGO)**
```bash
# GCC
gcc -fprofile-generate -o myapp myapp.c
./myapp  # 프로파일 수집
gcc -fprofile-use -o myapp myapp.c  # 프로파일 기반 최적화
```

**2. Link-Time Optimization (LTO)**
```bash
gcc -flto -o myapp *.c  # 전체 프로그램 최적화
```

### JVM 튜닝

```bash
# Heap 크기 설정
java -Xms2g -Xmx4g MyApp

# GC 선택
java -XX:+UseG1GC       # G1 (기본, 균형)
java -XX:+UseZGC        # ZGC (저지연)
java -XX:+UseShenandoahGC  # Shenandoah

# JIT 컴파일러 로깅
java -XX:+PrintCompilation MyApp
```

---

## 면접 필수 질문

### Q1: 컴파일러와 인터프리터의 차이는?

**A:**
- **컴파일러**: 전체 소스를 한 번에 기계어로 변환 → 빠른 실행
- **인터프리터**: 한 줄씩 해석하며 실행 → 느림, 동적
- **하이브리드**: 바이트코드 + JIT (Java, C#)

### Q2: JIT 컴파일이란?

**A:**
Just-In-Time 컴파일. 런타임에 자주 실행되는 코드(핫스팟)를 네이티브 코드로 컴파일하여 성능 향상.

### Q3: 가비지 컬렉션 알고리즘은?

**A:**
- Reference Counting (순환 참조 문제)
- Mark-and-Sweep (STW 발생)
- Copying GC
- Generational GC (대부분의 현대 GC)

### Q4: 정적 타입과 동적 타입의 장단점은?

**A:**
- **정적**: 컴파일 시 오류 발견, 빠름, IDE 지원 좋음
- **동적**: 유연함, 빠른 개발, 런타임 오류

### Q5: 메모리 누수를 방지하려면?

**A:**
- GC 언어: 순환 참조 주의, 리소스 해제
- 수동 관리: RAII (C++), defer (Go), with (Python)
- 프로파일링 도구 활용

---

**이것만 마스터하면 컴파일러와 프로그래밍 언어는 끝!** 🔧
