// Random Access Memory
module RAM #(
    parameter MSIZE = 256,
    parameter WIDTH = 8
) (
    input [WIDTH-1:0] in,
    input write,
    input clk,
    input [$clog2(MSIZE)-1:0] addr,
    output [WIDTH-1:0] out
);

reg [WIDTH-1:0] mem [MSIZE-1:0];

integer i;

initial begin
    for(i = 0; i < MSIZE; i = i + 1)
        mem[i] = {WIDTH{1'b0}};

    $readmemh("Data.hex", mem);
end

assign out = mem[addr];

always @(posedge clk) begin

    if (write)
        mem[addr] <= in;

end

endmodule
