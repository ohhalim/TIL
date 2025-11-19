# 🎵 음악 딥러닝 마스터 로드맵 (1-2년)

> **최종 목표: 찰리 파커 스타일 재즈 즉흥 연주 AI 구축**
>
> "AI 찰리 파커가 실시간으로 즉흥 연주하는 세상"

---

## 🎯 프로젝트 비전

### 최종 결과물
```
사용자: [코드 진행 입력] Gm7 - C7 - Fmaj7
AI 찰리 파커: [실시간 즉흥 연주 생성]
→ MIDI 출력 → 오디오 재생
→ 음악가들이 구분 못할 수준
```

### 핵심 차별화 포인트
- ✅ **LLM이 아닌 음악 생성** (블루오션)
- ✅ **재즈 즉흥** (초희귀 분야)
- ✅ **실시간 생성** (기존 모델 대부분 오프라인)
- ✅ **백엔드 + AI** (풀스택 역량)

---

## 📅 전체 로드맵 (12-24개월)

```
Phase 0: 준비 (1개월)
- GPU 환경 세팅
- 음악 이론 기초
- Python 딥러닝 복습

Phase 1: 기초 다지기 (2-3개월)
- 음악 데이터 처리
- MIDI 생성 모델 실습
- Transformer 구현

Phase 2: 모델 실험 (3-4개월)
- Music Transformer 파인튜닝
- 재즈 데이터셋 구축
- LoRA/QLoRA 학습

Phase 3: 찰리 파커 AI (4-6개월)
- 찰리 파커 전용 데이터셋
- 코드 컨디셔닝
- 스타일 학습

Phase 4: 배포 & 완성 (3-4개월)
- 실시간 추론 최적화
- 웹 데모 구축
- 오픈소스 공개
```

**병행 작업:**
- 평일 저녁 2-3시간
- 주말 하루 8시간
- 백엔드 취업 후 퇴근 후 진행

---

## 🗺️ 단계별 상세 로드맵

### Phase 0: 환경 준비 (1개월)

**GPU 환경**
- [ ] Google Colab Pro 가입 ($10/월)
- [ ] Kaggle Notebooks 활용 (무료 GPU)
- [ ] RunPod 계정 생성 (필요시)
- [ ] Hugging Face 가입

**음악 이론 기초**
- [ ] 재즈 화성학 기초
- [ ] MIDI 파일 구조 이해
- [ ] 음악 특징 추출 (Pitch, Duration, Velocity)
- [ ] 코드 진행 분석

**Python 복습**
- [ ] PyTorch 기초
- [ ] NumPy/Pandas
- [ ] MIDI 라이브러리 (music21, pretty_midi)
- [ ] 오디오 처리 (librosa)

**학습 자료:**
- 재즈 이론: "The Jazz Piano Book" (Mark Levine)
- MIDI 처리: music21 공식 문서
- PyTorch: "PyTorch로 시작하는 딥러닝 입문"

📁 [Phase 0 상세 가이드](./Phase0-Preparation/README.md)

---

### Phase 1: 음악 ML 기초 (2-3개월)

**Week 1-2: 데이터 처리**
```python
# MIDI 파일 읽기
import pretty_midi
midi = pretty_midi.PrettyMIDI('charlie_parker.mid')

# 특징 추출
notes = []
for instrument in midi.instruments:
    for note in instrument.notes:
        notes.append({
            'pitch': note.pitch,
            'start': note.start,
            'end': note.end,
            'velocity': note.velocity
        })
```

**Week 3-4: 간단한 LSTM 모델**
```python
# 음악 생성 RNN
class MusicLSTM(nn.Module):
    def __init__(self, vocab_size, embedding_dim, hidden_dim):
        super().__init__()
        self.embedding = nn.Embedding(vocab_size, embedding_dim)
        self.lstm = nn.LSTM(embedding_dim, hidden_dim, num_layers=2)
        self.fc = nn.Linear(hidden_dim, vocab_size)

    def forward(self, x):
        x = self.embedding(x)
        x, _ = self.lstm(x)
        x = self.fc(x)
        return x
```

**Week 5-6: Transformer 구현**
- Self-Attention 이해
- Positional Encoding
- Music Transformer 논문 읽기
- 간단한 멜로디 생성

**Week 7-8: 평가 지표**
- 음악적 일관성 측정
- Pitch Class Histogram
- Rhythm Complexity
- 사람 평가 (Blind Test)

**미니 프로젝트:** 동요 생성기 (Happy Birthday 등)

📁 [Phase 1 상세 가이드](./Phase1-Music-ML-Basics/README.md)

---

### Phase 2: 재즈 모델 실험 (3-4개월)

**데이터셋 구축**
```python
# 재즈 MIDI 수집
데이터 소스:
1. The Jazz MIDI Dataset (공개 데이터)
2. YouTube 연주 → MIDI 변환 (Basic Pitch)
3. 악보 PDF → MIDI (MuseScore)
4. 직접 입력 (소량)

목표: 1000+ 재즈 곡
```

**데이터 전처리**
```python
# 코드 진행 레이블링
from music21 import chord

def extract_chord_progression(midi_file):
    """코드 진행 추출"""
    score = converter.parse(midi_file)
    chords = []
    for element in score.flat:
        if isinstance(element, chord.Chord):
            chords.append(element.pitchClasses)
    return chords

# 데이터 증강
def transpose_midi(midi, semitones):
    """조옮김으로 데이터 12배 증강"""
    pass
```

**모델 선택**
1. **Music Transformer** (Google Magenta)
   - 장점: 오픈소스, 검증됨
   - 단점: 무거움

2. **MuseNet** (OpenAI)
   - 장점: 다양한 장르
   - 단점: 클로즈드

3. **Custom Transformer**
   - 장점: 재즈 전용 설계 가능
   - 단점: 처음부터 구현

**선택: Music Transformer + LoRA 파인튜닝**

**LoRA 파인튜닝**
```python
from peft import LoraConfig, get_peft_model

# LoRA 설정
lora_config = LoraConfig(
    r=16,  # Rank
    lora_alpha=32,
    target_modules=["q_proj", "v_proj"],
    lora_dropout=0.1,
)

model = get_peft_model(base_model, lora_config)

# 파라미터 수 비교
print(f"Trainable params: {model.num_parameters(only_trainable=True):,}")
# 기존: 300M → LoRA: 10M (30배 감소!)
```

**코드 컨디셔닝**
```python
# 코드 진행에 따른 생성
def generate_with_chords(model, chord_progression):
    """
    Input: ['Gm7', 'C7', 'Fmaj7']
    Output: MIDI notes
    """
    chord_tokens = encode_chords(chord_progression)
    context = torch.cat([chord_tokens, start_token])

    generated = model.generate(
        context,
        max_length=128,
        temperature=0.9,
        top_k=50
    )
    return decode_to_midi(generated)
```

**실험 추적**
```python
import wandb

wandb.init(project="jazz-improvisation")

for epoch in range(100):
    loss = train_epoch()
    wandb.log({
        'loss': loss,
        'perplexity': perplexity,
        'musical_coherence': coherence_score
    })
```

📁 [Phase 2 상세 가이드](./Phase2-Jazz-Model/README.md)

---

### Phase 3: 찰리 파커 AI (4-6개월)

**찰리 파커 전용 데이터셋**
```
데이터 수집:
1. 공식 앨범 전곡 (Savoy & Dial Sessions 등)
2. YouTube 연주 영상 → 음원 추출
3. 악보집 (Omnibook) → MIDI 변환
4. 트랜스크립션 커뮤니티 자료

목표: 200+ 솔로 트랜스크립션
```

**스타일 학습 전략**
```python
# 1. 찰리 파커 특징 추출
charlie_features = {
    'rhythm_patterns': analyze_rhythm(),
    'note_density': calculate_density(),
    'interval_distribution': get_intervals(),
    'bebop_patterns': detect_bebop_licks()
}

# 2. 스타일 임베딩
class StyleEncoder(nn.Module):
    def encode_style(self, midi_sequence):
        """찰리 파커 스타일을 벡터로 인코딩"""
        return style_vector

# 3. 스타일 가이드 생성
def generate_parker_style(chords, style_vector):
    """스타일 벡터로 컨디셔닝"""
    return model.generate(chords, style=style_vector)
```

**파인튜닝 전략**
```python
# 2단계 학습
# Stage 1: 일반 재즈 데이터 (1000곡)
model.train(jazz_dataset, epochs=50)

# Stage 2: 찰리 파커만 (200곡)
model.train(charlie_parker_dataset, epochs=100, lr=1e-5)

# LoRA로 메모리 절약
# A100 40GB 대신 T4 16GB로 가능!
```

**실시간 생성 최적화**
```python
# 1. Model Quantization
import torch.quantization
model_int8 = torch.quantization.quantize_dynamic(
    model, {nn.Linear}, dtype=torch.qint8
)
# 크기: 1.2GB → 300MB
# 속도: 2x 빨라짐

# 2. ONNX Runtime
import onnxruntime
session = onnxruntime.InferenceSession("model.onnx")
# 추론 속도 3x 향상

# 3. 스트리밍 생성
def stream_improvisation(chord_sequence):
    """4마디씩 실시간 생성"""
    for i in range(0, len(chord_sequence), 4):
        chunk = generate_chunk(chord_sequence[i:i+4])
        yield chunk  # 즉시 재생
```

**평가 시스템**
```python
# 1. 자동 평가
metrics = {
    'note_accuracy': pitch_accuracy(),
    'rhythm_coherence': rhythm_score(),
    'harmonic_fit': chord_tone_percentage(),
    'bebop_authenticity': bebop_pattern_detection()
}

# 2. 사람 평가
def blind_test():
    """음악가들에게 블라인드 테스트"""
    # 5명의 재즈 뮤지션
    # 10개 샘플 (5개 실제, 5개 AI)
    # "AI인가요?"
    pass

# 목표: 60% 이상 속이기
```

📁 [Phase 3 상세 가이드](./Phase3-Charlie-Parker-AI/README.md)

---

### Phase 4: 배포 & 오픈소스 (3-4개월)

**웹 데모 구축**
```python
# FastAPI 백엔드
from fastapi import FastAPI
import torch

app = FastAPI()

@app.post("/generate")
async def generate_solo(chords: List[str]):
    """
    Input: ["Gm7", "C7", "Fmaj7"]
    Output: MIDI 파일
    """
    midi = model.generate(chords)
    return {"midi_url": "https://..."}

# 프론트엔드 (React)
function ImprovGenerator() {
    const [chords, setChords] = useState([]);
    const [midi, setMidi] = useState(null);

    const generate = async () => {
        const res = await fetch('/generate', {
            method: 'POST',
            body: JSON.stringify({chords})
        });
        const data = await res.json();
        setMidi(data.midi_url);
    };

    return (
        <div>
            <ChordInput onChange={setChords} />
            <button onClick={generate}>Generate Solo</button>
            <MidiPlayer src={midi} />
        </div>
    );
}
```

**배포 아키텍처**
```
사용자 브라우저
    ↓
CloudFlare CDN
    ↓
AWS Load Balancer
    ↓
EC2 (FastAPI) ← → Redis (캐싱)
    ↓
S3 (모델 파일)
```

**Hugging Face 공개**
```python
# 모델 업로드
from huggingface_hub import HfApi

api = HfApi()
api.upload_folder(
    folder_path="./charlie-parker-ai",
    repo_id="your-username/charlie-parker-ai",
    repo_type="model"
)

# README.md 작성
"""
# 🎺 Charlie Parker AI

재즈 전설 찰리 파커의 즉흥 연주 스타일을 학습한 AI

## Quick Start
```python
from transformers import AutoModel
model = AutoModel.from_pretrained("charlie-parker-ai")
chords = ["Gm7", "C7", "Fmaj7"]
solo = model.generate(chords)
```

## Demos
- [Web Demo](https://charlie-parker-ai.com)
- [Colab Notebook](https://colab...)

## Citation
...
"""
```

**마케팅 & 홍보**
```
1. GitHub README 극강
   - 데모 영상 (YouTube)
   - 샘플 오디오
   - 기술 블로그 링크

2. 커뮤니티 공유
   - Hacker News
   - r/MachineLearning
   - 음악 AI 포럼

3. 논문 제출 (선택)
   - ISMIR (음악 정보 검색)
   - ICML Workshop
   - NeurIPS Creative AI

4. 언론 보도
   - "AI가 찰리 파커처럼 연주"
   - 테크 미디어 관심

5. YouTube 채널
   - 프로젝트 과정 브이로그
   - 기술 설명 영상
```

📁 [Phase 4 상세 가이드](./Phase4-Deploy/README.md)

---

## 💻 기술 스택

### 딥러닝
```python
핵심:
- PyTorch 2.0
- Hugging Face Transformers
- PEFT (LoRA)

음악 처리:
- music21
- pretty_midi
- librosa
- mido

학습:
- Weights & Biases (실험 추적)
- DeepSpeed (분산 학습)
```

### 웹 개발
```python
백엔드:
- FastAPI
- Celery (비동기 작업)
- Redis

프론트엔드:
- React
- Tone.js (MIDI 재생)
- Web MIDI API

배포:
- Docker
- AWS (EC2, S3)
- GitHub Actions
```

---

## 📊 예상 비용

### GPU 비용 (월간)
```
학습 단계:
- Colab Pro: $10/월
- 추가 RunPod (A40): $50/월
총: $60/월

배포 후:
- AWS EC2 (추론): $30/월
- S3 스토리지: $5/월
총: $35/월

연간 총액: ~$1,000
```

### 무료/저렴한 대안
```
학습:
- Kaggle Notebooks: 무료 (주 30시간 GPU)
- Colab 무료: T4 GPU
- Paperspace Gradient: Free tier

배포:
- Hugging Face Spaces: 무료 (추론)
- Render: 무료 tier
- Vercel: 프론트엔드 무료
```

---

## 🎯 마일스톤

### 3개월
- [ ] LSTM으로 간단한 멜로디 생성
- [ ] MIDI 데이터 처리 완벽 숙지
- [ ] Transformer 구조 이해

### 6개월
- [ ] 재즈 데이터셋 1000곡 수집
- [ ] Music Transformer 파인튜닝 성공
- [ ] 코드 컨디셔닝 구현

### 12개월
- [ ] 찰리 파커 스타일 학습 완료
- [ ] 블라인드 테스트 통과 (60%)
- [ ] 웹 데모 런칭

### 18-24개월
- [ ] 실시간 생성 최적화
- [ ] Hugging Face 공개
- [ ] GitHub 100+ stars
- [ ] 음악 AI 컨퍼런스 발표

---

## 📚 핵심 논문 & 자료

### 필수 논문
1. **Music Transformer** (Huang et al., 2018)
   - 음악 생성의 표준

2. **MuseNet** (OpenAI, 2019)
   - 다양한 장르 생성

3. **Jukebox** (OpenAI, 2020)
   - 오디오 직접 생성

4. **MusicLM** (Google, 2023)
   - 텍스트→음악 생성

### 음악 AI 리소스
- **Google Magenta**: 오픈소스 음악 AI 툴킷
- **MIDI Dataset**: Jazz MIDI DB
- **Hugging Face Audio**: 음악 모델 모음
- **ISMIR**: 음악 정보 검색 학회

### 재즈 이론
- "The Jazz Theory Book" (Mark Levine)
- "Chord-Scale Theory & Jazz Harmony" (Barrie Nettles)
- Charlie Parker Omnibook (악보집)

---

## 🔥 차별화 전략

### 기존 음악 AI vs 찰리 파커 AI

| 기존 모델 | 찰리 파커 AI |
|----------|-------------|
| 일반 음악 생성 | **재즈 즉흥 전문** |
| 오프라인 생성 | **실시간 생성** |
| 스타일 랜덤 | **특정 연주자 스타일** |
| 텍스트 입력 | **코드 진행 입력** |
| 결과물 평가 어려움 | **음악가 블라인드 테스트** |

### 독보적 강점
1. **니치 마켓**: 재즈 즉흥 AI는 거의 없음
2. **실용성**: 재즈 뮤지션이 실제 사용 가능
3. **확장성**: 다른 연주자 스타일 추가 가능
4. **백엔드 역량**: 실제 서비스로 배포

---

## 💡 성공을 위한 조언

### DO ✅
1. **작게 시작**: 동요 생성 → 재즈 → 찰리 파커
2. **공개적으로**: GitHub 매일 커밋, 과정 공유
3. **피드백**: 음악가 친구들에게 들려주기
4. **문서화**: README, 블로그 포스팅 철저히
5. **인내심**: 좋은 결과는 6개월 이상 걸림

### DON'T ❌
1. **완벽주의**: 70% 완성하고 다음 단계로
2. **혼자 고민**: 커뮤니티에 질문하기
3. **GPU 집착**: Colab 무료로도 충분히 시작 가능
4. **비교**: SOTA 모델과 비교 말고 꾸준히
5. **조급함**: 당장 취업 안 돼도 장기 프로젝트

---

## 🎼 최종 비전

### 1년 후
```
GitHub 프로필:
- charlie-parker-ai ⭐ 500+
- Hugging Face 모델 다운로드 1000+
- 기술 블로그 조회수 10,000+
- YouTube 프로젝트 영상 조회수 50,000+
```

### 2년 후
```
커리어:
- AI 스타트업 취업 또는
- 음악 AI 스타트업 창업
- 음악 + AI 컨퍼런스 발표
- 음악가들이 실제 사용하는 도구
```

### 궁극의 꿈
```
"AI 찰리 파커와 실제 밴드의 잼 세션"
→ YouTube 라이브 100만 조회
→ 음악 AI의 새로운 지평
```

---

## 🚀 지금 시작하기

### 이번 주말 (4시간)
```python
# 1. Colab 노트북 생성
!pip install pretty_midi music21

# 2. MIDI 파일 다운로드
!wget "jazz-midi-sample.mid"

# 3. 첫 번째 노트 읽기
import pretty_midi
midi = pretty_midi.PrettyMIDI('sample.mid')
for note in midi.instruments[0].notes:
    print(f"Pitch: {note.pitch}, Duration: {note.end - note.start}")

# 4. GitHub 레포 생성
# charlie-parker-ai
```

### 다음 주 (평일 2시간 x 5일)
- music21 튜토리얼 완료
- MIDI 데이터 10개 수집
- 간단한 LSTM 모델 코딩
- 블로그 첫 포스팅

**지금 이 순간이 시작입니다!** 🎺

---

**Last Updated**: 2025-11-18
**Version**: 1.0

**Made with ❤️ for 음악을 사랑하는 개발자**
