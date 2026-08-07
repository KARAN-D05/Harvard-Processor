# Computer

A parameterized Harvard Architecture processor implemented entirely in synthesizable Verilog HDL.

The processor features a custom Instruction Set Architecture (ISA), a hardwired control unit and parameterized components. It supports arithmetic, logical, memory, and conditional branch instructions while demonstrating the complete RTL-to-Gate synthesis flow using the Sky130 HD standard-cell library.

<p align="center">
  <img src="images/computer_synthesis.png" width="1000"/>
  <br>
  <sub>Yosys-Synthesis</sub>
</p>

## Architecture

The processor consists of the following major hardware blocks:

* Program Counter (PC)
* Program ROM
* Instruction Register (IR)
* Hardwired Control Unit (CU)
* T-State Counter
* Memory Address Register (MAR)
* Data RAM
* Register A
* Register B
* Arithmetic Logic Unit (ALU)
* Flag Register (FR)
* Shared Internal Bus Multiplexer

The processor follows a Harvard architecture where instruction memory and data memory are physically separated.

## Synthesis Results

**Technology:** Sky130 HD
**Synthesis Tool:** Yosys

| Metric         |          Value |
| -------------- | -------------: |
| Chip Area      | 80347.0592 µm² |

## Static Timing Analysis (OpenSTA)

Clock Constraint

```
10 ns
```

| Metric               |     Value |
| -------------------- | --------: |
| Clock Period         |     10 ns |
| Critical Path Delay  |  25.55 ns |
| Worst Negative Slack | -16.04 ns |

## Timing Analysis

The complete processor was synthesized to the Sky130 HD standard-cell library and verified using Static Timing Analysis (STA).

No dedicated SRAM macro was used for the 256 × 8 Data RAM. Instead, the behavioral Verilog memory was synthesized entirely from Sky130 HD standard cells, resulting in a register-based memory implementation consisting of approximately 2048 D Flip-Flops, together with synthesized address decoding via hierarchical multiplexing logic.

As a consequence, the synthesized memory becomes the dominant contributor to both silicon area and timing. Static Timing Analysis consistently identified the worst-case path as originating from the Memory Address Register (MAR), propagating through the synthesized memory network before reaching the destination register. Rather than reflecting the intrinsic speed of the processor datapath, the reported worst negative slack is therefore primarily a characteristic of the synthesized register-based memory implementation.

To better understand this behavior, the memory was characterized across multiple synthesized depths (8 B, 64 B, 128 B, 256 B). As expected, increasing memory depth produced a corresponding increase in silicon area and critical path delay. For memories up to 256 bytes, the reported logical fanout of the least significant address bit (MAR[0]) closely followed the theoretical fanout expected from a hierarchical multiplexer tree generated during synthesis. 

Further investigation of the timing reports revealed that the critical path consistently originated from the lower address bits of the Memory Address Register. By experimentally characterizing the Clock-to-Q delay of every MAR bit, it was observed that the least significant address bits experienced the largest launch delays, with the delay decreasing toward the more significant bits. This behavior is consistent with the synthesized multiplexer hierarchy, where lower address bits control the widest levels of the selection network and therefore experience the greatest effective capacitive loading. Although some address bits exhibit identical reported logical fanout, the internal implementation of the synthesized multiplexers results in different electrical loading, demonstrating that identical logical connectivity does not necessarily imply identical timing behavior.

This characterization provides a practical illustration of how memory organization, synthesis decisions, and electrical loading influence Static Timing Analysis results. The reported timing therefore represents the performance of a standard-cell synthesized register-based memory, rather than an optimized memory subsystem. In a practical ASIC implementation, the behavioral RAM would normally be replaced with a dedicated SRAM macro, substantially reducing silicon area, lowering memory access delay, and shifting the processor's critical path away from the synthesized memory read network.

### Experimental Characterization
| RAM Size | Approx. Area (µm²) | MAR[0] Fanout (Reported) | Critical Path Launch | MAR[0] Clock→Q (ns) | Data Arrival (ns) | Slack @ 10 ns |
| ------- | ----------------- | ----------------------- | -------------------- | ------------------ | ---------------- | ------------ |
|     64 B |            ~26,000 |                      131 | MAR[0]               |                4.71 |              8.30 |         +1.58 |
|    128 B |            ~42,700 |                      259 | MAR[0]               |                9.10 |             13.78 |         −3.92 |
|    256 B |            ~80,400 |                      515 | MAR[0]               |               17.89 |             25.55 |        −16.04 |

### Clock→Q Characterization of MAR Address Bits
| Address Bit | 64 B | 128 B | 256 B |
| ----------- | --- | ---- | ---- |
| MAR[0]      | 4.71 |  9.10 | 17.89 |
| MAR[1]      | 2.81 |  5.31 | 10.31 |
| MAR[2]      | 1.25 |  2.24 |  4.11 |
| MAR[3]      | 1.10 |  1.83 |  3.41 |
| MAR[4]      | 0.61 |  0.85 |  1.25 |
| MAR[5]      | 0.48 |  0.64 |  1.10 |
| MAR[6]      | 0.33 |  0.46 |  0.60 |
| MAR[7]      | 0.33 |  0.33 |  0.48 |

### Clock→Q Difference Between Adjacent Address-Bit Pairs
| Pair            |     64 B |    128 B |    256 B |
| --------------- | ------- | ------- | ------- |
| MAR[0] − MAR[1] | **1.90** | **3.79** | **7.58** |
| MAR[2] − MAR[3] | **0.15** | **0.41** | **0.70** |
| MAR[4] − MAR[5] | **0.13** | **0.21** | **0.15** |
| MAR[6] − MAR[7] | **0.00** | **0.13** | **0.12** |

### Deductions
- The synthesized RAM dominates both chip area and critical path delay.
- The critical path consistently launches from MAR[0], indicating that the least significant address bit experiences the greatest effective capacitive loading.
- For memories up to 256 B, the reported logical fanout of MAR[0] closely matches the expected fanout of the first level of the synthesized multiplexer hierarchy (131 → 259 → 515).
- Clock→Q delay increases rapidly with memory depth, becoming the dominant contributor to the overall critical path. For the 256 B memory, MAR[0] Clock→Q (17.89 ns) accounts for approximately 70% of the total 25.55 ns data arrival time.
- Characterizing every MAR bit shows that Clock→Q delay decreases toward more significant address bits, consistent with progressively smaller multiplexer stages and reduced effective capacitive loading.
- Although adjacent address-bit pairs exhibit approximately the same logical fanout at the synthesized 4:1 multiplexer level, decomposition into internal 2:1 multiplexers indicates that the lower bit of each pair drives roughly twice the internal load. This provides a plausible explanation for the measured Clock→Q differences despite identical reported fanout.
- The Clock→Q difference between adjacent address-bit pairs decreases toward the more significant bits, supporting the hypothesis that while the load ratio remains approximately constant, the absolute load difference shrinks as the multiplexer hierarchy narrows.

## Power

| Metric               |     Value |
| -------------------- | -------- |
| Total Power          |   8.67 mW |
