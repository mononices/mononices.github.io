"""Builds the site: runs site.bf with the current year as input and writes every file it prints.

site.bf prints each file as byte 28 (file separator), its path, a newline and its contents.
"""
import datetime
import os
import sys


def run(program, data):
    """Runs a Brainfuck program on an 8-bit tape and returns its output, end of input reads as 0."""
    code = [c for c in program if c in '+-<>[].,']
    jumps, stack = {}, []
    for i, c in enumerate(code):
        if c == '[':
            stack.append(i)
        elif c == ']':
            j = stack.pop()
            jumps[i], jumps[j] = j, i

    tape, ptr, read, out = bytearray(65536), 0, 0, bytearray()
    pc = 0
    while pc < len(code):
        c = code[pc]
        if c == '+':
            tape[ptr] = (tape[ptr] + 1) % 256
        elif c == '-':
            tape[ptr] = (tape[ptr] - 1) % 256
        elif c == '>':
            ptr += 1
        elif c == '<':
            ptr -= 1
        elif c == '.':
            out.append(tape[ptr])
        elif c == ',':
            tape[ptr] = data[read] if read < len(data) else 0
            read += 1
        elif c == '[' and not tape[ptr]:
            pc = jumps[pc]
        elif c == ']' and tape[ptr]:
            pc = jumps[pc]
        pc += 1
    return bytes(out)


def main(dest='_site'):
    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'site.bf')) as f:
        program = f.read()
    year = str(datetime.date.today().year).encode()
    for chunk in run(program, year).split(b'\x1c')[1:]:
        path, contents = chunk.split(b'\n', 1)
        target = os.path.join(dest, path.decode())
        os.makedirs(os.path.dirname(target), exist_ok=True)
        with open(target, 'wb') as f:
            f.write(contents)


if __name__ == '__main__':
    main(*sys.argv[1:])
