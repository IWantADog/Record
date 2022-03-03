from greenlet import greenlet


def echo_user_input(user_input):
    print('    <<< ' + user_input.strip())
    return user_input

def process_commands():
    print("start process commands")
    while True:
        line = ''
        while not line.endswith('\n'):
            line += read_next_char()
        echo_user_input(line)
        if line == 'quit\n':
            print("Are you sure?")
            if echo_user_input(read_next_char()) != 'y':
                continue    # ignore the command
            print("(Exiting loop.)")
            break # stop the command loop
        process_command(line)

def process_command(line):
    print(f"(Processing command {line.strip()})")

def event_keydown(key):
    g_processor.switch(key)

def read_next_char():
    next_char = main_greenlet.switch("blocking in read_next_char")
    return next_char


def gui_mainloop():
    for c in 'hello\n':
        event_keydown(c)

    for c in 'quit\n':
        event_keydown(c)
    event_keydown("y")

g_processor = greenlet(process_commands)
main_greenlet = greenlet.getcurrent()
print("*" * 5)
g_processor.switch()
print("*" * 5)

if __name__ == '__main__':
    gui_mainloop()

    


