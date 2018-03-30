#!/usr/bin/python
# -*- coding: UTF-8 -*-
#    Copyright 2016, 2015, 2014, 2013, 2012 Pavel Kostelnik
#    Copyright 2017, 2018 Michael Schwager

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

# File: DragNDropWidget.py
#       the drag and drop widget library for Kivy.
# Version 0.4
from __future__ import print_function

import copy

from kivy.animation import Animation
from kivy.core.window import Window
from kivy.properties import (
	ListProperty, NumericProperty, BooleanProperty, ObjectProperty, StringProperty)
from kivy.uix.widget import Widget

from .debug_print import Debug
from kivydnd.dnd_storage_singletons import draggables_dict, drag_destinations_dict

debug = Debug() # Is False by default.
DEBUG_COLLIDE_POINT=0x00
DEBUG_BIND_DROP_GROUP=0x00
DEBUG_BIND_MOUSE_MOTION=0x00
DEBUG_ON_MOTION=0x00
DEBUG_ON_MOTION_FLEE=0x00
DEBUG_ON_MOTION_OVER=0x00
DEBUG_ON_MOTION_OUTSIDE=0x00
DEBUG_ON_MOTION_INSIDE=0x00

debug.register = DEBUG_COLLIDE_POINT | DEBUG_BIND_DROP_GROUP |\
                 DEBUG_BIND_MOUSE_MOTION | DEBUG_ON_MOTION | DEBUG_ON_MOTION_FLEE |\
                 DEBUG_ON_MOTION_OVER | DEBUG_ON_MOTION_OUTSIDE | DEBUG_ON_MOTION_INSIDE

# draggables_dict=dnd_storage_singletons.draggables_dict
# drag_destinations_dict=dnd_storage_singletons.drag_destinations_dict

class DropDestination(Widget):
    motion_over_widget_func = ObjectProperty(None)
    motion_over_widget_args = ListProperty([])
    motion_flee_widget_func = ObjectProperty(None)
    motion_flee_widget_args = ListProperty([])
    motion_outside_widget_func = ObjectProperty(None)
    motion_outside_widget_args = ListProperty([])
    motion_inside_widget_func = ObjectProperty(None)
    motion_inside_widget_args = ListProperty([])
    while_dragging_func = StringProperty(None)
    drop_group = StringProperty("_palm_default")
    widget_entered = None

    def __init__(self, **kw):
        super(DropDestination, self).__init__(**kw)
        self.register_event_type("on_motion_over")
        self.register_event_type("on_motion_flee")
        self.register_event_type("on_motion_outside")
        self.register_event_type("on_motion_inside")
        self.register_event_type("on_close")
        self.bind(motion_over_widget_func=self.bind_mouse_motion)
        self.bind(motion_flee_widget_func=self.bind_mouse_motion)
        self.bind(motion_outside_widget_func=self.bind_mouse_motion)
        self.bind(motion_inside_widget_func=self.bind_mouse_motion)
        self.motion_is_bound_to_window = False
        self.bind(drop_group=self.bind_drop_group)
        self.in_me = False

    def close(self):
        """
        You must call close() when you are removing the widget from the display.
        :return: 
        """
        self.dispatch("on_close")

    def on_close(self):
        self.unbind(motion_over_widget_func=self.bind_mouse_motion)
        self.unbind(motion_flee_widget_func=self.bind_mouse_motion)
        self.unbind(motion_outside_widget_func=self.bind_mouse_motion)
        self.unbind(motion_inside_widget_func=self.bind_mouse_motion)
        self.unbind(drop_group=self.bind_drop_group)
        self.unregister_event_types("on_motion_over")
        self.unregister_event_types("on_motion_flee")
        self.unregister_event_types("on_motion_outside")
        self.unregister_event_types("on_motion_inside")
        self.unregister_event_types("on_close")
        if self.motion_is_bound_to_window:
            Window.unbind(mouse_pos=self.on_motion)
            self.motion_is_bound_to_window = False

        for drop_group in drag_destinations_dict:
            if drag_destinations_dict[drop_group].get(self):
                del drag_destinations_dict[drop_group][self]
        # TODO: close all children (they have bound properties, too!

    def bind_drop_group(self, arg1, arg2):
        global DEBUG_BIND_DROP_GROUP
        debug.print ("BINDING DROP GROUP", self.drop_group, level=DEBUG_BIND_DROP_GROUP)
        if self.drop_group not in drag_destinations_dict:
            drag_destinations_dict[self.drop_group]={}
        drag_destinations_dict[self.drop_group][self]=True

    def bind_mouse_motion(self, instance, value):
        global DEBUG_BIND_MOUSE_MOTION
        # debug.print ("DropDestination: BINDNG WIDGETS to Mouse Motion!", instance, value, level=DEBUG_BIND_MOUSE_MOTION
        if self.motion_is_bound_to_window is False:
            Window.bind(mouse_pos=self.on_motion)
        self.motion_is_bound_to_window = True

    def on_motion(self, top_level_window, motion_xy_tuple):
        """
        As the mouse moves in the window, do stuff:
        - If it hits this widget, and
          - If it had not marked this widget as entered,
            - If it had not marked ANY widget as entered,,
              - we have moved over this widget; dispatch on_motion_over
              - make this widget as entered
            else: (it hit this widget, but it had marked another widget as entered)
                  (This means it left that widget without dispatching on_motion_flee)
              - dispatch on_motion_flee for the other widget
              - dispatch on_motion_over for this widget
              - mark this widget as entered.
        NOTE: Be careful if there's a RelativeLayout involved in your widget
        heirarchy. collide_point may not intersect with the widget you expect, and
        so you'll get false results! Remember that the x,y of the motion is in the
        parent coordinate system, and the parent coordinate system is lost on any
        widgets that are children of a RelativeLayout. ...But see the TODO just below.
        :param top_level_window: The top level kivy window
        :param motion_xy_tuple: The coordinates of the mouse in the Window's coordinate system
        :return:
        """
        global DEBUG_ON_MOTION
        # debug.print "event x,y:", motionevent[0], motionevent[1], "self x,y,w,h:", self.x, self.y, self.width, self.height
        # debug.print "event x,y:", motionevent[0], motionevent[1], "self:", self
        # motionevent is in the main Window's coordinate system.
        # debug.print "Self.to_window:", self.to_window(self.x, self.y)
        # TODO: I believe I have compensated for any relative widget, here.
        # TODO: ...but be wary. I'm still not sure about how RelativeLayout will behave.
        #debug.print("START motion", self, "window coords (self):",
        #            self.to_window(motion_xy_tuple[0], motion_xy_tuple[1]),
        #            level=DEBUG_ON_MOTION)
        #debug.print("Coords of motion:", motion_xy_tuple[0], motion_xy_tuple[1],
        #            level=DEBUG_ON_MOTION)
        # "self x,y,w,h:", self.x, self.y, self.width, self.height,
        if self.absolute_collide_point(motion_xy_tuple[0], motion_xy_tuple[1]):
            # debug.print(motion_xy_tuple[0], motion_xy_tuple[1], "pointer collides",
            #             self, level=DEBUG_ON_MOTION)
            if self.in_me:
                self.dispatch("on_motion_inside", motion_xy_tuple)
            else:
                # DropDestination.widget_entered.dispatch("on_motion_flee")
                self.in_me = True
                self.dispatch("on_motion_over", motion_xy_tuple)
        else:
            if self.in_me:
                self.dispatch("on_motion_flee", motion_xy_tuple)
                self.in_me = False
            else:
                self.dispatch("on_motion_outside", motion_xy_tuple)

    def absolute_collide_point(self, x, y):
        """

        :param x: x-value of a point in *Window* coordinates
        :param y: y-value of a point in *Window* coordinates
        :return: True or False
        """
        global DEBUG_COLLIDE_POINT
        (my_x, my_y)=self.to_window(self.x, self.y)
        if Window.mouse_pos[0] != x or Window.mouse_pos[1] != y:
            try:
                debug.print("Title:", self.title(), "==========================", level=DEBUG_COLLIDE_POINT)
            except:
                pass
            debug.print("point, x,y:       ", x, y, level=DEBUG_COLLIDE_POINT)
            debug.print("Window mouse pos:", Window.mouse_pos, level=DEBUG_COLLIDE_POINT)
            debug.print("me:", self, level=DEBUG_COLLIDE_POINT)
            debug.print("x,y,r,t:", my_x, my_y, self.width + my_x, my_y + self.height,
                        level=DEBUG_COLLIDE_POINT)
        #debug.print_widget_ancestry(self, level=DEBUG_COLLIDE_POINT)
        return my_x <= x <= (self.width + my_x) and my_y <= y <= (my_y + self.height)

    def on_motion_flee(self, motion_xy_tuple):
        """
        Called when your touch point leaves a draggable item.
        :return:
        """
        global DEBUG_ON_MOTION_FLEE
        # debug.print "DropDestination: MOTION flee"
        if self.motion_flee_widget_func is not None:
            self.motion_flee_widget_func(self, self.motion_flee_widget_args)
            # TODO: WAS... adding these binds. Not sure why.
            # self.easy_access_dnd_function_binds)
        else:
            pass
            # debug.print "FUNCTION MOTION FLEE NONE"
        DropDestination.widget_entered = None

    def on_motion_over(self, motion_xy_tuple):
        """
        Called when your touch point crosses into a DropDestination object.
        Self is added as an argument because if you set this up in a .kv file, the self
        given there is always the self of the object created in the .kv file.
        For example, if you want to create a copy of the object in the Python code, the self
        will still refer to the self of the original object.

        TODO: Doesn't this apply exclusively to DragNDropWidgets? This should not be a problem
        in DragDestination widgets, because the library is not creating copies of these
        objects.

        :return:
        """
        global DEBUG_ON_MOTION_OVER
        # debug.print "DropDestination: MOTION over", motion_xy_tuple
        if self.motion_over_widget_func is not None:
            self.motion_over_widget_func(self, self.motion_over_widget_args)
            # self.easy_access_dnd_function_binds)
        # else:
        #    debug.print "FUNCTION MOTION OVER NONE"

    def on_motion_outside(self, motion_xy_tuple):
        global DEBUG_ON_MOTION_OUTSIDE
        # debug.print "DropDestination: MOTION outside"
        try:
            if self.motion_outside_widget_func is not None:
                self.motion_outside_widget_func(self, self.motion_outside_widget_args)
            else:
                pass
                # debug.print "FUNCTION OUT NONE"
        except AttributeError:
            pass

    def on_motion_inside(self, motion_xy_tuple):
        global DEBUG_ON_MOTION_INSIDE
        # debug.print "on_motion_inside: DropDestination INSIDE"
        try:
            if self.motion_inside_widget_func is not None:
                self.motion_inside_widget_func(self, self.motion_inside_widget_args)
            else:
                pass
                # debug.print "FUNCTION OUT NONE"
        except AttributeError:
            pass
