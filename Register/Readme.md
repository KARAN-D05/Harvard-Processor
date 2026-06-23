# A Register (8-Bit)

## Overview

An 8-bit loadable register with asynchronous reset and tri-state output enable.

### Features

- 8-bit data storage (Parameterized)
- Clocked load operation
- Asynchronous reset
- Tri-state output enable
- Synthesizable Verilog RTL
- Gate-Level Simulation (GLS) verified
- Synthesized using Sky130 HD standard-cell library

## RTL Interface

| Signal | Direction | Width | Description |
|----------|----------|----------|----------|
| clk | Input | 1 | System clock |
| rst | Input | 1 | Asynchronous reset |
| loadA | Input | 1 | Load enable |
| enableA | Input | 1 | Output enable |
| in | Input | 8 | Data input |
| out | Output | 8 | Tri-state data output |

## Verification

### RTL Simulation

The register was verified using Icarus Verilog and GTKWave.

Verified functionality:

- Reset operation
- Data loading
- Data retention
- Tri-state output enable
- Simultaneous load and enable behavior

### Gate-Level Simulation (GLS)

The Sky130-mapped netlist was simulated to verify post-synthesis functionality.

---

## Synthesis Results

**Technology:** Sky130 HD  
**Synthesis Tool:** Yosys

| Metric | Value |
|----------|----------|
| Area | 370.3552 µm² |
| Technology Library | Sky130 HD |

---

## Static Timing Analysis (OpenSTA)

### Scenario 1: Ideal Timing

Clock period constraint:

```text
10 ns
```

No input/output timing constraints applied.

| Metric | Value |
|----------|----------|
| Clock Period | 10 ns |
| Worst Slack | 9.26 ns |
| Estimated Critical Path | 0.74 ns |
| Estimated Fmax | ~1.35 GHz |

### Scenario 2: Constrained Timing

Timing constraints:

```text
Input Delay  = 1 ns
Output Delay = 1 ns
Clock Period = 10 ns
```

| Metric | Value |
|----------|----------|
| Clock Period | 10 ns |
| Input Delay | 1 ns |
| Output Delay | 1 ns |
| Worst Slack | 8.59 ns |
| Estimated Fmax | ~709 MHz |

## Timing Comparison

| Scenario | Worst Slack (ns) | Estimated Fmax |
|----------|----------:|----------:|
| Ideal STA | 9.26 | ~1.35 GHz |
| Constrained STA | 8.59 | ~709 MHz |

## Power Analysis

**Operating Frequency:** 100 MHz (10 ns clock period)

| Metric | Value |
|----------|----------|
| Total Power | 41.3  µW |

## Tool Flow

```text
Verilog RTL
    ↓
Icarus Verilog
    ↓
GTKWave
    ↓
Yosys Synthesis
    ↓
Sky130 HD Mapping
    ↓
OpenSTA Timing Analysis
    ↓
Power Analysis
    ↓
Gate-Level Simulation
```
