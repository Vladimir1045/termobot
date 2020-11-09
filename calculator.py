#!/usr/bin/python3
# -*- coding: utf-8 -*-

def parse_token(ls):
    b = 0
    e = 0  # Begin/End
    r = []  # return
    while b < len(ls):
        e = b + 1
        # print("%d:%d=%s" % (b,e,ls[b:e]))
        if ls[b:e].isdigit():
            # парсим число
            while ls[b:e].isdigit():
                if e >= len(ls):
                    break
                e += 1
            else:
                e -= 1
        # print ("token [%d:%d] %s" % (b,e,ls[b:e]))
        r.append(ls[b:e])
        b = e
    # print ("res %s" % r)
    return r


op = {
    '+': {'pri': 5, 'func': lambda a, b: a + b},
    '-': {'pri': 5, 'func': lambda a, b: a - b},
    '*': {'pri': 6, 'func': lambda a, b: a * b},
    '/': {'pri': 6, 'func': lambda a, b: a / b},
    '(': {'pri': 0},
    ')': {'pri': 0}
}


def transform(inp):
    op_stack = []
    out = []
    for token in inp:
        print("Token: '%s'" % token)
        if token.isdigit():
            out.append(token)
            print("Digit: %s" % out)
            continue
        if token in op:
            if len(op_stack) == 0:
                op_stack.append(token)
                print("Opstack 0(: %s" % op_stack)
                continue
            elif token not in ['(', ')']:
                if op[token]['pri'] <= op[op_stack[-1]]['pri']:
                    if len(op_stack) > 0:
                        op2 = op_stack.pop()
                        out.append(op2)
                        print("Op: %s" % out)
                op_stack.append(token)
                print("Opstack pri: %s" % op_stack)
                continue
            if token == '(':
                op_stack.append(token)
                print("Opstack (: %s" % op_stack)
            elif token == ')':
                while op_stack[-1] != '(':
                    op2 = op_stack.pop()
                    out.append(op2)
                    print(f"(): {out} {op_stack}")
                print("pop (")
                op_stack.pop()
            else:
                print("Syntax error with '%s'" % token)
        else:
            print("Invalid op '%s'" % token)
    for token in op_stack[::-1]:
        if token == '(':
            print("Unbalanced (")
            pass
        else:
            out.append(token)
            print("To evaluate: %s" % out)
    return out


def result(formula):
    stack = []
    for t in formula:
        if t in op and t not in ['(', ')']:
            # Это операция
            op2 = float(stack.pop())
            op1 = float(stack.pop())
            print(f'{op1} {t} {op2}')
            stack.append(op[t]['func'](op1, op2))
        else:
            if t.isdigit:
                print(f'push {t}')
                stack.append(t)
            else:
                # Ошибка
                print(f"Непонятный символ {t}")
    return stack.pop()


try:
    while True:
        rc = transform(parse_token(input("Что сосчитать? ")))
        print(rc)
        print(f"Результат = {result(rc)}")
except (KeyboardInterrupt, EOFError):
    print("всего хорошего!")
