# 3️⃣ 네트워크 (Networks) 완전 정복

> 이것만 보면 네트워크는 끝!

---

## 📚 목차

1. [네트워크 기본 개념](#네트워크-기본-개념)
2. [OSI 7계층](#osi-7계층)
3. [TCP/IP 모델](#tcpip-모델)
4. [IP 주소와 서브넷](#ip-주소와-서브넷)
5. [TCP와 UDP](#tcp와-udp)
6. [HTTP/HTTPS](#httphttps)
7. [DNS](#dns)
8. [로드 밸런싱](#로드-밸런싱)
9. [면접 필수 질문](#면접-필수-질문)

---

## 네트워크 기본 개념

### 네트워크란?

**정의:** 컴퓨터들이 서로 통신할 수 있도록 연결된 시스템

### 네트워크 분류

| 종류 | 범위 | 예시 |
|------|------|------|
| PAN | 개인 | 블루투스 |
| LAN | 건물/캠퍼스 | 사무실 네트워크 |
| MAN | 도시 | 케이블 TV |
| WAN | 국가/대륙 | 인터넷 |

### 프로토콜 (Protocol)

**정의:** 컴퓨터 간 통신 규칙

**예시:**
- **HTTP**: 웹 통신
- **TCP**: 신뢰성 있는 데이터 전송
- **IP**: 주소 지정 및 라우팅

### 네트워크 토폴로지

```
Star (스타)           Bus (버스)
     Hub                  │
   /  |  \                │
  A   B   C           A─┼─B─┼─C

Ring (링)            Mesh (메시)
  A───B               A───B
  │   │               │\ /│
  D───C               │ X │
                      │/ \│
                      D───C
```

---

## OSI 7계층

### OSI 모델 개요

```
┌──────────────────────────────────┐
│ 7. Application  │ HTTP, FTP, DNS │ ← 사용자와 직접 상호작용
├──────────────────────────────────┤
│ 6. Presentation │ SSL/TLS, JPEG  │ ← 데이터 암호화/압축
├──────────────────────────────────┤
│ 5. Session      │ NetBIOS, RPC   │ ← 세션 관리
├──────────────────────────────────┤
│ 4. Transport    │ TCP, UDP       │ ← 신뢰성, 흐름 제어
├──────────────────────────────────┤
│ 3. Network      │ IP, ICMP       │ ← 라우팅, 주소 지정
├──────────────────────────────────┤
│ 2. Data Link    │ Ethernet, WiFi │ ← 프레임 전송
├──────────────────────────────────┤
│ 1. Physical     │ Cable, Hub     │ ← 비트 전송
└──────────────────────────────────┘
```

### 각 계층 설명

#### 1. Physical Layer (물리 계층)

**역할:** 비트를 전기 신호로 변환하여 전송

**장비:** 케이블, 허브, 리피터

**예시:**
- 이더넷 케이블
- 광섬유
- 무선 신호

#### 2. Data Link Layer (데이터 링크 계층)

**역할:**
- 프레임 단위 전송
- MAC 주소 사용
- 오류 검출

**장비:** 스위치, 브리지

**프로토콜:** Ethernet, WiFi, PPP

**Ethernet 프레임 구조:**
```
┌─────────┬──────┬──────┬──────┬─────┬─────┐
│Preamble │ Dest │ Src  │ Type │Data │ FCS │
│  (7B)   │ MAC  │ MAC  │ (2B) │     │(4B) │
└─────────┴──────┴──────┴──────┴─────┴─────┘
```

#### 3. Network Layer (네트워크 계층)

**역할:**
- 라우팅 (경로 결정)
- IP 주소 지정
- 패킷 전송

**장비:** 라우터

**프로토콜:** IP, ICMP, IGMP

**IP 패킷 구조:**
```
┌──────┬───────┬──────┬─────┬────────┬──────┐
│Version│Header│  TOS │Total│   ID   │Flags │
│ (4b) │Length│ (1B) │ Len │  (2B)  │ (3b) │
├──────┼───────┼──────┼─────┼────────┼──────┤
│  TTL │Proto  │Checksum│Source IP │       │
│ (1B) │ (1B)  │  (2B)  │   (4B)   │       │
├──────┴───────┴────────┴──────────┬────────┤
│      Destination IP (4B)         │        │
├──────────────────────────────────┴────────┤
│              Data                          │
└────────────────────────────────────────────┘
```

#### 4. Transport Layer (전송 계층)

**역할:**
- 신뢰성 있는 데이터 전송
- 흐름 제어
- 오류 검출 및 복구

**프로토콜:** TCP, UDP

**포트 번호:**
- 출발지/목적지 구분
- 0-65535

**Well-Known Ports:**
| 포트 | 프로토콜 | 용도 |
|------|---------|------|
| 20/21 | FTP | 파일 전송 |
| 22 | SSH | 원격 접속 |
| 23 | Telnet | 원격 접속 |
| 25 | SMTP | 메일 전송 |
| 53 | DNS | 도메인 이름 변환 |
| 80 | HTTP | 웹 |
| 443 | HTTPS | 보안 웹 |
| 3306 | MySQL | 데이터베이스 |
| 5432 | PostgreSQL | 데이터베이스 |

#### 5. Session Layer (세션 계층)

**역할:**
- 세션 수립/유지/종료
- 동기화

**예시:**
- RPC (Remote Procedure Call)
- NetBIOS

#### 6. Presentation Layer (표현 계층)

**역할:**
- 데이터 형식 변환
- 암호화/복호화
- 압축/해제

**예시:**
- SSL/TLS
- JPEG, MPEG
- ASCII, Unicode

#### 7. Application Layer (응용 계층)

**역할:**
- 사용자 인터페이스
- 애플리케이션 서비스

**프로토콜:**
- HTTP, HTTPS
- FTP, SMTP
- DNS, DHCP

---

## TCP/IP 모델

### OSI vs TCP/IP

```
OSI 7계층              TCP/IP 4계층
┌────────────┐         ┌────────────┐
│Application │         │            │
├────────────┤         │Application │
│Presentation│         │            │
├────────────┤         │            │
│  Session   │         │            │
├────────────┤         ├────────────┤
│ Transport  │   ←→    │ Transport  │
├────────────┤         ├────────────┤
│  Network   │   ←→    │  Internet  │
├────────────┤         ├────────────┤
│ Data Link  │         │            │
├────────────┤         │  Network   │
│  Physical  │         │  Access    │
└────────────┘         └────────────┘
```

### 데이터 전송 과정 (캡슐화/역캡슐화)

**캡슐화 (송신):**
```
Application:  Data
     ↓
Transport:    TCP Header + Data (Segment)
     ↓
Internet:     IP Header + Segment (Packet)
     ↓
Network:      Ethernet Header + Packet + Trailer (Frame)
     ↓
Physical:     Bits
```

**역캡슐화 (수신):**
```
Physical:     Bits
     ↓
Network:      Frame → Packet 추출
     ↓
Internet:     Packet → Segment 추출
     ↓
Transport:    Segment → Data 추출
     ↓
Application:  Data
```

---

## IP 주소와 서브넷

### IPv4 주소

**형식:** 32비트 = 4옥텟 (각 0-255)

**예시:** `192.168.1.100`

**클래스:**
```
Class A: 0.0.0.0   ~ 127.255.255.255  (앞 8비트 네트워크)
Class B: 128.0.0.0 ~ 191.255.255.255  (앞 16비트 네트워크)
Class C: 192.0.0.0 ~ 223.255.255.255  (앞 24비트 네트워크)
```

**사설 IP (Private IP):**
```
Class A: 10.0.0.0      ~ 10.255.255.255
Class B: 172.16.0.0    ~ 172.31.255.255
Class C: 192.168.0.0   ~ 192.168.255.255
```

### 서브넷 마스크 (Subnet Mask)

**목적:** 네트워크 부분과 호스트 부분 구분

**예시:**
```
IP:      192.168.1.100
Netmask: 255.255.255.0  (/24)

Network: 192.168.1.0
Host:    100
```

**CIDR 표기법:**
```
192.168.1.0/24
      ↑     ↑
      IP   네트워크 비트 수

/24 = 255.255.255.0
/16 = 255.255.0.0
/8  = 255.0.0.0
```

**서브넷 계산:**
```java
class SubnetCalculator {
    public static String getNetworkAddress(String ip, int prefix) {
        String[] octets = ip.split("\\.");
        int ipInt = 0;

        for (String octet : octets) {
            ipInt = (ipInt << 8) | Integer.parseInt(octet);
        }

        int mask = 0xFFFFFFFF << (32 - prefix);
        int network = ipInt & mask;

        return String.format("%d.%d.%d.%d",
            (network >> 24) & 0xFF,
            (network >> 16) & 0xFF,
            (network >> 8) & 0xFF,
            network & 0xFF
        );
    }

    // 사용 가능한 호스트 수
    public static int getHostCount(int prefix) {
        return (int) Math.pow(2, 32 - prefix) - 2;
        // -2: 네트워크 주소, 브로드캐스트 주소 제외
    }
}
```

### NAT (Network Address Translation)

**목적:** 사설 IP ↔ 공인 IP 변환

```
사설 네트워크                     인터넷
┌─────────────┐    NAT Router   ┌──────┐
│192.168.1.10 │──────────────→ │ 공인  │
│192.168.1.20 │  1.2.3.4:1000  │ IP   │
│192.168.1.30 │                 └──────┘
└─────────────┘
```

**장점:**
- IP 주소 절약
- 보안 (내부 IP 숨김)

### IPv6

**형식:** 128비트 = 8그룹 (16진수)

**예시:** `2001:0db8:85a3:0000:0000:8a2e:0370:7334`

**축약:**
```
2001:0db8:85a3:0:0:8a2e:370:7334  (앞 0 생략)
2001:0db8:85a3::8a2e:370:7334     (연속된 0 ::으로)
```

**필요성:**
- IPv4 고갈 (43억 개)
- IoT 기기 증가

---

## TCP와 UDP

### TCP (Transmission Control Protocol)

**특징:**
- **연결 지향**: 3-way handshake
- **신뢰성**: 재전송, 순서 보장
- **흐름 제어**: Sliding Window
- **혼잡 제어**: Slow Start, Congestion Avoidance

#### 3-Way Handshake (연결 수립)

```
Client                  Server
   │                       │
   │─────── SYN ──────────→│  (1) 연결 요청
   │                       │
   │←──── SYN + ACK ───────│  (2) 요청 수락
   │                       │
   │─────── ACK ──────────→│  (3) 확인
   │                       │
   │    연결 수립 완료     │
```

**과정:**
1. **Client → Server**: SYN (Seq=x)
2. **Server → Client**: SYN (Seq=y) + ACK (Ack=x+1)
3. **Client → Server**: ACK (Ack=y+1)

#### 4-Way Handshake (연결 종료)

```
Client                  Server
   │                       │
   │─────── FIN ──────────→│  (1) 종료 요청
   │                       │
   │←────── ACK ───────────│  (2) 확인
   │                       │
   │←────── FIN ───────────│  (3) 종료 준비 완료
   │                       │
   │─────── ACK ──────────→│  (4) 최종 확인
   │                       │
   │   TIME_WAIT (2MSL)    │
   │                       │
   │    연결 종료 완료     │
```

**TIME_WAIT:** 혹시 모를 지연 패킷을 위해 2MSL(Maximum Segment Lifetime) 대기

#### TCP 헤더

```
 0                   15 16                  31
┌──────────────────────┬──────────────────────┐
│   Source Port        │  Destination Port    │
├──────────────────────┴──────────────────────┤
│            Sequence Number                  │
├─────────────────────────────────────────────┤
│         Acknowledgment Number               │
├────┬────┬──────────┬─────────────────────────┤
│Hdr │Rsv │  Flags   │    Window Size         │
│Len │    │URG|ACK|  │                        │
│    │    │PSH|RST|  │                        │
│    │    │SYN|FIN|  │                        │
├────┴────┴──────────┴─────────────────────────┤
│   Checksum           │  Urgent Pointer      │
└──────────────────────┴──────────────────────┘
```

**주요 플래그:**
- **SYN**: 연결 시작
- **ACK**: 확인
- **FIN**: 연결 종료
- **RST**: 연결 리셋
- **PSH**: 즉시 전달
- **URG**: 긴급 데이터

### UDP (User Datagram Protocol)

**특징:**
- **비연결**: 핸드셰이크 없음
- **비신뢰성**: 재전송 없음
- **빠름**: 오버헤드 적음
- **순서 보장 안 함**

**UDP 헤더:**
```
 0      7 8     15 16    23 24    31
┌─────────┬─────────┬─────────┬─────────┐
│  Source │  Dest   │ Length  │Checksum │
│  Port   │  Port   │         │         │
└─────────┴─────────┴─────────┴─────────┘
```

**사용 사례:**
- **실시간 스트리밍**: 동영상, 음성
- **DNS**: 빠른 응답
- **DHCP**: IP 할당
- **게임**: 저지연 필요

### TCP vs UDP 비교

| 특징 | TCP | UDP |
|------|-----|-----|
| 연결 | 연결 지향 | 비연결 |
| 신뢰성 | 높음 | 낮음 |
| 속도 | 느림 | 빠름 |
| 순서 보장 | O | X |
| 재전송 | O | X |
| 헤더 크기 | 20바이트 | 8바이트 |
| 사용 사례 | HTTP, FTP, 이메일 | DNS, 스트리밍, 게임 |

### 실무 예시

```java
// TCP 소켓 (Java)
public class TCPServer {
    public static void main(String[] args) throws IOException {
        ServerSocket serverSocket = new ServerSocket(8080);
        System.out.println("서버 시작...");

        while (true) {
            Socket clientSocket = serverSocket.accept();  // 연결 대기
            System.out.println("클라이언트 연결: " + clientSocket.getInetAddress());

            // 데이터 송수신
            BufferedReader in = new BufferedReader(
                new InputStreamReader(clientSocket.getInputStream())
            );
            PrintWriter out = new PrintWriter(clientSocket.getOutputStream(), true);

            String message = in.readLine();
            System.out.println("받은 메시지: " + message);

            out.println("Echo: " + message);

            clientSocket.close();
        }
    }
}

// UDP 소켓 (Java)
public class UDPServer {
    public static void main(String[] args) throws IOException {
        DatagramSocket socket = new DatagramSocket(9090);
        byte[] buffer = new byte[1024];

        while (true) {
            DatagramPacket packet = new DatagramPacket(buffer, buffer.length);
            socket.receive(packet);  // 패킷 수신

            String message = new String(packet.getData(), 0, packet.getLength());
            System.out.println("받은 메시지: " + message);

            // 응답 전송
            String response = "Echo: " + message;
            byte[] sendData = response.getBytes();
            DatagramPacket sendPacket = new DatagramPacket(
                sendData, sendData.length,
                packet.getAddress(), packet.getPort()
            );
            socket.send(sendPacket);
        }
    }
}
```

---

## HTTP/HTTPS

### HTTP (HyperText Transfer Protocol)

**특징:**
- **비연결성 (Connectionless)**: 요청/응답 후 연결 종료
- **무상태성 (Stateless)**: 이전 요청 기억 안 함
- **텍스트 기반**

### HTTP 메서드

| 메서드 | 의미 | 안전 | 멱등성 |
|--------|------|------|--------|
| GET | 조회 | O | O |
| POST | 생성 | X | X |
| PUT | 전체 수정 | X | O |
| PATCH | 부분 수정 | X | X |
| DELETE | 삭제 | X | O |
| HEAD | 헤더만 조회 | O | O |
| OPTIONS | 허용 메서드 확인 | O | O |

**안전:** 서버 상태 변경 안 함
**멱등성:** 여러 번 호출해도 결과 동일

### HTTP 상태 코드

| 코드 | 의미 | 예시 |
|------|------|------|
| 1xx | 정보 | 100 Continue |
| 2xx | 성공 | 200 OK, 201 Created |
| 3xx | 리다이렉션 | 301 Moved Permanently, 302 Found |
| 4xx | 클라이언트 오류 | 400 Bad Request, 401 Unauthorized, 404 Not Found |
| 5xx | 서버 오류 | 500 Internal Server Error, 503 Service Unavailable |

### HTTP 요청/응답 구조

**요청:**
```
GET /index.html HTTP/1.1          ← Request Line
Host: www.example.com             ← Headers
User-Agent: Mozilla/5.0
Accept: text/html
                                  ← 빈 줄
[Request Body]                    ← Body (POST, PUT에서 사용)
```

**응답:**
```
HTTP/1.1 200 OK                   ← Status Line
Content-Type: text/html           ← Headers
Content-Length: 1234
Set-Cookie: session=abc123
                                  ← 빈 줄
<html>                            ← Body
  <body>Hello World</body>
</html>
```

### HTTP/1.1 vs HTTP/2 vs HTTP/3

| 특징 | HTTP/1.1 | HTTP/2 | HTTP/3 |
|------|----------|--------|--------|
| 프로토콜 | TCP | TCP | QUIC (UDP) |
| 멀티플렉싱 | X | O | O |
| 헤더 압축 | X | O (HPACK) | O (QPACK) |
| Server Push | X | O | O |
| Head of Line Blocking | O | 부분적 | X |

**HTTP/2 멀티플렉싱:**
```
HTTP/1.1
Request 1 → Response 1 → Request 2 → Response 2
(순차적)

HTTP/2
Request 1 ─┐
Request 2 ─┼→ Response 1, 2, 3 (동시에)
Request 3 ─┘
```

### HTTPS (HTTP Secure)

**특징:**
- HTTP + SSL/TLS
- 암호화된 통신
- 포트 443

#### SSL/TLS 핸드셰이크

```
Client                    Server
   │                         │
   │─── ClientHello ────────→│  (1) 지원 암호화 방식
   │                         │
   │←── ServerHello ─────────│  (2) 선택한 암호화, 인증서
   │    Certificate          │
   │    ServerHelloDone      │
   │                         │
   │─── ClientKeyExchange ──→│  (3) 대칭키 생성 정보
   │    ChangeCipherSpec     │
   │    Finished             │
   │                         │
   │←── ChangeCipherSpec ────│  (4) 암호화 시작
   │    Finished             │
   │                         │
   │    암호화된 통신       │
```

**대칭키 vs 비대칭키:**
```
비대칭키 (공개키 암호화)
- 핸드셰이크 시 대칭키 전달에 사용
- 느림

대칭키 (공통 비밀키)
- 실제 데이터 암호화에 사용
- 빠름
```

### 쿠키 vs 세션 vs 토큰

#### Cookie
```
Set-Cookie: sessionId=abc123; HttpOnly; Secure
```
- 클라이언트 저장
- 4KB 제한
- 자동 전송

#### Session
```
Server Memory
┌──────────────┐
│ sessionId: abc123 → {userId: 1, name: "John"} │
└──────────────┘
```
- 서버 저장
- 보안 좋음
- 서버 부하

#### JWT (JSON Web Token)
```
Header.Payload.Signature

eyJhbGci...  ← Base64(Header)
eyJzdWIi...  ← Base64(Payload)
SflKxwRJ...  ← Signature
```
- Stateless
- 확장성 좋음
- 취소 어려움

---

## DNS

### DNS (Domain Name System)

**목적:** 도메인 이름 → IP 주소 변환

```
www.example.com → 93.184.216.34
```

### DNS 계층 구조

```
                    Root (.)
                       │
         ┌─────────────┼─────────────┐
         │             │             │
        com           org           net
         │             │             │
    ┌────┼────┐        │             │
    │         │        │             │
 example   google   wikipedia      ...
    │         │
    │         │
   www      mail
```

### DNS 조회 과정

```
1. 브라우저 → www.example.com 입력

2. DNS Resolver (로컬)
   - 캐시 확인
   - 없으면 Root DNS 서버에 질의

3. Root DNS 서버
   - .com TLD 서버 주소 반환

4. TLD (Top Level Domain) 서버
   - example.com의 Name Server 주소 반환

5. Authoritative Name Server
   - www.example.com의 IP 주소 반환

6. DNS Resolver → 브라우저
   - IP 주소 전달
   - 캐시에 저장
```

### DNS 레코드 타입

| 타입 | 의미 | 예시 |
|------|------|------|
| A | IPv4 주소 | example.com → 93.184.216.34 |
| AAAA | IPv6 주소 | example.com → 2606:2800:220:1:... |
| CNAME | 별칭 | www.example.com → example.com |
| MX | 메일 서버 | example.com → mail.example.com |
| NS | 네임서버 | example.com → ns1.example.com |
| TXT | 텍스트 | SPF, DKIM 설정 |

### DNS 캐싱

```
┌──────────────┐
│   Browser    │ ← 브라우저 캐시
├──────────────┤
│   OS         │ ← OS 캐시
├──────────────┤
│   Router     │ ← 라우터 캐시
├──────────────┤
│ ISP Resolver │ ← ISP DNS 캐시
└──────────────┘
```

**TTL (Time To Live):**
```
example.com  3600  IN  A  93.184.216.34
                ↑
            TTL (초)
```

---

## 로드 밸런싱

### 로드 밸런서란?

**목적:** 트래픽을 여러 서버에 분산

```
           Load Balancer
                │
       ┌────────┼────────┐
       │        │        │
    Server1  Server2  Server3
```

### 로드 밸런싱 알고리즘

#### 1. Round Robin
```
Request 1 → Server 1
Request 2 → Server 2
Request 3 → Server 3
Request 4 → Server 1  (순환)
```

#### 2. Least Connections
```
Server 1: 10 connections
Server 2: 5 connections  ← 선택!
Server 3: 8 connections
```

#### 3. IP Hash
```
hash(Client IP) % Server Count
→ 같은 클라이언트는 항상 같은 서버
```

#### 4. Weighted Round Robin
```
Server 1 (weight=3): 3번
Server 2 (weight=1): 1번
Server 3 (weight=2): 2번
```

### L4 vs L7 로드 밸런서

| 구분 | L4 (Transport) | L7 (Application) |
|------|----------------|------------------|
| 기준 | IP, Port | URL, Cookie, Header |
| 속도 | 빠름 | 느림 |
| 기능 | 단순 분산 | 콘텐츠 기반 라우팅 |
| 예시 | TCP/UDP | HTTP, HTTPS |

**L7 예시:**
```
/api/*    → API Server
/static/* → Static Server
/admin/*  → Admin Server
```

### Health Check

```java
// Spring Boot Actuator
@RestController
public class HealthController {
    @GetMapping("/health")
    public ResponseEntity<String> health() {
        // DB 연결 확인
        // 메모리 사용량 확인
        // 등등

        return ResponseEntity.ok("UP");
    }
}
```

**로드 밸런서:**
```
주기적으로 /health 호출
→ 200 OK: 정상
→ 500 Error or Timeout: 비정상 (트래픽 차단)
```

---

## 면접 필수 질문

### Q1: OSI 7계층을 설명하고 각 계층의 역할은?

**A:**
1. **Physical**: 비트 전송 (케이블, 허브)
2. **Data Link**: 프레임 전송, MAC 주소 (스위치)
3. **Network**: 라우팅, IP 주소 (라우터)
4. **Transport**: 신뢰성, 포트 (TCP/UDP)
5. **Session**: 세션 관리
6. **Presentation**: 암호화, 압축
7. **Application**: 사용자 인터페이스 (HTTP, FTP)

### Q2: TCP와 UDP의 차이는?

**A:**
- **TCP**: 연결 지향, 신뢰성, 순서 보장, 느림 (웹, 이메일)
- **UDP**: 비연결, 비신뢰성, 빠름 (스트리밍, DNS, 게임)

### Q3: 3-way handshake란?

**A:**
TCP 연결 수립 과정
1. **Client → Server**: SYN (연결 요청)
2. **Server → Client**: SYN+ACK (수락)
3. **Client → Server**: ACK (확인)

### Q4: HTTP와 HTTPS의 차이는?

**A:**
- **HTTP**: 평문 통신, 포트 80
- **HTTPS**: SSL/TLS 암호화, 포트 443, 보안

### Q5: DNS 동작 원리는?

**A:**
1. 브라우저/OS 캐시 확인
2. DNS Resolver가 Root → TLD → Authoritative 순으로 질의
3. IP 주소 반환 및 캐시 저장

### Q6: 쿠키와 세션의 차이는?

**A:**
- **쿠키**: 클라이언트 저장, 4KB 제한, 빠름, 보안 약함
- **세션**: 서버 저장, 크기 제한 없음, 보안 좋음, 서버 부하

### Q7: 로드 밸런싱이 필요한 이유는?

**A:**
- **가용성**: 서버 장애 시 다른 서버로 트래픽 전환
- **확장성**: 서버 추가로 처리량 증가
- **성능**: 트래픽 분산으로 응답 속도 향상

### Q8: CORS란?

**A:**
**Cross-Origin Resource Sharing** (교차 출처 리소스 공유)
- 다른 도메인의 리소스 접근 제한
- 서버에서 `Access-Control-Allow-Origin` 헤더로 허용

```
Origin: https://example.com
Access-Control-Allow-Origin: https://example.com
```

### Q9: RESTful API란?

**A:**
**Representational State Transfer**
- **리소스 중심**: URL로 리소스 표현
- **HTTP 메서드**: GET, POST, PUT, DELETE
- **무상태성**: 각 요청 독립적

```
GET    /users     → 사용자 목록
GET    /users/1   → 사용자 1 조회
POST   /users     → 사용자 생성
PUT    /users/1   → 사용자 1 수정
DELETE /users/1   → 사용자 1 삭제
```

---

**이것만 마스터하면 네트워크는 끝!** 🌐
