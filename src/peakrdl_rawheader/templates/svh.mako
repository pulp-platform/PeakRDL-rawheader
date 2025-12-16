<%!
    from peakrdl_rawheader.utils import fmt_hex, fmt_addr_expr, fmt_idx_expr, fmt_license, clog2
%>
% if license_str is not None:
${fmt_license(license_str)}
% endif

`ifndef ${top_name.upper() + "_SVH"}
`define ${top_name.upper() + "_SVH"}

% for block in blocks:
% if not block["array_info"]:
`define ${"_".join(block["name"] + ["base_addr"]).upper()} ${fmt_hex(block["addr"], "svh")}
% else:
`define ${"_".join(block["name"] + ["base_addr"]).upper()}(${fmt_idx_expr(block["array_info"], "svh")}) (${fmt_addr_expr(block["addr"], block["array_info"], "svh")} )
`define ${"_".join(block["name"] + ["num"]).upper()} ${fmt_hex(block["array_info"][-1]["dim"][-1], "svh")}
% endif
`define ${"_".join(block["name"] + ["size"]).upper()} ${fmt_hex(block["size"], "svh")}
% if "stride" in block:
`define ${"_".join(block["name"] + ["stride"]).upper()} ${fmt_hex(block["stride"], "svh")}
% endif
% if "total_size" in block:
`define ${"_".join(block["name"] + ["total_size"]).upper()} ${fmt_hex(block["total_size"], "svh")}
% endif

% endfor

% for reg in registers:
% if not reg["array_info"]:
`define ${"_".join(reg["name"] + ["base_addr"]).upper()} ${fmt_hex(reg["addr"], "svh")}
% else:
`define ${"_".join(reg["name"] + ["base_addr"]).upper()}(${fmt_idx_expr(reg["array_info"], "svh")}) (${fmt_addr_expr(reg["addr"], reg["array_info"], "svh")} )
`define ${"_".join(reg["name"] + ["num"]).upper()} ${fmt_hex(reg["array_info"][-1]["dim"][-1], "svh")}
% endif

% endfor

% for enum in enums:
% for field in enum["choices"]:
`define ${enum["name"].upper()}__${field["name"]} ${field["value"]}
% endfor

% endfor

`endif /* ${top_name.upper() + "_SVH"} */
