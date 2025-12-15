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

def idx_expr(array_info):
    return ", ".join([f"{a['idx_name']}_idx" for a in array_info])

def addr_expr(base, array_info):
    terms = [fmt_hex(base)]
    for a in array_info:
        if a["stride"] == 0:
            continue
        terms.append(f"({a['idx_name']}_idx) * {fmt_hex(a['stride'])}")
    return " + ".join(terms)

%>

% for block in blocks:
% if not block["array_info"]:
#define ${"_".join(block["name"] + ["base_addr"]).upper()} ${fmt_hex(block["addr"])}
% else:
#define ${"_".join(block["name"] + ["base_addr"]).upper()}(${idx_expr(block["array_info"])}) (${addr_expr(block["addr"], block["array_info"])} )
#define ${"_".join(block["name"] + ["num"]).upper()} ${fmt_hex(block["array_info"][-1]["dim"][-1])}
% endif
#define ${"_".join(block["name"] + ["size"]).upper()} ${fmt_hex(block["size"])}
% if "stride" in block:
#define ${"_".join(block["name"] + ["stride"]).upper()} ${fmt_hex(block["stride"])}
% endif
% if "total_size" in block:
#define ${"_".join(block["name"] + ["total_size"]).upper()} ${fmt_hex(block["total_size"])}
% endif

% endfor

% for reg in registers:
% if not reg["array_info"]:
#define ${"_".join(reg["name"] + ["base_addr"]).upper()} ${fmt_hex(reg["addr"])}
% else:
#define ${"_".join(reg["name"] + ["base_addr"]).upper()}(${idx_expr(reg["array_info"])}) (${addr_expr(reg["addr"], reg["array_info"])} )
#define ${"_".join(reg["name"] + ["num"]).upper()} ${fmt_hex(reg["array_info"][-1]["dim"][-1])}
% endif

% endfor

% for enum in enums:
% for field in enum["choices"]:
#define ${enum["name"]}__${field["name"]} ${field["value"]}
% endfor

% endfor

#endif /* ${top_name.upper() + "_H"} */
