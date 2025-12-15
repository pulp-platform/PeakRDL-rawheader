% if license_str is not None:
% for line in license_str.strip().split('\n'):
// ${line}
% endfor

%endif
package ${top_name + "_addrmap_pkg"};
<%
def fmt_hex(num):
    return f"64'h{num:08X}"

def idx_expr(array_info):
    return ", ".join([f"input int unsigned {a['idx_name']}_idx" for a in array_info])

def addr_expr(base, array_info):
    terms = [fmt_hex(base)]
    for a in array_info:
        if a["stride"] == 0:
            continue
        terms.append(f"{a['idx_name']}_idx * {fmt_hex(a['stride'])}")
    return " + ".join(terms)

def clog2(x):
    return (x - 1).bit_length()
%>

% for block in blocks:
% if not block["array_info"]:
localparam longint unsigned ${"_".join(block["name"] + ["base_addr"]).upper()} = ${fmt_hex(block["addr"])};
% else:
function automatic longint unsigned ${"_".join(block["name"] + ["base_addr"]).upper()}(${idx_expr(block["array_info"])});
    return ${addr_expr(block["addr"], block["array_info"])};
endfunction
% endif
localparam longint unsigned ${"_".join(block["name"] + ["size"]).upper()} = ${fmt_hex(block["size"])};
% if "stride" in block:
localparam longint unsigned ${"_".join(block["name"] + ["stride"]).upper()} = ${fmt_hex(block["stride"])};
% endif
% if "total_size" in block:
localparam longint unsigned ${"_".join(block["name"] + ["total_size"]).upper()} = ${fmt_hex(block["total_size"])};
% endif

% endfor

% for reg in registers:
% if not reg["array_info"]:
localparam longint unsigned ${"_".join(reg["name"] + ["base_addr"]).upper()} = ${fmt_hex(reg["addr"])};
% else:
function automatic longint unsigned ${"_".join(reg["name"] + ["base_addr"]).upper()}(${idx_expr(reg["array_info"])});
    return ${addr_expr(reg["addr"], reg["array_info"])};
endfunction
% endif
localparam longint unsigned ${"_".join(reg["name"] + ["offset"]).upper()} = ${fmt_hex(reg["offset"])};
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
