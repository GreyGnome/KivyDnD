#!/usr/bin/python
# -*- coding: UTF-8 -*-
#    Copyright 2016, 2015, 2014, 2013, 2012 Pavel Kostelnik
#    Copyright 2017 Michael Schwager

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
from __future__ import print_function

import copy

from kivy.animation import Animation
from kivy.core.window import Window
from kivy.properties import (
	ListProperty, NumericProperty, BooleanProperty, ObjectProperty, StringProperty)
from kivy.uix.widget import Widget

from source.debug_print import Debug

debug = Debug() # Is False by default.

# This looks like:
# dictionary[drag_group][widget] = true
drag_destinations_dict={}
draggables_dict={}


class DragNDropWidget(Widget):
    # let kivy take care of kwargs and get signals for free by using
    # properties
    droppable_zone_objects = ListProperty([])
    bound_zone_objects = ListProperty([])
    drag_opacity = NumericProperty(1.0)
    drop_func = ObjectProperty(None)
    drop_args = ListProperty([])
    while_dragging_func = ObjectProperty(None) # The touch is given in Window coordinates
    failed_drop_func = ObjectProperty(None)
    failed_drop_args = ListProperty([])
    remove_on_drag = BooleanProperty(True)
    drop_ok_do_animation = BooleanProperty(True)
    drop_ok_animation_time = NumericProperty(0.5)
    not_drop_ok_do_animation = BooleanProperty(True)
    not_drop_ok_animation_time = NumericProperty(0.2)
    motion_over_widget_func = ObjectProperty(None)
    motion_over_widget_args = ListProperty([])
    motion_flee_widget_func = ObjectProperty(None)
    motion_flee_widget_args = ListProperty([])
    motion_outside_widget_func = ObjectProperty(None)
    motion_outside_widget_args = ListProperty([])
    drag_start_func = ObjectProperty(None)
    drag_start_args = ListProperty([])
    can_drop_into_parent = BooleanProperty(False)
    drop_group = StringProperty(None)
    # This is not a Property
    widget_entered = None

    def __init__(self, **kw):
        super(DragNDropWidget, self).__init__(**kw)

        self.register_event_type("on_drag_start")
        self.register_event_type("on_being_dragged")
        self.register_event_type("on_drag_finish")
        self.register_event_type("on_motion_over")
        self.register_event_type("on_motion_flee")
        self.register_event_type("on_motion_outside")
        self.register_event_type("on_close")
        self._old_opacity = self.opacity
        self._drag_started = False
        self._dragged = False
        self._draggable = True
        self.copy = False
        self.touch_offset_x = 0
        self.touch_offset_y = 0
        self.drop_recipients = []
        self.am_touched = False
        self.double_tap_drag = False
        self.is_double_tap = False
        self.motion_is_bound_to_window = False
        self.bind(motion_over_widget_func=self.bind_mouse_motion)
        self.bind(motion_flee_widget_func=self.bind_mouse_motion)
        self.bind(motion_outside_widget_func=self.bind_mouse_motion)
        self.bind(drop_group=self.bind_drop_group)
        if self.drop_group is None:
            self.drop_group = "_palm_default"
        self.found_drop_recipients_ok_dict = {}
        self.min_x = -1
        self.min_y = -1
        self.max_x = -1
        self.max_y = -1
        self.move_counter = 0
        self.touch_up_event_start = 0

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
        self.unbind(drop_group=self.bind_drop_group)
        self.unregister_event_types("on_drag_start")
        self.unregister_event_types("on_being_dragged")
        self.unregister_event_types("on_drag_finish")
        self.unregister_event_types("on_motion_over")
        self.unregister_event_types("on_motion_flee")
        self.unregister_event_types("on_motion_outside")
        self.unregister_event_types("on_close")
        if self.motion_is_bound_to_window:
            Window.unbind(mouse_pos=self.on_motion)
            self.motion_is_bound_to_window = False

    def bind_drop_group(self, arg1, arg2):
        if self.drop_group not in draggables_dict:
            draggables_dict[self.drop_group] = {}
        draggables_dict[self.drop_group][self] = True

    run_already = False

    def bind_mouse_motion(self, the_widget, which_function):
        if self.motion_is_bound_to_window is False:
            Window.bind(mouse_pos=self.on_motion)
        self.motion_is_bound_to_window = True

    def set_draggable(self, value):
        self._draggable = value

    def set_remove_on_drag(self, value):
        """
        This function sets the property that determines whether the dragged widget is just
        copied from its parent or taken from its parent.
        @param value: either True or False. If True then the widget will disappear from its
        parent on drag, else the widget will just get copied for dragging
        """
        self.remove_on_drag = value

    def set_drag_start_state(self):
        self._move_counter = 0
        self._old__opacity = self.opacity
        self.opacity = self.drag_opacity
        self.set_bound_axis_positions()
        self._old_drag_pos = self.pos
        self._old_parent = self.parent
        self._old_parent_children_reversed_list = self.parent.children[:]
        self._old_parent_children_reversed_list.reverse()
        DragNDropWidget.widget_entered = None
        if self.copy:
            self._old_index = -1
        else:
            self._old_index = self.parent.children.index(self)
        self._drag_started = True

    def set_drag_finish_state(self, set_opacity=True):
        self._drag_started = False
        self.is_double_tap = False
        self._dragged = False
        self.copy = False
        # TODO: If I was the copy, I need to not be a copy :-). Set it to false...
        # TODO: (after current debugging on 6/17/17)
        if set_opacity:
            self.opacity = self._old_opacity
        debug.print (" ****************** DRAG N DROP TOTALLY DONE *********************")

    def set_bound_axis_positions(self):
        for obj in self.bound_zone_objects:
            if self.min_x == -1:
                self.max_x = obj.x + obj.size[0] - self.size[0]
                self.max_y = obj.y + obj.size[1] - self.size[1]
                self.min_x = obj.x
                self.min_y = obj.y
            if self.max_y < obj.y+obj.size[1]-self.size[1]:
                self.max_y = obj.y+obj.size[1]-self.size[1]
            if self.max_x < obj.x+obj.size[0]-self.size[0]:
                self.max_x = obj.x + obj.size[0]-self.size[0]
            if self.min_y > obj.y:
                self.min_y = obj.y
            if self.min_x > obj.x:
                self.min_x = obj.x

    def on_touch_down(self, touch):
        """
        on_touch_down contains a numerical value. If the object is touched for a period longer than
        this value then we may be entering a drag operation. The value should probably be made
        configurable. As a matter of fact, I'm sure it should be. ...TODO.
        
        touch.is_double_tap is maintained by Kivy.
        self.is_double_tap is maintained by the widget, because we don't want on_touch_up to 
        set "am_touched" to be false too quickly..
        :param touch:
        :return:
        """
        # TODO: make the drag delay configurable
        if self.collide_point(touch.x, touch.y) and self._draggable:
            # detect if the touch is "long"... (if not, dispatch drag)
            if (abs(touch.time_end - touch.time_start) > 0.1) or touch.is_double_tap:
                self.touch_offset_x = touch.x - self.x
                self.touch_offset_y = touch.y - self.y
                self.am_touched = True
                if touch.is_double_tap:
                    self.is_double_tap = True
                    debug.print ( "DOUBLE TAPPED THIS ONE!", self)

    def on_touch_up(self, mouse_motion_event):
        """
        In a double tap, this gets called after each tap, which sets am_touched to be False.
        So there's a bit of a complication, which is dealt with in the first if statement.
        :param touch:
        :return:
        """
        #if self.collide_point(mouse_motion_event.x, mouse_motion_event.y) and self._draggable:
        debug.print ("***                 DragNDropWidget")
        debug.print ("***  on_touch_up: self:", self, "copy:", self.copy, "parent:", self.parent)
        debug.print ("***  id:", hex(id(self)))
        debug.print ("***  am_touched:", self.am_touched, "is_double_tap:", self.is_double_tap)
        debug.print ("***  was dragged?", self._dragged, "event:", mouse_motion_event.__repr__())
        debug.print ("***                 on_touch_up                ***")
        debug.print ("***  Mouse Motion Event:", mouse_motion_event)
        # We if a widget is reborn, this event may be called a second time. Don't do that.
        if self.touch_up_event_start == mouse_motion_event.time_start:
            return
        self.touch_up_event_start = mouse_motion_event.time_start

        if self.is_double_tap and not self._dragged:
            debug.print ("on_touch_up: DOUBLE TAP AND NOT DRAGGED")
            self.set_drag_finish_state()
            return
        self.am_touched = False
        if self._draggable and self._dragged:
            debug.print ("on_touch_up: DRAGGED!!!!!!!")
            self.touch_x = mouse_motion_event.x
            self.touch_y = mouse_motion_event.y
            debug.print ('dispatch "on_drag_finish", mouse_motion_event) *******************************')
            self.dispatch("on_drag_finish", mouse_motion_event)
            # TODO: Is this right? How do I send on_touch_up after
            # TODO: a double tap?
        else:
            debug.print ("on_touch_up: NOT DRAGGED")
            self.set_drag_finish_state()
    # TODO: LOOK ALL OVER FOR DISPATCH, AND SEND COORDS

    # TODO: Need to set         Window.bind(mouse_pos=self.on_motion)
    # TODO: The functions are Properties, so I can do this when they're set!!!
    def on_touch_move(the_widget, mouse_motion_event):
        if the_widget.am_touched:
            if not the_widget._drag_started:
                the_widget.dispatch("on_drag_start", mouse_motion_event)
                the_widget.am_touched = False
        if not the_widget._drag_started:
            return
        the_widget._move_counter += 1
        if the_widget._draggable and the_widget._drag_started:
            # if the_widget._dragged and the_widget._draggable:
            the_widget._dragged = True
            x = mouse_motion_event.x - the_widget.touch_offset_x
            y = mouse_motion_event.y - the_widget.touch_offset_y
            # debug.print ("on_touch_move: widget pos:", x, y, "parent:", the_widget.parent)

            if the_widget.min_x != -1:
                if x <= the_widget.min_x:
                    x = the_widget.min_x
                if x > the_widget.max_x:
                    x = the_widget.max_x
                if y <= the_widget.min_y:
                    y = the_widget.min_y
                if y > the_widget.max_y:
                    y = the_widget.max_y
            the_widget.pos = (x, y)
            # SPECIAL! Takes a herky-jerky GUI and makes it smoooooth....
            the_widget.canvas.ask_update()
            # Execute widget's while_dragging_func while dragging the widget
            if the_widget.while_dragging_func is not None:
                the_widget.while_dragging_func(the_widget, mouse_motion_event)
            # Execute while_dragging_func for all drag destinations that are in the same
            # drop group as the widget, that the widget passes over.
            for drop_group in draggables_dict:
                if draggables_dict[drop_group].get(the_widget):
                    if drag_destinations_dict.get(drop_group) is not None:
                        for drag_destination in drag_destinations_dict.get(drop_group):
                            if drag_destination.while_dragging_func is not None:
                                if drag_destination.absolute_collide_point(mouse_motion_event.x, mouse_motion_event.y):
                                    drag_destination.while_dragging_func(the_widget, mouse_motion_event)

    # DEPRECATED.................................................................
    # No longer used. ...But what is the purpose of bind_functions? Pavel wrote
    # it but I don't understand its purpose.
    def easy_access_dnd(self, function_to_do_over, function_to_do_flee,
                        function_to_do_outside, arguments = None, bind_functions = None):
        """
        This function enables something that can be used instead of drag n drop
        @param function_to_do: function that is to be called when mouse_over event is fired on the widget
        @param bind_functions: what is really to be done - background function for GUI functionality
        """
        if arguments is None:
            arguments = []
        if bind_functions is None:
            bind_functions = []
        Window.bind(mouse_pos=self.on_motion)
        self.easy_access_dnd_function_over = function_to_do_over
        self.easy_access_dnd_function_flee = function_to_do_flee
        self.easy_access_dnd_function_outside = function_to_do_outside
        self.easy_access_dnd_function_arguments = arguments
        self.easy_access_dnd_function_binds = bind_functions
    # ^^^ DEPRECATED..............................................................

    def on_motion(self, top_level_window, motion_xy_tuple):
        """
        As the mouse moves in the window, do stuff:
        - If it hits this widget, and
          - If it had not marked this widget as entered,
            - If it had not marked ANY widget as entered,,
              - we have moved over this widget; dispatch on_motion_over
              - make this widget as entered
            else: (it hit this widget, but it had marked another widget as entered)
n                  (This means it left that widget without dispatching on_motion_flee)
              - dispatch on_motion_flee for the other widget
              - dispatch on_motion_over for this widget
              - mark this widget as entered.
        :param top_level_window: The top level kivy window
        :param motion_xy_typle: the coordinates of the mouse in the Window's coord system 
        :return:
        """
        if self._drag_started:
            return
        if self.collide_point(*self.to_widget(motion_xy_tuple[0], motion_xy_tuple[1])):
            if DragNDropWidget.widget_entered is not self:
                if DragNDropWidget.widget_entered is not None:
                    # widget_entered is set, but it's not us. That means we just jumped
                    # from another widget to this one. We should make sure we fled the
                    # old one properly.
                    DragNDropWidget.widget_entered.dispatch("on_motion_flee", motion_xy_tuple)
                self.dispatch("on_motion_over", motion_xy_tuple)
                DragNDropWidget.widget_entered = self
        else:
            if DragNDropWidget.widget_entered is not None:
                if self is DragNDropWidget.widget_entered:
                    self.dispatch("on_motion_flee", motion_xy_tuple)
                    DragNDropWidget.widget_entered = None
            else:
                self.dispatch("on_motion_outside", motion_xy_tuple)

    def on_motion_flee(self, motion_xy_tupel):
        """
        Called when your touch point leaves a draggable item.
        :return:
        """
        if self.motion_flee_widget_func is not None:
            self.motion_flee_widget_func(self, self.motion_flee_widget_args)
            # TODO: WAS... adding this binds. Not sure why.
            # self.easy_access_dnd_function_binds)
        else:
            pass
            # debug.print "FUNCTION MOTION FLEE NONE"
        DragNDropWidget.widget_entered = None

    def on_motion_over(self, motion_xy_tuple):
        """
        Called when your touch point crosses into a draggable item.
        :return:
        """
        if self.motion_over_widget_func is not None:
            self.motion_over_widget_func(self, self.motion_over_widget_args)
                # self.easy_access_dnd_function_binds)
        else:
            pass
            # debug.print "FUNCTION MOTION OVER NONE"

    def on_motion_outside(self, motion_xy_tuple):
        try:
            if self.motion_outside_widget_func is not None:
                self.motion_outside_widget_func(self, self.motion_outside_widget_args)
            else:
                pass
                # debug.print "FUNCTION OUT NONE"
        except AttributeError:
            pass

    def deepen_the_copy(self, copy_of_self):
        copy_of_self.copy = True
        copy_of_self.parent = self.parent
        copy_of_self.droppable_zone_objects = self.droppable_zone_objects
        copy_of_self.bound_zone_objects = self.bound_zone_objects
        copy_of_self.drag_opacity = self.drag_opacity
        copy_of_self.drop_func = self.drop_func
        copy_of_self.drop_args = self.drop_args
        copy_of_self.drag_start_func = self.drag_start_func
        copy_of_self.drag_start_args = self.drag_start_args
        copy_of_self.failed_drop_func = self.failed_drop_func
        copy_of_self.failed_drop_args = self.failed_drop_args
        copy_of_self.remove_on_drag = self.remove_on_drag
        copy_of_self.drop_ok_do_animation = self.drop_ok_do_animation
        copy_of_self.drop_ok_animation_time = self.drop_ok_animation_time
        copy_of_self.not_drop_ok_do_animation = self.not_drop_ok_do_animation
        copy_of_self.not_drop_ok_animation_time = self.not_drop_ok_animation_time
        copy_of_self.touch_offset_x = self.touch_offset_x
        copy_of_self.touch_offset_y = self.touch_offset_y
        copy_of_self.drop_recipients = self.drop_recipients
        copy_of_self.am_touched = self.am_touched
        copy_of_self._drag_started = self._drag_started
        copy_of_self.is_double_tap = self.is_double_tap

    def on_drag_start(self, mouse_motion_event):
        if self._drag_started:
            return
        if self.remove_on_drag:
            self._dragged = True
            if self.drag_start_func is not None:
                self.drag_start_func(self, self.drag_start_args)
            self.set_drag_start_state()
            self.root_window = self.parent.get_root_window()
            self.root_parent(self)
        else:
            #create copy of object to drag
            copy_of_self = copy.deepcopy(self)
            # We'll handle those variables that are common to ALL d-n-d
            # widgets. The widgets' classes can handle specifics
            # (such as text, etc.)
            self.deepen_the_copy(copy_of_self)
            copy_of_self._dragged = True
            if copy_of_self.drag_start_func is not None:
                copy_of_self.drag_start_func(copy_of_self, copy_of_self.drag_start_args)
            copy_of_self.set_drag_start_state()
            copy_of_self.root_window = self.parent.get_root_window()
            ## the final child class MUST implement __deepcopy__
            ## IF self.remove_on_drag == False !!! In this case this is
            ## met in draggableArhellModelImage class
            # TODO: MIKE: it used to be that copy_of_self was added to _old_parent
            # self._old_parent.add_widget(copy_of_self, index=self._old_index)
            copy_of_self.root_parent(copy_of_self)
            copy_of_self.pos = self.pos

    def absolute_collide_point(self, x, y):
        (my_x, my_y)=self.to_window(self.x, self.y)
        (event_x, event_y) = self.to_window(x, y)
        # debug.print "absolute_collide_point:", self, "x,y,w,h:", my_x, my_y, self.right + my_x, my_y + self.top
        return my_x <= event_x <= (self.width + my_x) and my_y <= event_y <= (my_y + self.height)

    def on_drag_finish(self, mouse_motion_event):
        # Don't worry, opacity will be properly set in set_drag_finish_state()
        # after the animation
        debug.print ("on_drag_finish: ================================================================")
        debug.print ("on_drag_finish, beginning, parent:", self.parent, "copy?", self.copy)
        debug.print ("self:", self, "is_double_tap?", self.is_double_tap)
        debug.print ("on_drag_finish: ================================================================")
        self.opacity = 1.0
        drag_destination_list = []
        self.found_drop_recipients_ok_dict = {}
        # del self.drop_recipients[:]
        if self._dragged and self._draggable:
            # -------------------------------------------------------------------------
            # --- assemble list of possible drag destinations
            # These destinations are based on either drop groups, or simply because
            # they've been added to droppable_zone_objects
            # debug.print "on_drag_finish: DRAGGABLES_DICT:", draggables_dict
            for drop_group in draggables_dict:
                if draggables_dict[drop_group].get(self):
                    if drop_group in drag_destinations_dict:
                        for drop_recipient in drag_destinations_dict[drop_group]:
                            if not drop_recipient in drag_destination_list:
                                drag_destination_list.append(drop_recipient)
            for drop_group in drag_destinations_dict:
                if draggables_dict[drop_group].get(self):
                    for drop_recipient in drag_destinations_dict[drop_group]:
                        if not drop_recipient in drag_destination_list:
                            drag_destination_list.append(drop_recipient)
            for obj in self.droppable_zone_objects:
                if not obj in drag_destination_list:
                    drag_destination_list.append(obj)
            #for obj in drag_destination_list:
            #    debug.print ("Possible drop destination:", obj.text)
            # --- end of assemble list

            # -------------------------------------------------------------------------
            # --- check which object(s) did receive this drop.
            for obj in drag_destination_list:
                (touch_window_x, touch_window_y) = self.to_window(self.touch_x, self.touch_y)
                debug.print ("Check if drop ok: touch:", touch_window_x, touch_window_y, "Object's pos in Window:", obj.to_window(obj.x, obj.y), obj.width, obj.height, end=" ")
                # TODO: IF object does not subclass DropDestination, it won't have this
                # TODO: method defined!
                if self.widget_absolute_collide_point(obj, touch_window_x, touch_window_y):
                    debug.print ("COLLIDE: True", end=" ")
                    if obj is self._old_parent and not self.can_drop_into_parent:
                        self.found_drop_recipients_ok_dict[obj] = False
                        debug.print ("OK: False")
                    else:
                        self.found_drop_recipients_ok_dict[obj] = True
                        debug.print ("OK: True")
                else:
                    debug.print ("COLLIDE: False")
                    pass
            # --- end of check

            # -------------------------------------------------------------------------
            # - (Possibly) perform animations
            #   - if a drop recipient is found (could include the parent), and it's ok
            #     to drop there (parent may not be, so this could be false), then set
            #     - not_drop_ok_do_animation = False
            #     - got_one_successful_drop = True
            #     - drop_ok_do_animation = False (if dropped onto old parent)
            # - Run self.drop_func or self.failed_drop_func
            drop_ok_do_animation = self.drop_ok_do_animation
            not_drop_ok_do_animation = self.not_drop_ok_do_animation
            got_one_successful_drop = False
            got_one_drop_not_parent = False

            # -------------------------------------------------------------------------
            for found_drop_recipient, dropped_ok in self.found_drop_recipients_ok_dict.items():
                debug.print ("Drop Recipient:", found_drop_recipient, dropped_ok)
                if dropped_ok:
                    not_drop_ok_do_animation = False
                    got_one_successful_drop = True
                    if found_drop_recipient != self._old_parent:
                        # TODO: Animation runs when the widget is not added to the
                        # TODO: drop recipient. This is a problem, because the widget
                        # TODO: exists but is invisible!
                        # TODO: for app_relative_layout: If a copied widget is dragged,
                        # TODO: its original parent may be the Window (not a widget).
                        # TODO: Therefore, animation is running when we don't want it.
                        got_one_drop_not_parent = True

            if not got_one_drop_not_parent:
                drop_ok_do_animation = False

            # -------------------------------------------------------------------------
            # Perform after-drop functions
            if got_one_successful_drop:
                debug.print("I will call on_successful_drop")
                if drop_ok_do_animation:
                    anim = Animation(opacity=0, duration=self.drop_ok_animation_time, t="in_quad")
                    anim.bind(on_complete=self.post_successful_animation)
                    anim.start(self)
                    self.on_successful_drop()
                else:
                    self.on_successful_drop()
                    self.post_successful_animation()
                    return
            else:
                # TODO: Do we want to run the animation? MIKE check this... is it right
                # TODO: to be here???
                debug.print ("on_drag_finish:, I will call on_unsuccessful_drop")
                if not_drop_ok_do_animation:
                    anim = Animation(pos=self._old_drag_pos,
                                     duration=self.not_drop_ok_animation_time, t="in_quad")
                    anim.bind(on_complete = self.post_unsuccessful_animation)
                    anim.start(self)
                    self.on_unsuccessful_drop()
                else:
                    self.on_unsuccessful_drop()
                    self.post_unsuccessful_animation(False)  # Simply resets some flags; opacity will be set after the animation
            # On a successful drop, the widget will end up with no parent whatsoever.

            debug.print ("THE END. Drag finished, me:", self, "parent:", self.parent)

    def un_root_and_close(self, animation_object=None, same_as_self=None):
        self.un_root_me()
        self.close()

    def widget_absolute_collide_point(self, widget, x, y):
        (widget_x, widget_y) = widget.to_window(widget.x, widget.y)
        return widget_x <= x <= (widget.width + widget_x) and widget_y <= y <= (widget_y + widget.height)

    def un_root_me(self, widget="dumb", anim="dumb2"):
        debug.print ("Unroot start, parent: ", self.parent, "Me:", self)
        self.get_root_window().remove_widget(self)
        debug.print ("unroot done, parent: ", self.parent, "Me:", self)

    def on_being_dragged(self):
        pass

    def reborn(self, widget=None, anim=None):
        debug.print ("self.reborn(), old parent:", self._old_parent)
        self.un_root_me()
        # BUG: We don't just add the reborn child to the parent.
        # Adding child in the first position (the highest index) fails due
        # to a bug in Kivy. We remove all remaining children and then re-add
        # the bunch (including the original child which was not dropped in a new
        # area).
        for childs in self._old_parent.children[:]:
            self._old_parent.remove_widget(childs)
        for childs in self._old_parent_children_reversed_list:
            debug.print ("self.reborn(), add ", childs, "to", self._old_parent)
            self._old_parent.add_widget(childs)
        return
        #As of this moment, this code is unreachable- it's a placeholder.
        # See https://github.com/kivy/kivy/issues/4497
        self._old_parent.add_widget(self, index=self._old_index)

    def root_parent(self, widget):
        orig_size = widget.size
        if not self.remove_on_drag:
            self.root_window.add_widget(widget)
            return
        if widget.parent:
            parent = widget.parent
            parent.remove_widget(widget)
            parent.get_root_window().add_widget(widget)
            widget.size_hint = (None, None)
            widget.size = orig_size

    def on_unsuccessful_drop(self, animation=None, widget=None):
        """
        Called at the end of an unsuccessful drop, after the widget's animation is finished.
        :param animation:
        :param widget:
        :return:
        """
        if self.failed_drop_func is not None:
            self.failed_drop_func(self, *self.failed_drop_args)
        self.set_drag_finish_state(False)
        # TODO: CHECK THIS MIKE
        # self.post_unsuccessful_animation(False)

    def post_unsuccessful_animation(self, animation=None, widget=None):
        """
        A bit of a misnomer, this is called to clean up after any unsuccessful drop,
        but if there's an animation, it will be at the end of the animation.

        :param animation: the Animation object that called this, or nothing (not used)
        :param widget: the widget that this is run from, or nothing (not used)
        :return: nothing
        """
        if self.remove_on_drag:
            self.reborn()
        else:
            self.un_root_and_close()
        self.opacity = self._old_opacity


    # TODO: If a drop_func is defined, which runs first?
    # TODO: EACH _args for the funcs must have the calling widget!
    def on_successful_drop(self):
        """
        If we want an end-of-drop animation:
           Called at the end of a successful drop, after the widget's animation is finished.
        If we do not want an animation:
           Called immediately at the end of a successful drop.
        
        :param animation: the Animation object that called this, or nothing (not used)
        :param widget: the widget that this is run from, or nothing (not used)
        :return: nothing
        """
        debug.print ("on_successful_drop: ================================================================")
        debug.print ("on_successful_drop 1, Parent:", self.parent, "object: ", self, "copy?", self.copy)
        debug.print ("object:", self, "added args:", *self.drop_args)
        debug.print ("is_double_tap?", self.is_double_tap)
        #traceback.debug.print_stack()
        if self.drop_func is not None:
            debug.print (hex(id(self)), "Calling drop_func...")
            debug.print ("With args:", self, *self.drop_args)
            self.drop_func(self, *self.drop_args)
        for found_drop_recipient, dropped_ok in self.found_drop_recipients_ok_dict.items():
            if dropped_ok:
                if getattr(found_drop_recipient, "drop_func", None) is not None:
                    debug.print (hex(id(self)), "Calling recipient's drop_func")
                    found_drop_recipient.drop_func(self)
        self.set_drag_finish_state(False) # Opacity will be set after the animation.
        debug.print ("on_successful_drop: === end ========================================================")

    def post_successful_animation(self, animation=None, widget=None):
        """
        A bit of a misnomer, this is called to clean up after any successful drop,
        but if there's an animation, it will be at the end of the animation.
        :param animation:
        :param widget:
        :return:
        """
        debug.print ("post_successful_animation 1, Parent:", self.parent, "object: ", self, "copy?", self.copy)
        self.un_root_me()
        debug.print ("post_successful_animation 2, Parent:", self.parent, "object: ", self, "copy?", self.copy)
        self.opacity = self._old_opacity
        for found_drop_recipient, dropped_ok in self.found_drop_recipients_ok_dict.items():
            if dropped_ok:
                if getattr(found_drop_recipient, "post_drop_func", None) is not None:
                    found_drop_recipient.post_drop_func(self)


class DropDestination(Widget):
    motion_over_widget_func = ObjectProperty(None)
    motion_over_widget_args = ListProperty([])
    motion_flee_widget_func = ObjectProperty(None)
    motion_flee_widget_args = ListProperty([])
    motion_outside_widget_func = ObjectProperty(None)
    motion_outside_widget_args = ListProperty([])
    motion_inside_widget_func = ObjectProperty(None)
    motion_inside_widget_args = ListProperty([])
    drop_group = StringProperty(None)
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
        if self.drop_group is None:
            self.drop_group = "_palm_default"

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
        # debug.print "BINDING DROP GROUP"
        if self.drop_group not in drag_destinations_dict:
            drag_destinations_dict[self.drop_group]={}
        drag_destinations_dict[self.drop_group][self]=True

    def bind_mouse_motion(self, instance, value):
        # debug.print "DropDestination: BINDNG WIDGETS to Mouse Motion!", instance, value
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
        # debug.print "event x,y:", motionevent[0], motionevent[1], "self x,y,w,h:", self.x, self.y, self.width, self.height
        # debug.print "event x,y:", motionevent[0], motionevent[1], "self:", self
        # motionevent is in the main Window's coordinate system.
        # debug.print "Self.to_window:", self.to_window(self.x, self.y)
        # TODO: I believe I have compensated for any relative widget, here.
        # TODO: ...but be wary. I'm still not sure about how RelativeLayout will behave.
        if self.absolute_collide_point(motion_xy_tuple[0], motion_xy_tuple[1]):
            # debug.print motionevent[0], on_[1], "pointer collides DropDestination:", self
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
        (my_x, my_y)=self.to_window(self.x, self.y)
        (event_x, event_y) = self.to_window(x, y)
        # debug.print "absolute_collide_point:", self, "x,y,w,h:", my_x, my_y, self.right + my_x, my_y + self.top
        return my_x <= event_x <= (self.width + my_x) and my_y <= event_y <= (my_y + self.height)

    def on_motion_flee(self, motion_xy_tuple):
        """
        Called when your touch point leaves a draggable item.
        :return:
        """
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
        :return:
        """
        # debug.print "DropDestination: MOTION over", motion_xy_tuple
        if self.motion_over_widget_func is not None:
            self.motion_over_widget_func(self, self.motion_over_widget_args)
            # self.easy_access_dnd_function_binds)
        # else:
        #    debug.print "FUNCTION MOTION OVER NONE"

    def on_motion_outside(self, motion_xy_tuple):
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
        # debug.print "on_motion_inside: DropDestination INSIDE"
        try:
            if self.motion_inside_widget_func is not None:
                self.motion_inside_widget_func(self, self.motion_inside_widget_args)
            else:
                pass
                # debug.print "FUNCTION OUT NONE"
        except AttributeError:
            pass
