`timescale 1ns/1ns

module testbench;

  parameter STATES = 8;

  reg rst;
  reg clear;
  reg clk;

  wire [$clog2(STATES)-1:0] out;

  TC #(
    .STATES(STATES)
  ) dut (
    .rst(rst),
    .clear(clear),
    .clk(clk),
    .out(out)
  );

  initial clk = 0;
  always #5 clk = ~clk;

  initial begin

    $monitor(
      "t = %0t | rst = %b | clear = %b | out = %0d (%b)",
      $time, rst, clear, out, out
    );

    $dumpfile("Sim.vcd");
    $dumpvars(0, testbench);

    rst   = 1;
    clear = 0;

    // Release global reset
    @(negedge clk);
    #1;
    rst = 0;

    // Count: 0 -> 1 -> 2 -> 3 -> 4
    repeat (5) begin
      @(posedge clk);
      #1;
    end

    // Instruction finished -> Clear back to T0
    @(negedge clk);
    #1;
    clear = 1;

    @(posedge clk);
    #1;

    @(negedge clk);
    #1;
    clear = 0;

    // Count again
    repeat (4) begin
      @(posedge clk);
      #1;
    end

    // Count through wrap-around
    repeat (5) begin
      @(posedge clk);
      #1;
    end

    // Another instruction complete
    @(negedge clk);
    #1;
    clear = 1;

    @(posedge clk);
    #1;

    @(negedge clk);
    #1;
    clear = 0;

    // Count a few cycles
    repeat (3) begin
      @(posedge clk);
      #1;
    end

    // Global reset while running
    @(negedge clk);
    #1;
    rst = 1;

    @(posedge clk);
    #1;

    @(negedge clk);
    #1;
    rst = 0;

    // Verify counting restarts from T0
    repeat (4) begin
      @(posedge clk);
      #1;
    end

    $display("Simulation Complete");
    $finish;

  end

endmodule
