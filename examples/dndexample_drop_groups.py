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

# This example is like dndexample_relative_layout, with a few added twists:
# - The first and second buttons demonstrate the use of drop groups.
#   - Button 0 is a member of drop group 'Left', as is the blue label "Destination on the Left"
#     Hence that button will only successfully drop onto that label.
#   - Button 1 has a few items of note:
#     - Its remove_on_drag Property is set to False, so a copy of the button will be made
#       upon drag.
#     - It is a member of drop group "Relative Labels", as are the two greenish-gray
#       labels "Destination: Relative Left" and "Destination: Relative, Right". Hence
#       Button 1 (or rather, its copy) will drop successfully onto those two labels.
#     - In addition, its Property can_drop_into_parent is set to True, and its Property
#       droppable_zone_objects is set to [from_box], so its copy can be dropped onto its
#       parent, which is "from_box".
#   - Button 2 is not a member of any drop group. However, it has a Property
#     "droppable_zone_objects" which consists of a list with a single element, that of the
#     id "relative_left_label" (not a string), which is the id of the center of the upper
#     labels. Thus this button can drop only onto that label. Furthermore, the button will
#     be removed on drag, because its remove_on_drag Property was not set to False. So if
#     a drop is not successful, the button will be returned to its place.
# The Button being dragged will generate a kind of dialog box when it's dropped.
# That box is created from the app object.
# The destination widgets' text changes upon successful drop. That text is maintained
# in the destination widgets.

# File: example_relative_layout.py
from __future__ import print_function

from kivydnd.debug_print import Debug
from kivy.app import App
from kivy.lang import Builder

debug=Debug(False)


# Classes in the FloatLayout are defined in DraggableButton.py, included above.
kv = '''
#:import DragSourceBoxLayout example_base_classes.DragSourceBoxLayout
#:import DragDestinationBoxLayout example_base_classes.DragDestinationBoxLayout
#:import DraggableButton example_base_classes.DraggableButton

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

<DragDestinationDropLabel>:
    id: drag_destination_drop_label
    canvas.before:
        Color:
            rgb: 0.4, 0.5, 0.4
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
            id: draggable_button0
            text: '0:drop to\\nDest on Left'
            drop_ok_animation_time: 1.5
            drop_func: app.greet
            drop_args: [ root ]
            failed_drop_func: self.oops
            failed_drop_args: [ root, app ]
            remove_on_drag: False
            can_drop_into_parent: False
            drop_group: "Left"
        DraggableButton:
            id: draggable_button1
            droppable_zone_objects: [from_box]
            text: '1:drop to\\nRelative\\n(2 labels)\\nor parent'
            drop_ok_animation_time: 1.5
            drop_func: app.greet
            drop_args: [ root ]
            failed_drop_func: self.oops
            failed_drop_args: [ root, app ]
            remove_on_drag: False
            can_drop_into_parent: True
            drop_group: "Relative Labels"
        DraggableButton:
            id: draggable_button2
            droppable_zone_objects: [relative_left_label]            
            text: '2:drop to\\nmiddle Rel.\\nlabel'
            drop_ok_animation_time: 1.5
            drop_func: app.greet
            drop_args: [ root ]
            failed_drop_func: self.oops
            failed_drop_args: [ root, app ]
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
        DragDestinationDropLabel:
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
            drop_group: "Left"
        DragDestinationRelativeLayout:
            id: right_relative_layout
            size_hint: 0.67, 1.0
            canvas.before:
                Color:
                    rgba: 0.7, 0.7, 0.0, 1.0
                Rectangle:
                    pos: self.pos
                    size: self.size
            DragDestinationDropLabel:
                id: relative_left_label
                text: "Destination:\\nRelative, Left"
                pos_hint: {'x': 0.11, 'y': 0.3}
                drop_group: "Relative Labels"
            DragDestinationDropLabel:
                id: relative_right_label
                text: "Destination:\\nRelative, Right"
                pos_hint: {'x': 0.55, 'y': 0.3}
                drop_group: "Relative Labels"
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


class DnDExampleDropGroups(App):
    def __init__(self, **kw):
        super(DnDExampleDropGroups, self).__init__(**kw)

    def build(self):
        return Builder.load_string(kv)

    def greet(self, calling_widget, kv_root=None):
        """

        :param calling_widget: the widget that calls this method. It was the one that was
        dragged-and-dropped
        :param kv_root: the root window from the Kivy language.
        :return:
        """
        debug.print ("calling_widget:", calling_widget,
                     "======== SENDS THE MESSAGE ========== double tap:",
                     calling_widget.is_double_tap, "kv_root:", kv_root)
        messagebox = Builder.load_string(kv_msgbox)
        messagebox.text = "Drop Successful!!!"  # WHAT IF IT WAS DOUBLE_TAPPED? EXAMPLE!
        if calling_widget.is_double_tap:
            messagebox.text = "Make it a Double, barkeep!"
        kv_root.parent.add_widget(messagebox)
        messagebox.flash()

    def oops(self, calling_widget, kv_root=None, app=None):
        debug.print ("Self, arg1, arg2:", self, kv_root, app)
        messagebox = Builder.load_string(kv_msgbox)
        messagebox.text = "Ooops! Can't drop there!"

        kv_root.parent.add_widget(messagebox)
        messagebox.flash()


if __name__ == '__main__':
    DnDExampleDropGroups().run()
