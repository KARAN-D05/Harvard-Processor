import cocotb
from cocotb.clock import Clock
from cocotb.triggers import RisingEdge, Timer, ClockCycles

@cocotb.test()
async def test(dut):

    cocotb.start_soon(Clock(dut.clk, 10, unit="ns").start())

    dut.load.value = 0
    dut.inp.value = 0
    dut.rst.value = 1
    dut.en.value = 0

    await Timer(1, unit="ns")

    assert dut.out.value == 0, "1"

    dut.rst.value = 0

    await RisingEdge(dut.clk)

    dut.en.value = 1

    await ClockCycles(dut.clk, 10)
    await Timer(1, unit="ns")

    assert dut.out.value == 0x0A, "2"

    dut.en.value = 0
    dut.inp.value = 0x10
    dut.load.value = 1
    
    await RisingEdge(dut.clk)
    await Timer(1, unit="ns")

    assert dut.out.value == 0x10, "3"

    dut.load.value = 0
    dut.inp.value = 0x20

    await RisingEdge(dut.clk)
    await Timer(1, unit="ns")

    assert dut.out.value == 0x10, "4"

    dut.load.value = 1
    dut.inp.value = 0x45

    await RisingEdge(dut.clk)
    await Timer(1, unit="ns")

    assert dut.out.value == 0x45, "5"

    dut.en.value = 1
    dut.load.value = 0

    await ClockCycles(dut.clk, 8)
    await Timer(1, unit="ns")

    assert dut.out.value == 0x4D, "6"