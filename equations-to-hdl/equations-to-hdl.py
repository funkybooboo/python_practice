import re

OP_MAP = {
    '+': 'adder',
    '-': 'subtractor',
    '*': 'multiplier',
    '/': 'divider',
    '&': 'and_gate',
    '|': 'or_gate',
    '^': 'xor_gate',
}

PRECEDENCE = {
    '|': 1,
    '^': 2,
    '&': 3,
    '+': 4,
    '-': 4,
    '*': 5,
    '/': 5,
}

class ASTNode:
    def __init__(self, typ, value=None, left=None, right=None):
        self.typ = typ
        self.value = value
        self.left = left
        self.right = right

def tokenize(expr):
    scanner = re.Scanner([
        (r'[a-zA-Z_]\w*', lambda scanner, token: ('VAR', token)),
        (r'[+\-*/&|^]', lambda scanner, token: ('OP', token)),
        (r'\(', lambda scanner, token: ('LPAREN', token)),
        (r'\)', lambda scanner, token: ('RPAREN', token)),
        (r'\s+', None),
    ])
    tokens, remainder = scanner.scan(expr)
    if remainder:
        raise ValueError(f"Invalid characters: {remainder}")
    return tokens

def parse_expression(tokens):
    def parse_atom(pos):
        if pos >= len(tokens):
            raise ValueError("Unexpected end of input")
        typ, val = tokens[pos]
        if typ == 'VAR':
            return ASTNode('var', val), pos + 1
        elif typ == 'LPAREN':
            node, pos = parse_expr(pos + 1)
            if pos >= len(tokens) or tokens[pos][0] != 'RPAREN':
                raise ValueError("Missing closing parenthesis")
            return node, pos + 1
        else:
            raise ValueError(f"Unexpected token: {val}")

    def parse_expr(pos, min_prec=0):
        left, pos = parse_atom(pos)
        while pos < len(tokens):
            typ, val = tokens[pos]
            if typ != 'OP' or PRECEDENCE.get(val, 0) < min_prec:
                break
            op = val
            prec = PRECEDENCE[op]
            pos += 1
            right, pos = parse_expr(pos, prec + 1)
            left = ASTNode('op', op, left, right)
        return left, pos

    node, pos = parse_expr(0)
    if pos != len(tokens):
        raise ValueError("Unexpected extra tokens")
    return node

def extract_vars(node, vars_set):
    if node.typ == 'var':
        vars_set.add(node.value)
    else:
        extract_vars(node.left, vars_set)
        extract_vars(node.right, vars_set)

def generate_verilog_hdl(lhs_var, rhs_ast):
    wires = []
    components = []
    comp_counters = {mod: 0 for mod in OP_MAP.values()}
    wire_count = 0

    rhs_vars = set()
    extract_vars(rhs_ast, rhs_vars)

    inputs = sorted(rhs_vars - {lhs_var})
    outputs = [lhs_var]

    def gen_node(node):
        nonlocal wire_count
        if node.typ == 'var':
            return node.value
        else:
            left_sig = gen_node(node.left)
            right_sig = gen_node(node.right)
            wire_count += 1
            wire_name = f"w{wire_count}"
            wires.append(wire_name)

            mod_name = OP_MAP[node.value]
            comp_counters[mod_name] += 1
            comp_inst = f"{mod_name} {mod_name}{comp_counters[mod_name]} (\n" \
                        f"    .in1({left_sig}),\n" \
                        f"    .in2({right_sig}),\n" \
                        f"    .out({wire_name})\n);"
            components.append(comp_inst)
            return wire_name

    def gen_node_top(node):
        nonlocal wire_count
        if node.typ == 'var':
            return
        left_sig = gen_node(node.left)
        right_sig = gen_node(node.right)
        mod_name = OP_MAP[node.value]
        comp_counters[mod_name] += 1
        comp_inst = f"{mod_name} {mod_name}{comp_counters[mod_name]} (\n" \
                    f"    .in1({left_sig}),\n" \
                    f"    .in2({right_sig}),\n" \
                    f"    .out({lhs_var})\n);"
        components.append(comp_inst)

    gen_node_top(rhs_ast)

    lines = []
    for inp in inputs:
        lines.append(f"input wire {inp};")
    for outp in outputs:
        lines.append(f"output wire {outp};")
    if wires:
        lines.append("")
        for w in wires:
            lines.append(f"wire {w};")
    lines.append("")
    for comp in components:
        lines.append(comp)
        lines.append("")

    return "\n".join(lines)

def is_single_var(s):
    return re.fullmatch(r'[a-zA-Z_]\w*', s) is not None

def main():
    equation = input("Enter equation (e.g. a + b = c): ").strip()
    if '=' not in equation:
        print("Equation must contain '='")
        return

    lhs, rhs = equation.split('=', 1)
    lhs = lhs.strip()
    rhs = rhs.strip()

    if is_single_var(lhs):
        # LHS is output variable, RHS is expression
        output_var = lhs
        expr_str = rhs
    elif is_single_var(rhs):
        # RHS is output variable, LHS is expression
        output_var = rhs
        expr_str = lhs
    else:
        print("Error: One side of the equation must be a single variable.")
        return

    try:
        tokens = tokenize(expr_str)
        ast = parse_expression(tokens)
    except Exception as e:
        print(f"Parse error: {e}")
        return

    hdl = generate_verilog_hdl(output_var, ast)
    print("\nGenerated Verilog HDL:\n")
    print(hdl)

if __name__ == '__main__':
    main()
