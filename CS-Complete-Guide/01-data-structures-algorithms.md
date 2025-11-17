# 1️⃣ 자료구조 & 알고리즘 완전 정복

> 이것만 보면 자료구조와 알고리즘은 끝!

---

## 📚 목차

1. [시간 복잡도와 공간 복잡도](#시간-복잡도와-공간-복잡도)
2. [배열과 리스트](#배열과-리스트)
3. [스택과 큐](#스택과-큐)
4. [해시 테이블](#해시-테이블)
5. [트리](#트리)
6. [그래프](#그래프)
7. [정렬 알고리즘](#정렬-알고리즘)
8. [탐색 알고리즘](#탐색-알고리즘)
9. [동적 프로그래밍](#동적-프로그래밍)
10. [면접 필수 문제 패턴](#면접-필수-문제-패턴)

---

## 시간 복잡도와 공간 복잡도

### Big-O 표기법

알고리즘의 효율성을 나타내는 표기법

**시간 복잡도 순서 (빠른 순)**
```
O(1) < O(log n) < O(n) < O(n log n) < O(n²) < O(2ⁿ) < O(n!)
```

### 시간 복잡도 예시

| 복잡도 | 이름 | 예시 |
|--------|------|------|
| O(1) | 상수 | 배열 인덱스 접근, 해시 테이블 조회 |
| O(log n) | 로그 | 이진 탐색, 균형 트리 탐색 |
| O(n) | 선형 | 배열 순회, 선형 탐색 |
| O(n log n) | 선형로그 | 병합 정렬, 힙 정렬, 퀵 정렬(평균) |
| O(n²) | 이차 | 이중 for문, 버블 정렬, 선택 정렬 |
| O(2ⁿ) | 지수 | 피보나치(재귀), 부분집합 생성 |
| O(n!) | 팩토리얼 | 순열 생성, 외판원 문제 |

### 코드로 보는 복잡도

```java
// O(1) - 상수 시간
int getFirst(int[] arr) {
    return arr[0];  // 항상 1번
}

// O(n) - 선형 시간
int sum(int[] arr) {
    int total = 0;
    for (int num : arr) {  // n번 반복
        total += num;
    }
    return total;
}

// O(n²) - 이차 시간
void printPairs(int[] arr) {
    for (int i = 0; i < arr.length; i++) {      // n번
        for (int j = 0; j < arr.length; j++) {  // n번
            System.out.println(arr[i] + ", " + arr[j]);
        }
    }
}

// O(log n) - 로그 시간
int binarySearch(int[] arr, int target) {
    int left = 0, right = arr.length - 1;
    while (left <= right) {
        int mid = (left + right) / 2;
        if (arr[mid] == target) return mid;
        else if (arr[mid] < target) left = mid + 1;
        else right = mid - 1;
    }
    return -1;
}
```

### 공간 복잡도

메모리 사용량을 나타냄

```java
// O(1) - 상수 공간
void swap(int a, int b) {
    int temp = a;  // 변수 몇 개만 사용
    a = b;
    b = temp;
}

// O(n) - 선형 공간
int[] copy(int[] arr) {
    int[] newArr = new int[arr.length];  // n 크기만큼 메모리 사용
    for (int i = 0; i < arr.length; i++) {
        newArr[i] = arr[i];
    }
    return newArr;
}
```

---

## 배열과 리스트

### 배열 (Array)

**특징:**
- 고정 크기
- 연속된 메모리 공간
- 인덱스로 빠른 접근 O(1)

**장점:**
- 인덱스 접근 빠름
- 캐시 지역성 좋음

**단점:**
- 크기 변경 불가
- 삽입/삭제 느림 O(n)

```java
// 배열 기본
int[] arr = new int[5];  // 크기 5로 고정
arr[0] = 10;             // O(1) 접근

// 삽입: 중간에 삽입하려면 뒤 요소들을 이동
void insert(int[] arr, int index, int value) {
    for (int i = arr.length - 1; i > index; i--) {
        arr[i] = arr[i-1];  // 요소들을 뒤로 이동
    }
    arr[index] = value;
}
```

### 동적 배열 (ArrayList)

**특징:**
- 크기 자동 조절
- 내부적으로 배열 사용
- 꽉 차면 2배 크기로 확장

```java
// ArrayList 구현 원리
class MyArrayList {
    private int[] data;
    private int size;
    private int capacity;

    public MyArrayList() {
        capacity = 10;
        data = new int[capacity];
        size = 0;
    }

    public void add(int value) {
        if (size == capacity) {
            resize();  // 2배 확장
        }
        data[size++] = value;
    }

    private void resize() {
        capacity *= 2;
        int[] newData = new int[capacity];
        System.arraycopy(data, 0, newData, 0, size);
        data = newData;
    }
}
```

**시간 복잡도:**
| 연산 | 복잡도 |
|------|--------|
| 접근 | O(1) |
| 끝에 추가 | O(1) 평균, O(n) 최악 |
| 중간 삽입/삭제 | O(n) |
| 탐색 | O(n) |

### 연결 리스트 (Linked List)

**특징:**
- 노드들이 포인터로 연결
- 동적 크기
- 비연속적 메모리

```java
// 단일 연결 리스트
class Node {
    int data;
    Node next;

    Node(int data) {
        this.data = data;
        this.next = null;
    }
}

class LinkedList {
    Node head;

    // 삽입 O(1) - 맨 앞
    void insertFirst(int data) {
        Node newNode = new Node(data);
        newNode.next = head;
        head = newNode;
    }

    // 삭제 O(n) - 값 찾아서 삭제
    void delete(int data) {
        if (head == null) return;

        if (head.data == data) {
            head = head.next;
            return;
        }

        Node current = head;
        while (current.next != null) {
            if (current.next.data == data) {
                current.next = current.next.next;
                return;
            }
            current = current.next;
        }
    }

    // 탐색 O(n)
    Node find(int data) {
        Node current = head;
        while (current != null) {
            if (current.data == data) return current;
            current = current.next;
        }
        return null;
    }
}
```

### 이중 연결 리스트 (Doubly Linked List)

```java
class DoublyNode {
    int data;
    DoublyNode prev;
    DoublyNode next;

    DoublyNode(int data) {
        this.data = data;
    }
}

class DoublyLinkedList {
    DoublyNode head;
    DoublyNode tail;

    // 끝에 추가 O(1)
    void append(int data) {
        DoublyNode newNode = new DoublyNode(data);
        if (tail == null) {
            head = tail = newNode;
            return;
        }
        tail.next = newNode;
        newNode.prev = tail;
        tail = newNode;
    }
}
```

**배열 vs 연결 리스트 비교**

| 연산 | 배열 | 연결 리스트 |
|------|------|------------|
| 접근 | O(1) | O(n) |
| 맨 앞 삽입 | O(n) | O(1) |
| 맨 뒤 삽입 | O(1) | O(1) 또는 O(n) |
| 중간 삽입 | O(n) | O(1) (위치 알 때) |
| 탐색 | O(n) | O(n) |
| 메모리 | 연속적 | 비연속적 |

---

## 스택과 큐

### 스택 (Stack)

**특징:**
- LIFO (Last In First Out) - 후입선출
- 마지막에 넣은 것이 먼저 나옴

**사용 사례:**
- 함수 호출 스택
- 괄호 매칭
- 되돌리기(Undo) 기능
- DFS (깊이 우선 탐색)

```java
// 배열로 구현
class Stack {
    private int[] data;
    private int top;
    private int capacity;

    public Stack(int size) {
        capacity = size;
        data = new int[capacity];
        top = -1;
    }

    // O(1)
    public void push(int value) {
        if (isFull()) throw new RuntimeException("Stack overflow");
        data[++top] = value;
    }

    // O(1)
    public int pop() {
        if (isEmpty()) throw new RuntimeException("Stack underflow");
        return data[top--];
    }

    // O(1)
    public int peek() {
        if (isEmpty()) throw new RuntimeException("Stack is empty");
        return data[top];
    }

    public boolean isEmpty() {
        return top == -1;
    }

    public boolean isFull() {
        return top == capacity - 1;
    }
}

// 사용 예시: 괄호 매칭
boolean isValidParentheses(String s) {
    Stack<Character> stack = new Stack<>();

    for (char c : s.toCharArray()) {
        if (c == '(' || c == '{' || c == '[') {
            stack.push(c);
        } else {
            if (stack.isEmpty()) return false;
            char top = stack.pop();
            if (c == ')' && top != '(') return false;
            if (c == '}' && top != '{') return false;
            if (c == ']' && top != '[') return false;
        }
    }

    return stack.isEmpty();
}
```

### 큐 (Queue)

**특징:**
- FIFO (First In First Out) - 선입선출
- 먼저 넣은 것이 먼저 나옴

**사용 사례:**
- BFS (너비 우선 탐색)
- 프린터 대기열
- 프로세스 스케줄링

```java
// 배열로 구현 (원형 큐)
class Queue {
    private int[] data;
    private int front;
    private int rear;
    private int size;
    private int capacity;

    public Queue(int capacity) {
        this.capacity = capacity;
        data = new int[capacity];
        front = 0;
        rear = -1;
        size = 0;
    }

    // O(1)
    public void enqueue(int value) {
        if (isFull()) throw new RuntimeException("Queue is full");
        rear = (rear + 1) % capacity;  // 원형 큐
        data[rear] = value;
        size++;
    }

    // O(1)
    public int dequeue() {
        if (isEmpty()) throw new RuntimeException("Queue is empty");
        int value = data[front];
        front = (front + 1) % capacity;  // 원형 큐
        size--;
        return value;
    }

    public boolean isEmpty() {
        return size == 0;
    }

    public boolean isFull() {
        return size == capacity;
    }
}
```

### 우선순위 큐 (Priority Queue)

**특징:**
- 우선순위가 높은 것이 먼저 나옴
- 힙으로 구현

```java
// Java의 PriorityQueue 사용
PriorityQueue<Integer> minHeap = new PriorityQueue<>();
PriorityQueue<Integer> maxHeap = new PriorityQueue<>(Collections.reverseOrder());

// 사용 예시: K개의 가장 큰 수 찾기
int[] findKLargest(int[] arr, int k) {
    PriorityQueue<Integer> minHeap = new PriorityQueue<>();

    for (int num : arr) {
        minHeap.offer(num);
        if (minHeap.size() > k) {
            minHeap.poll();  // 가장 작은 것 제거
        }
    }

    int[] result = new int[k];
    for (int i = 0; i < k; i++) {
        result[i] = minHeap.poll();
    }
    return result;
}
```

---

## 해시 테이블

### 해시 테이블 (Hash Table)

**특징:**
- Key-Value 쌍으로 저장
- 해시 함수로 인덱스 계산
- 평균 O(1) 탐색/삽입/삭제

**해시 함수:**
```
index = hashCode(key) % tableSize
```

### 충돌 해결 방법

#### 1. 체이닝 (Chaining)

같은 인덱스에 연결 리스트로 저장

```java
class HashTable {
    private class Node {
        String key;
        int value;
        Node next;

        Node(String key, int value) {
            this.key = key;
            this.value = value;
        }
    }

    private Node[] table;
    private int capacity;

    public HashTable(int capacity) {
        this.capacity = capacity;
        table = new Node[capacity];
    }

    private int hash(String key) {
        return Math.abs(key.hashCode()) % capacity;
    }

    // O(1) 평균
    public void put(String key, int value) {
        int index = hash(key);
        Node head = table[index];

        // 이미 존재하면 업데이트
        Node current = head;
        while (current != null) {
            if (current.key.equals(key)) {
                current.value = value;
                return;
            }
            current = current.next;
        }

        // 새로 추가
        Node newNode = new Node(key, value);
        newNode.next = head;
        table[index] = newNode;
    }

    // O(1) 평균
    public Integer get(String key) {
        int index = hash(key);
        Node current = table[index];

        while (current != null) {
            if (current.key.equals(key)) {
                return current.value;
            }
            current = current.next;
        }

        return null;
    }
}
```

#### 2. 개방 주소법 (Open Addressing)

빈 자리를 찾을 때까지 탐색

```java
// 선형 탐사
public void put(String key, int value) {
    int index = hash(key);

    while (table[index] != null && !table[index].key.equals(key)) {
        index = (index + 1) % capacity;  // 다음 인덱스
    }

    table[index] = new Entry(key, value);
}
```

### 실무 활용

```java
// 두 수의 합 찾기 (Two Sum) - O(n)
int[] twoSum(int[] nums, int target) {
    Map<Integer, Integer> map = new HashMap<>();

    for (int i = 0; i < nums.length; i++) {
        int complement = target - nums[i];
        if (map.containsKey(complement)) {
            return new int[] {map.get(complement), i};
        }
        map.put(nums[i], i);
    }

    return null;
}

// 문자열에서 첫 번째 유일한 문자 찾기
char firstUniqChar(String s) {
    Map<Character, Integer> count = new HashMap<>();

    for (char c : s.toCharArray()) {
        count.put(c, count.getOrDefault(c, 0) + 1);
    }

    for (char c : s.toCharArray()) {
        if (count.get(c) == 1) return c;
    }

    return '\0';
}
```

---

## 트리

### 이진 트리 (Binary Tree)

**특징:**
- 각 노드가 최대 2개의 자식
- 왼쪽 자식, 오른쪽 자식

```java
class TreeNode {
    int val;
    TreeNode left;
    TreeNode right;

    TreeNode(int val) {
        this.val = val;
    }
}
```

### 트리 순회

```java
// 1. 전위 순회 (Pre-order): 루트 → 왼쪽 → 오른쪽
void preorder(TreeNode root) {
    if (root == null) return;
    System.out.print(root.val + " ");  // 방문
    preorder(root.left);
    preorder(root.right);
}

// 2. 중위 순회 (In-order): 왼쪽 → 루트 → 오른쪽
void inorder(TreeNode root) {
    if (root == null) return;
    inorder(root.left);
    System.out.print(root.val + " ");  // 방문
    inorder(root.right);
}

// 3. 후위 순회 (Post-order): 왼쪽 → 오른쪽 → 루트
void postorder(TreeNode root) {
    if (root == null) return;
    postorder(root.left);
    postorder(root.right);
    System.out.print(root.val + " ");  // 방문
}

// 4. 레벨 순회 (Level-order): BFS
void levelOrder(TreeNode root) {
    if (root == null) return;

    Queue<TreeNode> queue = new LinkedList<>();
    queue.offer(root);

    while (!queue.isEmpty()) {
        TreeNode node = queue.poll();
        System.out.print(node.val + " ");

        if (node.left != null) queue.offer(node.left);
        if (node.right != null) queue.offer(node.right);
    }
}
```

### 이진 탐색 트리 (BST)

**특징:**
- 왼쪽 자식 < 부모 < 오른쪽 자식
- 중위 순회 시 정렬된 순서

```java
class BST {
    TreeNode root;

    // 삽입 O(log n) 평균, O(n) 최악
    TreeNode insert(TreeNode root, int val) {
        if (root == null) {
            return new TreeNode(val);
        }

        if (val < root.val) {
            root.left = insert(root.left, val);
        } else {
            root.right = insert(root.right, val);
        }

        return root;
    }

    // 탐색 O(log n) 평균, O(n) 최악
    boolean search(TreeNode root, int val) {
        if (root == null) return false;

        if (val == root.val) return true;
        else if (val < root.val) return search(root.left, val);
        else return search(root.right, val);
    }

    // 삭제
    TreeNode delete(TreeNode root, int val) {
        if (root == null) return null;

        if (val < root.val) {
            root.left = delete(root.left, val);
        } else if (val > root.val) {
            root.right = delete(root.right, val);
        } else {
            // 노드 찾음
            // Case 1: 자식 없음
            if (root.left == null && root.right == null) {
                return null;
            }
            // Case 2: 자식 1개
            if (root.left == null) return root.right;
            if (root.right == null) return root.left;

            // Case 3: 자식 2개 - 오른쪽 서브트리의 최소값으로 대체
            TreeNode minNode = findMin(root.right);
            root.val = minNode.val;
            root.right = delete(root.right, minNode.val);
        }

        return root;
    }

    TreeNode findMin(TreeNode root) {
        while (root.left != null) {
            root = root.left;
        }
        return root;
    }
}
```

### 균형 이진 트리

**AVL 트리:**
- 모든 노드에서 왼쪽/오른쪽 서브트리 높이 차이 ≤ 1
- 회전으로 균형 유지
- 탐색/삽입/삭제 O(log n) 보장

**트리 높이 계산:**
```java
int height(TreeNode root) {
    if (root == null) return 0;
    return 1 + Math.max(height(root.left), height(root.right));
}

boolean isBalanced(TreeNode root) {
    if (root == null) return true;

    int leftHeight = height(root.left);
    int rightHeight = height(root.right);

    return Math.abs(leftHeight - rightHeight) <= 1
        && isBalanced(root.left)
        && isBalanced(root.right);
}
```

### 힙 (Heap)

**특징:**
- 완전 이진 트리
- 최대 힙: 부모 ≥ 자식
- 최소 힙: 부모 ≤ 자식

**배열로 구현:**
```
부모 인덱스 = (i-1) / 2
왼쪽 자식 = 2*i + 1
오른쪽 자식 = 2*i + 2
```

```java
class MinHeap {
    private int[] heap;
    private int size;
    private int capacity;

    public MinHeap(int capacity) {
        this.capacity = capacity;
        heap = new int[capacity];
        size = 0;
    }

    // O(log n)
    public void insert(int val) {
        if (size == capacity) throw new RuntimeException("Heap is full");

        heap[size] = val;
        size++;
        heapifyUp(size - 1);
    }

    private void heapifyUp(int index) {
        int parent = (index - 1) / 2;

        if (index > 0 && heap[index] < heap[parent]) {
            swap(index, parent);
            heapifyUp(parent);
        }
    }

    // O(log n)
    public int extractMin() {
        if (size == 0) throw new RuntimeException("Heap is empty");

        int min = heap[0];
        heap[0] = heap[size - 1];
        size--;
        heapifyDown(0);

        return min;
    }

    private void heapifyDown(int index) {
        int left = 2 * index + 1;
        int right = 2 * index + 2;
        int smallest = index;

        if (left < size && heap[left] < heap[smallest]) {
            smallest = left;
        }
        if (right < size && heap[right] < heap[smallest]) {
            smallest = right;
        }

        if (smallest != index) {
            swap(index, smallest);
            heapifyDown(smallest);
        }
    }

    private void swap(int i, int j) {
        int temp = heap[i];
        heap[i] = heap[j];
        heap[j] = temp;
    }
}
```

---

## 그래프

### 그래프 표현 방법

#### 1. 인접 행렬 (Adjacency Matrix)

```java
// N x N 2차원 배열
int[][] graph = new int[n][n];
graph[i][j] = 1;  // i → j 간선 존재
```

**장점:** 간선 존재 확인 O(1)
**단점:** 공간 O(N²), 모든 간선 탐색 O(N²)

#### 2. 인접 리스트 (Adjacency List)

```java
// 각 노드마다 연결된 노드 리스트
List<List<Integer>> graph = new ArrayList<>();
for (int i = 0; i < n; i++) {
    graph.add(new ArrayList<>());
}
graph.get(i).add(j);  // i → j 간선 추가
```

**장점:** 공간 O(V+E), 인접 노드 탐색 빠름
**단점:** 간선 존재 확인 O(degree)

### DFS (깊이 우선 탐색)

**특징:**
- 스택 또는 재귀 사용
- 깊이를 우선으로 탐색

```java
// 재귀 버전
void dfs(List<List<Integer>> graph, int node, boolean[] visited) {
    visited[node] = true;
    System.out.print(node + " ");

    for (int neighbor : graph.get(node)) {
        if (!visited[neighbor]) {
            dfs(graph, neighbor, visited);
        }
    }
}

// 스택 버전
void dfsIterative(List<List<Integer>> graph, int start) {
    boolean[] visited = new boolean[graph.size()];
    Stack<Integer> stack = new Stack<>();

    stack.push(start);

    while (!stack.isEmpty()) {
        int node = stack.pop();

        if (!visited[node]) {
            visited[node] = true;
            System.out.print(node + " ");

            for (int neighbor : graph.get(node)) {
                if (!visited[neighbor]) {
                    stack.push(neighbor);
                }
            }
        }
    }
}
```

### BFS (너비 우선 탐색)

**특징:**
- 큐 사용
- 레벨별로 탐색
- 최단 경로 찾기에 유용

```java
void bfs(List<List<Integer>> graph, int start) {
    boolean[] visited = new boolean[graph.size()];
    Queue<Integer> queue = new LinkedList<>();

    queue.offer(start);
    visited[start] = true;

    while (!queue.isEmpty()) {
        int node = queue.poll();
        System.out.print(node + " ");

        for (int neighbor : graph.get(node)) {
            if (!visited[neighbor]) {
                queue.offer(neighbor);
                visited[neighbor] = true;
            }
        }
    }
}

// 최단 거리 계산
int[] shortestPath(List<List<Integer>> graph, int start) {
    int[] distance = new int[graph.size()];
    Arrays.fill(distance, -1);

    Queue<Integer> queue = new LinkedList<>();
    queue.offer(start);
    distance[start] = 0;

    while (!queue.isEmpty()) {
        int node = queue.poll();

        for (int neighbor : graph.get(node)) {
            if (distance[neighbor] == -1) {
                distance[neighbor] = distance[node] + 1;
                queue.offer(neighbor);
            }
        }
    }

    return distance;
}
```

### 다익스트라 (Dijkstra) - 최단 경로

```java
// 우선순위 큐 사용
class Edge {
    int to;
    int weight;

    Edge(int to, int weight) {
        this.to = to;
        this.weight = weight;
    }
}

int[] dijkstra(List<List<Edge>> graph, int start) {
    int n = graph.size();
    int[] dist = new int[n];
    Arrays.fill(dist, Integer.MAX_VALUE);
    dist[start] = 0;

    PriorityQueue<int[]> pq = new PriorityQueue<>((a, b) -> a[1] - b[1]);
    pq.offer(new int[] {start, 0});  // {노드, 거리}

    while (!pq.isEmpty()) {
        int[] current = pq.poll();
        int node = current[0];
        int distance = current[1];

        if (distance > dist[node]) continue;

        for (Edge edge : graph.get(node)) {
            int newDist = dist[node] + edge.weight;

            if (newDist < dist[edge.to]) {
                dist[edge.to] = newDist;
                pq.offer(new int[] {edge.to, newDist});
            }
        }
    }

    return dist;
}
```

### 위상 정렬 (Topological Sort)

**DAG(방향 비순환 그래프)의 선형 정렬**

```java
// 진입 차수 이용
List<Integer> topologicalSort(List<List<Integer>> graph) {
    int n = graph.size();
    int[] inDegree = new int[n];

    // 진입 차수 계산
    for (int i = 0; i < n; i++) {
        for (int neighbor : graph.get(i)) {
            inDegree[neighbor]++;
        }
    }

    Queue<Integer> queue = new LinkedList<>();
    for (int i = 0; i < n; i++) {
        if (inDegree[i] == 0) {
            queue.offer(i);
        }
    }

    List<Integer> result = new ArrayList<>();
    while (!queue.isEmpty()) {
        int node = queue.poll();
        result.add(node);

        for (int neighbor : graph.get(node)) {
            inDegree[neighbor]--;
            if (inDegree[neighbor] == 0) {
                queue.offer(neighbor);
            }
        }
    }

    return result.size() == n ? result : null;  // 사이클이 있으면 null
}
```

---

## 정렬 알고리즘

### 버블 정렬 (Bubble Sort)

**시간 복잡도:** O(n²)
**공간 복잡도:** O(1)

```java
void bubbleSort(int[] arr) {
    int n = arr.length;
    for (int i = 0; i < n - 1; i++) {
        for (int j = 0; j < n - i - 1; j++) {
            if (arr[j] > arr[j + 1]) {
                swap(arr, j, j + 1);
            }
        }
    }
}
```

### 선택 정렬 (Selection Sort)

**시간 복잡도:** O(n²)
**공간 복잡도:** O(1)

```java
void selectionSort(int[] arr) {
    int n = arr.length;
    for (int i = 0; i < n - 1; i++) {
        int minIdx = i;
        for (int j = i + 1; j < n; j++) {
            if (arr[j] < arr[minIdx]) {
                minIdx = j;
            }
        }
        swap(arr, i, minIdx);
    }
}
```

### 삽입 정렬 (Insertion Sort)

**시간 복잡도:** O(n²) 평균, O(n) 최선
**공간 복잡도:** O(1)

```java
void insertionSort(int[] arr) {
    for (int i = 1; i < arr.length; i++) {
        int key = arr[i];
        int j = i - 1;

        while (j >= 0 && arr[j] > key) {
            arr[j + 1] = arr[j];
            j--;
        }
        arr[j + 1] = key;
    }
}
```

### 병합 정렬 (Merge Sort)

**시간 복잡도:** O(n log n)
**공간 복잡도:** O(n)

```java
void mergeSort(int[] arr, int left, int right) {
    if (left < right) {
        int mid = (left + right) / 2;

        mergeSort(arr, left, mid);
        mergeSort(arr, mid + 1, right);
        merge(arr, left, mid, right);
    }
}

void merge(int[] arr, int left, int mid, int right) {
    int[] temp = new int[right - left + 1];
    int i = left, j = mid + 1, k = 0;

    while (i <= mid && j <= right) {
        if (arr[i] <= arr[j]) {
            temp[k++] = arr[i++];
        } else {
            temp[k++] = arr[j++];
        }
    }

    while (i <= mid) temp[k++] = arr[i++];
    while (j <= right) temp[k++] = arr[j++];

    for (i = 0; i < temp.length; i++) {
        arr[left + i] = temp[i];
    }
}
```

### 퀵 정렬 (Quick Sort)

**시간 복잡도:** O(n log n) 평균, O(n²) 최악
**공간 복잡도:** O(log n)

```java
void quickSort(int[] arr, int low, int high) {
    if (low < high) {
        int pi = partition(arr, low, high);
        quickSort(arr, low, pi - 1);
        quickSort(arr, pi + 1, high);
    }
}

int partition(int[] arr, int low, int high) {
    int pivot = arr[high];
    int i = low - 1;

    for (int j = low; j < high; j++) {
        if (arr[j] < pivot) {
            i++;
            swap(arr, i, j);
        }
    }

    swap(arr, i + 1, high);
    return i + 1;
}
```

### 힙 정렬 (Heap Sort)

**시간 복잡도:** O(n log n)
**공간 복잡도:** O(1)

```java
void heapSort(int[] arr) {
    int n = arr.length;

    // 힙 구성
    for (int i = n / 2 - 1; i >= 0; i--) {
        heapify(arr, n, i);
    }

    // 하나씩 추출
    for (int i = n - 1; i > 0; i--) {
        swap(arr, 0, i);
        heapify(arr, i, 0);
    }
}

void heapify(int[] arr, int n, int i) {
    int largest = i;
    int left = 2 * i + 1;
    int right = 2 * i + 2;

    if (left < n && arr[left] > arr[largest]) {
        largest = left;
    }
    if (right < n && arr[right] > arr[largest]) {
        largest = right;
    }

    if (largest != i) {
        swap(arr, i, largest);
        heapify(arr, n, largest);
    }
}
```

### 정렬 알고리즘 비교

| 알고리즘 | 최선 | 평균 | 최악 | 공간 | 안정성 |
|---------|------|------|------|------|--------|
| 버블 정렬 | O(n) | O(n²) | O(n²) | O(1) | ✓ |
| 선택 정렬 | O(n²) | O(n²) | O(n²) | O(1) | ✗ |
| 삽입 정렬 | O(n) | O(n²) | O(n²) | O(1) | ✓ |
| 병합 정렬 | O(n log n) | O(n log n) | O(n log n) | O(n) | ✓ |
| 퀵 정렬 | O(n log n) | O(n log n) | O(n²) | O(log n) | ✗ |
| 힙 정렬 | O(n log n) | O(n log n) | O(n log n) | O(1) | ✗ |

---

## 탐색 알고리즘

### 선형 탐색 (Linear Search)

**시간 복잡도:** O(n)

```java
int linearSearch(int[] arr, int target) {
    for (int i = 0; i < arr.length; i++) {
        if (arr[i] == target) return i;
    }
    return -1;
}
```

### 이진 탐색 (Binary Search)

**시간 복잡도:** O(log n)
**조건:** 정렬된 배열

```java
// 반복문
int binarySearch(int[] arr, int target) {
    int left = 0, right = arr.length - 1;

    while (left <= right) {
        int mid = left + (right - left) / 2;

        if (arr[mid] == target) return mid;
        else if (arr[mid] < target) left = mid + 1;
        else right = mid - 1;
    }

    return -1;
}

// 재귀
int binarySearchRecursive(int[] arr, int target, int left, int right) {
    if (left > right) return -1;

    int mid = left + (right - left) / 2;

    if (arr[mid] == target) return mid;
    else if (arr[mid] < target) return binarySearchRecursive(arr, target, mid + 1, right);
    else return binarySearchRecursive(arr, target, left, mid - 1);
}

// 응용: 첫 번째 위치 찾기
int findFirst(int[] arr, int target) {
    int left = 0, right = arr.length - 1;
    int result = -1;

    while (left <= right) {
        int mid = left + (right - left) / 2;

        if (arr[mid] == target) {
            result = mid;
            right = mid - 1;  // 왼쪽 계속 탐색
        } else if (arr[mid] < target) {
            left = mid + 1;
        } else {
            right = mid - 1;
        }
    }

    return result;
}
```

---

## 동적 프로그래밍

### 핵심 개념

1. **최적 부분 구조**: 큰 문제의 최적해가 작은 문제의 최적해로 구성
2. **중복 부분 문제**: 같은 문제를 여러 번 계산

### 접근 방법

1. **Top-down (메모이제이션)**: 재귀 + 캐싱
2. **Bottom-up (타뷸레이션)**: 작은 문제부터 해결

### 피보나치

```java
// 일반 재귀 O(2^n) - 매우 느림
int fib(int n) {
    if (n <= 1) return n;
    return fib(n-1) + fib(n-2);
}

// 메모이제이션 O(n)
int fibMemo(int n, int[] memo) {
    if (n <= 1) return n;
    if (memo[n] != 0) return memo[n];

    memo[n] = fibMemo(n-1, memo) + fibMemo(n-2, memo);
    return memo[n];
}

// 타뷸레이션 O(n)
int fibTab(int n) {
    if (n <= 1) return n;

    int[] dp = new int[n + 1];
    dp[0] = 0;
    dp[1] = 1;

    for (int i = 2; i <= n; i++) {
        dp[i] = dp[i-1] + dp[i-2];
    }

    return dp[n];
}

// 공간 최적화 O(1)
int fibOptimized(int n) {
    if (n <= 1) return n;

    int prev2 = 0, prev1 = 1;
    for (int i = 2; i <= n; i++) {
        int current = prev1 + prev2;
        prev2 = prev1;
        prev1 = current;
    }

    return prev1;
}
```

### 0/1 배낭 문제 (Knapsack)

```java
int knapsack(int[] weights, int[] values, int capacity) {
    int n = weights.length;
    int[][] dp = new int[n + 1][capacity + 1];

    for (int i = 1; i <= n; i++) {
        for (int w = 1; w <= capacity; w++) {
            if (weights[i-1] <= w) {
                dp[i][w] = Math.max(
                    dp[i-1][w],  // 포함 안 함
                    dp[i-1][w - weights[i-1]] + values[i-1]  // 포함
                );
            } else {
                dp[i][w] = dp[i-1][w];
            }
        }
    }

    return dp[n][capacity];
}
```

### 최장 공통 부분 수열 (LCS)

```java
int lcs(String s1, String s2) {
    int m = s1.length(), n = s2.length();
    int[][] dp = new int[m + 1][n + 1];

    for (int i = 1; i <= m; i++) {
        for (int j = 1; j <= n; j++) {
            if (s1.charAt(i-1) == s2.charAt(j-1)) {
                dp[i][j] = dp[i-1][j-1] + 1;
            } else {
                dp[i][j] = Math.max(dp[i-1][j], dp[i][j-1]);
            }
        }
    }

    return dp[m][n];
}
```

### 동전 교환 (Coin Change)

```java
// 최소 동전 개수
int coinChange(int[] coins, int amount) {
    int[] dp = new int[amount + 1];
    Arrays.fill(dp, amount + 1);
    dp[0] = 0;

    for (int i = 1; i <= amount; i++) {
        for (int coin : coins) {
            if (i >= coin) {
                dp[i] = Math.min(dp[i], dp[i - coin] + 1);
            }
        }
    }

    return dp[amount] > amount ? -1 : dp[amount];
}
```

---

## 면접 필수 문제 패턴

### 1. Two Pointers

```java
// 두 수의 합 (정렬된 배열)
int[] twoSum(int[] arr, int target) {
    int left = 0, right = arr.length - 1;

    while (left < right) {
        int sum = arr[left] + arr[right];
        if (sum == target) return new int[] {left, right};
        else if (sum < target) left++;
        else right--;
    }

    return null;
}

// 팰린드롬 체크
boolean isPalindrome(String s) {
    int left = 0, right = s.length() - 1;

    while (left < right) {
        if (s.charAt(left) != s.charAt(right)) return false;
        left++;
        right--;
    }

    return true;
}
```

### 2. Sliding Window

```java
// 크기 k의 부분 배열 최대 합
int maxSubarraySum(int[] arr, int k) {
    int maxSum = 0, windowSum = 0;

    // 첫 윈도우
    for (int i = 0; i < k; i++) {
        windowSum += arr[i];
    }
    maxSum = windowSum;

    // 슬라이딩
    for (int i = k; i < arr.length; i++) {
        windowSum += arr[i] - arr[i - k];
        maxSum = Math.max(maxSum, windowSum);
    }

    return maxSum;
}

// 최장 부분 문자열 (중복 없이)
int lengthOfLongestSubstring(String s) {
    Set<Character> set = new HashSet<>();
    int left = 0, maxLen = 0;

    for (int right = 0; right < s.length(); right++) {
        while (set.contains(s.charAt(right))) {
            set.remove(s.charAt(left));
            left++;
        }
        set.add(s.charAt(right));
        maxLen = Math.max(maxLen, right - left + 1);
    }

    return maxLen;
}
```

### 3. Fast & Slow Pointers

```java
// 연결 리스트 사이클 탐지
boolean hasCycle(ListNode head) {
    ListNode slow = head, fast = head;

    while (fast != null && fast.next != null) {
        slow = slow.next;
        fast = fast.next.next;

        if (slow == fast) return true;
    }

    return false;
}

// 연결 리스트 중간 노드
ListNode findMiddle(ListNode head) {
    ListNode slow = head, fast = head;

    while (fast != null && fast.next != null) {
        slow = slow.next;
        fast = fast.next.next;
    }

    return slow;
}
```

### 4. 백트래킹

```java
// 순열 생성
void permute(int[] nums, List<Integer> current, boolean[] used, List<List<Integer>> result) {
    if (current.size() == nums.length) {
        result.add(new ArrayList<>(current));
        return;
    }

    for (int i = 0; i < nums.length; i++) {
        if (!used[i]) {
            used[i] = true;
            current.add(nums[i]);
            permute(nums, current, used, result);
            current.remove(current.size() - 1);
            used[i] = false;
        }
    }
}

// 조합 생성
void combine(int n, int k, int start, List<Integer> current, List<List<Integer>> result) {
    if (current.size() == k) {
        result.add(new ArrayList<>(current));
        return;
    }

    for (int i = start; i <= n; i++) {
        current.add(i);
        combine(n, k, i + 1, current, result);
        current.remove(current.size() - 1);
    }
}
```

---

## 🎯 면접 대비 체크리스트

### 자료구조
- [ ] 배열 vs 연결 리스트 차이 설명
- [ ] 스택/큐 실생활 예시
- [ ] 해시 테이블 충돌 해결 방법
- [ ] BST 삽입/삭제 구현
- [ ] 힙과 우선순위 큐 차이

### 알고리즘
- [ ] Big-O 계산할 수 있음
- [ ] 정렬 알고리즘 3가지 이상 구현
- [ ] 이진 탐색 변형 문제
- [ ] DFS/BFS 차이와 사용 사례
- [ ] DP 문제 접근 방법

### 코딩 테스트
- [ ] Two Pointers 패턴
- [ ] Sliding Window 패턴
- [ ] 백트래킹 기본 구조
- [ ] 그리디 vs DP 판단

---

**이것만 마스터하면 자료구조와 알고리즘은 끝!** 🚀
