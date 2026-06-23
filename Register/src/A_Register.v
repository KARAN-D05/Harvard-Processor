module A_Register #(
    parameter WIDTH = 8 
)(
    input [WIDTH-1:0] in,
    input enableA,
    input loadA,
    input rst,
    input clk,
    output [WIDTH-1:0] out
);

   reg [WIDTH-1:0] val;

  always@(posedge clk or posedge rst) begin
    
    if(rst) begin
        val <= 8'b0000000;
    end else if (loadA) begin
        val <= in;
    end

  end

  assign out = enableA ? val : {{(WIDTH){1'bz}}};

endmodule
