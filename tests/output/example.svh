

`ifndef TOP_SVH
`define TOP_SVH

`define TOP_BASE_ADDR 64'h0
`define TOP_SIZE 64'h8


`define TOP_STATUS_BASE_ADDR(status_idx) (64'h0 + (status_idx * 64'h4) )
`define TOP_STATUS_NUM 64'h2


`define STATE__IDLE 0
`define STATE__BUSY 1


`endif /* TOP_SVH */
