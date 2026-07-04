import cocotb
from cocotb.triggers import Timer
from pathlib import Path


@cocotb.test()
async def test(dut):

    hex_file = Path(__file__).parent / "Program.hex"

    expected = [0] * 256

    with open(hex_file, "r") as f:

        for i, line in enumerate(f):

            line = line.strip()

            if line:
                expected[i] = int(line, 16)

    for addr in range(256):

        dut.addr.value = addr

        await Timer(1, unit="ns")

        assert int(dut.out.value) == expected[addr], (
            f"ADDR={addr:02X} "
            f"Expected={expected[addr]:02X} "
            f"Got={int(dut.out.value):02X}"
        )