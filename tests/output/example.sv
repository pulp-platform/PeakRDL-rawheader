

package top_addrmap_pkg;

localparam longint unsigned TOP_BASE_ADDR = 64'h0;
localparam longint unsigned TOP_SIZE = 64'h8;


function automatic longint unsigned TOP_STATUS_BASE_ADDR(input int unsigned status_idx);
    return 64'h0 + (status_idx * 64'h4);
endfunction
localparam longint unsigned TOP_STATUS_NUM = 64'h2;


typedef enum logic [0:0] {
    IDLE = 1'd0,
    BUSY = 1'd1
} state_e;


endpackage;
