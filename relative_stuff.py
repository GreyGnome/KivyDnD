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

# File: DraggableButton.py
#       Part of the DragNDropWidget example.
'''
Created on Oct 24, 2012

@author: Pavel Kostelnik
'''


from __future__ import print_function

from dragndropwidget import DragNDropWidget
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.relativelayout import RelativeLayout
from kivy.clock import Clock


class DraggableButton(Button, DragNDropWidget):
    '''
    classdocs
    '''
    def __init__(self, **kw):
        '''
        Constructor
        '''
        #Button.__init__(self, **kw)
        super(DraggableButton, self).__init__(**kw)
        self.size_hint = (None, None)

    def __deepcopy__(self, dumb):
        return DraggableButton(text=self.text)

    def greet(self, object):
        print ("greetings from DROPBUTTON")

    def oops(self, root, app):
        app.oops(root, app)
        print ("OOOPS!!!")

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
        self.text = args[0].text + " drop: " + str(self.i)


class DragDestinationRelativeLayout(RelativeLayout):
    def __init__(self, *args, **kwargs):
        super(DragDestinationRelativeLayout, self).__init__(**kwargs)
        pass


class DragDestinationBoxLayout(BoxLayout):
    def __init__(self, *args, **kwargs):
        super(DragDestinationBoxLayout, self).__init__(**kwargs)
        pass


class DragSourceBoxLayout(BoxLayout):
    def on_touch_down(self, touch):
        super (DragSourceBoxLayout, self).on_touch_down(touch)

    def drop_func(self, arg1):
        print ("Arg1:", arg1, "parent:", arg1.parent)
        print ("drop_func: Dropped here", self)
        self.add_widget(arg1)
        arg1.opacity = 1.0