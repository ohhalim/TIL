# 08. 보안과 암호학 (Security & Cryptography)

## 목차
1. [암호학 기초](#암호학-기초)
2. [대칭키 암호화](#대칭키-암호화)
3. [공개키 암호화](#공개키-암호화)
4. [해시 함수와 MAC](#해시-함수와-mac)
5. [디지털 서명](#디지털-서명)
6. [네트워크 보안](#네트워크-보안)
7. [웹 보안](#웹-보안)
8. [시스템 보안](#시스템-보안)

---

## 암호학 기초

### 1. 암호학의 핵심 개념

**보안의 3대 요소 (CIA Triad):**
- **기밀성 (Confidentiality)**: 인가된 사용자만 정보 접근
- **무결성 (Integrity)**: 데이터가 변조되지 않음을 보장
- **가용성 (Availability)**: 필요할 때 시스템 사용 가능

**추가 보안 속성:**
- **인증 (Authentication)**: 사용자/시스템 신원 검증
- **부인방지 (Non-repudiation)**: 행위를 부인할 수 없음
- **접근제어 (Access Control)**: 권한에 따른 접근 제한

### 2. Kerckhoffs의 원칙

> "암호 시스템은 키를 제외한 모든 것이 공개되어도 안전해야 한다"

```python
# 나쁜 예: 보안은 알고리즘의 비밀에 의존
def bad_encrypt(plaintext, secret_algo):
    # 알고리즘이 노출되면 즉시 무력화
    return secret_algo(plaintext)

# 좋은 예: 보안은 키의 비밀에 의존
def good_encrypt(plaintext, key, public_algorithm):
    # 알고리즘이 공개되어도 키가 안전하면 보안 유지
    return public_algorithm(plaintext, key)
```

### 3. 완전 순방향 비밀성 (Perfect Forward Secrecy)

```python
import os
from cryptography.hazmat.primitives.asymmetric import dh
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives import hashes

class DHKeyExchange:
    """Diffie-Hellman 키 교환으로 PFS 구현"""

    def __init__(self):
        # 파라미터 생성 (2048-bit)
        self.parameters = dh.generate_parameters(
            generator=2,
            key_size=2048
        )

    def generate_keypair(self):
        """세션마다 새로운 키쌍 생성"""
        private_key = self.parameters.generate_private_key()
        public_key = private_key.public_key()
        return private_key, public_key

    def derive_shared_secret(self, my_private, peer_public):
        """공유 비밀 유도"""
        shared_key = my_private.exchange(peer_public)

        # HKDF로 키 유도
        derived_key = HKDF(
            algorithm=hashes.SHA256(),
            length=32,
            salt=None,
            info=b'session key'
        ).derive(shared_key)

        return derived_key

# 사용 예
kex = DHKeyExchange()

# Alice
alice_private, alice_public = kex.generate_keypair()

# Bob
bob_private, bob_public = kex.generate_keypair()

# 각자 공유 비밀 계산
alice_shared = kex.derive_shared_secret(alice_private, bob_public)
bob_shared = kex.derive_shared_secret(bob_private, alice_public)

assert alice_shared == bob_shared  # 동일한 공유 비밀

# 세션 종료 후 개인키 삭제 → 이전 통신 복호화 불가능
```

---

## 대칭키 암호화

### 1. AES (Advanced Encryption Standard)

**AES-256 완전 구현:**

```python
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import os

class AES256:
    def __init__(self, key):
        """
        key: 32 bytes (256 bits)
        """
        if len(key) != 32:
            raise ValueError("Key must be 32 bytes for AES-256")
        self.key = key

    def encrypt_gcm(self, plaintext, associated_data=None):
        """
        GCM 모드: 인증 암호화 (AEAD)
        - 기밀성 + 무결성 동시 제공
        - Nonce는 절대 재사용 금지!
        """
        nonce = os.urandom(12)  # 96-bit nonce

        cipher = Cipher(
            algorithms.AES(self.key),
            modes.GCM(nonce),
            backend=default_backend()
        )

        encryptor = cipher.encryptor()

        if associated_data:
            encryptor.authenticate_additional_data(associated_data)

        ciphertext = encryptor.update(plaintext) + encryptor.finalize()
        tag = encryptor.tag  # 128-bit authentication tag

        return nonce, ciphertext, tag

    def decrypt_gcm(self, nonce, ciphertext, tag, associated_data=None):
        """GCM 복호화 및 인증 검증"""
        cipher = Cipher(
            algorithms.AES(self.key),
            modes.GCM(nonce, tag),
            backend=default_backend()
        )

        decryptor = cipher.decryptor()

        if associated_data:
            decryptor.authenticate_additional_data(associated_data)

        try:
            plaintext = decryptor.update(ciphertext) + decryptor.finalize()
            return plaintext
        except Exception:
            # Tag 검증 실패 → 위조 또는 변조
            raise ValueError("Authentication failed")

    def encrypt_cbc(self, plaintext):
        """
        CBC 모드: 고전적인 블록 암호 모드
        - Padding 필요
        - 인증 기능 없음 (별도 HMAC 필요)
        """
        from cryptography.hazmat.primitives import padding

        # PKCS7 패딩
        padder = padding.PKCS7(128).padder()
        padded_data = padder.update(plaintext) + padder.finalize()

        iv = os.urandom(16)  # 128-bit IV

        cipher = Cipher(
            algorithms.AES(self.key),
            modes.CBC(iv),
            backend=default_backend()
        )

        encryptor = cipher.encryptor()
        ciphertext = encryptor.update(padded_data) + encryptor.finalize()

        return iv, ciphertext

    def decrypt_cbc(self, iv, ciphertext):
        """CBC 복호화"""
        from cryptography.hazmat.primitives import padding

        cipher = Cipher(
            algorithms.AES(self.key),
            modes.CBC(iv),
            backend=default_backend()
        )

        decryptor = cipher.decryptor()
        padded_plaintext = decryptor.update(ciphertext) + decryptor.finalize()

        # 패딩 제거
        unpadder = padding.PKCS7(128).unpadder()
        plaintext = unpadder.update(padded_plaintext) + unpadder.finalize()

        return plaintext

# 사용 예
key = os.urandom(32)
aes = AES256(key)

message = b"Top secret information"
associated = b"user_id=12345"  # 암호화는 안 하지만 인증은 함

# GCM 모드 (권장)
nonce, ct, tag = aes.encrypt_gcm(message, associated)
pt = aes.decrypt_gcm(nonce, ct, tag, associated)
assert pt == message

# CBC 모드
iv, ct = aes.encrypt_cbc(message)
pt = aes.decrypt_cbc(iv, ct)
assert pt == message
```

### 2. ChaCha20-Poly1305

```python
from cryptography.hazmat.primitives.ciphers.aead import ChaCha20Poly1305

class ChaCha20Cipher:
    """
    ChaCha20-Poly1305: 스트림 암호 기반 AEAD
    - 소프트웨어에서 AES보다 빠름
    - 하드웨어 AES-NI 없는 환경에 적합
    """

    def __init__(self, key):
        if len(key) != 32:
            raise ValueError("Key must be 32 bytes")
        self.cipher = ChaCha20Poly1305(key)

    def encrypt(self, plaintext, associated_data=None):
        nonce = os.urandom(12)  # 96-bit nonce
        ciphertext = self.cipher.encrypt(nonce, plaintext, associated_data)
        return nonce, ciphertext

    def decrypt(self, nonce, ciphertext, associated_data=None):
        plaintext = self.cipher.decrypt(nonce, ciphertext, associated_data)
        return plaintext

# 성능 비교 벤치마크
import time

def benchmark_encryption(cipher, data, iterations=10000):
    start = time.time()
    for _ in range(iterations):
        nonce, ct = cipher.encrypt(data)
        pt = cipher.decrypt(nonce, ct)
    elapsed = time.time() - start
    return elapsed

data = b"A" * 1024  # 1KB

aes_key = os.urandom(32)
chacha_key = os.urandom(32)

aes = AES256(aes_key)
chacha = ChaCha20Cipher(chacha_key)

# 소프트웨어 구현: ChaCha20이 일반적으로 빠름
```

### 3. 암호 모드 비교

```python
"""
블록 암호 운영 모드 비교

ECB (Electronic Codebook):
❌ 사용 금지
- 동일한 평문 블록 → 동일한 암호문 블록
- 패턴이 노출됨

CBC (Cipher Block Chaining):
⚠️ 주의해서 사용
- IV 필수, IV는 예측 불가능해야 함
- Padding Oracle 공격 주의
- 병렬 복호화 가능, 암호화는 순차적

CTR (Counter Mode):
✅ 좋음
- 스트림 암호처럼 동작
- 병렬 처리 가능
- Nonce 재사용 절대 금지

GCM (Galois/Counter Mode):
✅ 최고
- AEAD: 인증 암호화
- 고속 병렬 처리
- TLS 1.3 기본 모드
"""

# ECB 취약점 시연
from cryptography.hazmat.primitives.ciphers import modes

def demonstrate_ecb_weakness():
    key = os.urandom(16)

    # 같은 평문 블록 반복
    plaintext = b"AAAAAAAAAAAAAAAA" * 4  # 64 bytes

    cipher = Cipher(algorithms.AES(key), modes.ECB())
    encryptor = cipher.encryptor()
    ciphertext = encryptor.update(plaintext) + encryptor.finalize()

    # 암호문에서 패턴 확인
    blocks = [ciphertext[i:i+16] for i in range(0, len(ciphertext), 16)]
    print("ECB blocks (all identical):")
    for i, block in enumerate(blocks):
        print(f"Block {i}: {block.hex()}")

    # 모든 블록이 동일 → 정보 누출!
    assert all(b == blocks[0] for b in blocks)

# Padding Oracle 공격
def padding_oracle_attack():
    """
    CBC 모드에서 패딩 검증 여부를 통해 평문 복구
    """
    def padding_oracle(iv, ciphertext):
        """패딩이 올바른지만 반환 (취약점)"""
        try:
            aes.decrypt_cbc(iv, ciphertext)
            return True
        except:
            return False

    # 공격자는 패딩 오류 여부만으로 평문을 한 바이트씩 복구 가능
    # 실제 구현은 복잡하므로 개념만 설명
    pass
```

---

## 공개키 암호화

### 1. RSA 완전 구현

```python
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes, serialization
import math

class RSACipher:
    def __init__(self, key_size=2048):
        """RSA 키 생성"""
        self.private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=key_size
        )
        self.public_key = self.private_key.public_key()

    def encrypt(self, plaintext):
        """
        OAEP 패딩 사용 (RSA-OAEP)
        - 평문 길이 제한: key_size/8 - 2*hash_size - 2
        - 2048-bit RSA + SHA-256: 최대 190 bytes
        """
        ciphertext = self.public_key.encrypt(
            plaintext,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        return ciphertext

    def decrypt(self, ciphertext):
        """RSA-OAEP 복호화"""
        plaintext = self.private_key.decrypt(
            ciphertext,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        return plaintext

    def sign(self, message):
        """RSA-PSS 서명"""
        signature = self.private_key.sign(
            message,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )
        return signature

    def verify(self, message, signature):
        """서명 검증"""
        try:
            self.public_key.verify(
                signature,
                message,
                padding.PSS(
                    mgf=padding.MGF1(hashes.SHA256()),
                    salt_length=padding.PSS.MAX_LENGTH
                ),
                hashes.SHA256()
            )
            return True
        except:
            return False

    def export_public_key(self):
        """공개키 PEM 포맷으로 내보내기"""
        pem = self.public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )
        return pem

    def export_private_key(self, password=None):
        """개인키 내보내기 (암호화 옵션)"""
        encryption = (
            serialization.BestAvailableEncryption(password.encode())
            if password
            else serialization.NoEncryption()
        )

        pem = self.private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=encryption
        )
        return pem

# RSA 수학적 원리
def rsa_math_demonstration():
    """RSA 알고리즘의 수학적 원리"""
    import random

    # 1. 두 큰 소수 선택
    p = 61
    q = 53

    # 2. n = p * q
    n = p * q  # 3233

    # 3. φ(n) = (p-1)(q-1)
    phi_n = (p - 1) * (q - 1)  # 3120

    # 4. e 선택: 1 < e < φ(n), gcd(e, φ(n)) = 1
    e = 17  # 공개 지수

    # 5. d 계산: d * e ≡ 1 (mod φ(n))
    d = pow(e, -1, phi_n)  # 2753, 개인 지수

    # 공개키: (e, n) = (17, 3233)
    # 개인키: (d, n) = (2753, 3233)

    # 암호화: c = m^e mod n
    message = 123
    ciphertext = pow(message, e, n)  # 855

    # 복호화: m = c^d mod n
    decrypted = pow(ciphertext, d, n)  # 123

    assert decrypted == message

    print(f"Message: {message}")
    print(f"Encrypted: {ciphertext}")
    print(f"Decrypted: {decrypted}")

# 하이브리드 암호화 (RSA + AES)
class HybridEncryption:
    """
    공개키로 대칭키 암호화, 대칭키로 데이터 암호화
    - 대용량 데이터에 적합
    - 공개키 암호의 속도 문제 해결
    """

    def __init__(self):
        self.rsa = RSACipher()

    def encrypt(self, plaintext):
        # 1. 랜덤 AES 키 생성
        aes_key = os.urandom(32)
        aes = AES256(aes_key)

        # 2. AES로 데이터 암호화
        nonce, ciphertext, tag = aes.encrypt_gcm(plaintext)

        # 3. RSA로 AES 키 암호화
        encrypted_key = self.rsa.encrypt(aes_key)

        return {
            'encrypted_key': encrypted_key,
            'nonce': nonce,
            'ciphertext': ciphertext,
            'tag': tag
        }

    def decrypt(self, encrypted_data):
        # 1. RSA로 AES 키 복호화
        aes_key = self.rsa.decrypt(encrypted_data['encrypted_key'])
        aes = AES256(aes_key)

        # 2. AES로 데이터 복호화
        plaintext = aes.decrypt_gcm(
            encrypted_data['nonce'],
            encrypted_data['ciphertext'],
            encrypted_data['tag']
        )

        return plaintext
```

### 2. 타원곡선 암호 (ECC)

```python
from cryptography.hazmat.primitives.asymmetric import ec

class ECCCipher:
    """
    ECC: RSA보다 작은 키로 동일한 보안 수준
    - 256-bit ECC ≈ 3072-bit RSA
    - 모바일/IoT에 적합
    """

    def __init__(self, curve=ec.SECP256R1()):
        """
        표준 곡선:
        - SECP256R1 (P-256): NIST 표준
        - SECP384R1 (P-384): 더 높은 보안
        - Curve25519: 최신, 고속
        """
        self.private_key = ec.generate_private_key(curve)
        self.public_key = self.private_key.public_key()

    def sign(self, message):
        """ECDSA 서명"""
        signature = self.private_key.sign(
            message,
            ec.ECDSA(hashes.SHA256())
        )
        return signature

    def verify(self, message, signature):
        """ECDSA 서명 검증"""
        try:
            self.public_key.verify(
                signature,
                message,
                ec.ECDSA(hashes.SHA256())
            )
            return True
        except:
            return False

    def ecdh_exchange(self, peer_public_key):
        """ECDH 키 교환"""
        shared_key = self.private_key.exchange(
            ec.ECDH(),
            peer_public_key
        )

        # KDF로 키 유도
        from cryptography.hazmat.primitives.kdf.hkdf import HKDF
        derived_key = HKDF(
            algorithm=hashes.SHA256(),
            length=32,
            salt=None,
            info=b'ecdh key'
        ).derive(shared_key)

        return derived_key

# Curve25519 (X25519)
from cryptography.hazmat.primitives.asymmetric import x25519

class X25519KeyExchange:
    """
    X25519: 최신 타원곡선 DH
    - 매우 빠름
    - Side-channel 공격에 강함
    - TLS 1.3, Signal Protocol 사용
    """

    def __init__(self):
        self.private_key = x25519.X25519PrivateKey.generate()
        self.public_key = self.private_key.public_key()

    def exchange(self, peer_public_key):
        shared_secret = self.private_key.exchange(peer_public_key)
        return shared_secret

# 사용 예: Signal Protocol 스타일 Double Ratchet
class DoubleRatchet:
    """
    Signal Protocol의 핵심 메커니즘
    - Forward Secrecy
    - Future Secrecy (Break-in Recovery)
    """

    def __init__(self):
        self.dh_ratchet = X25519KeyExchange()
        self.send_chain_key = os.urandom(32)
        self.recv_chain_key = os.urandom(32)
        self.message_number = 0

    def ratchet_encrypt(self, plaintext, peer_public_key):
        # DH Ratchet
        shared = self.dh_ratchet.exchange(peer_public_key)

        # KDF Chain
        from cryptography.hazmat.primitives.kdf.hkdf import HKDF
        new_chain = HKDF(
            algorithm=hashes.SHA256(),
            length=64,
            salt=self.send_chain_key,
            info=b'ratchet'
        ).derive(shared)

        self.send_chain_key = new_chain[:32]
        message_key = new_chain[32:]

        # 메시지 암호화
        aes = AES256(message_key)
        nonce, ct, tag = aes.encrypt_gcm(plaintext)

        self.message_number += 1

        return {
            'dh_public': self.dh_ratchet.public_key.public_bytes(
                encoding=serialization.Encoding.Raw,
                format=serialization.PublicFormat.Raw
            ),
            'message_number': self.message_number,
            'nonce': nonce,
            'ciphertext': ct,
            'tag': tag
        }
```

---

## 해시 함수와 MAC

### 1. 암호학적 해시 함수

```python
import hashlib
import hmac

class CryptographicHash:
    """
    해시 함수의 3가지 핵심 속성:
    1. Preimage Resistance: h(x) → x 계산 불가능
    2. Second Preimage Resistance: x, h(x) → x' (h(x') = h(x)) 찾기 불가능
    3. Collision Resistance: h(x) = h(y)인 x, y 찾기 불가능
    """

    @staticmethod
    def sha256(data):
        """SHA-256: 가장 널리 사용"""
        return hashlib.sha256(data).digest()

    @staticmethod
    def sha3_256(data):
        """SHA-3: Keccak 기반, 새로운 표준"""
        return hashlib.sha3_256(data).digest()

    @staticmethod
    def blake2b(data, key=None):
        """BLAKE2: 매우 빠름, 키 지원"""
        return hashlib.blake2b(data, key=key).digest()

# 비밀번호 해싱 (절대 일반 해시 사용 금지!)
import bcrypt
import argon2

class PasswordHashing:
    """
    비밀번호 해싱 원칙:
    - Salt 사용 (Rainbow Table 방어)
    - Slow Hash (Brute Force 방어)
    - Memory-Hard (ASIC/GPU 공격 방어)
    """

    @staticmethod
    def hash_bcrypt(password):
        """
        bcrypt: 시간이 지나도 안전
        - Work factor 조정 가능
        """
        salt = bcrypt.gensalt(rounds=12)  # 2^12 iterations
        hashed = bcrypt.hashpw(password.encode(), salt)
        return hashed

    @staticmethod
    def verify_bcrypt(password, hashed):
        return bcrypt.checkpw(password.encode(), hashed)

    @staticmethod
    def hash_argon2(password):
        """
        Argon2: 최신 표준 (PHC 우승)
        - Memory-hard
        - Argon2id 권장 (hybrid)
        """
        ph = argon2.PasswordHasher(
            time_cost=2,        # iterations
            memory_cost=65536,  # 64 MB
            parallelism=4,      # threads
            hash_len=32,
            salt_len=16
        )
        hashed = ph.hash(password)
        return hashed

    @staticmethod
    def verify_argon2(password, hashed):
        ph = argon2.PasswordHasher()
        try:
            ph.verify(hashed, password)
            return True
        except:
            return False

# 사용 예
pw = "MySecurePassword123!"

# ❌ 절대 이렇게 하지 마세요
bad_hash = hashlib.sha256(pw.encode()).hexdigest()

# ✅ 올바른 방법
good_hash = PasswordHashing.hash_argon2(pw)
is_valid = PasswordHashing.verify_argon2(pw, good_hash)
```

### 2. HMAC (Hash-based Message Authentication Code)

```python
class MessageAuthentication:
    """
    HMAC: 메시지 무결성 및 인증
    - 키를 가진 사람만 생성/검증 가능
    - 변조 감지
    """

    def __init__(self, key):
        self.key = key

    def generate_hmac(self, message):
        """HMAC-SHA256 생성"""
        h = hmac.new(self.key, message, hashlib.sha256)
        return h.digest()

    def verify_hmac(self, message, mac):
        """Constant-time 비교 (Timing Attack 방지)"""
        expected = self.generate_hmac(message)
        return hmac.compare_digest(expected, mac)

# Timing Attack 예시
def insecure_compare(a, b):
    """❌ 취약한 비교"""
    if len(a) != len(b):
        return False
    for i in range(len(a)):
        if a[i] != b[i]:
            return False  # 즉시 반환 → 시간 차이 발생
    return True

def secure_compare(a, b):
    """✅ 안전한 비교"""
    return hmac.compare_digest(a, b)  # Constant-time

# Encrypt-then-MAC (권장)
class AuthenticatedEncryption:
    def __init__(self, enc_key, mac_key):
        self.aes = AES256(enc_key)
        self.mac = MessageAuthentication(mac_key)

    def encrypt(self, plaintext):
        # 1. 암호화
        iv, ciphertext = self.aes.encrypt_cbc(plaintext)

        # 2. MAC 생성 (암호문에 대해)
        mac = self.mac.generate_hmac(iv + ciphertext)

        return iv, ciphertext, mac

    def decrypt(self, iv, ciphertext, mac):
        # 1. MAC 검증 먼저!
        if not self.mac.verify_hmac(iv + ciphertext, mac):
            raise ValueError("MAC verification failed")

        # 2. 복호화
        plaintext = self.aes.decrypt_cbc(iv, ciphertext)
        return plaintext
```

### 3. Merkle Tree

```python
class MerkleTree:
    """
    Merkle Tree: 대량 데이터 무결성 검증
    - 블록체인, Git, 분산 시스템 사용
    - O(log n) 검증
    """

    def __init__(self, data_blocks):
        self.leaves = [hashlib.sha256(d).digest() for d in data_blocks]
        self.root = self._build_tree(self.leaves)

    def _build_tree(self, nodes):
        """Bottom-up으로 트리 구축"""
        if len(nodes) == 1:
            return nodes[0]

        # 짝수 개로 만들기
        if len(nodes) % 2 == 1:
            nodes.append(nodes[-1])

        # 상위 레벨 계산
        parent_nodes = []
        for i in range(0, len(nodes), 2):
            combined = nodes[i] + nodes[i+1]
            parent_hash = hashlib.sha256(combined).digest()
            parent_nodes.append(parent_hash)

        return self._build_tree(parent_nodes)

    def get_proof(self, index):
        """특정 leaf의 Merkle Proof 생성"""
        proof = []
        nodes = self.leaves.copy()

        while len(nodes) > 1:
            if len(nodes) % 2 == 1:
                nodes.append(nodes[-1])

            # Sibling 추가
            if index % 2 == 0:
                sibling = nodes[index + 1] if index + 1 < len(nodes) else nodes[index]
                proof.append(('right', sibling))
            else:
                sibling = nodes[index - 1]
                proof.append(('left', sibling))

            # 상위 레벨로
            index //= 2
            parent_nodes = []
            for i in range(0, len(nodes), 2):
                parent = hashlib.sha256(nodes[i] + nodes[i+1]).digest()
                parent_nodes.append(parent)
            nodes = parent_nodes

        return proof

    def verify_proof(self, leaf_data, index, proof, root):
        """Merkle Proof 검증"""
        current_hash = hashlib.sha256(leaf_data).digest()

        for direction, sibling in proof:
            if direction == 'left':
                current_hash = hashlib.sha256(sibling + current_hash).digest()
            else:
                current_hash = hashlib.sha256(current_hash + sibling).digest()

        return current_hash == root

# 사용 예
data = [b"block1", b"block2", b"block3", b"block4"]
tree = MerkleTree(data)

# block2의 존재 증명
proof = tree.get_proof(1)
is_valid = tree.verify_proof(b"block2", 1, proof, tree.root)
print(f"Proof valid: {is_valid}")
```

---

## 디지털 서명

### 1. 서명 체계

```python
from cryptography.hazmat.primitives.asymmetric import ed25519

class DigitalSignature:
    """
    디지털 서명의 속성:
    1. Authentication: 서명자 신원 확인
    2. Integrity: 메시지 무결성
    3. Non-repudiation: 부인 방지
    """

    def __init__(self):
        # Ed25519: 최신 서명 알고리즘
        # - 매우 빠름
        # - 작은 서명 크기 (64 bytes)
        # - 결정적 (동일 메시지 → 동일 서명)
        self.private_key = ed25519.Ed25519PrivateKey.generate()
        self.public_key = self.private_key.public_key()

    def sign(self, message):
        signature = self.private_key.sign(message)
        return signature

    def verify(self, message, signature, public_key=None):
        key = public_key or self.public_key
        try:
            key.verify(signature, message)
            return True
        except:
            return False

# Blind Signature (익명 전자화폐에 사용)
class BlindSignature:
    """
    Blind Signature: 서명자가 내용을 모르고 서명
    - 전자 투표
    - 익명 인증
    - 디지털 캐시
    """

    def __init__(self):
        self.rsa = RSACipher(key_size=2048)

    def blind(self, message):
        """메시지 블라인딩"""
        # r^e * m mod n
        import random
        r = random.randint(2, self.rsa.public_key.public_numbers().n - 1)

        # 실제 구현은 복잡 - 개념만 설명
        blinded = message  # r^e * message mod n
        return blinded, r

    def sign_blind(self, blinded_message):
        """블라인딩된 메시지 서명"""
        # (r^e * m)^d = r * m^d mod n
        signature = self.rsa.decrypt(blinded_message)
        return signature

    def unblind(self, blind_signature, r):
        """서명 언블라인딩"""
        # signature / r = m^d mod n
        unblinded = blind_signature  # / r mod n
        return unblinded
```

### 2. 인증서와 PKI

```python
from cryptography import x509
from cryptography.x509.oid import NameOID, ExtensionOID
from datetime import datetime, timedelta

class CertificateAuthority:
    """
    PKI (Public Key Infrastructure)
    - CA (인증 기관)
    - 인증서 발급 및 검증
    - 인증서 체인
    """

    def __init__(self):
        # CA 키 생성
        self.ca_private = rsa.generate_private_key(
            public_exponent=65537,
            key_size=4096
        )
        self.ca_public = self.ca_private.public_key()

        # Self-signed CA 인증서
        self.ca_cert = self._create_ca_certificate()

    def _create_ca_certificate(self):
        """CA 자체 서명 인증서"""
        subject = issuer = x509.Name([
            x509.NameAttribute(NameOID.COUNTRY_NAME, "US"),
            x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, "California"),
            x509.NameAttribute(NameOID.ORGANIZATION_NAME, "My CA"),
            x509.NameAttribute(NameOID.COMMON_NAME, "My Root CA"),
        ])

        cert = x509.CertificateBuilder().subject_name(
            subject
        ).issuer_name(
            issuer
        ).public_key(
            self.ca_public
        ).serial_number(
            x509.random_serial_number()
        ).not_valid_before(
            datetime.utcnow()
        ).not_valid_after(
            datetime.utcnow() + timedelta(days=3650)  # 10년
        ).add_extension(
            x509.BasicConstraints(ca=True, path_length=None),
            critical=True
        ).add_extension(
            x509.KeyUsage(
                digital_signature=True,
                key_cert_sign=True,
                crl_sign=True,
                key_encipherment=False,
                content_commitment=False,
                data_encipherment=False,
                key_agreement=False,
                encipher_only=False,
                decipher_only=False
            ),
            critical=True
        ).sign(self.ca_private, hashes.SHA256())

        return cert

    def issue_certificate(self, csr, validity_days=365):
        """CSR로부터 인증서 발급"""
        cert = x509.CertificateBuilder().subject_name(
            csr.subject
        ).issuer_name(
            self.ca_cert.subject
        ).public_key(
            csr.public_key()
        ).serial_number(
            x509.random_serial_number()
        ).not_valid_before(
            datetime.utcnow()
        ).not_valid_after(
            datetime.utcnow() + timedelta(days=validity_days)
        ).add_extension(
            x509.BasicConstraints(ca=False, path_length=None),
            critical=True
        ).add_extension(
            x509.KeyUsage(
                digital_signature=True,
                key_encipherment=True,
                key_cert_sign=False,
                crl_sign=False,
                content_commitment=False,
                data_encipherment=False,
                key_agreement=False,
                encipher_only=False,
                decipher_only=False
            ),
            critical=True
        ).sign(self.ca_private, hashes.SHA256())

        return cert

    def verify_certificate(self, cert):
        """인증서 검증"""
        # 1. 서명 검증
        try:
            self.ca_public.verify(
                cert.signature,
                cert.tbs_certificate_bytes,
                padding.PKCS1v15(),
                cert.signature_hash_algorithm
            )
        except:
            return False

        # 2. 유효 기간 검증
        now = datetime.utcnow()
        if not (cert.not_valid_before <= now <= cert.not_valid_after):
            return False

        # 3. Revocation 검증 (CRL/OCSP)
        # 실제로는 CRL 또는 OCSP 확인 필요

        return True

# CSR (Certificate Signing Request) 생성
def create_csr(private_key, common_name):
    csr = x509.CertificateSigningRequestBuilder().subject_name(
        x509.Name([
            x509.NameAttribute(NameOID.COUNTRY_NAME, "US"),
            x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, "CA"),
            x509.NameAttribute(NameOID.ORGANIZATION_NAME, "My Company"),
            x509.NameAttribute(NameOID.COMMON_NAME, common_name),
        ])
    ).sign(private_key, hashes.SHA256())

    return csr

# 사용 예
ca = CertificateAuthority()

# 클라이언트 키 생성
client_private = rsa.generate_private_key(65537, 2048)
client_public = client_private.public_key()

# CSR 생성
csr = create_csr(client_private, "client.example.com")

# CA가 인증서 발급
client_cert = ca.issue_certificate(csr)

# 인증서 검증
is_valid = ca.verify_certificate(client_cert)
print(f"Certificate valid: {is_valid}")
```

---

## 네트워크 보안

### 1. TLS/SSL 완전 해부

```python
import ssl
import socket

class TLSConnection:
    """
    TLS 1.3 연결 과정:
    1. ClientHello
    2. ServerHello
    3. Encrypted Extensions
    4. Certificate
    5. CertificateVerify
    6. Finished
    """

    @staticmethod
    def create_secure_client(hostname, port=443):
        """안전한 TLS 클라이언트"""
        context = ssl.create_default_context()

        # 최신 프로토콜만 허용
        context.minimum_version = ssl.TLSVersion.TLSv1_3

        # 강력한 암호 스위트만
        context.set_ciphers('ECDHE+AESGCM:ECDHE+CHACHA20')

        # 인증서 검증 필수
        context.check_hostname = True
        context.verify_mode = ssl.CERT_REQUIRED

        # 연결
        with socket.create_connection((hostname, port)) as sock:
            with context.wrap_socket(sock, server_hostname=hostname) as ssock:
                print(f"TLS Version: {ssock.version()}")
                print(f"Cipher: {ssock.cipher()}")

                cert = ssock.getpeercert()
                print(f"Certificate: {cert['subject']}")

                return ssock

    @staticmethod
    def create_secure_server(certfile, keyfile, port=4433):
        """안전한 TLS 서버"""
        context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
        context.load_cert_chain(certfile, keyfile)

        # TLS 1.3 only
        context.minimum_version = ssl.TLSVersion.TLSv1_3

        # Forward Secrecy 필수
        context.set_ciphers('ECDHE+AESGCM')

        # 선택: 클라이언트 인증 요구
        # context.verify_mode = ssl.CERT_REQUIRED

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.bind(('localhost', port))
            sock.listen(5)

            with context.wrap_socket(sock, server_side=True) as ssock:
                conn, addr = ssock.accept()
                return conn

# Certificate Pinning
class CertificatePinning:
    """
    Certificate Pinning: 특정 인증서/공개키만 신뢰
    - MITM 공격 방어
    - 잘못된 CA로부터 보호
    """

    def __init__(self, pinned_certs):
        """pinned_certs: SHA-256 해시 리스트"""
        self.pinned_certs = set(pinned_certs)

    def verify_pin(self, cert_der):
        cert_hash = hashlib.sha256(cert_der).hexdigest()
        return cert_hash in self.pinned_certs

# HSTS (HTTP Strict Transport Security)
def check_hsts(hostname):
    """HSTS 헤더 확인"""
    import http.client

    conn = http.client.HTTPSConnection(hostname)
    conn.request("GET", "/")
    response = conn.getresponse()

    hsts = response.getheader("Strict-Transport-Security")
    if hsts:
        print(f"HSTS: {hsts}")
        # max-age=31536000; includeSubDomains; preload
    else:
        print("⚠️ HSTS not enabled")
```

### 2. VPN 및 터널링

```python
# IPsec / WireGuard 개념 구현
class WireGuardSimulator:
    """
    WireGuard: 최신 VPN 프로토콜
    - Noise Protocol Framework
    - Curve25519, ChaCha20, Poly1305
    - 매우 빠르고 간단
    """

    def __init__(self):
        self.static_private = x25519.X25519PrivateKey.generate()
        self.static_public = self.static_private.public_key()

    def handshake_init(self, peer_static_public):
        """Handshake Initiation"""
        # Ephemeral 키 생성
        ephemeral_private = x25519.X25519PrivateKey.generate()
        ephemeral_public = ephemeral_private.public_key()

        # DH 계산
        dh1 = ephemeral_private.exchange(peer_static_public)
        dh2 = self.static_private.exchange(peer_static_public)

        # KDF
        from cryptography.hazmat.primitives.kdf.hkdf import HKDF
        key_material = HKDF(
            algorithm=hashes.SHA256(),
            length=64,
            salt=None,
            info=b'wireguard'
        ).derive(dh1 + dh2)

        transport_send = key_material[:32]
        transport_recv = key_material[32:]

        return ephemeral_public, transport_send, transport_recv

# DNS over HTTPS (DoH)
class DoHClient:
    """
    DNS over HTTPS: DNS 쿼리 암호화
    - ISP로부터 DNS 쿼리 보호
    - 중간자 공격 방어
    """

    def __init__(self, doh_server="https://1.1.1.1/dns-query"):
        self.server = doh_server

    def query(self, domain, record_type="A"):
        import requests
        import base64

        # DNS 쿼리를 Base64 인코딩
        # 실제로는 DNS wire format 구성 필요
        response = requests.get(
            self.server,
            params={
                'name': domain,
                'type': record_type
            },
            headers={'Accept': 'application/dns-json'}
        )

        return response.json()
```

---

## 웹 보안

### 1. 주요 웹 공격 및 방어

```python
# XSS (Cross-Site Scripting) 방어
import html

def sanitize_html(user_input):
    """❌ HTML 태그 이스케이프"""
    return html.escape(user_input)

# Content Security Policy
def set_csp_header():
    """✅ CSP로 XSS 완전 차단"""
    return {
        'Content-Security-Policy':
            "default-src 'self'; "
            "script-src 'self' 'nonce-{random}'; "
            "style-src 'self' 'nonce-{random}'; "
            "img-src 'self' data: https:; "
            "font-src 'self'; "
            "connect-src 'self'; "
            "frame-ancestors 'none'; "
            "base-uri 'self'; "
            "form-action 'self'"
    }

# SQL Injection 방어
import sqlite3

def insecure_query(username):
    """❌ SQL Injection 취약"""
    query = f"SELECT * FROM users WHERE username = '{username}'"
    # username = "admin' OR '1'='1" → 모든 사용자 조회
    return query

def secure_query(username):
    """✅ Prepared Statement 사용"""
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM users WHERE username = ?",
        (username,)
    )
    return cursor.fetchall()

# CSRF (Cross-Site Request Forgery) 방어
import secrets

class CSRFProtection:
    """CSRF 토큰 기반 방어"""

    @staticmethod
    def generate_token():
        """암호학적으로 안전한 토큰 생성"""
        return secrets.token_urlsafe(32)

    @staticmethod
    def verify_token(submitted, session_token):
        """Constant-time 비교"""
        return hmac.compare_digest(submitted, session_token)

# 사용 예 (Flask)
"""
@app.before_request
def csrf_protect():
    if request.method == "POST":
        token = session.get('csrf_token')
        if not token or token != request.form.get('csrf_token'):
            abort(403)

@app.route('/form')
def form():
    csrf_token = CSRFProtection.generate_token()
    session['csrf_token'] = csrf_token
    return render_template('form.html', csrf_token=csrf_token)
"""

# Clickjacking 방어
def anti_clickjacking_headers():
    return {
        'X-Frame-Options': 'DENY',
        'Content-Security-Policy': "frame-ancestors 'none'"
    }

# Session Hijacking 방어
class SecureSession:
    """안전한 세션 관리"""

    def __init__(self):
        self.sessions = {}

    def create_session(self, user_id, request_info):
        # 강력한 세션 ID
        session_id = secrets.token_urlsafe(32)

        self.sessions[session_id] = {
            'user_id': user_id,
            'created_at': datetime.utcnow(),
            'ip_address': request_info['ip'],
            'user_agent': request_info['user_agent']
        }

        return session_id

    def validate_session(self, session_id, request_info):
        session = self.sessions.get(session_id)
        if not session:
            return False

        # IP/User-Agent 변경 감지
        if (session['ip_address'] != request_info['ip'] or
            session['user_agent'] != request_info['user_agent']):
            # Suspicious activity
            del self.sessions[session_id]
            return False

        # 세션 타임아웃 (30분)
        age = datetime.utcnow() - session['created_at']
        if age.total_seconds() > 1800:
            del self.sessions[session_id]
            return False

        return True

    def rotate_session(self, old_session_id, request_info):
        """세션 고정 공격 방어"""
        session = self.sessions.get(old_session_id)
        if not session:
            return None

        # 새 세션 ID 발급
        new_session_id = self.create_session(
            session['user_id'],
            request_info
        )

        # 구 세션 삭제
        del self.sessions[old_session_id]

        return new_session_id
```

### 2. API 보안

```python
# JWT (JSON Web Token)
import jwt
from datetime import datetime, timedelta

class JWTAuth:
    """
    JWT 보안 고려사항:
    - 짧은 만료 시간
    - Refresh Token 별도 관리
    - 민감 정보 포함 금지 (payload는 암호화 안 됨)
    """

    def __init__(self, secret_key):
        self.secret = secret_key
        self.algorithm = 'HS256'

    def generate_token(self, user_id, expires_in=3600):
        """Access Token 생성"""
        payload = {
            'user_id': user_id,
            'exp': datetime.utcnow() + timedelta(seconds=expires_in),
            'iat': datetime.utcnow(),
            'jti': secrets.token_urlsafe(16)  # JWT ID (revocation용)
        }

        token = jwt.encode(payload, self.secret, algorithm=self.algorithm)
        return token

    def verify_token(self, token):
        """토큰 검증"""
        try:
            payload = jwt.decode(
                token,
                self.secret,
                algorithms=[self.algorithm]
            )
            return payload
        except jwt.ExpiredSignatureError:
            raise ValueError("Token expired")
        except jwt.InvalidTokenError:
            raise ValueError("Invalid token")

    def generate_refresh_token(self, user_id):
        """Refresh Token (더 긴 만료 시간)"""
        payload = {
            'user_id': user_id,
            'exp': datetime.utcnow() + timedelta(days=30),
            'type': 'refresh'
        }

        return jwt.encode(payload, self.secret, algorithm=self.algorithm)

# OAuth 2.0 Flow
class OAuth2Server:
    """
    OAuth 2.0 Authorization Code Flow
    - 가장 안전한 OAuth 흐름
    - PKCE 필수 (Public Client)
    """

    def __init__(self):
        self.auth_codes = {}
        self.access_tokens = {}

    def authorization_request(self, client_id, redirect_uri, state, code_challenge):
        """Authorization Code 발급"""
        # PKCE: code_challenge = BASE64URL(SHA256(code_verifier))
        auth_code = secrets.token_urlsafe(32)

        self.auth_codes[auth_code] = {
            'client_id': client_id,
            'redirect_uri': redirect_uri,
            'code_challenge': code_challenge,
            'expires_at': datetime.utcnow() + timedelta(minutes=10)
        }

        # Redirect to: redirect_uri?code={auth_code}&state={state}
        return auth_code

    def token_request(self, auth_code, client_id, redirect_uri, code_verifier):
        """Access Token 발급"""
        code_data = self.auth_codes.get(auth_code)

        if not code_data:
            raise ValueError("Invalid authorization code")

        # 검증
        if code_data['client_id'] != client_id:
            raise ValueError("Client mismatch")

        if code_data['redirect_uri'] != redirect_uri:
            raise ValueError("Redirect URI mismatch")

        # PKCE 검증
        import base64
        verifier_hash = hashlib.sha256(code_verifier.encode()).digest()
        challenge = base64.urlsafe_b64encode(verifier_hash).rstrip(b'=').decode()

        if code_data['code_challenge'] != challenge:
            raise ValueError("PKCE verification failed")

        # Authorization code 일회용
        del self.auth_codes[auth_code]

        # Access Token 발급
        access_token = secrets.token_urlsafe(32)
        refresh_token = secrets.token_urlsafe(32)

        self.access_tokens[access_token] = {
            'client_id': client_id,
            'expires_at': datetime.utcnow() + timedelta(hours=1)
        }

        return {
            'access_token': access_token,
            'token_type': 'Bearer',
            'expires_in': 3600,
            'refresh_token': refresh_token
        }

# Rate Limiting
class RateLimiter:
    """
    Token Bucket Algorithm
    - API 남용 방지
    - DDoS 완화
    """

    def __init__(self, rate, capacity):
        """
        rate: tokens per second
        capacity: bucket size
        """
        self.rate = rate
        self.capacity = capacity
        self.buckets = {}

    def allow_request(self, identifier):
        """요청 허용 여부"""
        now = time.time()

        if identifier not in self.buckets:
            self.buckets[identifier] = {
                'tokens': self.capacity,
                'last_update': now
            }

        bucket = self.buckets[identifier]

        # Refill tokens
        elapsed = now - bucket['last_update']
        bucket['tokens'] = min(
            self.capacity,
            bucket['tokens'] + elapsed * self.rate
        )
        bucket['last_update'] = now

        # Consume token
        if bucket['tokens'] >= 1:
            bucket['tokens'] -= 1
            return True
        else:
            return False  # Rate limited
```

---

## 시스템 보안

### 1. 메모리 안전성

```c
// Buffer Overflow 방어
#include <string.h>
#include <stdio.h>

// ❌ 취약한 코드
void vulnerable_function(char* input) {
    char buffer[64];
    strcpy(buffer, input);  // Buffer overflow!
}

// ✅ 안전한 코드
void safe_function(char* input) {
    char buffer[64];
    strncpy(buffer, input, sizeof(buffer) - 1);
    buffer[sizeof(buffer) - 1] = '\0';
}

// ✅ 더 나은 방법: bounds checking
void safer_function(char* input, size_t input_len) {
    char buffer[64];

    if (input_len >= sizeof(buffer)) {
        fprintf(stderr, "Input too large\n");
        return;
    }

    memcpy(buffer, input, input_len);
    buffer[input_len] = '\0';
}

// Stack Canary (컴파일러 수준)
// gcc -fstack-protector-all
void protected_function() {
    // 컴파일러가 자동으로 스택 카나리 삽입
    // 카나리 변조 감지 시 프로그램 종료
}

// ASLR (Address Space Layout Randomization)
// OS 수준에서 메모리 배치 무작위화

// DEP/NX (Data Execution Prevention)
// 실행 불가능한 메모리 영역 설정
```

### 2. Sandboxing

```python
import subprocess
import resource

class Sandbox:
    """
    프로세스 샌드박싱
    - 권한 제한
    - 리소스 제한
    - 시스템 호출 제한
    """

    @staticmethod
    def run_limited(command, timeout=5):
        """제한된 환경에서 명령 실행"""

        def set_limits():
            # CPU 시간 제한 (5초)
            resource.setrlimit(resource.RLIMIT_CPU, (timeout, timeout))

            # 메모리 제한 (100MB)
            resource.setrlimit(resource.RLIMIT_AS, (100*1024*1024, 100*1024*1024))

            # 파일 크기 제한 (10MB)
            resource.setrlimit(resource.RLIMIT_FSIZE, (10*1024*1024, 10*1024*1024))

            # 프로세스 수 제한
            resource.setrlimit(resource.RLIMIT_NPROC, (10, 10))

        try:
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                timeout=timeout,
                preexec_fn=set_limits
            )
            return result.stdout, result.stderr
        except subprocess.TimeoutExpired:
            return None, "Timeout"
        except Exception as e:
            return None, str(e)

# Seccomp (Secure Computing Mode)
# 시스템 호출 화이트리스트

"""
// C 코드 예시
#include <seccomp.h>

scmp_filter_ctx ctx = seccomp_init(SCMP_ACT_KILL);
seccomp_rule_add(ctx, SCMP_ACT_ALLOW, SCMP_SYS(read), 0);
seccomp_rule_add(ctx, SCMP_ACT_ALLOW, SCMP_SYS(write), 0);
seccomp_rule_add(ctx, SCMP_ACT_ALLOW, SCMP_SYS(exit), 0);
seccomp_load(ctx);

// 이제 read, write, exit만 가능
// 다른 시스템 호출 시도 시 프로세스 종료
"""
```

### 3. 안전한 난수 생성

```python
import secrets
import os

class SecureRandom:
    """
    암호학적으로 안전한 난수
    - CSPRNG (Cryptographically Secure PRNG)
    - /dev/urandom, CryptGenRandom, etc.
    """

    @staticmethod
    def generate_key(length=32):
        """안전한 키 생성"""
        return os.urandom(length)

    @staticmethod
    def generate_token():
        """안전한 토큰 생성"""
        return secrets.token_urlsafe(32)

    @staticmethod
    def random_int(min_val, max_val):
        """안전한 정수 난수"""
        return secrets.randbelow(max_val - min_val + 1) + min_val

# ❌ 절대 사용 금지
import random
random.seed(12345)
weak_key = random.getrandbits(256)  # 예측 가능!

# ✅ 올바른 방법
strong_key = secrets.token_bytes(32)
```

---

**다음 주제:**
- AI/ML 기초
- 소프트웨어 공학

보안과 암호학의 모든 핵심을 마스터했습니다. 이제 실무에서 안전한 시스템을 설계할 수 있습니다.
