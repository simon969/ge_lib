from __future__ import annotations

import re
from pathlib import Path

ROOT = Path('/home/simon/Downloads/GEO_Addin_Source_2018-07-23/ConvertToPython')
OUT = Path('/home/simon/Apps/ge_lib/src/ge_lib/vba_converted')
OUT.mkdir(parents=True, exist_ok=True)


def split_args(args_text: str):
    if not args_text.strip():
        return []
    result = []
    current = []
    depth = 0
    for ch in args_text:
        if ch in '([':
            depth += 1
        elif ch in ')]':
            depth = max(0, depth - 1)
        if ch == ',' and depth == 0:
            result.append(''.join(current).strip())
            current = []
            continue
        current.append(ch)
    if current:
        result.append(''.join(current).strip())
    return result


def clean_param(param: str):
    p = param.strip()
    if not p:
        return ''
    p = p.replace('Optional ', '')
    p = p.replace('ByVal ', '')
    if '=' in p:
        p = p.split('=', 1)[0].strip()
    if ' As ' in p:
        name, typ = re.split(r'\s+As\s+', p, flags=re.I)
        return f'{name}: {typ.lower() if typ.lower() in {"double","float","integer","int","string","str","boolean","bool"} else "float"}'
    if ':' in p:
        name, typ = p.split(':', 1)
        return f'{name.strip()}: {typ.strip()}'
    return f'{p}: float'


def clean_body(body: str):
    body = body.replace('\r', '\n')
    lines = body.splitlines()
    out = []
    for raw in lines:
        line = raw.strip()
        if not line:
            continue
        # Remove whole-line comments
        if line.startswith("'"):
            continue
        if line.startswith('End '):
            continue
        if line.startswith('Exit '):
            continue
        if line.startswith('ReDim '):
            continue
        if line.startswith('Debug.Print'):
            continue
        if line.startswith('Call '):
            line = line[5:].strip() + '()'
            out.append(line)
            continue
        if line.startswith('Private Type') or line.startswith('Public Type'):
            continue
        if line.startswith('End Type'):
            continue
        if line.startswith('If ') and ' Then' in line:
            line = line.replace('If ', 'if ', 1)
            line = line.replace(' Then', ':')
        elif line.startswith('ElseIf '):
            line = line.replace('ElseIf ', 'elif ', 1)
            line = line.replace(' Then', ':')
        elif line.startswith('Else'):
            line = 'else:'
        elif line.startswith('Do While '):
            line = 'while ' + line[len('Do While '):].strip() + ':'
        elif line.startswith('Loop'):
            continue
        elif line.startswith('For ') and ' To ' in line and ' Next' not in line:
            # handle typical VBA loops, best-effort
            m = re.match(r'For\s+(\w+)\s*=\s*(.+?)\s+To\s+(.+)', line, re.I)
            if m:
                loop_var, start, end = m.groups()
                line = f'for {loop_var} in range({start}, {end} + 1):'
        elif line.startswith('Next'):
            continue
        if line.startswith('If ') and ' Then' not in line and line.endswith(':') is False and 'if ' not in line:
            line = 'if ' + line[3:]
        if ' = ' in line and not line.startswith(('if ', 'elif ', 'for ', 'while ', 'return ', 'else:')):
            lhs, rhs = line.split(' = ', 1)
            lhs = lhs.strip()
            rhs = rhs.strip()
            if lhs.startswith('m_'):
                out.append(f'self.{lhs} = {rhs}')
            else:
                out.append(f'{lhs} = {rhs}')
            continue
        if line.startswith('return ') or line.startswith('Return '):
            out.append(line)
            continue
        if line.startswith('calc_') and re.match(r'^calc_[A-Za-z0-9_]+\s*=', line):
            lhs, rhs = re.split(r'\s*=', line, 1)
            out.append(f'return {rhs.strip()}')
            continue
        if re.match(r'^[A-Za-z_][A-Za-z0-9_]*\s*=', line):
            lhs, rhs = re.split(r'\s*=', line, 1)
            if lhs.startswith('m_') or lhs.startswith('const_'):
                out.append(f'self.{lhs} = {rhs}')
            else:
                out.append(f'{lhs} = {rhs}')
            continue
        # Convert function assignments like `m_nq = Exp(...)`
        if re.match(r'^[A-Za-z_][A-Za-z0-9_]*\s*\+=', line):
            lhs, rhs = re.split(r'\s*\+=\s*', line, 1)
            out.append(f'{lhs} = {lhs} + {rhs}')
            continue
        # Convert common VBA math functions to Python equivalents
        for old, new in [
            ('Sin(', 'math.sin('), ('Cos(', 'math.cos('), ('Tan(', 'math.tan('),
            ('Exp(', 'math.exp('), ('Log(', 'math.log('), ('Sqr(', 'math.sqrt('),
            ('Abs(', 'abs('), ('Atn(', 'math.atan('), ('Atn2(', 'math.atan2('),
        ]:
            line = line.replace(old, new)
        # Replace power operator
        line = line.replace('^', '**')
        # Replace & in conditions
        if line.startswith(('if ', 'elif ')) and '&' in line:
            line = line.replace('&', ' and ')
        if line.startswith(('if ', 'elif ')) and ' = ' in line:
            line = line.replace(' = ', ' == ', 1)
        # Replace assignment forms to `return` for function name
        m_ret = re.match(r'^(\w+)\s*=\s*(.+)$', line)
        if m_ret and m_ret.group(1).startswith('calc_'):
            out.append(f'return {m_ret.group(2)}')
            continue
        # Replace leading self references if accidentally there
        line = line.replace('self.self.', 'self.')
        out.append(line)
    return '\n'.join(out)


def convert_file(path: Path):
    text = path.read_text(errors='ignore')
    class_match = re.search(r'Attribute VB_Name = "([^"]+)"', text)
    if not class_match:
        return None
    cls_name = class_match.group(1)
    # Collect fields from Private/Public declarations
    fields = []
    for match in re.finditer(r'(?:Private|Public)\s+(?:m_)?([A-Za-z_][A-Za-z0-9_]*)\s+As\s+(\w+)', text, re.I):
        name = match.group(1)
        if name.startswith('Const'):
            continue
        # ignore temporary locals with lower-case names or names not starting with m_ or common class state names.
        if name.startswith(('m_',)):
            fields.append(f'    {name}: float = 0.0')
        elif name not in {'const_PI'}:
            fields.append(f'    {name}: float = 0.0')
    # Unique ordering preserved
    seen = set()
    unique_fields = []
    for f in fields:
        if f not in seen:
            unique_fields.append(f)
            seen.add(f)
    if not unique_fields:
        unique_fields = ['    pass']

    # collect constants
    consts = []
    for match in re.finditer(r'Private\s+Const\s+(const_[A-Za-z0-9_]*)\s*=\s*([^\n]+)', text, re.I):
        consts.append(f'{match.group(1)} = {match.group(2).strip()}')
    for match in re.finditer(r'Public\s+Const\s+(const_[A-Za-z0-9_]*)\s*=\s*([^\n]+)', text, re.I):
        consts.append(f'{match.group(1)} = {match.group(2).strip()}')

    methods = []
    func_pattern = re.compile(r'(?:Public|Private)\s+(?:Function|Sub)\s+(\w+)\s*\((.*?)\)\s*(?:As\s+\w+)?\s*\n(.*?)(?=\n(?:Public|Private)\s+(?:Function|Sub)|\nEnd\s+(?:Function|Sub))', re.S | re.I)
    for m in func_pattern.finditer(text):
        name, args, body = m.groups()
        params = [clean_param(a) for a in split_args(args or '') if a.strip()]
        # skip weird signatures using no parameters
        sig = ', '.join(params) if params else ''
        clean = clean_body(body)
        indent = re.sub(r'^(?!\s*$)', '    ', clean, flags=re.M)
        methods.append(f'\n    def {name}(self, {sig}) -> float:\n{indent}')

    # Some files have no methods or methods with parameters that got omitted due patterns; still create placeholder methods from body-only regex.
    class_lines = [
        'from dataclasses import dataclass',
        'import math',
        '',
        '',
        '@dataclass',
        f'class {cls_name}:',
        *unique_fields,
    ]
    for c in consts:
        class_lines.append(f'    {c}')
    for method in methods:
        class_lines.append(method)
    if not methods:
        class_lines.append('    pass')

    # sanitize obvious invalid output
    result = '\n'.join(class_lines) + '\n'
    result = result.replace('math.sin(2 * alpha_rad) / 2', 'math.sin(2 * alpha_rad) / 2')
    result = result.replace('if (', 'if (')
    result = re.sub(r'\n\s*def \w+\(self, \) -> float:\n\s*', '\n', result)
    result = result.replace('self.self.', 'self.')
    result = result.replace('===', '==')
    result = result.replace(' = self.m_', ' = self.m_')
    result = result.replace('``', '')
    result = re.sub(r'\n{3,}', '\n\n', result)
    return result


for cls_file in sorted(ROOT.glob('*.cls')):
    converted = convert_file(cls_file)
    if converted is None:
        continue
    out_path = OUT / (cls_file.name.replace('.cls', '.py'))
    out_path.write_text(converted)
    print(f'Wrote {out_path.name}')

# package marker
(OUT / '__init__.py').write_text('"""Converted VBA helper classes from the GEO Addin source."""\n')
