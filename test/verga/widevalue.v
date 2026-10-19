module top;
  reg [64:0] value;
  reg [64:0] index;
  reg [7:0] data;

  initial begin
    value = 65'd0;
    if (value) $display("zero: FAIL");
    else $display("zero: PASS");
    value = 65'h10000000000000000;
    if (value) $display("high bit: PASS");
    else $display("high bit: FAIL");
    $display("decimal: %d", value);
    value = 65'd0;
    value[64] = 1'bx;
    $display("unknown: %d", value);
    value[64] = 1'bz;
    $display("high impedance: %d", value);
    data = 8'b10000000;
    index = 65'd7;
    $display("wide index: %b", data[index]);
  end
endmodule
