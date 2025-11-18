# 07. 컴퓨터 구조 (Computer Architecture)

## 목차
1. [CPU 내부 구조](#cpu-내부-구조)
2. [파이프라이닝과 해저드](#파이프라이닝과-해저드)
3. [메모리 계층 구조](#메모리-계층-구조)
4. [캐시 설계와 최적화](#캐시-설계와-최적화)
5. [가상 메모리 심화](#가상-메모리-심화)
6. [병렬 처리 아키텍처](#병렬-처리-아키텍처)
7. [GPU 아키텍처](#gpu-아키텍처)
8. [최신 CPU 기술](#최신-cpu-기술)

---

## CPU 내부 구조

### 1. 명령어 실행 사이클

**폰 노이만 아키텍처의 기본 사이클:**

```
Fetch → Decode → Execute → Memory Access → Write Back
```

**상세 구현:**

```c
// CPU 시뮬레이터 구현
typedef struct {
    uint32_t PC;        // Program Counter
    uint32_t IR;        // Instruction Register
    uint32_t MAR;       // Memory Address Register
    uint32_t MDR;       // Memory Data Register
    uint32_t ACC;       // Accumulator
    uint32_t registers[32]; // General Purpose Registers
    uint8_t flags;      // Status Flags (Z, N, C, V)
} CPU;

typedef struct {
    uint8_t opcode;
    uint8_t rs;         // Source Register
    uint8_t rt;         // Target Register
    uint8_t rd;         // Destination Register
    uint16_t immediate;
    uint32_t address;
} Instruction;

// Fetch Stage
void fetch(CPU* cpu, uint8_t* memory) {
    cpu->MAR = cpu->PC;
    cpu->IR = *(uint32_t*)(memory + cpu->MAR);
    cpu->PC += 4;  // RISC: 4바이트 고정
}

// Decode Stage
Instruction decode(uint32_t ir) {
    Instruction inst;
    inst.opcode = (ir >> 26) & 0x3F;        // 6 bits
    inst.rs = (ir >> 21) & 0x1F;            // 5 bits
    inst.rt = (ir >> 16) & 0x1F;            // 5 bits
    inst.rd = (ir >> 11) & 0x1F;            // 5 bits
    inst.immediate = ir & 0xFFFF;           // 16 bits
    inst.address = ir & 0x3FFFFFF;          // 26 bits
    return inst;
}

// Execute Stage
void execute(CPU* cpu, Instruction inst, uint8_t* memory) {
    switch(inst.opcode) {
        case 0x00: // ADD
            cpu->registers[inst.rd] =
                cpu->registers[inst.rs] + cpu->registers[inst.rt];
            // Overflow detection
            if (/* overflow check */) {
                cpu->flags |= 0x01; // Set overflow flag
            }
            break;

        case 0x08: // ADDI (Add Immediate)
            cpu->registers[inst.rt] =
                cpu->registers[inst.rs] + inst.immediate;
            break;

        case 0x23: // LW (Load Word)
            cpu->MAR = cpu->registers[inst.rs] + inst.immediate;
            cpu->MDR = *(uint32_t*)(memory + cpu->MAR);
            cpu->registers[inst.rt] = cpu->MDR;
            break;

        case 0x2B: // SW (Store Word)
            cpu->MAR = cpu->registers[inst.rs] + inst.immediate;
            cpu->MDR = cpu->registers[inst.rt];
            *(uint32_t*)(memory + cpu->MAR) = cpu->MDR;
            break;

        case 0x04: // BEQ (Branch Equal)
            if (cpu->registers[inst.rs] == cpu->registers[inst.rt]) {
                cpu->PC += (int16_t)inst.immediate << 2;
            }
            break;

        case 0x02: // J (Jump)
            cpu->PC = (cpu->PC & 0xF0000000) | (inst.address << 2);
            break;
    }
}
```

### 2. ALU (Arithmetic Logic Unit) 설계

**완전한 32비트 ALU 구현:**

```verilog
module ALU_32bit (
    input [31:0] A,
    input [31:0] B,
    input [3:0] ALU_Control,
    output reg [31:0] Result,
    output Zero,
    output Overflow,
    output Negative
);

    wire [31:0] sum;
    wire [31:0] sub;
    wire cout;

    // Adder/Subtractor
    assign {cout, sum} = A + B;
    assign sub = A - B;

    always @(*) begin
        case(ALU_Control)
            4'b0000: Result = A & B;           // AND
            4'b0001: Result = A | B;           // OR
            4'b0010: Result = sum;             // ADD
            4'b0110: Result = sub;             // SUB
            4'b0111: Result = (A < B) ? 1 : 0; // SLT (Set Less Than)
            4'b1100: Result = ~(A | B);        // NOR
            4'b0011: Result = A ^ B;           // XOR
            4'b0100: Result = A << B[4:0];     // SLL (Shift Left Logical)
            4'b0101: Result = A >> B[4:0];     // SRL (Shift Right Logical)
            4'b1101: Result = $signed(A) >>> B[4:0]; // SRA (Shift Right Arithmetic)
            default: Result = 0;
        endcase
    end

    assign Zero = (Result == 0);
    assign Overflow = (ALU_Control == 4'b0010 && A[31] == B[31] && Result[31] != A[31]) ||
                      (ALU_Control == 4'b0110 && A[31] != B[31] && Result[31] != A[31]);
    assign Negative = Result[31];

endmodule
```

### 3. 제어 유닛 (Control Unit)

**마이크로프로그래밍 방식:**

```c
// 마이크로명령어 정의
typedef struct {
    uint32_t control_signals;  // 각 비트가 제어 신호
    uint8_t next_address;      // 다음 마이크로명령어 주소
    uint8_t condition;         // 분기 조건
} MicroInstruction;

// 제어 신호 비트맵
#define CTRL_PC_WRITE       (1 << 0)
#define CTRL_IR_WRITE       (1 << 1)
#define CTRL_MEM_READ       (1 << 2)
#define CTRL_MEM_WRITE      (1 << 3)
#define CTRL_ALU_SRC_A      (1 << 4)
#define CTRL_ALU_SRC_B      (3 << 5)  // 2 bits
#define CTRL_ALU_OP         (15 << 7) // 4 bits
#define CTRL_REG_WRITE      (1 << 11)
#define CTRL_REG_DST        (1 << 12)

// 제어 메모리 (Control Store)
MicroInstruction control_store[256];

void init_control_store() {
    // Fetch 단계
    control_store[0].control_signals = CTRL_MEM_READ | CTRL_IR_WRITE;
    control_store[0].next_address = 1;

    // Decode 단계
    control_store[1].control_signals = 0;
    control_store[1].next_address = 2;  // opcode에 따라 분기

    // ADD 실행 (opcode = 0x00)
    control_store[32].control_signals =
        CTRL_ALU_OP | CTRL_REG_WRITE | CTRL_REG_DST;
    control_store[32].next_address = 0;  // Fetch로 복귀

    // LW 실행 (opcode = 0x23)
    control_store[67].control_signals = CTRL_MEM_READ;
    control_store[67].next_address = 68;

    control_store[68].control_signals = CTRL_REG_WRITE;
    control_store[68].next_address = 0;
}

uint8_t execute_microinstruction(CPU* cpu, uint8_t micro_addr) {
    MicroInstruction micro = control_store[micro_addr];

    // 제어 신호에 따라 데이터패스 활성화
    if (micro.control_signals & CTRL_MEM_READ) {
        // Memory Read 수행
    }
    if (micro.control_signals & CTRL_REG_WRITE) {
        // Register Write 수행
    }

    return micro.next_address;
}
```

---

## 파이프라이닝과 해저드

### 1. 5단계 파이프라인 구현

```c
typedef struct {
    // IF/ID Pipeline Register
    struct {
        uint32_t instruction;
        uint32_t pc;
    } IF_ID;

    // ID/EX Pipeline Register
    struct {
        uint32_t read_data1;
        uint32_t read_data2;
        uint32_t immediate;
        uint8_t rs, rt, rd;
        uint8_t alu_op;
        bool reg_write;
        bool mem_read;
        bool mem_write;
    } ID_EX;

    // EX/MEM Pipeline Register
    struct {
        uint32_t alu_result;
        uint32_t write_data;
        uint8_t write_reg;
        bool reg_write;
        bool mem_read;
        bool mem_write;
    } EX_MEM;

    // MEM/WB Pipeline Register
    struct {
        uint32_t read_data;
        uint32_t alu_result;
        uint8_t write_reg;
        bool reg_write;
        bool mem_to_reg;
    } MEM_WB;

    uint32_t registers[32];
    uint8_t* memory;
} PipelinedCPU;

void pipeline_cycle(PipelinedCPU* cpu) {
    // WB (Write Back) - Stage 5
    if (cpu->MEM_WB.reg_write) {
        uint32_t write_data = cpu->MEM_WB.mem_to_reg ?
            cpu->MEM_WB.read_data : cpu->MEM_WB.alu_result;
        cpu->registers[cpu->MEM_WB.write_reg] = write_data;
    }

    // MEM (Memory Access) - Stage 4
    if (cpu->EX_MEM.mem_read) {
        cpu->MEM_WB.read_data =
            *(uint32_t*)(cpu->memory + cpu->EX_MEM.alu_result);
    }
    if (cpu->EX_MEM.mem_write) {
        *(uint32_t*)(cpu->memory + cpu->EX_MEM.alu_result) =
            cpu->EX_MEM.write_data;
    }
    cpu->MEM_WB.alu_result = cpu->EX_MEM.alu_result;
    cpu->MEM_WB.write_reg = cpu->EX_MEM.write_reg;
    cpu->MEM_WB.reg_write = cpu->EX_MEM.reg_write;

    // EX (Execute) - Stage 3
    uint32_t alu_input1 = cpu->ID_EX.read_data1;
    uint32_t alu_input2 = cpu->ID_EX.read_data2;

    // Forwarding logic
    if (cpu->EX_MEM.reg_write &&
        cpu->EX_MEM.write_reg != 0 &&
        cpu->EX_MEM.write_reg == cpu->ID_EX.rs) {
        alu_input1 = cpu->EX_MEM.alu_result;
    }
    if (cpu->MEM_WB.reg_write &&
        cpu->MEM_WB.write_reg != 0 &&
        cpu->MEM_WB.write_reg == cpu->ID_EX.rs) {
        alu_input1 = cpu->MEM_WB.alu_result;
    }

    cpu->EX_MEM.alu_result = alu_execute(
        alu_input1, alu_input2, cpu->ID_EX.alu_op);
    cpu->EX_MEM.write_data = cpu->ID_EX.read_data2;
    cpu->EX_MEM.write_reg = cpu->ID_EX.rd;

    // ID (Instruction Decode) - Stage 2
    Instruction inst = decode(cpu->IF_ID.instruction);
    cpu->ID_EX.read_data1 = cpu->registers[inst.rs];
    cpu->ID_EX.read_data2 = cpu->registers[inst.rt];
    cpu->ID_EX.immediate = inst.immediate;
    cpu->ID_EX.rs = inst.rs;
    cpu->ID_EX.rt = inst.rt;
    cpu->ID_EX.rd = inst.rd;

    // Hazard Detection
    if (cpu->ID_EX.mem_read &&
        (cpu->ID_EX.rt == inst.rs || cpu->ID_EX.rt == inst.rt)) {
        // Insert bubble (stall)
        insert_bubble(cpu);
        return;
    }

    // IF (Instruction Fetch) - Stage 1
    // (fetch next instruction)
}
```

### 2. 해저드 처리 전략

**데이터 해저드 (Data Hazard):**

```c
// 1. Forwarding (Bypassing)
typedef struct {
    bool forward_A;
    bool forward_B;
    uint8_t forward_A_src;  // 0: none, 1: EX/MEM, 2: MEM/WB
    uint8_t forward_B_src;
} ForwardingUnit;

ForwardingUnit detect_forwarding(PipelinedCPU* cpu) {
    ForwardingUnit fu = {false, false, 0, 0};

    // EX hazard
    if (cpu->EX_MEM.reg_write && cpu->EX_MEM.write_reg != 0) {
        if (cpu->EX_MEM.write_reg == cpu->ID_EX.rs) {
            fu.forward_A = true;
            fu.forward_A_src = 1;
        }
        if (cpu->EX_MEM.write_reg == cpu->ID_EX.rt) {
            fu.forward_B = true;
            fu.forward_B_src = 1;
        }
    }

    // MEM hazard
    if (cpu->MEM_WB.reg_write && cpu->MEM_WB.write_reg != 0) {
        if (!(cpu->EX_MEM.reg_write &&
              cpu->EX_MEM.write_reg == cpu->ID_EX.rs) &&
            cpu->MEM_WB.write_reg == cpu->ID_EX.rs) {
            fu.forward_A = true;
            fu.forward_A_src = 2;
        }
        if (!(cpu->EX_MEM.reg_write &&
              cpu->EX_MEM.write_reg == cpu->ID_EX.rt) &&
            cpu->MEM_WB.write_reg == cpu->ID_EX.rt) {
            fu.forward_B = true;
            fu.forward_B_src = 2;
        }
    }

    return fu;
}

// 2. Stall (Pipeline Bubble)
bool detect_load_use_hazard(PipelinedCPU* cpu, Instruction inst) {
    if (cpu->ID_EX.mem_read) {
        if (cpu->ID_EX.rt == inst.rs || cpu->ID_EX.rt == inst.rt) {
            return true;  // Need to stall
        }
    }
    return false;
}

void insert_bubble(PipelinedCPU* cpu) {
    // NOP 삽입
    cpu->ID_EX.reg_write = false;
    cpu->ID_EX.mem_read = false;
    cpu->ID_EX.mem_write = false;
    cpu->ID_EX.alu_op = 0;
}
```

**제어 해저드 (Control Hazard):**

```c
// 1. Branch Prediction
typedef struct {
    uint32_t address;
    uint8_t state;  // 2-bit saturating counter
} BranchHistoryEntry;

#define BHT_SIZE 256
BranchHistoryEntry BHT[BHT_SIZE];

// 2-bit Saturating Counter States:
// 00: Strongly Not Taken
// 01: Weakly Not Taken
// 10: Weakly Taken
// 11: Strongly Taken

bool predict_branch(uint32_t pc) {
    uint8_t index = (pc >> 2) & 0xFF;
    return BHT[index].state >= 2;  // Predict taken if >= 10
}

void update_branch_predictor(uint32_t pc, bool actual_taken) {
    uint8_t index = (pc >> 2) & 0xFF;

    if (actual_taken) {
        if (BHT[index].state < 3) BHT[index].state++;
    } else {
        if (BHT[index].state > 0) BHT[index].state--;
    }
}

// 2. Branch Target Buffer (BTB)
typedef struct {
    uint32_t tag;
    uint32_t target;
    bool valid;
} BTBEntry;

#define BTB_SIZE 512
BTBEntry BTB[BTB_SIZE];

uint32_t predict_target(uint32_t pc) {
    uint16_t index = (pc >> 2) & 0x1FF;
    uint32_t tag = pc >> 11;

    if (BTB[index].valid && BTB[index].tag == tag) {
        return BTB[index].target;
    }
    return pc + 4;  // Default: sequential
}

void update_btb(uint32_t pc, uint32_t target) {
    uint16_t index = (pc >> 2) & 0x1FF;
    uint32_t tag = pc >> 11;

    BTB[index].tag = tag;
    BTB[index].target = target;
    BTB[index].valid = true;
}
```

---

## 메모리 계층 구조

### 1. 메모리 성능 분석

**평균 메모리 접근 시간 (AMAT):**

```
AMAT = Hit Time + Miss Rate × Miss Penalty

계층적:
AMAT = L1_HitTime + L1_MissRate × (L2_HitTime + L2_MissRate × (L3_HitTime + L3_MissRate × DRAM_Time))
```

**실제 계산 예시:**

```python
class MemoryHierarchy:
    def __init__(self):
        # L1 Cache
        self.l1_hit_time = 1      # 1 cycle
        self.l1_miss_rate = 0.05  # 5%

        # L2 Cache
        self.l2_hit_time = 10     # 10 cycles
        self.l2_miss_rate = 0.20  # 20% of L1 misses

        # L3 Cache
        self.l3_hit_time = 30     # 30 cycles
        self.l3_miss_rate = 0.30  # 30% of L2 misses

        # DRAM
        self.dram_time = 200      # 200 cycles

    def calculate_amat(self):
        """평균 메모리 접근 시간 계산"""
        l3_penalty = self.l3_hit_time + (self.l3_miss_rate * self.dram_time)
        l2_penalty = self.l2_hit_time + (self.l2_miss_rate * l3_penalty)
        l1_penalty = self.l1_miss_rate * l2_penalty

        amat = self.l1_hit_time + l1_penalty
        return amat

    def calculate_cpi(self, base_cpi, mem_instructions_ratio):
        """CPI (Cycles Per Instruction) 계산"""
        amat = self.calculate_amat()
        memory_stall_cycles = mem_instructions_ratio * (amat - self.l1_hit_time)
        total_cpi = base_cpi + memory_stall_cycles
        return total_cpi

# 사용 예
mem = MemoryHierarchy()
print(f"AMAT: {mem.calculate_amat():.2f} cycles")
print(f"CPI (30% mem inst): {mem.calculate_cpi(1.0, 0.3):.2f}")

# 출력:
# AMAT: 2.48 cycles
# CPI (30% mem inst): 1.44
```

### 2. 메모리 인터리빙

**뱅크 인터리빙으로 대역폭 증가:**

```c
#define NUM_BANKS 4
#define BANK_SIZE (1024 * 1024)  // 1MB per bank

typedef struct {
    uint8_t data[BANK_SIZE];
    bool busy;
    uint32_t busy_until;
} MemoryBank;

typedef struct {
    MemoryBank banks[NUM_BANKS];
    uint32_t current_cycle;
} InterleavedMemory;

// Low-order interleaving: 연속된 주소가 다른 뱅크로
uint32_t get_bank_number(uint32_t address) {
    return address & (NUM_BANKS - 1);  // address % NUM_BANKS
}

uint32_t get_bank_offset(uint32_t address) {
    return address >> 2;  // address / 4
}

bool read_memory(InterleavedMemory* mem, uint32_t address, uint32_t* data) {
    uint32_t bank = get_bank_number(address);
    uint32_t offset = get_bank_offset(address);

    if (mem->banks[bank].busy &&
        mem->current_cycle < mem->banks[bank].busy_until) {
        return false;  // Bank conflict
    }

    *data = *(uint32_t*)&mem->banks[bank].data[offset];
    mem->banks[bank].busy = true;
    mem->banks[bank].busy_until = mem->current_cycle + 10;  // 10 cycle latency

    return true;
}

// 벡터 로드 최적화 (4개 연속 워드)
bool load_vector(InterleavedMemory* mem, uint32_t base_addr, uint32_t data[4]) {
    // 연속된 4개 주소가 4개 다른 뱅크에 매핑됨
    // 병렬 접근 가능!
    for (int i = 0; i < 4; i++) {
        if (!read_memory(mem, base_addr + i*4, &data[i])) {
            return false;
        }
    }
    return true;
}
```

---

## 캐시 설계와 최적화

### 1. 캐시 구현 (Set-Associative)

```c
#define CACHE_SIZE (32 * 1024)     // 32KB
#define BLOCK_SIZE 64              // 64 bytes
#define ASSOCIATIVITY 4            // 4-way
#define NUM_SETS (CACHE_SIZE / (BLOCK_SIZE * ASSOCIATIVITY))

typedef struct {
    bool valid;
    bool dirty;
    uint32_t tag;
    uint8_t data[BLOCK_SIZE];
    uint32_t lru_counter;  // LRU replacement
} CacheLine;

typedef struct {
    CacheLine lines[ASSOCIATIVITY];
} CacheSet;

typedef struct {
    CacheSet sets[NUM_SETS];
    uint32_t global_counter;

    // Statistics
    uint64_t hits;
    uint64_t misses;
    uint64_t writebacks;
} Cache;

// 주소 분해
typedef struct {
    uint32_t tag;
    uint16_t index;
    uint8_t offset;
} AddressParts;

AddressParts parse_address(uint32_t address) {
    AddressParts parts;
    parts.offset = address & 0x3F;                    // 6 bits (64 bytes)
    parts.index = (address >> 6) & 0x1FF;             // 9 bits (512 sets)
    parts.tag = address >> 15;                         // 17 bits
    return parts;
}

bool cache_read(Cache* cache, uint32_t address, uint8_t* data) {
    AddressParts addr = parse_address(address);
    CacheSet* set = &cache->sets[addr.index];

    // 1. Tag 비교 (Hit check)
    for (int i = 0; i < ASSOCIATIVITY; i++) {
        if (set->lines[i].valid && set->lines[i].tag == addr.tag) {
            // Cache Hit
            *data = set->lines[i].data[addr.offset];
            set->lines[i].lru_counter = cache->global_counter++;
            cache->hits++;
            return true;
        }
    }

    // 2. Cache Miss
    cache->misses++;

    // 3. Victim 선택 (LRU)
    int victim = 0;
    uint32_t min_lru = set->lines[0].lru_counter;
    for (int i = 1; i < ASSOCIATIVITY; i++) {
        if (!set->lines[i].valid) {
            victim = i;
            break;
        }
        if (set->lines[i].lru_counter < min_lru) {
            min_lru = set->lines[i].lru_counter;
            victim = i;
        }
    }

    // 4. Write-back if dirty
    if (set->lines[victim].valid && set->lines[victim].dirty) {
        uint32_t wb_addr = (set->lines[victim].tag << 15) | (addr.index << 6);
        // write_to_memory(wb_addr, set->lines[victim].data);
        cache->writebacks++;
    }

    // 5. 메모리에서 블록 로드
    // load_from_memory(address & ~0x3F, set->lines[victim].data);

    // 6. 캐시 라인 업데이트
    set->lines[victim].valid = true;
    set->lines[victim].dirty = false;
    set->lines[victim].tag = addr.tag;
    set->lines[victim].lru_counter = cache->global_counter++;

    *data = set->lines[victim].data[addr.offset];
    return false;
}

void cache_write(Cache* cache, uint32_t address, uint8_t data) {
    AddressParts addr = parse_address(address);
    CacheSet* set = &cache->sets[addr.index];

    // Write-allocate + Write-back 정책
    for (int i = 0; i < ASSOCIATIVITY; i++) {
        if (set->lines[i].valid && set->lines[i].tag == addr.tag) {
            // Write Hit
            set->lines[i].data[addr.offset] = data;
            set->lines[i].dirty = true;
            set->lines[i].lru_counter = cache->global_counter++;
            cache->hits++;
            return;
        }
    }

    // Write Miss: allocate first, then write
    cache_read(cache, address, &data);  // Brings line into cache
    cache_write(cache, address, data);   // Write to cache
}
```

### 2. 캐시 일관성 프로토콜 (MESI)

```c
typedef enum {
    INVALID,    // 무효
    SHARED,     // 공유 (읽기 전용)
    EXCLUSIVE,  // 독점 (유일한 복사본, clean)
    MODIFIED    // 수정됨 (유일한 복사본, dirty)
} MESIState;

typedef struct {
    bool valid;
    MESIState state;
    uint32_t tag;
    uint8_t data[BLOCK_SIZE];
} MESICacheLine;

typedef enum {
    BUS_READ,      // 다른 캐시의 읽기
    BUS_READX,     // 다른 캐시의 쓰기
    BUS_UPGRADE,   // Shared → Exclusive/Modified
    BUS_WRITEBACK  // Modified 데이터 메모리 쓰기
} BusTransaction;

void mesi_bus_snoop(MESICacheLine* line, BusTransaction trans, uint32_t addr) {
    AddressParts parts = parse_address(addr);

    if (!line->valid || line->tag != parts.tag) {
        return;  // Not our line
    }

    switch (trans) {
        case BUS_READ:
            if (line->state == MODIFIED) {
                // 다른 캐시가 읽기 요청 -> 메모리에 쓰기
                // write_to_memory(addr, line->data);
                line->state = SHARED;
            } else if (line->state == EXCLUSIVE) {
                line->state = SHARED;
            }
            break;

        case BUS_READX:
        case BUS_UPGRADE:
            if (line->state == MODIFIED) {
                // write_to_memory(addr, line->data);
            }
            line->state = INVALID;
            line->valid = false;
            break;
    }
}

void mesi_read(MESICacheLine* line, uint32_t addr, bool other_has_copy) {
    if (line->state == INVALID) {
        // 미스: 메모리에서 로드
        // load_from_memory(addr, line->data);
        line->state = other_has_copy ? SHARED : EXCLUSIVE;
        line->valid = true;
    }
    // SHARED, EXCLUSIVE, MODIFIED: just read
}

void mesi_write(MESICacheLine* line, uint32_t addr, uint8_t data, bool other_has_copy) {
    AddressParts parts = parse_address(addr);

    switch (line->state) {
        case INVALID:
            // Read Exclusive
            // send BUS_READX
            // load_from_memory(addr, line->data);
            line->data[parts.offset] = data;
            line->state = MODIFIED;
            line->valid = true;
            break;

        case SHARED:
            // Upgrade
            // send BUS_UPGRADE (invalidate other copies)
            line->data[parts.offset] = data;
            line->state = MODIFIED;
            break;

        case EXCLUSIVE:
            line->data[parts.offset] = data;
            line->state = MODIFIED;
            break;

        case MODIFIED:
            line->data[parts.offset] = data;
            // Already modified
            break;
    }
}
```

### 3. 캐시 최적화 기법

**Prefetching:**

```c
// Stride Prefetcher
typedef struct {
    uint32_t last_addr;
    int32_t stride;
    uint8_t confidence;
} StridePrefetcher;

#define PREFETCH_DEGREE 2  // 2개 앞선 블록 prefetch

void stride_prefetch(StridePrefetcher* pf, Cache* cache, uint32_t access_addr) {
    if (pf->last_addr != 0) {
        int32_t current_stride = access_addr - pf->last_addr;

        if (current_stride == pf->stride) {
            // Stride 패턴 확인
            pf->confidence++;

            if (pf->confidence >= 3) {
                // 충분한 확신: prefetch 수행
                for (int i = 1; i <= PREFETCH_DEGREE; i++) {
                    uint32_t prefetch_addr = access_addr + (pf->stride * i);
                    uint8_t dummy;
                    cache_read(cache, prefetch_addr, &dummy);
                }
            }
        } else {
            // Stride 변경
            pf->stride = current_stride;
            pf->confidence = 0;
        }
    }

    pf->last_addr = access_addr;
}

// Stream Buffer
#define STREAM_BUFFER_SIZE 8

typedef struct {
    uint32_t tag;
    uint8_t data[STREAM_BUFFER_SIZE][BLOCK_SIZE];
    uint8_t valid_entries;
} StreamBuffer;

void stream_buffer_access(StreamBuffer* sb, uint32_t addr) {
    uint32_t block_addr = addr & ~(BLOCK_SIZE - 1);

    // Check if in stream
    if ((block_addr >> 6) == sb->tag) {
        // Hit: shift buffer, prefetch next
        for (int i = 0; i < STREAM_BUFFER_SIZE - 1; i++) {
            memcpy(sb->data[i], sb->data[i+1], BLOCK_SIZE);
        }
        // Prefetch next block
        uint32_t next_addr = block_addr + (STREAM_BUFFER_SIZE * BLOCK_SIZE);
        // load_from_memory(next_addr, sb->data[STREAM_BUFFER_SIZE-1]);
    } else {
        // Miss: allocate new stream
        sb->tag = block_addr >> 6;
        for (int i = 0; i < STREAM_BUFFER_SIZE; i++) {
            uint32_t fetch_addr = block_addr + (i * BLOCK_SIZE);
            // load_from_memory(fetch_addr, sb->data[i]);
        }
    }
}
```

---

## 가상 메모리 심화

### 1. 다단계 페이지 테이블

```c
// 4-level paging (x86-64 style)
#define PAGE_SIZE 4096
#define ENTRIES_PER_TABLE 512

typedef struct {
    uint64_t entries[ENTRIES_PER_TABLE];
} PageTable;

// Page Table Entry 구조 (64-bit)
#define PTE_PRESENT     (1ULL << 0)
#define PTE_WRITABLE    (1ULL << 1)
#define PTE_USER        (1ULL << 2)
#define PTE_ACCESSED    (1ULL << 5)
#define PTE_DIRTY       (1ULL << 6)
#define PTE_HUGE        (1ULL << 7)   // 2MB/1GB page
#define PTE_NX          (1ULL << 63)  // No Execute

typedef struct {
    uint16_t offset;      // 12 bits
    uint16_t pt_index;    // 9 bits  (Level 1)
    uint16_t pd_index;    // 9 bits  (Level 2)
    uint16_t pdpt_index;  // 9 bits  (Level 3)
    uint16_t pml4_index;  // 9 bits  (Level 4)
} VirtualAddress;

VirtualAddress parse_vaddr(uint64_t vaddr) {
    VirtualAddress va;
    va.offset = vaddr & 0xFFF;
    va.pt_index = (vaddr >> 12) & 0x1FF;
    va.pd_index = (vaddr >> 21) & 0x1FF;
    va.pdpt_index = (vaddr >> 30) & 0x1FF;
    va.pml4_index = (vaddr >> 39) & 0x1FF;
    return va;
}

uint64_t walk_page_table(uint64_t cr3, uint64_t vaddr) {
    VirtualAddress va = parse_vaddr(vaddr);

    // Level 4: PML4
    PageTable* pml4 = (PageTable*)(cr3 & ~0xFFF);
    uint64_t pml4e = pml4->entries[va.pml4_index];
    if (!(pml4e & PTE_PRESENT)) {
        return 0;  // Page fault
    }

    // Level 3: PDPT
    PageTable* pdpt = (PageTable*)(pml4e & ~0xFFF);
    uint64_t pdpte = pdpt->entries[va.pdpt_index];
    if (!(pdpte & PTE_PRESENT)) {
        return 0;
    }
    if (pdpte & PTE_HUGE) {  // 1GB huge page
        return (pdpte & ~0x3FFFFFFF) | (vaddr & 0x3FFFFFFF);
    }

    // Level 2: PD
    PageTable* pd = (PageTable*)(pdpte & ~0xFFF);
    uint64_t pde = pd->entries[va.pd_index];
    if (!(pde & PTE_PRESENT)) {
        return 0;
    }
    if (pde & PTE_HUGE) {  // 2MB huge page
        return (pde & ~0x1FFFFF) | (vaddr & 0x1FFFFF);
    }

    // Level 1: PT
    PageTable* pt = (PageTable*)(pde & ~0xFFF);
    uint64_t pte = pt->entries[va.pt_index];
    if (!(pte & PTE_PRESENT)) {
        return 0;
    }

    // Physical address
    return (pte & ~0xFFF) | va.offset;
}
```

### 2. TLB (Translation Lookaside Buffer)

```c
#define TLB_ENTRIES 64

typedef struct {
    bool valid;
    uint64_t vpn;       // Virtual Page Number
    uint64_t pfn;       // Physical Frame Number
    uint8_t asid;       // Address Space ID
    bool dirty;
    bool accessed;
    uint32_t lru;
} TLBEntry;

typedef struct {
    TLBEntry entries[TLB_ENTRIES];
    uint32_t global_counter;

    uint64_t hits;
    uint64_t misses;
} TLB;

bool tlb_lookup(TLB* tlb, uint64_t vaddr, uint8_t asid, uint64_t* paddr) {
    uint64_t vpn = vaddr >> 12;

    for (int i = 0; i < TLB_ENTRIES; i++) {
        if (tlb->entries[i].valid &&
            tlb->entries[i].vpn == vpn &&
            tlb->entries[i].asid == asid) {
            // TLB Hit
            *paddr = (tlb->entries[i].pfn << 12) | (vaddr & 0xFFF);
            tlb->entries[i].lru = tlb->global_counter++;
            tlb->entries[i].accessed = true;
            tlb->hits++;
            return true;
        }
    }

    // TLB Miss
    tlb->misses++;
    return false;
}

void tlb_insert(TLB* tlb, uint64_t vaddr, uint64_t paddr, uint8_t asid) {
    uint64_t vpn = vaddr >> 12;
    uint64_t pfn = paddr >> 12;

    // Find victim (LRU)
    int victim = 0;
    uint32_t min_lru = tlb->entries[0].lru;
    for (int i = 1; i < TLB_ENTRIES; i++) {
        if (!tlb->entries[i].valid) {
            victim = i;
            break;
        }
        if (tlb->entries[i].lru < min_lru) {
            min_lru = tlb->entries[i].lru;
            victim = i;
        }
    }

    // Insert
    tlb->entries[victim].valid = true;
    tlb->entries[victim].vpn = vpn;
    tlb->entries[victim].pfn = pfn;
    tlb->entries[victim].asid = asid;
    tlb->entries[victim].lru = tlb->global_counter++;
    tlb->entries[victim].dirty = false;
    tlb->entries[victim].accessed = true;
}

// 전체 주소 변환 과정
uint64_t translate_address(TLB* tlb, uint64_t cr3, uint64_t vaddr, uint8_t asid) {
    uint64_t paddr;

    // 1. TLB 체크
    if (tlb_lookup(tlb, vaddr, asid, &paddr)) {
        return paddr;
    }

    // 2. Page Table Walk
    paddr = walk_page_table(cr3, vaddr);
    if (paddr == 0) {
        // Page Fault
        handle_page_fault(vaddr);
        paddr = walk_page_table(cr3, vaddr);
    }

    // 3. TLB 갱신
    tlb_insert(tlb, vaddr, paddr, asid);

    return paddr;
}
```

### 3. 페이지 교체 알고리즘

```c
// Clock (Second Chance) Algorithm
typedef struct {
    uint32_t frame_number;
    bool referenced;
    bool dirty;
} ClockPage;

typedef struct {
    ClockPage* pages;
    uint32_t num_frames;
    uint32_t hand;  // Clock hand position
} ClockPageReplacement;

uint32_t clock_replace(ClockPageReplacement* clock) {
    while (true) {
        if (!clock->pages[clock->hand].referenced) {
            // Victim found
            uint32_t victim = clock->hand;
            clock->hand = (clock->hand + 1) % clock->num_frames;
            return victim;
        }

        // Give second chance
        clock->pages[clock->hand].referenced = false;
        clock->hand = (clock->hand + 1) % clock->num_frames;
    }
}

// Enhanced Second Chance (NFU - Not Frequently Used)
typedef struct {
    uint32_t frame_number;
    uint8_t reference_byte;  // 8-bit history
    bool dirty;
} NFUPage;

uint32_t nfu_replace(NFUPage* pages, uint32_t num_frames) {
    // Periodically right-shift reference bytes
    // and set high bit on access

    uint32_t min_frame = 0;
    uint8_t min_refs = 255;

    for (uint32_t i = 0; i < num_frames; i++) {
        if (pages[i].reference_byte < min_refs) {
            min_refs = pages[i].reference_byte;
            min_frame = i;
        } else if (pages[i].reference_byte == min_refs) {
            // Prefer clean pages
            if (!pages[i].dirty && pages[min_frame].dirty) {
                min_frame = i;
            }
        }
    }

    return min_frame;
}

// Aging: shift right and add reference bit
void age_reference_bits(NFUPage* pages, uint32_t num_frames) {
    for (uint32_t i = 0; i < num_frames; i++) {
        pages[i].reference_byte >>= 1;
        if (pages[i].referenced) {
            pages[i].reference_byte |= 0x80;
            pages[i].referenced = false;
        }
    }
}
```

---

## 병렬 처리 아키텍처

### 1. SIMD (Single Instruction Multiple Data)

```c
#include <immintrin.h>  // AVX intrinsics

// Scalar version
void add_arrays_scalar(float* a, float* b, float* c, int n) {
    for (int i = 0; i < n; i++) {
        c[i] = a[i] + b[i];
    }
}

// SIMD version (AVX - 256-bit)
void add_arrays_simd(float* a, float* b, float* c, int n) {
    int i;
    for (i = 0; i <= n - 8; i += 8) {
        __m256 va = _mm256_load_ps(&a[i]);  // Load 8 floats
        __m256 vb = _mm256_load_ps(&b[i]);
        __m256 vc = _mm256_add_ps(va, vb);  // Add 8 floats in parallel
        _mm256_store_ps(&c[i], vc);         // Store 8 floats
    }

    // Handle remaining elements
    for (; i < n; i++) {
        c[i] = a[i] + b[i];
    }
}

// Matrix multiplication with SIMD
void matmul_simd(float* A, float* B, float* C, int N) {
    for (int i = 0; i < N; i++) {
        for (int j = 0; j < N; j++) {
            __m256 sum = _mm256_setzero_ps();

            int k;
            for (k = 0; k <= N - 8; k += 8) {
                __m256 a = _mm256_load_ps(&A[i*N + k]);
                __m256 b = _mm256_load_ps(&B[k*N + j]);
                sum = _mm256_add_ps(sum, _mm256_mul_ps(a, b));
            }

            // Horizontal sum
            float temp[8];
            _mm256_store_ps(temp, sum);
            float result = 0;
            for (int t = 0; t < 8; t++) result += temp[t];

            // Remaining elements
            for (; k < N; k++) {
                result += A[i*N + k] * B[k*N + j];
            }

            C[i*N + j] = result;
        }
    }
}

// SIMD reduction
float sum_simd(float* arr, int n) {
    __m256 sum_vec = _mm256_setzero_ps();

    int i;
    for (i = 0; i <= n - 8; i += 8) {
        __m256 v = _mm256_load_ps(&arr[i]);
        sum_vec = _mm256_add_ps(sum_vec, v);
    }

    // Horizontal add
    float temp[8];
    _mm256_store_ps(temp, sum_vec);
    float sum = 0;
    for (int j = 0; j < 8; j++) sum += temp[j];

    // Tail
    for (; i < n; i++) {
        sum += arr[i];
    }

    return sum;
}
```

### 2. 멀티코어 동기화 프리미티브

```c
#include <stdatomic.h>

// Compare-And-Swap 기반 스핀락
typedef struct {
    atomic_int lock;
} Spinlock;

void spinlock_init(Spinlock* s) {
    atomic_store(&s->lock, 0);
}

void spinlock_acquire(Spinlock* s) {
    int expected = 0;
    while (!atomic_compare_exchange_weak(&s->lock, &expected, 1)) {
        expected = 0;
        // Busy wait
        _mm_pause();  // Hint to CPU for spinlock
    }
}

void spinlock_release(Spinlock* s) {
    atomic_store(&s->lock, 0);
}

// Ticket Lock (FIFO fairness)
typedef struct {
    atomic_uint next_ticket;
    atomic_uint now_serving;
} TicketLock;

void ticket_lock_init(TicketLock* t) {
    atomic_store(&t->next_ticket, 0);
    atomic_store(&t->now_serving, 0);
}

void ticket_lock_acquire(TicketLock* t) {
    uint my_ticket = atomic_fetch_add(&t->next_ticket, 1);
    while (atomic_load(&t->now_serving) != my_ticket) {
        _mm_pause();
    }
}

void ticket_lock_release(TicketLock* t) {
    uint current = atomic_load(&t->now_serving);
    atomic_store(&t->now_serving, current + 1);
}

// MCS Lock (scalable queue lock)
typedef struct MCSNode {
    atomic_bool locked;
    struct MCSNode* next;
} MCSNode;

typedef struct {
    atomic_ptr tail;
} MCSLock;

void mcs_lock_acquire(MCSLock* lock, MCSNode* node) {
    node->next = NULL;
    node->locked = true;

    MCSNode* predecessor = atomic_exchange(&lock->tail, node);

    if (predecessor != NULL) {
        predecessor->next = node;
        while (atomic_load(&node->locked)) {
            _mm_pause();
        }
    }
}

void mcs_lock_release(MCSLock* lock, MCSNode* node) {
    if (node->next == NULL) {
        MCSNode* expected = node;
        if (atomic_compare_exchange_strong(&lock->tail, &expected, NULL)) {
            return;  // No one waiting
        }
        // Wait for next to be set
        while (node->next == NULL) {
            _mm_pause();
        }
    }
    atomic_store(&node->next->locked, false);
}
```

### 3. Lock-Free 자료구조

```c
// Lock-Free Stack
typedef struct LFNode {
    int data;
    struct LFNode* next;
} LFNode;

typedef struct {
    atomic_ptr top;
} LockFreeStack;

void lf_stack_init(LockFreeStack* stack) {
    atomic_store(&stack->top, NULL);
}

void lf_stack_push(LockFreeStack* stack, int value) {
    LFNode* node = malloc(sizeof(LFNode));
    node->data = value;

    LFNode* old_top;
    do {
        old_top = atomic_load(&stack->top);
        node->next = old_top;
    } while (!atomic_compare_exchange_weak(&stack->top, &old_top, node));
}

bool lf_stack_pop(LockFreeStack* stack, int* value) {
    LFNode* old_top;
    LFNode* new_top;

    do {
        old_top = atomic_load(&stack->top);
        if (old_top == NULL) {
            return false;  // Empty
        }
        new_top = old_top->next;
    } while (!atomic_compare_exchange_weak(&stack->top, &old_top, new_top));

    *value = old_top->data;
    // Note: ABA problem! Need hazard pointers or epoch-based reclamation
    // free(old_top);  // Unsafe!

    return true;
}

// Lock-Free Queue (Michael-Scott)
typedef struct LFQNode {
    int data;
    atomic_ptr next;
} LFQNode;

typedef struct {
    atomic_ptr head;
    atomic_ptr tail;
} LockFreeQueue;

void lf_queue_init(LockFreeQueue* queue) {
    LFQNode* dummy = malloc(sizeof(LFQNode));
    atomic_store(&dummy->next, NULL);
    atomic_store(&queue->head, dummy);
    atomic_store(&queue->tail, dummy);
}

void lf_queue_enqueue(LockFreeQueue* queue, int value) {
    LFQNode* node = malloc(sizeof(LFQNode));
    node->data = value;
    atomic_store(&node->next, NULL);

    while (true) {
        LFQNode* tail = atomic_load(&queue->tail);
        LFQNode* next = atomic_load(&tail->next);

        if (tail == atomic_load(&queue->tail)) {
            if (next == NULL) {
                if (atomic_compare_exchange_weak(&tail->next, &next, node)) {
                    atomic_compare_exchange_weak(&queue->tail, &tail, node);
                    return;
                }
            } else {
                atomic_compare_exchange_weak(&queue->tail, &tail, next);
            }
        }
    }
}

bool lf_queue_dequeue(LockFreeQueue* queue, int* value) {
    while (true) {
        LFQNode* head = atomic_load(&queue->head);
        LFQNode* tail = atomic_load(&queue->tail);
        LFQNode* next = atomic_load(&head->next);

        if (head == atomic_load(&queue->head)) {
            if (head == tail) {
                if (next == NULL) {
                    return false;  // Empty
                }
                atomic_compare_exchange_weak(&queue->tail, &tail, next);
            } else {
                *value = next->data;
                if (atomic_compare_exchange_weak(&queue->head, &head, next)) {
                    // free(head);  // Unsafe! Need memory reclamation
                    return true;
                }
            }
        }
    }
}
```

---

## GPU 아키텍처

### 1. CUDA 프로그래밍 모델

```cuda
// Vector addition on GPU
__global__ void vectorAdd(float* A, float* B, float* C, int N) {
    int idx = blockIdx.x * blockDim.x + threadIdx.x;

    if (idx < N) {
        C[idx] = A[idx] + B[idx];
    }
}

// Host code
void gpuVectorAdd(float* h_A, float* h_B, float* h_C, int N) {
    float *d_A, *d_B, *d_C;
    size_t bytes = N * sizeof(float);

    // Allocate device memory
    cudaMalloc(&d_A, bytes);
    cudaMalloc(&d_B, bytes);
    cudaMalloc(&d_C, bytes);

    // Copy to device
    cudaMemcpy(d_A, h_A, bytes, cudaMemcpyHostToDevice);
    cudaMemcpy(d_B, h_B, bytes, cudaMemcpyHostToDevice);

    // Launch kernel
    int threadsPerBlock = 256;
    int blocksPerGrid = (N + threadsPerBlock - 1) / threadsPerBlock;
    vectorAdd<<<blocksPerGrid, threadsPerBlock>>>(d_A, d_B, d_C, N);

    // Copy result back
    cudaMemcpy(h_C, d_C, bytes, cudaMemcpyDeviceToHost);

    // Free device memory
    cudaFree(d_A);
    cudaFree(d_B);
    cudaFree(d_C);
}

// Matrix multiplication with shared memory
__global__ void matrixMul(float* A, float* B, float* C, int N) {
    __shared__ float As[TILE_SIZE][TILE_SIZE];
    __shared__ float Bs[TILE_SIZE][TILE_SIZE];

    int row = blockIdx.y * TILE_SIZE + threadIdx.y;
    int col = blockIdx.x * TILE_SIZE + threadIdx.x;

    float sum = 0.0f;

    for (int t = 0; t < (N + TILE_SIZE - 1) / TILE_SIZE; t++) {
        // Load tile into shared memory
        if (row < N && t * TILE_SIZE + threadIdx.x < N) {
            As[threadIdx.y][threadIdx.x] = A[row * N + t * TILE_SIZE + threadIdx.x];
        } else {
            As[threadIdx.y][threadIdx.x] = 0.0f;
        }

        if (col < N && t * TILE_SIZE + threadIdx.y < N) {
            Bs[threadIdx.y][threadIdx.x] = B[(t * TILE_SIZE + threadIdx.y) * N + col];
        } else {
            Bs[threadIdx.y][threadIdx.x] = 0.0f;
        }

        __syncthreads();

        // Compute partial sum
        for (int k = 0; k < TILE_SIZE; k++) {
            sum += As[threadIdx.y][k] * Bs[k][threadIdx.x];
        }

        __syncthreads();
    }

    if (row < N && col < N) {
        C[row * N + col] = sum;
    }
}

// Reduction (parallel sum)
__global__ void reduce(float* input, float* output, int N) {
    __shared__ float sdata[256];

    unsigned int tid = threadIdx.x;
    unsigned int idx = blockIdx.x * blockDim.x + threadIdx.x;

    sdata[tid] = (idx < N) ? input[idx] : 0;
    __syncthreads();

    // Reduction in shared memory
    for (unsigned int s = blockDim.x / 2; s > 0; s >>= 1) {
        if (tid < s) {
            sdata[tid] += sdata[tid + s];
        }
        __syncthreads();
    }

    if (tid == 0) {
        output[blockIdx.x] = sdata[0];
    }
}
```

### 2. GPU 메모리 계층

```cuda
// Global memory (slow, large)
__global__ void useGlobalMemory(float* global_data, int N) {
    int idx = blockIdx.x * blockDim.x + threadIdx.x;
    if (idx < N) {
        global_data[idx] *= 2.0f;  // ~400-600 cycles latency
    }
}

// Shared memory (fast, small, per-block)
__global__ void useSharedMemory(float* input, float* output, int N) {
    __shared__ float shared_data[256];

    int tid = threadIdx.x;
    int idx = blockIdx.x * blockDim.x + threadIdx.x;

    // Load from global to shared
    if (idx < N) {
        shared_data[tid] = input[idx];
    }
    __syncthreads();

    // Process using shared memory (~5 cycles latency)
    if (idx < N) {
        float value = shared_data[tid];
        // ... computation ...
        output[idx] = value;
    }
}

// Constant memory (cached, read-only)
__constant__ float const_coeffs[256];

__global__ void useConstantMemory(float* data, int N) {
    int idx = blockIdx.x * blockDim.x + threadIdx.x;
    if (idx < N) {
        data[idx] = data[idx] * const_coeffs[idx % 256];
    }
}

// Texture memory (cached, 2D locality)
texture<float, 2, cudaReadModeElementType> texRef;

__global__ void useTextureMemory(float* output, int width, int height) {
    int x = blockIdx.x * blockDim.x + threadIdx.x;
    int y = blockIdx.y * blockDim.y + threadIdx.y;

    if (x < width && y < height) {
        float value = tex2D(texRef, x, y);  // Cached read
        output[y * width + x] = value;
    }
}

// Register memory (fastest, per-thread)
__global__ void useRegisters(float* data, int N) {
    int idx = blockIdx.x * blockDim.x + threadIdx.x;

    // These are stored in registers (1 cycle access)
    float r0 = data[idx];
    float r1 = r0 * 2.0f;
    float r2 = r1 + 3.0f;

    data[idx] = r2;
}
```

---

## 최신 CPU 기술

### 1. Out-of-Order Execution

```c
// Tomasulo 알고리즘 시뮬레이션
typedef struct {
    bool busy;
    int op;
    int vj, vk;        // 값
    int qj, qk;        // 생산자 reservation station
    uint32_t address;
} ReservationStation;

typedef struct {
    bool busy;
    int value;
    int producer;      // 어느 reservation station이 쓸 예정인지
} RegisterFile;

typedef struct {
    ReservationStation rs[16];
    RegisterFile rf[32];
    int common_data_bus;
    int cdb_producer;
} TomasuloSimulator;

void issue_instruction(TomasuloSimulator* sim, Instruction inst) {
    // Find free reservation station
    int free_rs = -1;
    for (int i = 0; i < 16; i++) {
        if (!sim->rs[i].busy) {
            free_rs = i;
            break;
        }
    }

    if (free_rs == -1) {
        // Structural hazard: stall
        return;
    }

    ReservationStation* rs = &sim->rs[free_rs];
    rs->busy = true;
    rs->op = inst.opcode;

    // Check operands
    if (sim->rf[inst.rs].producer == -1) {
        rs->vj = sim->rf[inst.rs].value;
        rs->qj = -1;
    } else {
        rs->qj = sim->rf[inst.rs].producer;
    }

    if (sim->rf[inst.rt].producer == -1) {
        rs->vk = sim->rf[inst.rt].value;
        rs->qk = -1;
    } else {
        rs->qk = sim->rf[inst.rt].producer;
    }

    // Mark destination register
    sim->rf[inst.rd].producer = free_rs;
}

void execute_and_broadcast(TomasuloSimulator* sim) {
    // Find ready instruction
    for (int i = 0; i < 16; i++) {
        if (sim->rs[i].busy && sim->rs[i].qj == -1 && sim->rs[i].qk == -1) {
            // Execute
            int result = alu_execute(sim->rs[i].vj, sim->rs[i].vk, sim->rs[i].op);

            // Broadcast on CDB
            sim->common_data_bus = result;
            sim->cdb_producer = i;

            // Update waiting stations
            for (int j = 0; j < 16; j++) {
                if (sim->rs[j].qj == i) {
                    sim->rs[j].vj = result;
                    sim->rs[j].qj = -1;
                }
                if (sim->rs[j].qk == i) {
                    sim->rs[j].vk = result;
                    sim->rs[j].qk = -1;
                }
            }

            // Update register file
            for (int j = 0; j < 32; j++) {
                if (sim->rf[j].producer == i) {
                    sim->rf[j].value = result;
                    sim->rf[j].producer = -1;
                }
            }

            sim->rs[i].busy = false;
            break;
        }
    }
}
```

### 2. Speculative Execution과 Branch Prediction

```c
// Perceptron Branch Predictor
#define HISTORY_LENGTH 64
#define NUM_PERCEPTRONS 1024

typedef struct {
    int weights[HISTORY_LENGTH + 1];  // +1 for bias
} Perceptron;

typedef struct {
    Perceptron perceptrons[NUM_PERCEPTRONS];
    uint64_t global_history;
    int threshold;
} PerceptronPredictor;

void init_perceptron_predictor(PerceptronPredictor* pred) {
    pred->global_history = 0;
    pred->threshold = (int)(1.93 * HISTORY_LENGTH + 14);

    for (int i = 0; i < NUM_PERCEPTRONS; i++) {
        for (int j = 0; j <= HISTORY_LENGTH; j++) {
            pred->perceptrons[i].weights[j] = 0;
        }
    }
}

bool predict_perceptron(PerceptronPredictor* pred, uint32_t pc) {
    int index = pc % NUM_PERCEPTRONS;
    Perceptron* p = &pred->perceptrons[index];

    // Compute weighted sum
    int output = p->weights[0];  // Bias
    for (int i = 0; i < HISTORY_LENGTH; i++) {
        bool history_bit = (pred->global_history >> i) & 1;
        output += history_bit ? p->weights[i+1] : -p->weights[i+1];
    }

    return output >= 0;
}

void train_perceptron(PerceptronPredictor* pred, uint32_t pc, bool taken) {
    int index = pc % NUM_PERCEPTRONS;
    Perceptron* p = &pred->perceptrons[index];

    // Compute output
    int output = p->weights[0];
    for (int i = 0; i < HISTORY_LENGTH; i++) {
        bool history_bit = (pred->global_history >> i) & 1;
        output += history_bit ? p->weights[i+1] : -p->weights[i+1];
    }

    bool prediction = output >= 0;

    // Train if mispredicted or output close to threshold
    if (prediction != taken || abs(output) <= pred->threshold) {
        int t = taken ? 1 : -1;
        p->weights[0] += t;

        for (int i = 0; i < HISTORY_LENGTH; i++) {
            bool history_bit = (pred->global_history >> i) & 1;
            if (history_bit) {
                p->weights[i+1] += t;
            } else {
                p->weights[i+1] -= t;
            }
        }
    }

    // Update history
    pred->global_history <<= 1;
    pred->global_history |= taken ? 1 : 0;
}
```

### 3. Transactional Memory

```c
// Software Transactional Memory (STM)
typedef struct {
    void* address;
    uint64_t value;
    uint64_t version;
} STMLogEntry;

typedef struct {
    STMLogEntry read_set[256];
    int read_set_size;
    STMLogEntry write_set[256];
    int write_set_size;
    uint64_t start_timestamp;
} Transaction;

typedef struct {
    atomic_uint_least64_t version;
    atomic_uint_least64_t value;
    atomic_flag lock;
} STMVariable;

atomic_uint_least64_t global_clock = 0;

void stm_begin(Transaction* tx) {
    tx->read_set_size = 0;
    tx->write_set_size = 0;
    tx->start_timestamp = atomic_load(&global_clock);
}

uint64_t stm_read(Transaction* tx, STMVariable* var) {
    // Check write set first
    for (int i = 0; i < tx->write_set_size; i++) {
        if (tx->write_set[i].address == var) {
            return tx->write_set[i].value;
        }
    }

    // Read from memory
    uint64_t version, value;
    do {
        version = atomic_load(&var->version);
        value = atomic_load(&var->value);
    } while (version != atomic_load(&var->version));

    // Validate version
    if (version > tx->start_timestamp) {
        // Conflict detected
        return STM_ABORT;
    }

    // Add to read set
    tx->read_set[tx->read_set_size].address = var;
    tx->read_set[tx->read_set_size].value = value;
    tx->read_set[tx->read_set_size].version = version;
    tx->read_set_size++;

    return value;
}

void stm_write(Transaction* tx, STMVariable* var, uint64_t value) {
    // Add to write set (buffered write)
    tx->write_set[tx->write_set_size].address = var;
    tx->write_set[tx->write_set_size].value = value;
    tx->write_set_size++;
}

bool stm_commit(Transaction* tx) {
    // Lock all variables in write set
    for (int i = 0; i < tx->write_set_size; i++) {
        STMVariable* var = tx->write_set[i].address;
        while (atomic_flag_test_and_set(&var->lock)) {
            // Spin
        }
    }

    // Validate read set
    for (int i = 0; i < tx->read_set_size; i++) {
        STMVariable* var = tx->read_set[i].address;
        uint64_t current_version = atomic_load(&var->version);

        if (current_version != tx->read_set[i].version) {
            // Validation failed: abort
            for (int j = 0; j < tx->write_set_size; j++) {
                STMVariable* wvar = tx->write_set[j].address;
                atomic_flag_clear(&wvar->lock);
            }
            return false;
        }
    }

    // Get commit timestamp
    uint64_t commit_ts = atomic_fetch_add(&global_clock, 1) + 1;

    // Write values
    for (int i = 0; i < tx->write_set_size; i++) {
        STMVariable* var = tx->write_set[i].address;
        atomic_store(&var->value, tx->write_set[i].value);
        atomic_store(&var->version, commit_ts);
        atomic_flag_clear(&var->lock);
    }

    return true;
}
```

---

## 성능 분석 및 벤치마킹

### 실제 성능 측정

```c
#include <time.h>

typedef struct {
    double execution_time;
    uint64_t instructions;
    uint64_t cycles;
    uint64_t l1_hits;
    uint64_t l1_misses;
    uint64_t tlb_hits;
    uint64_t tlb_misses;
    uint64_t branch_mispredicts;
} PerformanceMetrics;

// RDTSC: Read Time-Stamp Counter
static inline uint64_t rdtsc() {
    uint32_t lo, hi;
    __asm__ volatile ("rdtsc" : "=a"(lo), "=d"(hi));
    return ((uint64_t)hi << 32) | lo;
}

void benchmark_cache_performance() {
    const int SIZE = 64 * 1024 * 1024;  // 64MB
    int* arr = malloc(SIZE * sizeof(int));

    // Sequential access (cache-friendly)
    uint64_t start = rdtsc();
    int sum = 0;
    for (int i = 0; i < SIZE; i++) {
        sum += arr[i];
    }
    uint64_t sequential_cycles = rdtsc() - start;

    // Random access (cache-unfriendly)
    start = rdtsc();
    sum = 0;
    for (int i = 0; i < SIZE; i++) {
        int index = (i * 12345) % SIZE;
        sum += arr[index];
    }
    uint64_t random_cycles = rdtsc() - start;

    printf("Sequential: %lu cycles\n", sequential_cycles);
    printf("Random: %lu cycles\n", random_cycles);
    printf("Ratio: %.2f\n", (double)random_cycles / sequential_cycles);

    free(arr);
}
```

---

**다음 주제:**
- 보안과 암호학
- AI/ML 기초
- 소프트웨어 공학

컴퓨터 구조의 모든 핵심 개념을 마스터했습니다. 이제 실제 프로세서가 어떻게 동작하는지 완벽히 이해할 수 있습니다.
