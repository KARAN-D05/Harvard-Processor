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

The complete processor successfully synthesized to the Sky130 HD standard-cell library and underwent Static Timing Analysis (STA).

The reported worst negative slack is dominated by the behavioral implementation of the 256 × 8 Data RAM. Since the synthesis flow targets only Sky130 HD standard cells, the memory is realized as approximately 2048 D Flip-Flops together with synthesized address decoding and hierarchical multiplexing logic rather than a dedicated SRAM macro.

Static Timing Analysis consistently identified the critical path as originating from the **Memory Address Register (MAR)**, propagating through the synthesized memory read network and associated combinational logic before reaching the destination register. Experimental characterization across multiple synthesized memory depths (8 B - 1024 B) showed that increasing memory depth significantly increases both area and address-path delay, confirming that the register-based memory implementation dominates the processor's timing.

Further investigation of the synthesized netlist showed that the least significant address bits experience the highest effective electrical loading due to the hierarchical multiplexer structure generated during synthesis, explaining why the critical path consistently originates from the lower MAR address bits.

These timing results therefore characterize the synthesized register-based memory implementation rather than the processor datapath itself. In a practical ASIC implementation, the behavioral RAM would typically be replaced by a dedicated SRAM macro, substantially reducing both silicon area and critical path delay.

## Power

| Metric               |     Value |
| -------------------- | -------- |
| Total Power          |   8.67 mW |
