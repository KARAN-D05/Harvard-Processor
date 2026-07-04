import cocotb
from cocotb.triggers import Timer

OP_ADD    = 0
OP_SUB    = 1
OP_AND    = 2
OP_OR     = 3
OP_XOR    = 4
OP_NOT_A  = 5
OP_PASS_A = 6
OP_PASS_B = 7


async def check_outputs(dut, a, b, sel, expected, carry):

    assert int(dut.out.value) == expected, (
        f"SEL={sel} A={a:02X} B={b:02X} "
        f"Expected={expected:02X} "
        f"Got={int(dut.out.value):02X}"
    )

    assert int(dut.carry.value) == carry, (
        f"SEL={sel} A={a:02X} B={b:02X} "
        f"Expected={carry} "
        f"Got={int(dut.carry.value)}"
    )

    assert int(dut.zero.value) == (expected == 0), (
        f"SEL={sel} A={a:02X} B={b:02X} "
        f"Expected={int(expected == 0)} "
        f"Got={int(dut.zero.value)}"
    )

    assert int(dut.neg.value) == ((expected >> 7) & 1), (
        f"SEL={sel} A={a:02X} B={b:02X} "
        f"Expected={((expected >> 7) & 1)} "
        f"Got={int(dut.neg.value)}"
    )

    assert int(dut.agtb.value) == int(a > b), (
        f"SEL={sel} A={a:02X} B={b:02X} "
        f"Expected={int(expected > b)} "
        f"Got={int(dut.agtb.value)}"
    )

    assert int(dut.aeqb.value) == int(a == b), (
        f"SEL={sel} A={a:02X} B={b:02X} "
        f"Expected={int(expected == b)} "
        f"Got={int(dut.aeqb.value)}"
    )


@cocotb.test()
async def test(dut):

    for sel in range(8):

        if sel in (OP_NOT_A, OP_PASS_A):

            b = 0

            for a in range(256):

                dut.a.value = a
                dut.b.value = b
                dut.sel.value = sel

                await Timer(1, unit="ns")

                if sel == OP_NOT_A:
                    expected = (~a) & 0xFF
                else:
                    expected = a

                await check_outputs(dut, a, b, sel, expected, carry)

        elif sel == OP_PASS_B:

            a = 0

            for b in range(256):

                dut.a.value = a
                dut.b.value = b
                dut.sel.value = sel

                await Timer(1, unit="ns")

                expected = b

                await check_outputs(dut, a, b, sel, expected, carry)

        else:

            for a in range(256):
                for b in range(256):

                    dut.a.value = a
                    dut.b.value = b
                    dut.sel.value = sel

                    await Timer(1, unit="ns")

                    if sel == OP_ADD:
                        result = a + b
                        expected = result & 0xFF
                        carry = (result >> 8) & 1

                    elif sel == OP_SUB:
                        result = (a - b) & 0x1FF
                        expected = result & 0xFF
                        carry = (result >> 8) & 1

                    elif sel == OP_AND:
                        expected = a & b
                        carry = 0

                    elif sel == OP_OR:
                        expected = a | b
                        carry = 0

                    else:   # XOR
                        expected = a ^ b
                        carry = 0

                    await check_outputs(
                        dut,
                        a,
                        b,
                        sel,
                        expected,
                        carry
                    )
