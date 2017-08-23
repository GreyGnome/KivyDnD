#    Copyright 2017 Michael Schwager
#    Copyright 2016, 2015, 2014, 2013, 2012 Pavel Kostelnik

#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.

# File: example_copy_draggable.py
#       Simple example of the DragNDropWidget Kivy library.
#       Expands on dndexample2.py. Additional features of the library:
#       * Copy the draggable widget, instead of removing it from the parent.
#       * Can drop onto the original's parent
#       * The parent has a drop_func defined

from __future__ import print_function

from kivy.app import App
from kivy.clock import Clock
from kivy.lang import Builder
from kivy.uix.label import Label

# Classes in the FloatLayout are defined in draggablestuff.py, included above.
kv = '''
FloatLayout:
    DragSourceBoxLayout:
        id: from_box
        canvas:
            Color:
                rgb: 1, 0.2, 0.2
            Rectangle:
                pos: self.pos
                size: self.size
        size_hint: 0.8, 0.25
        pos_hint: {'x': 0.1, 'y': 0.4}

        DraggableButton:
            text: 'Button 1'
            droppable_zone_objects: [upper_to_box, from_box]
            drop_ok_animation_time: 1.5
            drop_func: app.greet
            #drop_args: [ root, self ]
            failed_drop_func: app.oops
            #failed_drop_args: [ root, self ]
            remove_on_drag: False
            can_drop_into_parent: True

    DragDestinationLabel:
        id: upper_to_box
        text: 'drop here for some effect'
        canvas.before:
            Color:
                rgb: 0.4, 0.4, 1
            Rectangle:
                pos: self.pos
                size: self.size
        size_hint: 0.8, 0.2
        pos_hint: {'x': 0.1, 'y': 0.8}
        drop_func: self.greeter
'''

kv1 = '''
DialogLabel:
    rgba_list: (0.5, 0.5, 0.5, 1.0)
    canvas.before:
        Color:
            rgba: self.rgba_list
        Rectangle:
            pos: self.pos
            size: self.size
    size_hint: 0.4, 0.1
    pos_hint: {'x': 0.3, 'y': 0.65}
'''


class DialogLabel(Label):
    def __init__(self, *args, **kwargs):
        self.toggle_color = True
        self.i = 0
        super(DialogLabel, self).__init__(**kwargs)

    def flash(self):
        self.rgba_list_orig = self.rgba_list
        Clock.schedule_interval(self.cycle_color, 0.3)

    def cycle_color(self, dt):
        if self.i < 6:
            if self.toggle_color:
                # toggled color
                self.rgba_list = [0.8, 0.8, 0.0, 1.0]
                self.toggle_color = False
            else:
                # normal color
                self.rgba_list = self.rgba_list_orig
                self.toggle_color = True
            self.i += 1
        else:
            Clock.unschedule(self.cycle_color)
            self.i = 0
            self.toggle_color = True
            self.parent.remove_widget(self)


class dndapp0(App):
    def __init__(self, **kw):
        super(dndapp0, self).__init__(**kw)

    def build(self):
        return Builder.load_string(kv)

    def greet(self, arg1=None, arg2=None):
        '''
        
        :param arg1: the root window
        :param arg2: the widget that calls this method
        :return: 
        '''
        kv_root = arg1
        messagebox = Builder.load_string(kv1)
        messagebox.text = "Dragging done!!!"

        kv_root.parent.add_widget(messagebox)
        messagebox.flash()

    def oops(self, arg1=None, arg2=None):
        print("Self, arg1, arg2:", self, arg1, arg2)
        messagebox = Builder.load_string(kv1)
        messagebox.text = "Ooops! Can't drop there!"

        kv_root = arg1
        kv_root.parent.add_widget(messagebox)
        messagebox.flash()


if __name__ == '__main__':
    dndapp0().run()
