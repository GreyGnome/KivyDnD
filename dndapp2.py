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

# File: dndapp2.py
#       Example of the DragNDropWidget Kivy library.

from kivy.app import App
from kivy.lang import Builder
import DraggableButton  # import to get auto register
from kivy.clock import Clock

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
            text: '1. Defaults'
            bound_zone_objects: [from_box, lower_to_box, upper_to_box ]
            droppable_zone_objects: [lower_to_box, upper_to_box ]
            drop_ok_animation_time: 1.5
            drop_func: app.greet
            drop_args: [self]
            failed_drop_func: app.oops

        DraggableButton:
            text: '2. No Remove\\nNo Bounds'
            # Uncomment this to observe its effect.
            # bound_zone_objects: [from_box, lower_to_box, upper_to_box ]
            droppable_zone_objects: [lower_to_box, upper_to_box, upper_inner_box ]
            remove_on_drag: False
            drag_opacity: .5
            drop_func: self.greet
            drop_args: [self]
            failed_drop_func: self.oops

        DraggableButton:
            text: '3.\\nOpacity .5\\nTo Upper'
            bound_zone_objects: [from_box, upper_to_box ]
            droppable_zone_objects: [upper_to_box, ]
            drag_opacity: .5
            drop_func: self.greet
            drop_args: [self]
            failed_drop_func: self.oops
            drop_ok_animation_time: 1.5

    DragDestinationLabel:
        id: upper_to_box
        text: 'drag here for some effect'
        canvas.before:
            Color:
                rgb: 0.4, 0.4, 1
            Rectangle:
                pos: self.pos
                size: self.size
        size_hint: 0.8, 0.2
        pos_hint: {'x': 0.1, 'y': 0.8}
        drop_func: self.greeter

    DragDestinationLabel:
        id: upper_inner_box
        text: 'only 2 drops in this gray area'
        canvas.before:
            Color:
                rgb: 0.4, 0.4, 0.4
            Rectangle:
                pos: self.pos
                size: self.size
        size_hint: 0.3, 0.05
        pos_hint: {'x': 0.4, 'y': 0.8}
        drop_func: self.greeter

    Label:
        id: lower_to_box
        text: 'drag down low (if you can) for some effect'
        canvas.before:
            Color:
                rgb: 0.4, 0.8, 0.4
            Rectangle:
                pos: self.pos
                size: self.size
        size_hint: 0.8, 0.2
        pos_hint: {'x': 0.2, 'y': 0.0}


#    Label:
#        text: 'cannot\\ndrag here'
#        size_hint: 0.2, 0.1
#        pos_hint: {'x': 0.5, 'y': 0.8}
#        canvas.before:
#            Color:
#                rgb: 0.5, 0.5, 0.5
#            Rectangle:
#                pos: self.pos
#                size: self.size
'''


class dndapp2(App):
    def __init__(self, **kw):
        super(dndapp2, self).__init__(**kw)
        self.i = 0
        self.toggle_text = True

    def build(self):
        return Builder.load_string(kv)

    def greet(self, arg1=None, arg2=None):
        print "GREETINGS FROM APP!!!"
        print "Dragging done!!!",
        print str(arg1), str(arg2)
        #for destination in arg1.drop_recipients:
        #    print "TEXT:",destination.text
        #    self.initial_text = destination.text
        #    self.flash_widget = destination
        #    Clock.schedule_interval(self.cycle_message, 0.5)

    def cycle_message(self, dt):
        print "CYCLE!!!!"
        if self.i < 6:
            if self.toggle_text:
                self.flash_widget.text = "from app.greet: YAY! DROPPED HERE!"
                self.toggle_text = False
            else:
                self.flash_widget.text = self.initial_text
                self.toggle_text = True
            self.i += 1
        else:
            Clock.unschedule(self.cycle_message)
            self.i=0
            self.toggle_text = True
            # TODO: TEST!!!!!!!!!!!!!!!!!!!!!!!!!

        #print arg1, arg2

    def oops(self):
        print "Ooops!"

if __name__ == '__main__':
    dndapp2().run()
