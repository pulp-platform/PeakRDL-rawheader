% if license_str is not None:
% for line in license_str.strip().split('\n'):
// ${line}
% endfor

%endif
#ifndef ${top_name.upper() + "_H"}
#define ${top_name.upper() + "_H"}
<%
def fmt_hex(num):
    return f"0x{num:08X}"

def expr(base, params):
    terms = [fmt_hex(base)]
    for param in params:
        if param["stride"] == 0:
            continue
        terms.append(f"({param['name']}) * {fmt_hex(param['stride'])}")
    return " + ".join(terms)
%>

% if flat:
% for blk in blocks:
% for entry in blk:
#define ${entry["name"]} ${"0x{num:08X}".format(num = entry["num"])}
% endfor

% endfor
% else:
% for idx, blk in enumerate(blocks):
% for entry in blk:
#define ${entry["name"]} ${fmt_hex(entry["num"])}
% endfor
% if idx + 1 < len(blocks):

% endif
% endfor

% for reg in registers:
<% params = [p["name"] for p in reg["addr_params"]] %>
% if params:
#define ${reg["name"]}_REG_ADDR(${", ".join(params)}) (${expr(reg["addr_base"], reg["addr_params"])})
#define ${reg["name"]}_REG_OFFSET(${", ".join(params)}) (${expr(reg["offset_base"], reg["addr_params"][reg["reg_param_offset"]:])})
% else:
#define ${reg["name"]}_REG_ADDR ${fmt_hex(reg["addr_base"])}
#define ${reg["name"]}_REG_OFFSET ${fmt_hex(reg["offset_base"])}
% endif

% endfor
% endif
% for enum in enums:
% for field in enum["choices"]:
#define ${enum["name"]}__${field["name"]} ${field["value"]}
% endfor

% endfor

#endif /* ${top_name.upper() + "_H"} */
