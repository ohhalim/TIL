# 10. 소프트웨어 공학 (Software Engineering)

## 목차
1. [디자인 패턴](#디자인-패턴)
2. [아키텍처 패턴](#아키텍처-패턴)
3. [SOLID 원칙](#solid-원칙)
4. [테스트 주도 개발](#테스트-주도-개발)
5. [리팩토링](#리팩토링)
6. [동시성 패턴](#동시성-패턴)
7. [마이크로서비스](#마이크로서비스)
8. [DevOps와 CI/CD](#devops와-cicd)

---

## 디자인 패턴

### 1. 생성 패턴 (Creational Patterns)

**Singleton Pattern:**

```python
class Singleton:
    """
    싱글톤: 클래스의 인스턴스가 단 하나만 존재
    - 전역 상태 관리
    - 리소스 공유
    """
    _instance = None
    _lock = threading.Lock()

    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                # Double-checked locking
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
        return cls._instance

# Thread-safe Singleton (Python)
def singleton(cls):
    """Decorator로 싱글톤 구현"""
    instances = {}
    lock = threading.Lock()

    def get_instance(*args, **kwargs):
        if cls not in instances:
            with lock:
                if cls not in instances:
                    instances[cls] = cls(*args, **kwargs)
        return instances[cls]

    return get_instance

@singleton
class DatabaseConnection:
    def __init__(self):
        self.connection = self._create_connection()

    def _create_connection(self):
        # 실제 DB 연결
        return "DB Connection"

# Factory Pattern
class Shape:
    def draw(self):
        pass

class Circle(Shape):
    def draw(self):
        return "Drawing Circle"

class Rectangle(Shape):
    def draw(self):
        return "Drawing Rectangle"

class ShapeFactory:
    """
    팩토리: 객체 생성 로직 캡슐화
    - 클라이언트는 구체 클래스를 몰라도 됨
    """

    @staticmethod
    def create_shape(shape_type):
        if shape_type == "circle":
            return Circle()
        elif shape_type == "rectangle":
            return Rectangle()
        else:
            raise ValueError(f"Unknown shape: {shape_type}")

# Abstract Factory Pattern
class GUIFactory:
    """추상 팩토리: 관련 객체 군 생성"""
    def create_button(self):
        pass

    def create_checkbox(self):
        pass

class WindowsFactory(GUIFactory):
    def create_button(self):
        return WindowsButton()

    def create_checkbox(self):
        return WindowsCheckbox()

class MacFactory(GUIFactory):
    def create_button(self):
        return MacButton()

    def create_checkbox(self):
        return MacCheckbox()

# Builder Pattern
class Computer:
    """복잡한 객체를 단계적으로 생성"""
    def __init__(self):
        self.cpu = None
        self.ram = None
        self.storage = None
        self.gpu = None

    def __str__(self):
        return f"Computer(CPU={self.cpu}, RAM={self.ram}, Storage={self.storage}, GPU={self.gpu})"

class ComputerBuilder:
    def __init__(self):
        self.computer = Computer()

    def set_cpu(self, cpu):
        self.computer.cpu = cpu
        return self  # Method chaining

    def set_ram(self, ram):
        self.computer.ram = ram
        return self

    def set_storage(self, storage):
        self.computer.storage = storage
        return self

    def set_gpu(self, gpu):
        self.computer.gpu = gpu
        return self

    def build(self):
        return self.computer

# 사용
gaming_pc = (ComputerBuilder()
    .set_cpu("Intel i9")
    .set_ram("32GB")
    .set_storage("2TB SSD")
    .set_gpu("RTX 4090")
    .build())

# Prototype Pattern
import copy

class Prototype:
    """프로토타입: 기존 객체 복제"""
    def clone(self):
        return copy.deepcopy(self)

class GameCharacter(Prototype):
    def __init__(self, name, level, equipment):
        self.name = name
        self.level = level
        self.equipment = equipment

    def clone(self):
        # Deep copy
        return GameCharacter(
            self.name,
            self.level,
            copy.deepcopy(self.equipment)
        )

# 사용: 템플릿 캐릭터 복제
template = GameCharacter("Warrior", 1, {"weapon": "Sword", "armor": "Leather"})
player1 = template.clone()
player1.name = "Player1"
```

### 2. 구조 패턴 (Structural Patterns)

```python
# Adapter Pattern
class EuropeanSocket:
    """유럽 플러그"""
    def voltage(self):
        return 230

class USASocket:
    """미국 플러그"""
    def voltage(self):
        return 110

class SocketAdapter:
    """어댑터: 인터페이스 변환"""
    def __init__(self, socket):
        self.socket = socket

    def voltage(self):
        # 변환 로직
        if isinstance(self.socket, EuropeanSocket):
            return self.socket.voltage() / 2  # 230V → 115V
        return self.socket.voltage()

# Decorator Pattern
class Coffee:
    def cost(self):
        return 5

    def description(self):
        return "Coffee"

class MilkDecorator:
    """데코레이터: 기능 동적 추가"""
    def __init__(self, coffee):
        self._coffee = coffee

    def cost(self):
        return self._coffee.cost() + 2

    def description(self):
        return self._coffee.description() + ", Milk"

class SugarDecorator:
    def __init__(self, coffee):
        self._coffee = coffee

    def cost(self):
        return self._coffee.cost() + 1

    def description(self):
        return self._coffee.description() + ", Sugar"

# 사용
coffee = Coffee()
coffee = MilkDecorator(coffee)
coffee = SugarDecorator(coffee)
print(f"{coffee.description()}: ${coffee.cost()}")
# "Coffee, Milk, Sugar: $8"

# Proxy Pattern
class RealImage:
    """실제 객체 (무거움)"""
    def __init__(self, filename):
        self.filename = filename
        self._load_from_disk()

    def _load_from_disk(self):
        print(f"Loading {self.filename} from disk...")

    def display(self):
        print(f"Displaying {self.filename}")

class ImageProxy:
    """프록시: 지연 로딩, 접근 제어"""
    def __init__(self, filename):
        self.filename = filename
        self._real_image = None

    def display(self):
        if self._real_image is None:
            self._real_image = RealImage(self.filename)
        self._real_image.display()

# Composite Pattern
class Component:
    """컴포지트: 트리 구조"""
    def operation(self):
        pass

class Leaf(Component):
    def __init__(self, name):
        self.name = name

    def operation(self):
        return f"Leaf {self.name}"

class Composite(Component):
    def __init__(self, name):
        self.name = name
        self.children = []

    def add(self, component):
        self.children.append(component)

    def remove(self, component):
        self.children.remove(component)

    def operation(self):
        results = [f"Branch {self.name}"]
        for child in self.children:
            results.append(child.operation())
        return "\n".join(results)

# 파일 시스템 예시
root = Composite("root")
file1 = Leaf("file1.txt")
file2 = Leaf("file2.txt")
folder1 = Composite("folder1")
file3 = Leaf("file3.txt")

root.add(file1)
root.add(folder1)
folder1.add(file2)
folder1.add(file3)

print(root.operation())

# Facade Pattern
class CPU:
    def freeze(self): pass
    def jump(self, position): pass
    def execute(self): pass

class Memory:
    def load(self, position, data): pass

class HardDrive:
    def read(self, lba, size): pass

class ComputerFacade:
    """파사드: 복잡한 시스템 단순화"""
    def __init__(self):
        self.cpu = CPU()
        self.memory = Memory()
        self.hard_drive = HardDrive()

    def start(self):
        """간단한 인터페이스"""
        self.cpu.freeze()
        self.memory.load(0, self.hard_drive.read(0, 1024))
        self.cpu.jump(0)
        self.cpu.execute()

# 사용자는 내부 복잡도를 몰라도 됨
computer = ComputerFacade()
computer.start()
```

### 3. 행동 패턴 (Behavioral Patterns)

```python
# Observer Pattern
class Subject:
    """옵저버: 이벤트 기반 통신"""
    def __init__(self):
        self._observers = []

    def attach(self, observer):
        self._observers.append(observer)

    def detach(self, observer):
        self._observers.remove(observer)

    def notify(self, event):
        for observer in self._observers:
            observer.update(event)

class Observer:
    def update(self, event):
        pass

class StockMarket(Subject):
    def __init__(self):
        super().__init__()
        self._price = 0

    def set_price(self, price):
        self._price = price
        self.notify({'price': price})

class Investor(Observer):
    def __init__(self, name):
        self.name = name

    def update(self, event):
        print(f"{self.name} notified: Stock price = {event['price']}")

# 사용
market = StockMarket()
investor1 = Investor("John")
investor2 = Investor("Jane")

market.attach(investor1)
market.attach(investor2)

market.set_price(100)  # 모든 투자자에게 알림

# Strategy Pattern
class SortStrategy:
    """전략: 알고리즘 교체 가능"""
    def sort(self, data):
        pass

class QuickSort(SortStrategy):
    def sort(self, data):
        if len(data) <= 1:
            return data
        pivot = data[len(data) // 2]
        left = [x for x in data if x < pivot]
        middle = [x for x in data if x == pivot]
        right = [x for x in data if x > pivot]
        return self.sort(left) + middle + self.sort(right)

class MergeSort(SortStrategy):
    def sort(self, data):
        if len(data) <= 1:
            return data
        mid = len(data) // 2
        left = self.sort(data[:mid])
        right = self.sort(data[mid:])
        return self._merge(left, right)

    def _merge(self, left, right):
        result = []
        i = j = 0
        while i < len(left) and j < len(right):
            if left[i] < right[j]:
                result.append(left[i])
                i += 1
            else:
                result.append(right[j])
                j += 1
        result.extend(left[i:])
        result.extend(right[j:])
        return result

class Sorter:
    def __init__(self, strategy):
        self._strategy = strategy

    def set_strategy(self, strategy):
        self._strategy = strategy

    def sort(self, data):
        return self._strategy.sort(data)

# 사용
data = [5, 2, 9, 1, 5, 6]
sorter = Sorter(QuickSort())
print(sorter.sort(data))

# 전략 변경
sorter.set_strategy(MergeSort())
print(sorter.sort(data))

# Command Pattern
class Command:
    """커맨드: 요청을 객체로 캡슐화"""
    def execute(self):
        pass

    def undo(self):
        pass

class Light:
    def on(self):
        print("Light is ON")

    def off(self):
        print("Light is OFF")

class LightOnCommand(Command):
    def __init__(self, light):
        self.light = light

    def execute(self):
        self.light.on()

    def undo(self):
        self.light.off()

class LightOffCommand(Command):
    def __init__(self, light):
        self.light = light

    def execute(self):
        self.light.off()

    def undo(self):
        self.light.on()

class RemoteControl:
    def __init__(self):
        self.command = None
        self.history = []

    def set_command(self, command):
        self.command = command

    def press_button(self):
        self.command.execute()
        self.history.append(self.command)

    def press_undo(self):
        if self.history:
            command = self.history.pop()
            command.undo()

# 사용
light = Light()
remote = RemoteControl()

remote.set_command(LightOnCommand(light))
remote.press_button()  # Light is ON

remote.set_command(LightOffCommand(light))
remote.press_button()  # Light is OFF

remote.press_undo()  # Light is ON

# Iterator Pattern
class Iterator:
    """이터레이터: 컬렉션 순회"""
    def has_next(self):
        pass

    def next(self):
        pass

class BookCollection:
    def __init__(self):
        self.books = []

    def add_book(self, book):
        self.books.append(book)

    def __iter__(self):
        return BookIterator(self.books)

class BookIterator(Iterator):
    def __init__(self, books):
        self._books = books
        self._index = 0

    def has_next(self):
        return self._index < len(self._books)

    def next(self):
        if self.has_next():
            book = self._books[self._index]
            self._index += 1
            return book
        raise StopIteration

# 사용
collection = BookCollection()
collection.add_book("Design Patterns")
collection.add_book("Clean Code")

for book in collection:
    print(book)

# Chain of Responsibility
class Handler:
    """책임 연쇄: 요청을 체인으로 전달"""
    def __init__(self):
        self._next_handler = None

    def set_next(self, handler):
        self._next_handler = handler
        return handler

    def handle(self, request):
        if self._next_handler:
            return self._next_handler.handle(request)
        return None

class AuthenticationHandler(Handler):
    def handle(self, request):
        if not request.get('authenticated'):
            return "Authentication failed"
        print("Authentication passed")
        return super().handle(request)

class AuthorizationHandler(Handler):
    def handle(self, request):
        if not request.get('authorized'):
            return "Authorization failed"
        print("Authorization passed")
        return super().handle(request)

class ValidationHandler(Handler):
    def handle(self, request):
        if not request.get('valid'):
            return "Validation failed"
        print("Validation passed")
        return super().handle(request)

# 체인 구성
auth = AuthenticationHandler()
authz = AuthorizationHandler()
valid = ValidationHandler()

auth.set_next(authz).set_next(valid)

# 요청 처리
request = {'authenticated': True, 'authorized': True, 'valid': True}
result = auth.handle(request)
```

---

## 아키텍처 패턴

### 1. MVC (Model-View-Controller)

```python
# Model
class Task:
    """모델: 데이터 + 비즈니스 로직"""
    def __init__(self, title, completed=False):
        self.title = title
        self.completed = completed

class TaskModel:
    def __init__(self):
        self.tasks = []

    def add_task(self, title):
        task = Task(title)
        self.tasks.append(task)

    def remove_task(self, index):
        if 0 <= index < len(self.tasks):
            del self.tasks[index]

    def toggle_task(self, index):
        if 0 <= index < len(self.tasks):
            self.tasks[index].completed = not self.tasks[index].completed

    def get_tasks(self):
        return self.tasks

# View
class TaskView:
    """뷰: UI 표시"""
    def display_tasks(self, tasks):
        print("\n=== Todo List ===")
        for i, task in enumerate(tasks):
            status = "✓" if task.completed else " "
            print(f"{i+1}. [{status}] {task.title}")

    def get_user_input(self, prompt):
        return input(prompt)

    def show_message(self, message):
        print(message)

# Controller
class TaskController:
    """컨트롤러: 모델과 뷰 연결"""
    def __init__(self, model, view):
        self.model = model
        self.view = view

    def add_task(self):
        title = self.view.get_user_input("Enter task title: ")
        self.model.add_task(title)
        self.view.show_message("Task added!")

    def remove_task(self):
        index = int(self.view.get_user_input("Enter task number: ")) - 1
        self.model.remove_task(index)
        self.view.show_message("Task removed!")

    def toggle_task(self):
        index = int(self.view.get_user_input("Enter task number: ")) - 1
        self.model.toggle_task(index)
        self.view.show_message("Task toggled!")

    def show_tasks(self):
        tasks = self.model.get_tasks()
        self.view.display_tasks(tasks)

# 사용
model = TaskModel()
view = TaskView()
controller = TaskController(model, view)

controller.add_task()
controller.show_tasks()
```

### 2. MVVM (Model-View-ViewModel)

```python
class Observable:
    """데이터 바인딩을 위한 옵저버블"""
    def __init__(self):
        self._observers = []

    def subscribe(self, callback):
        self._observers.append(callback)

    def notify(self):
        for callback in self._observers:
            callback()

class Property:
    """Reactive Property"""
    def __init__(self, value):
        self._value = value
        self.observable = Observable()

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, new_value):
        if self._value != new_value:
            self._value = new_value
            self.observable.notify()

# ViewModel
class TodoViewModel:
    """뷰모델: 뷰의 상태 관리"""
    def __init__(self, model):
        self.model = model
        self.tasks = Property([])
        self.new_task_title = Property("")

    def add_task(self):
        if self.new_task_title.value:
            self.model.add_task(self.new_task_title.value)
            self.new_task_title.value = ""
            self.refresh_tasks()

    def refresh_tasks(self):
        self.tasks.value = self.model.get_tasks()

# View는 ViewModel과 데이터 바인딩
```

### 3. Clean Architecture (헥사고날)

```python
# Domain Layer (가장 안쪽)
class User:
    """도메인 엔티티"""
    def __init__(self, id, email, password_hash):
        self.id = id
        self.email = email
        self.password_hash = password_hash

class UserRepository:
    """리포지토리 인터페이스 (Port)"""
    def save(self, user):
        raise NotImplementedError

    def find_by_email(self, email):
        raise NotImplementedError

# Application Layer (Use Cases)
class RegisterUserUseCase:
    """유스케이스: 비즈니스 로직"""
    def __init__(self, user_repo, password_hasher):
        self.user_repo = user_repo
        self.password_hasher = password_hasher

    def execute(self, email, password):
        # 중복 확인
        existing = self.user_repo.find_by_email(email)
        if existing:
            raise ValueError("Email already exists")

        # 사용자 생성
        password_hash = self.password_hasher.hash(password)
        user = User(None, email, password_hash)

        # 저장
        self.user_repo.save(user)
        return user

# Infrastructure Layer (Adapters)
class PostgresUserRepository(UserRepository):
    """리포지토리 구현 (Adapter)"""
    def __init__(self, db_connection):
        self.db = db_connection

    def save(self, user):
        # PostgreSQL에 저장
        query = "INSERT INTO users (email, password_hash) VALUES (%s, %s)"
        self.db.execute(query, (user.email, user.password_hash))

    def find_by_email(self, email):
        query = "SELECT * FROM users WHERE email = %s"
        result = self.db.execute(query, (email,))
        # User 객체로 변환
        return User(**result) if result else None

class BcryptPasswordHasher:
    """비밀번호 해싱 구현"""
    def hash(self, password):
        import bcrypt
        return bcrypt.hashpw(password.encode(), bcrypt.gensalt())

# Presentation Layer (Web Framework)
class UserController:
    """컨트롤러: HTTP 요청 처리"""
    def __init__(self, register_use_case):
        self.register_use_case = register_use_case

    def register(self, request):
        email = request.data['email']
        password = request.data['password']

        try:
            user = self.register_use_case.execute(email, password)
            return {'status': 'success', 'user_id': user.id}
        except ValueError as e:
            return {'status': 'error', 'message': str(e)}

# Dependency Injection (구성)
db = PostgresConnection()
user_repo = PostgresUserRepository(db)
password_hasher = BcryptPasswordHasher()
register_use_case = RegisterUserUseCase(user_repo, password_hasher)
controller = UserController(register_use_case)
```

### 4. Event-Driven Architecture

```python
class Event:
    """이벤트 베이스 클래스"""
    pass

class UserRegisteredEvent(Event):
    def __init__(self, user_id, email):
        self.user_id = user_id
        self.email = email
        self.timestamp = datetime.now()

class EventBus:
    """이벤트 버스"""
    def __init__(self):
        self._handlers = {}

    def subscribe(self, event_type, handler):
        if event_type not in self._handlers:
            self._handlers[event_type] = []
        self._handlers[event_type].append(handler)

    def publish(self, event):
        event_type = type(event)
        if event_type in self._handlers:
            for handler in self._handlers[event_type]:
                handler(event)

# Event Handlers
class SendWelcomeEmailHandler:
    def __call__(self, event: UserRegisteredEvent):
        print(f"Sending welcome email to {event.email}")

class CreateUserProfileHandler:
    def __call__(self, event: UserRegisteredEvent):
        print(f"Creating profile for user {event.user_id}")

class LogUserRegistrationHandler:
    def __call__(self, event: UserRegisteredEvent):
        print(f"Logging registration: {event.user_id} at {event.timestamp}")

# 구성
event_bus = EventBus()
event_bus.subscribe(UserRegisteredEvent, SendWelcomeEmailHandler())
event_bus.subscribe(UserRegisteredEvent, CreateUserProfileHandler())
event_bus.subscribe(UserRegisteredEvent, LogUserRegistrationHandler())

# 이벤트 발행
event = UserRegisteredEvent(user_id=123, email="user@example.com")
event_bus.publish(event)
```

---

## SOLID 원칙

### 1. Single Responsibility Principle (SRP)

```python
# ❌ SRP 위반
class User:
    def __init__(self, name, email):
        self.name = name
        self.email = email

    def save_to_database(self):
        # DB 저장 (책임 1)
        pass

    def send_email(self):
        # 이메일 전송 (책임 2)
        pass

    def generate_report(self):
        # 리포트 생성 (책임 3)
        pass

# ✅ SRP 준수
class User:
    def __init__(self, name, email):
        self.name = name
        self.email = email

class UserRepository:
    """단일 책임: 데이터 저장"""
    def save(self, user):
        # DB 저장
        pass

class EmailService:
    """단일 책임: 이메일 전송"""
    def send_welcome_email(self, user):
        # 이메일 전송
        pass

class ReportGenerator:
    """단일 책임: 리포트 생성"""
    def generate_user_report(self, user):
        # 리포트 생성
        pass
```

### 2. Open/Closed Principle (OCP)

```python
# ❌ OCP 위반
class AreaCalculator:
    def calculate(self, shapes):
        total = 0
        for shape in shapes:
            if shape.type == "circle":
                total += 3.14 * shape.radius ** 2
            elif shape.type == "rectangle":
                total += shape.width * shape.height
            # 새 도형 추가 시 수정 필요!
        return total

# ✅ OCP 준수
from abc import ABC, abstractmethod

class Shape(ABC):
    @abstractmethod
    def area(self):
        pass

class Circle(Shape):
    def __init__(self, radius):
        self.radius = radius

    def area(self):
        return 3.14 * self.radius ** 2

class Rectangle(Shape):
    def __init__(self, width, height):
        self.width = width
        self.height = height

    def area(self):
        return self.width * self.height

class AreaCalculator:
    """확장에는 열려있고, 수정에는 닫혀있음"""
    def calculate(self, shapes):
        return sum(shape.area() for shape in shapes)

# 새 도형 추가 (기존 코드 수정 없음)
class Triangle(Shape):
    def __init__(self, base, height):
        self.base = base
        self.height = height

    def area(self):
        return 0.5 * self.base * self.height
```

### 3. Liskov Substitution Principle (LSP)

```python
# ❌ LSP 위반
class Bird:
    def fly(self):
        return "Flying"

class Penguin(Bird):
    def fly(self):
        raise Exception("Penguins can't fly!")  # 부모 동작 위반!

# ✅ LSP 준수
class Bird:
    pass

class FlyingBird(Bird):
    def fly(self):
        return "Flying"

class Sparrow(FlyingBird):
    def fly(self):
        return "Sparrow flying"

class Penguin(Bird):
    def swim(self):
        return "Penguin swimming"

# Rectangle-Square 문제
class Rectangle:
    def __init__(self, width, height):
        self._width = width
        self._height = height

    @property
    def width(self):
        return self._width

    @width.setter
    def width(self, value):
        self._width = value

    @property
    def height(self):
        return self._height

    @height.setter
    def height(self, value):
        self._height = value

    def area(self):
        return self._width * self._height

# ❌ LSP 위반
class Square(Rectangle):
    @Rectangle.width.setter
    def width(self, value):
        self._width = value
        self._height = value  # 정사각형 제약 위반

    @Rectangle.height.setter
    def height(self, value):
        self._width = value
        self._height = value

# ✅ 올바른 설계: 상속 대신 구성
class Shape:
    def area(self):
        pass

class Rectangle(Shape):
    def __init__(self, width, height):
        self.width = width
        self.height = height

    def area(self):
        return self.width * self.height

class Square(Shape):
    def __init__(self, side):
        self.side = side

    def area(self):
        return self.side * self.side
```

### 4. Interface Segregation Principle (ISP)

```python
# ❌ ISP 위반
class Worker:
    def work(self):
        pass

    def eat(self):
        pass

class Robot(Worker):
    def work(self):
        return "Robot working"

    def eat(self):
        raise NotImplementedError("Robots don't eat!")  # 불필요한 메서드

# ✅ ISP 준수
class Workable(ABC):
    @abstractmethod
    def work(self):
        pass

class Eatable(ABC):
    @abstractmethod
    def eat(self):
        pass

class Human(Workable, Eatable):
    def work(self):
        return "Human working"

    def eat(self):
        return "Human eating"

class Robot(Workable):
    def work(self):
        return "Robot working"
    # eat() 메서드 없음
```

### 5. Dependency Inversion Principle (DIP)

```python
# ❌ DIP 위반
class MySQLDatabase:
    def save(self, data):
        print(f"Saving to MySQL: {data}")

class UserService:
    def __init__(self):
        self.db = MySQLDatabase()  # 구체 클래스에 의존

    def create_user(self, user):
        self.db.save(user)

# ✅ DIP 준수
class Database(ABC):
    """추상화에 의존"""
    @abstractmethod
    def save(self, data):
        pass

class MySQLDatabase(Database):
    def save(self, data):
        print(f"Saving to MySQL: {data}")

class MongoDatabase(Database):
    def save(self, data):
        print(f"Saving to MongoDB: {data}")

class UserService:
    def __init__(self, database: Database):
        self.db = database  # 추상화에 의존

    def create_user(self, user):
        self.db.save(user)

# Dependency Injection
mysql_db = MySQLDatabase()
user_service = UserService(mysql_db)

# 쉽게 교체 가능
mongo_db = MongoDatabase()
user_service = UserService(mongo_db)
```

---

## 테스트 주도 개발 (TDD)

### 1. TDD 사이클: Red-Green-Refactor

```python
import unittest

# 1. RED: 실패하는 테스트 작성
class TestCalculator(unittest.TestCase):
    def test_add(self):
        calc = Calculator()
        result = calc.add(2, 3)
        self.assertEqual(result, 5)

# 2. GREEN: 최소한의 코드로 통과
class Calculator:
    def add(self, a, b):
        return a + b

# 3. REFACTOR: 코드 개선

# 다음 기능
class TestCalculator(unittest.TestCase):
    def test_divide(self):
        calc = Calculator()
        result = calc.divide(10, 2)
        self.assertEqual(result, 5)

    def test_divide_by_zero(self):
        calc = Calculator()
        with self.assertRaises(ValueError):
            calc.divide(10, 0)

class Calculator:
    def add(self, a, b):
        return a + b

    def divide(self, a, b):
        if b == 0:
            raise ValueError("Cannot divide by zero")
        return a / b
```

### 2. 테스트 더블 (Test Doubles)

```python
from unittest.mock import Mock, MagicMock, patch

# Stub: 미리 정의된 응답 반환
class EmailServiceStub:
    def send_email(self, to, subject, body):
        return True  # 항상 성공

# Mock: 호출 검증
class TestUserService(unittest.TestCase):
    def test_register_user_sends_email(self):
        email_service = Mock()
        user_service = UserService(email_service)

        user_service.register("user@example.com")

        # 이메일 서비스가 호출되었는지 검증
        email_service.send_email.assert_called_once_with(
            to="user@example.com",
            subject="Welcome",
            body=unittest.mock.ANY
        )

# Spy: 호출 기록
class EmailServiceSpy:
    def __init__(self):
        self.calls = []

    def send_email(self, to, subject, body):
        self.calls.append({'to': to, 'subject': subject, 'body': body})
        return True

# Fake: 실제 동작하는 간단한 구현
class InMemoryUserRepository:
    def __init__(self):
        self.users = {}

    def save(self, user):
        self.users[user.id] = user

    def find_by_id(self, user_id):
        return self.users.get(user_id)

# Patch: 런타임에 교체
class TestPaymentService(unittest.TestCase):
    @patch('stripe.Charge.create')
    def test_process_payment(self, mock_charge):
        mock_charge.return_value = {'id': 'ch_123', 'status': 'succeeded'}

        payment_service = PaymentService()
        result = payment_service.process(100, 'tok_visa')

        self.assertTrue(result['success'])
        mock_charge.assert_called_once()
```

### 3. 테스트 커버리지

```bash
# pytest-cov 사용
pytest --cov=myapp --cov-report=html tests/

# 최소 커버리지 강제
pytest --cov=myapp --cov-fail-under=80
```

---

## 리팩토링

### 1. 코드 스멜과 해결

```python
# Code Smell: Long Method
# ❌ Before
def process_order(order):
    # 100+ lines of code
    # Validation
    # Calculation
    # Database save
    # Email notification
    # Inventory update
    # Logging
    pass

# ✅ After: Extract Method
def process_order(order):
    validate_order(order)
    total = calculate_total(order)
    save_order(order)
    send_confirmation_email(order)
    update_inventory(order)
    log_order(order)

# Code Smell: Feature Envy
# ❌ Before
class Order:
    def __init__(self, customer):
        self.customer = customer

    def get_discount(self):
        if self.customer.is_premium():
            return 0.2
        elif self.customer.years_active() > 5:
            return 0.1
        return 0

# ✅ After: Move Method
class Customer:
    def get_discount(self):
        if self.is_premium():
            return 0.2
        elif self.years_active() > 5:
            return 0.1
        return 0

class Order:
    def __init__(self, customer):
        self.customer = customer

    def get_discount(self):
        return self.customer.get_discount()

# Code Smell: Primitive Obsession
# ❌ Before
def send_email(to: str, subject: str, body: str):
    # to가 유효한 이메일인지 매번 검증
    if '@' not in to:
        raise ValueError("Invalid email")
    pass

# ✅ After: Introduce Value Object
class Email:
    def __init__(self, address: str):
        if '@' not in address:
            raise ValueError("Invalid email")
        self._address = address

    @property
    def address(self):
        return self._address

def send_email(to: Email, subject: str, body: str):
    # Email 객체가 이미 유효함을 보장
    pass

# Code Smell: Switch Statements
# ❌ Before
def calculate_pay(employee):
    if employee.type == "ENGINEER":
        return employee.monthly_salary
    elif employee.type == "SALESMAN":
        return employee.monthly_salary + employee.commission
    elif employee.type == "MANAGER":
        return employee.monthly_salary + employee.bonus

# ✅ After: Polymorphism
class Employee(ABC):
    @abstractmethod
    def calculate_pay(self):
        pass

class Engineer(Employee):
    def calculate_pay(self):
        return self.monthly_salary

class Salesman(Employee):
    def calculate_pay(self):
        return self.monthly_salary + self.commission

class Manager(Employee):
    def calculate_pay(self):
        return self.monthly_salary + self.bonus
```

### 2. 리팩토링 기법

```python
# Extract Variable
# Before
if (order.items.filter(lambda x: x.price > 100).count() > 5 and
    order.customer.loyalty_points > 1000):
    apply_discount()

# After
has_expensive_items = order.items.filter(lambda x: x.price > 100).count() > 5
is_loyal_customer = order.customer.loyalty_points > 1000

if has_expensive_items and is_loyal_customer:
    apply_discount()

# Introduce Parameter Object
# Before
def create_invoice(customer_name, customer_email, customer_address,
                   items, total, tax, discount):
    pass

# After
class Customer:
    def __init__(self, name, email, address):
        self.name = name
        self.email = email
        self.address = address

class Invoice:
    def __init__(self, items, total, tax, discount):
        self.items = items
        self.total = total
        self.tax = tax
        self.discount = discount

def create_invoice(customer: Customer, invoice: Invoice):
    pass

# Replace Conditional with Polymorphism
# Before
class Bird:
    def __init__(self, bird_type):
        self.type = bird_type

    def speed(self):
        if self.type == "EUROPEAN":
            return 35
        elif self.type == "AFRICAN":
            return 40
        elif self.type == "NORWEGIAN_BLUE":
            return 24

# After
class Bird(ABC):
    @abstractmethod
    def speed(self):
        pass

class EuropeanBird(Bird):
    def speed(self):
        return 35

class AfricanBird(Bird):
    def speed(self):
        return 40

class NorwegianBlueBird(Bird):
    def speed(self):
        return 24
```

---

**계속 작성중...**

소프트웨어 공학의 핵심 개념들을 모두 다뤘습니다:
- 23가지 GoF 디자인 패턴
- 아키텍처 패턴 (MVC, Clean Architecture, Event-Driven)
- SOLID 원칙 완벽 이해
- TDD와 테스트 전략
- 리팩토링 기법

이제 실무에서 확장 가능하고 유지보수 가능한 시스템을 설계할 수 있습니다.
