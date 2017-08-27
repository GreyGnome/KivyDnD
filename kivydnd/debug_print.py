from __future__ import print_function
import traceback
import sys

# There are two ways to use this: as a Singleton, all controlled by this global
# debug_flag. Or you can instantiate an object of class Debug, and print using the
# object's print method. The upside is that the latter can be controlled on a file-by-file
# basis.
debug_flag = False


def set_debug_flag(flag):
    global debug_flag
    debug_flag = flag


def debug_print(*args, **kwargs):
    if not debug_flag:
        return
    trace = traceback.extract_stack()
    # print (len(trace))
    this_entry=trace[len(trace)-2]
    basename = this_entry[0].split('/')
    basename = "%-10s" % basename[len(basename)-1]
    method = this_entry[2] + "()"
    method = "%-15s" % method
    print (basename + ":" + str(this_entry[1]), method, *args, **kwargs)


class Debug():
    """
    Instantiate this bad boy in your file, and you can turn it on and off as you
    wish in your file. Then you can print debug messages, like so:

    from debug_print import Debug
    debug = Debug(True)

    debug.print ("Here's a message")

    Output looks like this:

    dndwidgets.py:453 on_drag_finish() beginning, parent: <kivy.core.window.window_sdl2.WindowSDL object at 0x7f707ef0a2f0> copy? False
    dndwidgets.py:454 on_drag_finish() self: <draggablestuff.DraggableButton object at 0x7f707eec0d70> is_double_tap? False

    That is, it prints:

    filename:line_number method()  <your_text_here>
    """
    def __init__(self, debug_flag=False):
        self.debug_flag = debug_flag

    def print(self, *args, **kwargs):
        if not self.debug_flag:
            return
        trace = traceback.extract_stack()
        # print (len(trace))
        this_entry = trace[len(trace) - 2]
        basename = this_entry[0].split('/')
        basename = "%-10s" % basename[len(basename) - 1]
        method = this_entry[2] + "()"
        method = "%-15s" % method
        print(basename + ":" + str(this_entry[1]), method, *args, **kwargs)
