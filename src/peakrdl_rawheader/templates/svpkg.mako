% if license_str is not None:
% for line in license_str.strip().split('\n'):
// ${line}
% endfor

%endif
package ${top_name + "_addrmap_pkg"};
<%
def fmt_hex(num):
    return f"64'h{num:08X}"

def expr(base, params):
    terms = [fmt_hex(base)]
    for param in params:
        if param["stride"] == 0:
            continue
        terms.append(f"({param['name']}) * {fmt_hex(param['stride'])}")
    return " + ".join(terms)

def param_decl(params):
    return ", ".join(f\"input int unsigned {p['name']}\" for p in params)
%>

% if flat:
% for blk in blocks:
% for entry in blk:
localparam longint unsigned ${entry["name"]} = ${"64'h{num:08X}".format(num = entry["num"])};
% endfor

% endfor
% else:
% for idx, blk in enumerate(blocks):
% for entry in blk:
localparam longint unsigned ${entry["name"]} = ${fmt_hex(entry["num"])};
% endfor
% if idx + 1 < len(blocks):

% endif
% endfor

% for reg in registers:
<% params = reg["addr_params"] %>
% if params:
function automatic longint unsigned ${reg["name"]}_REG_ADDR(${param_decl(params)});
    return ${expr(reg["addr_base"], params)};
endfunction
function automatic longint unsigned ${reg["name"]}_REG_OFFSET(${param_decl(params)});
    return ${expr(reg["offset_base"], params[reg["reg_param_offset"]:])};
endfunction
% else:
localparam longint unsigned ${reg["name"]}_REG_ADDR = ${fmt_hex(reg["addr_base"])};
localparam longint unsigned ${reg["name"]}_REG_OFFSET = ${fmt_hex(reg["offset_base"])};
% endif

% endfor
% endif

endpackage;
