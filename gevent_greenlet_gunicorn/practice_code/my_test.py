from greenlet import greenlet, getcurrent

def read_one_char():
    return main_greenlet.switch('switch to input one char')

def process_one_line(input):
    input = input.strip()
    print(f"<<<< get {input} transform to {input.upper()}")

def input_one_char(one_char):
    process_greenlet.switch(one_char)

def process():
    while True:
        input = ''
        while not input.endswith("\n"):
            input += read_one_char()

        if input == 'quit\n':
            print(">>> terminate!")
            break
        
        process_one_line(input)

def inpute_some_lines():
    for i in "hello\n":
        input_one_char(i)

    for i in "world\n":
        input_one_char(i)
    
    for i in "quit\n":
        input_one_char(i)

process_greenlet = greenlet(process)
main_greenlet = getcurrent()
process_greenlet.switch()

if __name__ == '__main__':
    inpute_some_lines()

