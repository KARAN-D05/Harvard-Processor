// T-State Counter
module TC #(
    parameter STATES = 8
) (
    input clear,
    input clk,
    input rst,
    output reg [$clog2(STATES)-1:0] out
);

  always @(posedge clk or posedge rst) begin

    if (rst) begin
        out <= {$clog2(STATES){1'b0}};
    end else if (clear) begin 
        out <= {$clog2(STATES){1'b0}};
    end else begin
        out <= out + 1;
    end

  end

endmodule
