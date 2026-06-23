`include "A_Register.v"

module testbench;

  reg [7:0] in;
  reg enable;
  reg load;
  reg rst;
  reg clk;
  wire [7:0] out;

  A_Register dut(
    .in(in),
    .enableA(enable),
    .loadA(load),
    .rst(rst),
    .clk(clk),
    .out(out)
  );

  initial clk = 0;
  always #5 clk = ~clk;

  initial begin

   $monitor("t = %0t | in = %b | load = %b | enable = %b | rst = %b | out = %b", $time, in, load, enable, rst, out);

   $dumpfile("Sim.vcd");
   $dumpvars(0, testbench);

  in     = 8'b00000000;
  load   = 0;
  enable = 0;
  rst    = 1;

  @(negedge clk);
  #1;
  rst = 0;

  @(negedge clk);
  #1;
  in     = 8'b11111111;
  load   = 1;
  enable = 0;

  @(negedge clk);
  #1;
  load   = 0;

  @(negedge clk);
  #1;
  enable = 1;

  @(negedge clk);
  #1;
  in     = 8'b10101010;
  load   = 1;
  enable = 0;

  @(negedge clk);
  #1;
  in     = 8'b10000001;
  load   = 1;
  enable = 1;

  @(posedge clk);
  #1;


   $display("Simulation Complete!");
   $finish;

  end

endmodule
