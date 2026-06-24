`timescale 1ns/1ns

module testbench;

 parameter MSIZE = 256;
 parameter IWIDTH = 8;

 reg  [$clog2(MSIZE)-1:0] addr;
 wire [IWIDTH-1:0] out;

 ROM #(
     .IWIDTH(IWIDTH),
     .MSIZE(MSIZE)
 ) dut (
     .addr(addr),
     .out(out)
 );

  initial begin

    $monitor("t = %0t | addr=%d | out=%h", $time, addr, out);

    $dumpfile("Sim.vcd");
    $dumpvars(0, testbench);

    addr = 0;
    #10;

    addr = 1;
    #10;

    addr = 2;
    #10;

    addr = 3;
    #10;

    addr = 4;
    #10;

    addr = 5;
    #10;

    $display("Simulation Complete");
    $finish;

 end

endmodule
