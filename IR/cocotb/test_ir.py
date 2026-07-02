import cocotb
from cocotb.clock import Clock
from cocotb.triggers import RisingEdge, Timer

@cocotb.test()
async def test (dut):

    cocotb.start_soon(Clock(dut.clk, 10, unit="ns").start())

    dut.load.value = 0
    dut.inp.value = 0
    dut.rst.value = 1

    await Timer(1, unit="ns")

    assert dut.out.value == 0

    dut.rst.value = 0

    await RisingEdge(dut.clk)

    dut.inp.value = 0x4900
    dut.load.value = 1

    await RisingEdge(dut.clk)

    await Timer(1, unit="ns")

    assert dut.out.value == 0x4900

    dut.load.value = 0
    dut.inp.value = 0x2000

    await RisingEdge(dut.clk)
    await Timer(1, unit="ns")

    assert dut.out.value == 0x4900

    dut.load.value = 1
    dut.inp.value = 0x453E

    await RisingEdge(dut.clk)
    await Timer(1, unit="ns")

    assert dut.out.value == 0x453E

    dut.load.value = 0
    dut.inp.value = 0x0000

    await RisingEdge(dut.clk)
    await Timer(1, unit="ns")

    assert dut.out.value == 0x453E