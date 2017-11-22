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

# File: example_base_classes.py
#       Part of the DragNDropWidget example.
'''
Created on Oct 24, 2012

@author: Pavel Kostelnik
'''

from __future__ import print_function

from kivy.uix.relativelayout import RelativeLayout
from kivydnd.debug_print import Debug
from kivy.clock import Clock
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label

from kivydnd.dragndropwidget import DragNDropWidget

debug = Debug(False)


class DraggableButton(Button, DragNDropWidget):
    '''
    classdocs
    '''

    def __init__(self, **kw):
        '''
        Constructor
        '''
        super(DraggableButton, self).__init__(**kw)
        self.size_hint = (None, None)
        self.text = hex(id(self))

    def __deepcopy__(self, dumb):
        return DraggableButton(text=self.text)

    def greet(self, object, arg2):
        print("greetings from DROPBUTTON")

    def oops(self, calling_widget):
        print("oops() Args:", self, calling_widget, kv_root, app)
        app.oops(calling_widget, kv_root, app)
        print("OOOPS!!!")

    def on_successful_drop(self, arg1=None, arg2=None):
        super(DraggableButton, self).on_successful_drop()
        print("on_successful_drop: Run overridden method")

    def on_unsuccessful_drop(self, arg1=None, arg2=None):
        super(DraggableButton, self).on_unsuccessful_drop(arg1, arg2)
        print("on_unsuccessful_drop: Run overridden method")


class DragDestinationLabel(Label):
    def __init__(self, *args, **kwargs):
        super(DragDestinationLabel, self).__init__(**kwargs)
        self.i = 0

    def on_touch_down(self, touch):
        pass

    def cycle_message(self, text):
        if self.i < 6:
            if self.toggle_text:
                self.text = self.dropped_text
                self.toggle_text = False
            else:
                self.text = self.initial_text
                self.toggle_text = True
            self.i += 1
        else:
            Clock.unschedule(self.cycle_message)
            self.i = 0
            self.toggle_text = True
            self.text = "Drag and Drop done!"

    def greeter(self, *args):
        self.i += 1
        self.toggle_text = True
        self.initial_text = self.text
        self.text = args[0].text + " dropped here! " + str(self.i) + " times"


class DragDestinationRelativeLayout(RelativeLayout):
    def __init__(self, *args, **kwargs):
        super(DragDestinationRelativeLayout, self).__init__(**kwargs)
        pass


class DragDestinationBoxLayout(BoxLayout):
    def __init__(self, *args, **kwargs):
        super(DragDestinationBoxLayout, self).__init__(**kwargs)
        pass


class DragSourceBoxLayout(BoxLayout):
    def __init__(self, *args, **kwargs):
        super(DragSourceBoxLayout, self).__init__(**kwargs)
        self.last_touch_up_time=0

    def on_touch_down(self, touch):
        super(DragSourceBoxLayout, self).on_touch_down(touch)

    def on_touch_up(self, touch):
        '''Receive a touch up event. The touch is in parent coordinates.

        See :meth:`on_touch_down` for more information.
        '''
        print ("--- START START START TOUCH UP --- on_touch_up: DragSourceBoxLayout", self, "Kids:", self.children)
        print ("touch start:", touch.time_start)
        super(DragSourceBoxLayout, self).on_touch_up(touch)


    def post_drop_func(self, arg1):
        print ("DragSourceBoxLayout:post_drop_func: TODO: HOW to get this copied widget to parent here...?")
        print ("DragSourceBoxLayout:post_drop_func: Arg1:", arg1, "parent:", arg1.parent)
        print ("DragSourceBoxLayout:post_drop_func: Dropped here", self)
        # TODO: This is not right. What am I trying to do here?
        if arg1.parent == None:
            self.add_widget(arg1)
        arg1.opacity = 1.0 # Because the animation makes it disappear


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