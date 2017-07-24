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

# This example is used to test widgets in a relative layout.
# The Button being dragged will generate a kind of dialog box when it's dropped.
# That box is created from the app object.
# The destination widgets' text changes upon successful drop. That text is maintained
# in the destination widgets.

# File: app_relative_layout.py
from __future__ import print_function

from kivy.app import App
from kivy.lang import Builder
import relative_stuff
from kivy.clock import Clock
from kivy.uix.label import Label
from kivy.factory import Factory
from kivy.properties import NumericProperty, ListProperty


# Classes in the FloatLayout are defined in DraggableButton.py, included above.
kv = '''
<DragDestinationLabel>:
    id: drag_destination_label
    canvas.before:
        Color:
            rgb: 0.8, 0.8, 0.2
        Rectangle:
            pos: self.pos
            size: self.size
    size_hint: 0.33, 0.4
    pos_hint: {'x': 0.1, 'y': 0.3}

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
        pos_hint: {'x': 0.1, 'y': 0.25}

        DraggableButton:
            id: draggable_button
            text: 'Button 1'
            droppable_zone_objects: [left_label, relative_left_label, relative_right_label, from_box]
            drop_ok_animation_time: 1.5
            drop_func: app.greet
            drop_args: [ root ]
            failed_drop_func: self.oops
            failed_drop_args: [ root, app ]
            remove_on_drag: False
            can_drop_into_parent: True

    DragDestinationBoxLayout:
        id: upper_box
        size_hint: 0.8, 0.2
        pos_hint: {'x': 0.1, 'y': 0.65}
        canvas.before:
            Color:
                rgb: 0.2, 0.2, 0.2
            Rectangle:
                pos: self.pos
                size: self.size
        DragDestinationLabel:
            id: left_label
            text: 'Destination on the Left'
            pos_hint: {'x': 0.1, 'y': 0.3}
            size_hint: 0.33, 0.4 # The x-coordinate dictates how wide the layout's box will be
                                 # (the label fills the entire box)
            drop_func: self.greeter
            canvas.before:
                Color:
                    rgb: 0.2, 0.2, 0.8
                Rectangle:
                    pos: self.pos
                    size: self.size
        DragDestinationRelativeLayout:
            id: right_relative_layout
            size_hint: 0.67, 1.0
            canvas.before:
                Color:
                    rgba: 0.7, 0.7, 0.0, 1.0
                Rectangle:
                    pos: self.pos
                    size: self.size
            DragDestinationLabel:
                id: relative_left_label
                text: "Destination:\\nRelative, Left"
                pos_hint: {'x': 0.11, 'y': 0.3}
            DragDestinationLabel:
                id: relative_right_label
                text: "Destination:\\nRelative, Right"
                pos_hint: {'x': 0.55, 'y': 0.3}
'''

kv_msgbox = '''
DialogLabel:
    rgba_list: (0.5, 0.5, 0.5, 1.0)
    canvas.before:
        Color:
            rgba: self.rgba_list
        Rectangle:
            pos: self.pos
            size: self.size
    size_hint: 0.4, 0.1
    pos_hint: {'x': 0.3, 'y': 0.55}
'''


class app_relative_layout(App):
    def __init__(self, **kw):
        super(app_relative_layout, self).__init__(**kw)

    def build(self):
        return Builder.load_string(kv)

    def greet(self, calling_widget, kv_root=None):
        '''

        :param calling_widget: the widget that calls this method. It was the one that was
        dragged-and-dropped
        :param kv_root: the root window from the Kivy language.
        :return:
        '''
        print ("app.greet()... calling_widget:", calling_widget,
               "======== SENDS THE MESSAGE ========== double tap:",
               calling_widget.is_double_tap, "kv_root:", kv_root)
        messagebox = Builder.load_string(kv_msgbox)
        messagebox.text = "Dragging done!!!" # WHAT IF IT WAS DOUBLE_TAPPED? EXAMPLE!
        if calling_widget.is_double_tap:
            messagebox.text = "Make it a Double, barkeep!"
        kv_root.parent.add_widget(messagebox)
        messagebox.flash()

    def oops(self, calling_widget, kv_root=None, app=None):
        print ("app_relative_layout.oops(): Self, arg1, arg2:", self, kv_root, app)
        messagebox = Builder.load_string(kv_msgbox)
        messagebox.text = "Ooops! Can't drop there!"

        kv_root.parent.add_widget(messagebox)
        messagebox.flash()

if __name__ == '__main__':
    app_relative_layout().run()
