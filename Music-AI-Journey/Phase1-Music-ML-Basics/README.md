# Phase 1: 음악 ML 기초 (2-3개월)

> **목표: MIDI 데이터로 간단한 멜로디 생성하기**

---

## 📅 학습 계획

### Week 1-2: MIDI 데이터 처리
### Week 3-4: LSTM 음악 생성 모델
### Week 5-6: Transformer 기초
### Week 7-8: 평가 및 개선

---

## Week 1-2: MIDI 데이터 처리

### Day 1: MIDI 기초 이해

**MIDI란?**
- Musical Instrument Digital Interface
- 음악 악보를 디지털로 표현
- 오디오 파일이 아님 (악보 정보만)

**MIDI 파일 구조:**
```
MIDI File
├── Track 0 (메타 정보)
│   ├── Tempo
│   ├── Time Signature
│   └── Key Signature
└── Track 1 (악기 연주)
    ├── Note On (pitch, velocity, time)
    ├── Note Off (pitch, time)
    └── Control Changes
```

**Google Colab 환경 세팅:**
```python
# Colab 노트북 생성
# https://colab.research.google.com/

# 1. 라이브러리 설치
!pip install pretty_midi music21 matplotlib numpy torch

# 2. 샘플 MIDI 다운로드
!wget https://www.midiworld.com/download/1234
!mv 1234 sample.mid

# 3. 기본 읽기
import pretty_midi

midi = pretty_midi.PrettyMIDI('sample.mid')

print(f"곡 길이: {midi.get_end_time():.2f}초")
print(f"악기 수: {len(midi.instruments)}")

# 악기별 정보
for i, instrument in enumerate(midi.instruments):
    print(f"Track {i}: {pretty_midi.program_to_instrument_name(instrument.program)}")
    print(f"  노트 개수: {len(instrument.notes)}")
```

---

### Day 2-3: MIDI 파일 읽고 쓰기

**1. 노트 정보 추출:**
```python
import pretty_midi
import numpy as np
import matplotlib.pyplot as plt

def extract_notes(midi_file):
    """MIDI 파일에서 노트 정보 추출"""
    midi = pretty_midi.PrettyMIDI(midi_file)

    notes = []
    for instrument in midi.instruments:
        if not instrument.is_drum:  # 드럼 제외
            for note in instrument.notes:
                notes.append({
                    'pitch': note.pitch,          # 0-127 (C0 ~ G10)
                    'start': note.start,          # 시작 시간 (초)
                    'end': note.end,              # 끝 시간 (초)
                    'velocity': note.velocity,     # 세기 (0-127)
                    'duration': note.end - note.start
                })

    return notes

# 사용
notes = extract_notes('sample.mid')
print(f"총 노트 수: {len(notes)}")
print(f"첫 번째 노트: {notes[0]}")

# 피치 분포 시각화
pitches = [n['pitch'] for n in notes]
plt.hist(pitches, bins=50)
plt.xlabel('MIDI Pitch')
plt.ylabel('Frequency')
plt.title('Note Distribution')
plt.show()
```

**2. Piano Roll 시각화:**
```python
def plot_piano_roll(notes, title="Piano Roll"):
    """피아노 롤 시각화"""
    fig, ax = plt.subplots(figsize=(15, 5))

    for note in notes:
        ax.barh(
            note['pitch'],
            width=note['duration'],
            left=note['start'],
            height=0.8,
            alpha=0.8
        )

    ax.set_xlabel('Time (seconds)')
    ax.set_ylabel('MIDI Pitch')
    ax.set_title(title)
    ax.grid(axis='y', alpha=0.3)
    plt.tight_layout()
    plt.show()

# 처음 10초만 시각화
notes_subset = [n for n in notes if n['start'] < 10]
plot_piano_roll(notes_subset)
```

**3. MIDI 파일 생성:**
```python
def create_simple_melody():
    """간단한 멜로디 생성"""
    midi = pretty_midi.PrettyMIDI()
    piano = pretty_midi.Instrument(program=0)  # Acoustic Grand Piano

    # C major scale
    pitches = [60, 62, 64, 65, 67, 69, 71, 72]  # C D E F G A B C
    duration = 0.5  # 0.5초

    for i, pitch in enumerate(pitches):
        note = pretty_midi.Note(
            velocity=100,
            pitch=pitch,
            start=i * duration,
            end=(i + 1) * duration
        )
        piano.notes.append(note)

    midi.instruments.append(piano)
    midi.write('my_melody.mid')
    print("멜로디 생성 완료!")

create_simple_melody()

# 생성된 파일 재생 (Colab)
from IPython.display import Audio, display
audio = midi.fluidsynth()
display(Audio(audio, rate=44100))
```

---

### Day 4-7: 데이터 전처리

**1. MIDI → 시퀀스 변환:**
```python
def midi_to_sequence(midi_file, time_step=0.125):
    """
    MIDI 파일을 시퀀스로 변환

    time_step: 시간 간격 (초), 0.125 = 32분음표
    """
    midi = pretty_midi.PrettyMIDI(midi_file)

    # 전체 길이
    end_time = midi.get_end_time()
    num_steps = int(end_time / time_step) + 1

    # 피아노 롤 (pitch x time)
    piano_roll = np.zeros((128, num_steps))

    for instrument in midi.instruments:
        if not instrument.is_drum:
            # get_piano_roll: 각 시간에 어떤 노트가 울리는지
            roll = instrument.get_piano_roll(fs=1/time_step)
            piano_roll += roll

    # 이진화 (소리 있음/없음)
    piano_roll = (piano_roll > 0).astype(int)

    return piano_roll

# 사용
piano_roll = midi_to_sequence('sample.mid')
print(f"Shape: {piano_roll.shape}")  # (128, time_steps)

# 시각화
plt.figure(figsize=(15, 5))
plt.imshow(piano_roll[:, :200], aspect='auto', cmap='binary')
plt.xlabel('Time Steps')
plt.ylabel('MIDI Pitch')
plt.title('Piano Roll')
plt.show()
```

**2. 시퀀스 → 학습 데이터:**
```python
def prepare_sequences(piano_roll, seq_length=32):
    """
    슬라이딩 윈도우로 학습 데이터 생성

    Input:  [t-31, t-30, ..., t-1]  (32 time steps)
    Output: [t]                     (1 time step)
    """
    X, y = [], []

    # 활성화된 피치만 (0이 아닌 행)
    active_pitches = np.where(piano_roll.sum(axis=1) > 0)[0]
    piano_roll_active = piano_roll[active_pitches, :]

    num_pitches = piano_roll_active.shape[0]
    num_steps = piano_roll_active.shape[1]

    # 슬라이딩 윈도우
    for i in range(seq_length, num_steps):
        X.append(piano_roll_active[:, i-seq_length:i])
        y.append(piano_roll_active[:, i])

    X = np.array(X)  # (samples, pitches, seq_length)
    y = np.array(y)  # (samples, pitches)

    print(f"X shape: {X.shape}")
    print(f"y shape: {y.shape}")

    return X, y, active_pitches

X, y, pitches = prepare_sequences(piano_roll)
```

**3. 데이터셋 클래스:**
```python
import torch
from torch.utils.data import Dataset, DataLoader

class MIDIDataset(Dataset):
    def __init__(self, X, y):
        self.X = torch.FloatTensor(X)
        self.y = torch.FloatTensor(y)

    def __len__(self):
        return len(self.X)

    def __getitem__(self, idx):
        return self.X[idx], self.y[idx]

# 데이터 로더
dataset = MIDIDataset(X, y)
dataloader = DataLoader(dataset, batch_size=32, shuffle=True)

# 확인
for batch_X, batch_y in dataloader:
    print(f"Batch X: {batch_X.shape}")
    print(f"Batch y: {batch_y.shape}")
    break
```

---

## Week 3-4: LSTM 음악 생성 모델

### LSTM 모델 구현

```python
import torch
import torch.nn as nn

class MusicLSTM(nn.Module):
    """
    LSTM 기반 음악 생성 모델

    입력: (batch, seq_length, num_pitches)
    출력: (batch, num_pitches)
    """

    def __init__(self, num_pitches, hidden_size=256, num_layers=2, dropout=0.3):
        super(MusicLSTM, self).__init__()

        self.num_pitches = num_pitches
        self.hidden_size = hidden_size
        self.num_layers = num_layers

        # LSTM layers
        self.lstm = nn.LSTM(
            input_size=num_pitches,
            hidden_size=hidden_size,
            num_layers=num_layers,
            dropout=dropout,
            batch_first=True
        )

        # Output layer
        self.fc = nn.Linear(hidden_size, num_pitches)
        self.sigmoid = nn.Sigmoid()

    def forward(self, x):
        # x: (batch, seq_length, num_pitches)

        # LSTM
        lstm_out, (h_n, c_n) = self.lstm(x)

        # 마지막 time step의 출력
        last_output = lstm_out[:, -1, :]  # (batch, hidden_size)

        # Fully connected
        output = self.fc(last_output)  # (batch, num_pitches)
        output = self.sigmoid(output)  # 0-1 확률

        return output

# 모델 생성
num_pitches = X.shape[1]
model = MusicLSTM(num_pitches=num_pitches)

print(model)
print(f"파라미터 수: {sum(p.numel() for p in model.parameters()):,}")
```

---

### 모델 학습

```python
import torch.optim as optim

# 하이퍼파라미터
learning_rate = 0.001
num_epochs = 50
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

# 모델 GPU로 이동
model = model.to(device)

# 손실 함수 & 옵티마이저
criterion = nn.BCELoss()  # Binary Cross Entropy
optimizer = optim.Adam(model.parameters(), lr=learning_rate)

# 학습 루프
losses = []

for epoch in range(num_epochs):
    epoch_loss = 0

    for batch_X, batch_y in dataloader:
        batch_X = batch_X.to(device)
        batch_y = batch_y.to(device)

        # Forward
        outputs = model(batch_X)
        loss = criterion(outputs, batch_y)

        # Backward
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

        epoch_loss += loss.item()

    avg_loss = epoch_loss / len(dataloader)
    losses.append(avg_loss)

    if (epoch + 1) % 10 == 0:
        print(f'Epoch [{epoch+1}/{num_epochs}], Loss: {avg_loss:.4f}')

# 학습 곡선
plt.plot(losses)
plt.xlabel('Epoch')
plt.ylabel('Loss')
plt.title('Training Loss')
plt.show()

# 모델 저장
torch.save(model.state_dict(), 'music_lstm.pth')
```

---

### 음악 생성

```python
def generate_music(model, seed_sequence, num_steps=100, temperature=1.0):
    """
    LSTM 모델로 음악 생성

    Args:
        model: 학습된 LSTM 모델
        seed_sequence: 시작 시퀀스 (seq_length, num_pitches)
        num_steps: 생성할 time step 수
        temperature: 샘플링 온도 (낮으면 결정론적, 높으면 랜덤)
    """
    model.eval()
    device = next(model.parameters()).device

    # 시드 시퀀스 복사
    current_seq = torch.FloatTensor(seed_sequence).unsqueeze(0).to(device)
    generated = []

    with torch.no_grad():
        for _ in range(num_steps):
            # 예측
            output = model(current_seq)

            # Temperature 적용
            output = output / temperature

            # 확률적 샘플링
            probs = output.cpu().numpy()[0]

            # 이진 샘플링 (각 피치마다 독립적)
            next_step = (np.random.rand(len(probs)) < probs).astype(float)

            generated.append(next_step)

            # 다음 입력 준비
            current_seq = torch.cat([
                current_seq[:, 1:, :],
                torch.FloatTensor(next_step).unsqueeze(0).unsqueeze(0).to(device)
            ], dim=1)

    return np.array(generated)

# 생성
seed = X[0]  # 첫 번째 시퀀스를 시드로
generated_seq = generate_music(model, seed, num_steps=200, temperature=0.8)

print(f"생성된 시퀀스: {generated_seq.shape}")  # (200, num_pitches)

# 시각화
plt.figure(figsize=(15, 5))
plt.imshow(generated_seq.T, aspect='auto', cmap='binary')
plt.xlabel('Time Steps')
plt.ylabel('Pitch')
plt.title('Generated Music')
plt.show()
```

---

### MIDI 파일로 저장

```python
def sequence_to_midi(sequence, active_pitches, time_step=0.125, output_file='generated.mid'):
    """
    생성된 시퀀스를 MIDI 파일로 저장

    Args:
        sequence: (time_steps, num_pitches) numpy array
        active_pitches: 실제 MIDI 피치 번호
        time_step: 시간 간격
    """
    midi = pretty_midi.PrettyMIDI()
    piano = pretty_midi.Instrument(program=0)

    # 각 피치에 대해
    for pitch_idx, midi_pitch in enumerate(active_pitches):
        # 해당 피치가 켜진 time step 찾기
        active_steps = np.where(sequence[:, pitch_idx] > 0.5)[0]

        if len(active_steps) == 0:
            continue

        # 연속된 구간으로 그룹핑
        note_starts = [active_steps[0]]
        note_ends = []

        for i in range(1, len(active_steps)):
            if active_steps[i] != active_steps[i-1] + 1:
                note_ends.append(active_steps[i-1])
                note_starts.append(active_steps[i])

        note_ends.append(active_steps[-1])

        # Note 객체 생성
        for start, end in zip(note_starts, note_ends):
            note = pretty_midi.Note(
                velocity=80,
                pitch=int(midi_pitch),
                start=start * time_step,
                end=(end + 1) * time_step
            )
            piano.notes.append(note)

    midi.instruments.append(piano)
    midi.write(output_file)
    print(f"MIDI 파일 저장: {output_file}")

    return midi

# 사용
midi = sequence_to_midi(generated_seq, pitches, output_file='generated_lstm.mid')

# 재생 (Colab)
audio = midi.fluidsynth()
display(Audio(audio, rate=44100))
```

---

## Week 5-6: Transformer 기초

### Positional Encoding

```python
import math

def positional_encoding(seq_length, d_model):
    """
    위치 인코딩 생성

    PE(pos, 2i) = sin(pos / 10000^(2i/d_model))
    PE(pos, 2i+1) = cos(pos / 10000^(2i/d_model))
    """
    pe = np.zeros((seq_length, d_model))

    for pos in range(seq_length):
        for i in range(0, d_model, 2):
            pe[pos, i] = math.sin(pos / (10000 ** ((2 * i) / d_model)))
            if i + 1 < d_model:
                pe[pos, i + 1] = math.cos(pos / (10000 ** ((2 * i) / d_model)))

    return pe

# 시각화
pe = positional_encoding(100, 128)
plt.figure(figsize=(10, 5))
plt.imshow(pe, aspect='auto', cmap='RdBu')
plt.xlabel('Dimension')
plt.ylabel('Position')
plt.title('Positional Encoding')
plt.colorbar()
plt.show()
```

---

### Simple Transformer 모델

```python
class MusicTransformer(nn.Module):
    """
    Transformer 기반 음악 생성 모델
    """

    def __init__(self, num_pitches, d_model=128, nhead=8, num_layers=3, dropout=0.1):
        super(MusicTransformer, self).__init__()

        self.num_pitches = num_pitches
        self.d_model = d_model

        # Input embedding
        self.embedding = nn.Linear(num_pitches, d_model)

        # Positional encoding
        self.register_buffer('pe', torch.FloatTensor(
            positional_encoding(1000, d_model)
        ))

        # Transformer encoder
        encoder_layer = nn.TransformerEncoderLayer(
            d_model=d_model,
            nhead=nhead,
            dim_feedforward=d_model * 4,
            dropout=dropout,
            batch_first=True
        )
        self.transformer = nn.TransformerEncoder(encoder_layer, num_layers=num_layers)

        # Output layer
        self.fc = nn.Linear(d_model, num_pitches)
        self.sigmoid = nn.Sigmoid()

    def forward(self, x):
        # x: (batch, seq_length, num_pitches)
        batch_size, seq_length, _ = x.shape

        # Embedding
        x = self.embedding(x)  # (batch, seq_length, d_model)

        # Positional encoding
        x = x + self.pe[:seq_length, :].unsqueeze(0)

        # Transformer
        x = self.transformer(x)

        # Output (마지막 time step)
        x = x[:, -1, :]
        x = self.fc(x)
        x = self.sigmoid(x)

        return x

# 모델 생성
model = MusicTransformer(num_pitches=num_pitches)
print(f"파라미터 수: {sum(p.numel() for p in model.parameters()):,}")
```

---

## Week 7-8: 평가 및 개선

### 음악적 평가 지표

```python
def evaluate_musicality(generated_seq, original_seq=None):
    """
    생성된 음악의 품질 평가
    """
    metrics = {}

    # 1. Note Density (음표 밀도)
    active_notes = generated_seq.sum()
    total_steps = generated_seq.shape[0] * generated_seq.shape[1]
    metrics['note_density'] = active_notes / total_steps

    # 2. Pitch Range (음역대)
    active_pitches = np.where(generated_seq.sum(axis=0) > 0)[0]
    if len(active_pitches) > 0:
        metrics['pitch_range'] = active_pitches.max() - active_pitches.min()
    else:
        metrics['pitch_range'] = 0

    # 3. Polyphony (동시 발음 수)
    polyphony = generated_seq.sum(axis=1)
    metrics['avg_polyphony'] = polyphony.mean()
    metrics['max_polyphony'] = polyphony.max()

    # 4. Rhythmic Regularity (리듬 규칙성)
    # 음표 시작 간격의 표준편차
    note_starts = []
    for i in range(generated_seq.shape[0] - 1):
        if generated_seq[i].sum() > 0:
            note_starts.append(i)

    if len(note_starts) > 1:
        intervals = np.diff(note_starts)
        metrics['rhythm_std'] = intervals.std()
    else:
        metrics['rhythm_std'] = 0

    return metrics

# 평가
metrics = evaluate_musicality(generated_seq)
for key, value in metrics.items():
    print(f"{key}: {value:.2f}")
```

---

## 🎯 Phase 1 체크리스트

### MIDI 처리
- [ ] MIDI 파일 읽고 노트 추출
- [ ] Piano Roll 시각화
- [ ] MIDI 파일 생성
- [ ] 시퀀스 데이터로 변환

### LSTM 모델
- [ ] LSTM 모델 구현
- [ ] 학습 데이터 준비
- [ ] 모델 학습 (Loss < 0.1)
- [ ] 음악 생성 및 저장

### Transformer
- [ ] Positional Encoding 구현
- [ ] Transformer 모델 구현
- [ ] LSTM과 성능 비교

### 평가
- [ ] 음악적 평가 지표 계산
- [ ] 생성 결과 청취 및 피드백

---

## 🚀 다음 단계

Phase 1을 완료하면:
1. ✅ MIDI 데이터 처리 완벽 이해
2. ✅ 간단한 멜로디 생성 가능
3. ✅ Transformer 구조 이해

**다음:** [Phase 2 - 재즈 모델 실험](../Phase2-Jazz-Model/README.md)

---

**연습 프로젝트:**
- "Happy Birthday" 자동 생성기
- 동요 멜로디 생성 (비행기, 학교종 등)
- C major scale 패턴 학습

**화이팅!** 🎵
