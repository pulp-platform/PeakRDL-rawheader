<%!
    from peakrdl_rawheader.utils import fmt_hex, fmt_addr_expr, fmt_idx_expr, fmt_license, clog2
%>
% if license_str is not None:
${fmt_license(license_str)}
% endif

package ${top_name + "_addrmap_pkg"};

% for block in blocks:
% if not block["array_info"]:
localparam longint unsigned ${"_".join(block["name"] + ["base_addr"]).upper()} = ${fmt_hex(block["addr"], "svpkg")};
% else:
function automatic longint unsigned ${"_".join(block["name"] + ["base_addr"]).upper()}(${fmt_idx_expr(block["array_info"], "svpkg")});
    return ${fmt_addr_expr(block["addr"], block["array_info"], "svpkg")};
endfunction
localparam longint unsigned ${"_".join(block["name"] + ["num"]).upper()} = ${fmt_hex(block["array_info"][-1]["dim"][-1], "svpkg")};
% endif
localparam longint unsigned ${"_".join(block["name"] + ["size"]).upper()} = ${fmt_hex(block["size"], "svpkg")};
% if "stride" in block:
localparam longint unsigned ${"_".join(block["name"] + ["stride"]).upper()} = ${fmt_hex(block["stride"], "svpkg")};
% endif
% if "total_size" in block:
localparam longint unsigned ${"_".join(block["name"] + ["total_size"]).upper()} = ${fmt_hex(block["total_size"], "svpkg")};
% endif

% endfor

% for reg in registers:
% if not reg["array_info"]:
localparam longint unsigned ${"_".join(reg["name"] + ["base_addr"]).upper()} = ${fmt_hex(reg["addr"], "svpkg")};
% else:
function automatic longint unsigned ${"_".join(reg["name"] + ["base_addr"]).upper()}(${fmt_idx_expr(reg["array_info"], "svpkg")});
    return ${fmt_addr_expr(reg["addr"], reg["array_info"], "svpkg")};
endfunction
localparam longint unsigned ${"_".join(reg["name"] + ["num"]).upper()} = ${fmt_hex(reg["array_info"][-1]["dim"][-1], "svpkg")};
% endif
% endfor

% for enum in enums:
<% enum_width = clog2(len(enum["choices"])) %>
typedef enum logic [${enum_width-1}:0] {
% for field in enum["choices"]:
    ${field["name"].upper()} = ${enum_width}'d${field["value"]}${"," if not loop.last else ""}
% endfor
} ${enum["name"]}_e;
% endfor


endpackage;
