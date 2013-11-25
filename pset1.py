#!/usr/bin/env python
# Simple debugger
# See instructions around line 34
import sys
import readline

# Our buggy program
def remove_html_markup(s):
    tag   = False
    quote = False
    out   = ""

    for c in s:
        if c == '<' and not quote:
            tag = True
        elif c == '>' and not quote:
            tag = False
        elif c == '"' or c == "'" and tag:
            quote = not quote
        elif not tag:
            out = out + c
    return out
    
# main program that runs the buggy program
def main():
    print remove_html_markup('xyz')
    print remove_html_markup('"<b>foo</b>"')
    print remove_html_markup("'<b>foo</b>'")

# globals
breakpoints = {9: True}
stepping = False

"""
Our debug function
Improve and expand this function to accept 
a breakpoint command 'b <line>'.
Add the line number to the breakpoints dictionary
or print 'You must supply a line number' 
if 'b' is not followed by a line number.
"""
def debug(command, my_locals):
    global stepping
    global breakpoints
    
    if command.find(' ') > 0:
        arg = command.split(' ')[1]
    else:
        arg = None

    if command.startswith('s'):     # step
        stepping = True
        return True
    elif command.startswith('c'):   # continue
        stepping = False
        return True
    elif command.startswith('p'):    # print
        if arg:
            if my_locals.__contains__(arg):
                print arg, "=", repr(my_locals[arg])
            else:
                print "No such variable:", arg
        else:
            print my_locals
    elif command.startswith('b'):    # breakpoint
        # YOUR CODE HERE
        if not arg:
            print "You must supply a line number"
        else:
            breakpoints[arg] = True
        
    elif command.startswith('q'):   # quit
        sys.exit(0)
    else:
        print "No such command", repr(command)
        
    return False

commands = ["p", "s", "p tag", "p foo", "q"] # p foo should fail

def input_command():
    #command = raw_input("(my-spyder) ")
    global commands
    command = commands.pop(0)
    return command

def traceit(frame, event, trace_arg):
    global stepping

    if event == 'line':
        if stepping or breakpoints.has_key(frame.f_lineno):
            resume = False
            while not resume:
                print event, frame.f_lineno, frame.f_code.co_name, frame.f_locals
                command = input_command()
                resume = debug(command, frame.f_locals)
    return traceit

# Using the tracer
sys.settrace(traceit)
main()
sys.settrace(None)
