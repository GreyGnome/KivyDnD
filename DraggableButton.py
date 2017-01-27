'''
Created on Oct 24, 2012

@author: Pavel Kostelnik
'''


from DragNDropWidget import DragNDropWidget
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
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
        print "greetings from DROPBUTTON"

    def oops(self):
        print "OOOPS!!!"

class DragDestinationLabel(Label):
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

    def greeter(self, *args):
        self.i = 0
        self.toggle_text = True
        self.initial_text = self.text
        self.dropped_text = "YAY! " + args[0].text + " dropped here!"
        Clock.schedule_interval(self.cycle_message, 0.3)


class DragSourceBoxLayout(BoxLayout):
    def on_touch_down(self, touch):
        print "BOXLAYOUT GOT TOUCHED!", str(self)
        super (DragSourceBoxLayout, self).on_touch_down(touch)
