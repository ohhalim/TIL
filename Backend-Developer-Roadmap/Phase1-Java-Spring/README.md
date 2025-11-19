# Phase 1: Java & Spring Boot 기초 (4주)

> **목표: Java 핵심 + Spring Boot로 첫 API 만들기**

---

## 📅 주차별 계획

### Week 1-2: Java 핵심 문법
### Week 3-4: Spring Boot 입문
### 최종 결과물: Todo REST API

---

## Week 1-2: Java 핵심

### Day 1-2: 기본 문법

```java
// 1. Hello World
public class HelloWorld {
    public static void main(String[] args) {
        System.out.println("Hello, Backend Developer!");
    }
}

// 2. 변수와 자료형
public class DataTypes {
    public static void main(String[] args) {
        // 기본 자료형 (Primitive)
        int age = 25;
        double height = 175.5;
        boolean isStudent = true;
        char grade = 'A';

        // 참조 자료형 (Reference)
        String name = "홍길동";
        Integer boxedAge = 25;  // Wrapper class

        // 배열
        int[] numbers = {1, 2, 3, 4, 5};
        String[] names = new String[3];

        // 출력
        System.out.println("이름: " + name);
        System.out.println("나이: " + age);
    }
}

// 3. 조건문과 반복문
public class ControlFlow {
    public static void main(String[] args) {
        // if-else
        int score = 85;
        if (score >= 90) {
            System.out.println("A");
        } else if (score >= 80) {
            System.out.println("B");
        } else {
            System.out.println("C");
        }

        // switch
        String day = "Monday";
        switch (day) {
            case "Monday":
                System.out.println("월요일");
                break;
            case "Tuesday":
                System.out.println("화요일");
                break;
            default:
                System.out.println("기타");
        }

        // for 루프
        for (int i = 0; i < 5; i++) {
            System.out.println(i);
        }

        // while 루프
        int count = 0;
        while (count < 5) {
            System.out.println(count);
            count++;
        }

        // enhanced for (for-each)
        int[] numbers = {1, 2, 3, 4, 5};
        for (int num : numbers) {
            System.out.println(num);
        }
    }
}
```

**연습 문제:**
1. 1부터 100까지의 합 구하기
2. 구구단 출력하기
3. 배열에서 최댓값 찾기
4. 문자열 역순 출력하기

---

### Day 3-4: 객체지향 프로그래밍 (OOP)

```java
// 1. 클래스와 객체
public class Person {
    // 필드 (Field)
    private String name;
    private int age;

    // 생성자 (Constructor)
    public Person(String name, int age) {
        this.name = name;
        this.age = age;
    }

    // 기본 생성자
    public Person() {
        this("Unknown", 0);
    }

    // Getter/Setter
    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public int getAge() {
        return age;
    }

    public void setAge(int age) {
        if (age > 0) {
            this.age = age;
        }
    }

    // 메서드
    public void introduce() {
        System.out.println("제 이름은 " + name + "이고, " + age + "살입니다.");
    }
}

// 사용
public class Main {
    public static void main(String[] args) {
        Person person = new Person("김철수", 25);
        person.introduce();

        person.setAge(26);
        System.out.println(person.getAge());
    }
}

// 2. 상속 (Inheritance)
public class Animal {
    protected String name;

    public Animal(String name) {
        this.name = name;
    }

    public void eat() {
        System.out.println(name + "이(가) 먹고 있습니다.");
    }
}

public class Dog extends Animal {
    public Dog(String name) {
        super(name);  // 부모 생성자 호출
    }

    // 메서드 오버라이딩
    @Override
    public void eat() {
        System.out.println(name + "이(가) 사료를 먹고 있습니다.");
    }

    // 자식 클래스만의 메서드
    public void bark() {
        System.out.println("멍멍!");
    }
}

// 3. 다형성 (Polymorphism)
public class PolymorphismExample {
    public static void main(String[] args) {
        Animal animal1 = new Animal("동물");
        Animal animal2 = new Dog("강아지");  // 업캐스팅

        animal1.eat();  // "동물이(가) 먹고 있습니다."
        animal2.eat();  // "강아지이(가) 사료를 먹고 있습니다." (오버라이딩)

        // 다운캐스팅
        if (animal2 instanceof Dog) {
            Dog dog = (Dog) animal2;
            dog.bark();
        }
    }
}

// 4. 추상 클래스와 인터페이스
public abstract class Shape {
    protected String color;

    public Shape(String color) {
        this.color = color;
    }

    // 추상 메서드 (자식 클래스에서 반드시 구현)
    public abstract double calculateArea();

    // 일반 메서드
    public void displayColor() {
        System.out.println("색상: " + color);
    }
}

public class Circle extends Shape {
    private double radius;

    public Circle(String color, double radius) {
        super(color);
        this.radius = radius;
    }

    @Override
    public double calculateArea() {
        return Math.PI * radius * radius;
    }
}

// 인터페이스
public interface Drawable {
    void draw();  // public abstract 생략 가능
}

public interface Movable {
    void move(int x, int y);
}

// 다중 인터페이스 구현
public class Rectangle extends Shape implements Drawable, Movable {
    private double width;
    private double height;
    private int x, y;

    public Rectangle(String color, double width, double height) {
        super(color);
        this.width = width;
        this.height = height;
    }

    @Override
    public double calculateArea() {
        return width * height;
    }

    @Override
    public void draw() {
        System.out.println("사각형을 그립니다.");
    }

    @Override
    public void move(int x, int y) {
        this.x = x;
        this.y = y;
        System.out.println("(" + x + ", " + y + ")로 이동");
    }
}
```

**OOP 4대 원칙:**
1. **캡슐화** (Encapsulation): private 필드 + getter/setter
2. **상속** (Inheritance): extends 키워드
3. **다형성** (Polymorphism): 오버라이딩, 업캐스팅
4. **추상화** (Abstraction): abstract class, interface

---

### Day 5-7: 컬렉션 프레임워크

```java
import java.util.*;

public class CollectionExamples {
    public static void main(String[] args) {
        // 1. List (순서 O, 중복 O)
        List<String> arrayList = new ArrayList<>();
        arrayList.add("Apple");
        arrayList.add("Banana");
        arrayList.add("Apple");  // 중복 가능

        for (String fruit : arrayList) {
            System.out.println(fruit);
        }

        // 2. Set (순서 X, 중복 X)
        Set<Integer> hashSet = new HashSet<>();
        hashSet.add(1);
        hashSet.add(2);
        hashSet.add(1);  // 중복 무시
        System.out.println(hashSet.size());  // 2

        // 3. Map (Key-Value)
        Map<String, Integer> hashMap = new HashMap<>();
        hashMap.put("Alice", 25);
        hashMap.put("Bob", 30);
        hashMap.put("Charlie", 35);

        // 순회
        for (Map.Entry<String, Integer> entry : hashMap.entrySet()) {
            System.out.println(entry.getKey() + ": " + entry.getValue());
        }

        // 값 가져오기
        System.out.println(hashMap.get("Alice"));  // 25
        System.out.println(hashMap.getOrDefault("David", 0));  // 0

        // 4. Queue
        Queue<String> queue = new LinkedList<>();
        queue.offer("First");
        queue.offer("Second");
        queue.offer("Third");

        System.out.println(queue.poll());  // "First"
        System.out.println(queue.peek());  // "Second"

        // 5. Stack
        Stack<Integer> stack = new Stack<>();
        stack.push(1);
        stack.push(2);
        stack.push(3);

        System.out.println(stack.pop());  // 3
        System.out.println(stack.peek());  // 2
    }
}

// 실전 예제: 중복 제거
public class RemoveDuplicates {
    public static List<Integer> removeDuplicates(List<Integer> list) {
        Set<Integer> set = new LinkedHashSet<>(list);  // 순서 유지
        return new ArrayList<>(set);
    }

    public static void main(String[] args) {
        List<Integer> numbers = Arrays.asList(1, 2, 3, 2, 4, 1, 5);
        List<Integer> unique = removeDuplicates(numbers);
        System.out.println(unique);  // [1, 2, 3, 4, 5]
    }
}
```

---

### Day 8-10: 람다와 스트림

```java
import java.util.*;
import java.util.stream.*;

public class LambdaStreamExample {
    public static void main(String[] args) {
        List<Integer> numbers = Arrays.asList(1, 2, 3, 4, 5, 6, 7, 8, 9, 10);

        // 1. 람다식 기본
        // 기존 방식
        Collections.sort(numbers, new Comparator<Integer>() {
            @Override
            public int compare(Integer a, Integer b) {
                return a - b;
            }
        });

        // 람다식
        Collections.sort(numbers, (a, b) -> a - b);

        // 2. Stream API
        // 짝수만 필터링
        List<Integer> evens = numbers.stream()
            .filter(n -> n % 2 == 0)
            .collect(Collectors.toList());
        System.out.println(evens);  // [2, 4, 6, 8, 10]

        // 각 요소에 2 곱하기
        List<Integer> doubled = numbers.stream()
            .map(n -> n * 2)
            .collect(Collectors.toList());

        // 합계 구하기
        int sum = numbers.stream()
            .reduce(0, (a, b) -> a + b);
        System.out.println(sum);  // 55

        // 평균 구하기
        double average = numbers.stream()
            .mapToInt(Integer::intValue)
            .average()
            .orElse(0.0);

        // 정렬
        List<String> names = Arrays.asList("Charlie", "Alice", "Bob");
        names.stream()
            .sorted()
            .forEach(System.out::println);

        // 3. 실전 예제: 학생 관리
        class Student {
            String name;
            int score;

            Student(String name, int score) {
                this.name = name;
                this.score = score;
            }
        }

        List<Student> students = Arrays.asList(
            new Student("Alice", 85),
            new Student("Bob", 92),
            new Student("Charlie", 78),
            new Student("David", 95)
        );

        // 90점 이상 학생 이름
        List<String> topStudents = students.stream()
            .filter(s -> s.score >= 90)
            .map(s -> s.name)
            .collect(Collectors.toList());
        System.out.println(topStudents);  // [Bob, David]

        // 평균 점수
        double avgScore = students.stream()
            .mapToInt(s -> s.score)
            .average()
            .orElse(0.0);

        // 최고 점수 학생
        Optional<Student> topStudent = students.stream()
            .max(Comparator.comparingInt(s -> s.score));
    }
}
```

---

### Day 11-12: 예외 처리

```java
public class ExceptionExample {
    // 1. try-catch
    public static void divide(int a, int b) {
        try {
            int result = a / b;
            System.out.println("결과: " + result);
        } catch (ArithmeticException e) {
            System.out.println("0으로 나눌 수 없습니다: " + e.getMessage());
        } finally {
            System.out.println("항상 실행됩니다");
        }
    }

    // 2. 다중 catch
    public static void parseNumber(String str) {
        try {
            int num = Integer.parseInt(str);
            int[] arr = {1, 2, 3};
            System.out.println(arr[10]);  // ArrayIndexOutOfBoundsException
        } catch (NumberFormatException e) {
            System.out.println("숫자 형식이 아닙니다");
        } catch (ArrayIndexOutOfBoundsException e) {
            System.out.println("배열 인덱스 초과");
        } catch (Exception e) {
            System.out.println("기타 예외: " + e.getMessage());
        }
    }

    // 3. throws (예외 던지기)
    public static void validateAge(int age) throws IllegalArgumentException {
        if (age < 0 || age > 150) {
            throw new IllegalArgumentException("유효하지 않은 나이: " + age);
        }
        System.out.println("유효한 나이입니다");
    }

    // 4. 커스텀 예외
    static class InvalidEmailException extends Exception {
        public InvalidEmailException(String message) {
            super(message);
        }
    }

    public static void validateEmail(String email) throws InvalidEmailException {
        if (!email.contains("@")) {
            throw new InvalidEmailException("이메일에 @가 없습니다");
        }
    }

    // 5. try-with-resources (자동 자원 해제)
    public static void readFile(String filename) {
        try (BufferedReader br = new BufferedReader(new FileReader(filename))) {
            String line;
            while ((line = br.readLine()) != null) {
                System.out.println(line);
            }
        } catch (IOException e) {
            System.out.println("파일 읽기 오류: " + e.getMessage());
        }
        // br.close() 자동 호출
    }

    public static void main(String[] args) {
        divide(10, 0);
        parseNumber("abc");

        try {
            validateAge(-5);
        } catch (IllegalArgumentException e) {
            System.out.println(e.getMessage());
        }

        try {
            validateEmail("test");
        } catch (InvalidEmailException e) {
            System.out.println(e.getMessage());
        }
    }
}
```

---

## Week 3-4: Spring Boot 입문

### Day 1-3: Spring Boot 프로젝트 생성

**1. Spring Initializr로 프로젝트 생성**
```
https://start.spring.io/

Settings:
- Project: Gradle
- Language: Java
- Spring Boot: 3.2.x
- Java: 17
- Dependencies:
  - Spring Web
  - Spring Data JPA
  - H2 Database
  - Lombok
```

**2. 프로젝트 구조**
```
src/
├── main/
│   ├── java/
│   │   └── com/example/todo/
│   │       ├── TodoApplication.java
│   │       ├── controller/
│   │       ├── service/
│   │       ├── repository/
│   │       ├── entity/
│   │       └── dto/
│   └── resources/
│       ├── application.yml
│       └── data.sql
└── test/
```

**3. application.yml 설정**
```yaml
spring:
  h2:
    console:
      enabled: true
      path: /h2-console

  datasource:
    url: jdbc:h2:mem:testdb
    driver-class-name: org.h2.Driver
    username: sa
    password:

  jpa:
    hibernate:
      ddl-auto: create
    show-sql: true
    properties:
      hibernate:
        format_sql: true

server:
  port: 8080
```

---

### Day 4-7: Todo API 구현

**1. Entity (데이터베이스 테이블)**
```java
package com.example.todo.entity;

import jakarta.persistence.*;
import lombok.Getter;
import lombok.Setter;
import lombok.NoArgsConstructor;

import java.time.LocalDateTime;

@Entity
@Table(name = "todos")
@Getter @Setter
@NoArgsConstructor
public class Todo {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(nullable = false)
    private String title;

    @Column(length = 1000)
    private String description;

    @Column(nullable = false)
    private Boolean completed = false;

    @Column(name = "created_at")
    private LocalDateTime createdAt;

    @PrePersist
    protected void onCreate() {
        createdAt = LocalDateTime.now();
    }

    public Todo(String title, String description) {
        this.title = title;
        this.description = description;
        this.completed = false;
    }
}
```

**2. Repository (데이터 접근)**
```java
package com.example.todo.repository;

import com.example.todo.entity.Todo;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.List;

@Repository
public interface TodoRepository extends JpaRepository<Todo, Long> {

    // 완료 여부로 조회
    List<Todo> findByCompleted(Boolean completed);

    // 제목으로 검색 (부분 일치)
    List<Todo> findByTitleContaining(String keyword);

    // 제목과 완료 여부로 조회
    List<Todo> findByTitleContainingAndCompleted(String keyword, Boolean completed);
}
```

**3. Service (비즈니스 로직)**
```java
package com.example.todo.service;

import com.example.todo.entity.Todo;
import com.example.todo.repository.TodoRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.List;

@Service
@RequiredArgsConstructor
@Transactional(readOnly = true)
public class TodoService {

    private final TodoRepository todoRepository;

    // 전체 조회
    public List<Todo> findAll() {
        return todoRepository.findAll();
    }

    // ID로 조회
    public Todo findById(Long id) {
        return todoRepository.findById(id)
            .orElseThrow(() -> new IllegalArgumentException("Todo not found: " + id));
    }

    // 생성
    @Transactional
    public Todo create(Todo todo) {
        return todoRepository.save(todo);
    }

    // 수정
    @Transactional
    public Todo update(Long id, Todo updateTodo) {
        Todo todo = findById(id);
        todo.setTitle(updateTodo.getTitle());
        todo.setDescription(updateTodo.getDescription());
        todo.setCompleted(updateTodo.getCompleted());
        return todo;  // JPA dirty checking
    }

    // 삭제
    @Transactional
    public void delete(Long id) {
        todoRepository.deleteById(id);
    }

    // 완료 토글
    @Transactional
    public Todo toggleCompleted(Long id) {
        Todo todo = findById(id);
        todo.setCompleted(!todo.getCompleted());
        return todo;
    }
}
```

**4. Controller (API 엔드포인트)**
```java
package com.example.todo.controller;

import com.example.todo.entity.Todo;
import com.example.todo.service.TodoService;
import lombok.RequiredArgsConstructor;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/api/todos")
@RequiredArgsConstructor
public class TodoController {

    private final TodoService todoService;

    // 전체 조회
    @GetMapping
    public ResponseEntity<List<Todo>> getAllTodos() {
        return ResponseEntity.ok(todoService.findAll());
    }

    // ID로 조회
    @GetMapping("/{id}")
    public ResponseEntity<Todo> getTodoById(@PathVariable Long id) {
        return ResponseEntity.ok(todoService.findById(id));
    }

    // 생성
    @PostMapping
    public ResponseEntity<Todo> createTodo(@RequestBody Todo todo) {
        Todo created = todoService.create(todo);
        return ResponseEntity.status(HttpStatus.CREATED).body(created);
    }

    // 수정
    @PutMapping("/{id}")
    public ResponseEntity<Todo> updateTodo(
            @PathVariable Long id,
            @RequestBody Todo todo) {
        Todo updated = todoService.update(id, todo);
        return ResponseEntity.ok(updated);
    }

    // 삭제
    @DeleteMapping("/{id}")
    public ResponseEntity<Void> deleteTodo(@PathVariable Long id) {
        todoService.delete(id);
        return ResponseEntity.noContent().build();
    }

    // 완료 토글
    @PatchMapping("/{id}/toggle")
    public ResponseEntity<Todo> toggleCompleted(@PathVariable Long id) {
        Todo toggled = todoService.toggleCompleted(id);
        return ResponseEntity.ok(toggled);
    }
}
```

---

### Day 8-10: 테스트 및 실행

**1. 테스트 코드**
```java
package com.example.todo.service;

import com.example.todo.entity.Todo;
import com.example.todo.repository.TodoRepository;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.transaction.annotation.Transactional;

import static org.assertj.core.api.Assertions.*;

@SpringBootTest
@Transactional
class TodoServiceTest {

    @Autowired
    private TodoService todoService;

    @Autowired
    private TodoRepository todoRepository;

    @Test
    void createTodo() {
        // given
        Todo todo = new Todo("테스트", "테스트 설명");

        // when
        Todo saved = todoService.create(todo);

        // then
        assertThat(saved.getId()).isNotNull();
        assertThat(saved.getTitle()).isEqualTo("테스트");
        assertThat(saved.getCompleted()).isFalse();
    }

    @Test
    void toggleCompleted() {
        // given
        Todo todo = todoRepository.save(new Todo("테스트", "설명"));
        assertThat(todo.getCompleted()).isFalse();

        // when
        Todo toggled = todoService.toggleCompleted(todo.getId());

        // then
        assertThat(toggled.getCompleted()).isTrue();
    }
}
```

**2. Postman 테스트**
```
1. 생성 (POST http://localhost:8080/api/todos)
{
  "title": "Spring Boot 공부",
  "description": "Phase 1 완료하기"
}

2. 전체 조회 (GET http://localhost:8080/api/todos)

3. 수정 (PUT http://localhost:8080/api/todos/1)
{
  "title": "Spring Boot 마스터",
  "description": "Phase 1 완벽 이해",
  "completed": true
}

4. 삭제 (DELETE http://localhost:8080/api/todos/1)
```

---

## 🎯 Phase 1 체크리스트

### Java 기초
- [ ] Hello World 실행
- [ ] 변수, 조건문, 반복문 이해
- [ ] 클래스와 객체 생성
- [ ] 상속, 다형성 구현
- [ ] List, Map, Set 사용
- [ ] 람다식, 스트림 활용
- [ ] 예외 처리 작성

### Spring Boot
- [ ] 프로젝트 생성
- [ ] Entity 작성
- [ ] Repository 인터페이스 구현
- [ ] Service 로직 작성
- [ ] Controller API 구현
- [ ] Postman 테스트 완료
- [ ] JUnit 테스트 작성

---

## 📚 추가 학습 자료

### 온라인 강의
- 인프런: "스프링 입문" (김영한) - 무료
- YouTube: "얄팍한 코딩사전 - 자바"

### 책
- "이것이 자바다" (신용권)
- "스프링 부트 3 백엔드 개발자 되기" (신선영)

### 연습 사이트
- 백준: Bronze ~ Silver 문제
- 프로그래머스: Level 1 문제

---

**다음:** [Phase 2 - Database & REST API](../Phase2-Database-API/README.md)
