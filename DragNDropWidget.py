#!/usr/bin/python
# -*- coding: UTF-8 -*-
# Modified by Mike Schwager
from kivy.core.window import Window
from kivy.animation import Animation
import copy
from kivy.uix.widget import Widget
from kivy.properties import (
    ListProperty, NumericProperty, BooleanProperty, ObjectProperty)


class DragNDropWidget(Widget):
    # let kivy take care of kwargs and get signals for free by using
    # properties
    droppable_zone_objects = ListProperty([])
    bound_zone_objects = ListProperty([])
    drag_opacity = NumericProperty(1.0)
    drop_func = ObjectProperty(None)
    drop_args = ListProperty([])
    failed_drop_func = ObjectProperty(None)
    failed_drop_args = ListProperty([])
    remove_on_drag = BooleanProperty(True)
    drop_ok_animation_time = NumericProperty(0.5)
    not_drop_ok_animation_time = NumericProperty(0.2)

    def __init__(self, **kw):
        super(DragNDropWidget, self).__init__(**kw)

        self.register_event_type("on_drag_start")
        self.register_event_type("on_being_dragged")
        self.register_event_type("on_drag_finish")
        self.register_event_type("on_motion_over")
        self.register_event_type("on_motion_out")
        self._old_opacity = self.opacity
        self._drag_started = False
        self._dragged = False
        self._draggable = True
        self._fired_already = False
        self.copy = False
        self.touch_offset_x = 0
        self.touch_offset_y = 0
        self.drop_recipients = []
        self.am_touched = False
        if not self.drop_func:
            self.drop_func = self.drop_function

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
        if self.copy:
            self._old_index = -1
        else:
            self._old_index = self.parent.children.index(self)
        self._drag_started = True

    def set_drag_finish_state(self):
        self._drag_started = False
        self.opacity = self._old_opacity

    def set_bound_axis_positions(self):
        for obj in self.bound_zone_objects:
            try:
                if self.max_y < obj.y+obj.size[1]-self.size[1]:
                    self.max_y = obj.y+obj.size[1]-self.size[1]
            except AttributeError:
                self.max_y = obj.y+obj.size[1]-self.size[1]
            try:
                if self.max_x < obj.x+obj.size[0]-self.size[0]:
                    self.max_x = obj.x + obj.size[0]-self.size[0]
            except AttributeError:
                self.max_x = obj.x+obj.size[0]-self.size[0]
            try:
                if self.min_y > obj.y:
                    self.min_y = obj.y
            except AttributeError:
                self.min_y = obj.y
            try:
                if self.min_x > obj.x:
                    self.min_x = obj.x
            except AttributeError:
                self.min_x = obj.x

    def on_touch_down(self, touch):

        if self.collide_point(touch.x, touch.y) and self._draggable:
            # detect if the touch is short - has time and end (if not dispatch drag)
            if abs(touch.time_end - touch.time_start) > 0.2:
                self.touch_offset_x = touch.x - self.x
                self.touch_offset_y = touch.y - self.y
                self.am_touched = True

    def on_touch_up(self, touch):
        if self.am_touched:
            self.am_touched = False
        if self._draggable and self._dragged:
            self.short_touch = True
            self.touch_x = touch.x
            self.touch_y = touch.y
            self.dispatch("on_drag_finish")
            self.short_touch = False
        else:
            self.opacity = self._old_opacity


    def on_touch_move(the_widget, touch):
        if the_widget.am_touched:
            if not the_widget._drag_started:
                the_widget.dispatch("on_drag_start")
                the_widget.am_touched = False

        if not the_widget._drag_started:
            return
        the_widget._move_counter += 1
        if the_widget._draggable and the_widget._drag_started:
            # if the_widget._dragged and the_widget._draggable:
            the_widget._dragged = True
            x = touch.x - the_widget.touch_offset_x
            y = touch.y - the_widget.touch_offset_y

            try:
                if x <= the_widget.min_x:
                    x = the_widget.min_x
                if x > the_widget.max_x:
                    x = the_widget.max_x
                if y <= the_widget.min_y:
                    y = the_widget.min_y
                if y > the_widget.max_y:
                    y = the_widget.max_y
            except AttributeError:
                pass
            the_widget.pos = (x, y)
            # SPECIAL! Takes a herky-jerky GUI and makes it smoooooth....
            the_widget.canvas.ask_update()



    def easy_access_dnd(self, function_to_do, function_to_do_out, arguments = [], bind_functions = []):
        """
        This function enables something that can be used instead of drag n drop
        @param function_to_do: function that is to be called when mouse_over event is fired on the widget
        @param bind_functions: what is really to be done - background function for GUI functionality
        """
        Window.bind(mouse_pos=self.on_motion)
        self.easy_access_dnd_function = function_to_do
        self.easy_access_dnd_function_out = function_to_do_out
        self.easy_access_dnd_function_arguments = arguments
        self.easy_access_dnd_function_binds = bind_functions

    def on_motion(self, etype, moutionevent):
        if self.collide_point(Window.mouse_pos[0], Window.mouse_pos[1]):
            if not self._fired_already:
                self.dispatch("on_motion_over")
        else:
            self.dispatch("on_motion_out")

    def on_motion_over(self):
        self.easy_access_dnd_function(
            self.easy_access_dnd_function_arguments,
            self.easy_access_dnd_function_binds)

        self._fired_already = True

    def on_motion_out(self):
        try:
            self.easy_access_dnd_function_out()
        except AttributeError:
            pass
        self._fired_already = False

    def deepen_the_copy(self, copy_of_self):
        copy_of_self.copy = True
        copy_of_self.parent = self.parent
        copy_of_self.droppable_zone_objects = self.droppable_zone_objects
        copy_of_self.nbound_zone_objects = self.bound_zone_objects
        copy_of_self.drag_opacity = self.drag_opacity
        copy_of_self.drop_func = self.drop_func
        copy_of_self.drop_args = self.drop_args
        copy_of_self.failed_drop_func = self.failed_drop_func
        copy_of_self.failed_drop_args = self.failed_drop_args
        copy_of_self.remove_on_drag = self.remove_on_drag
        copy_of_self.drop_ok_animation_time = self.drop_ok_animation_time
        copy_of_self.not_drop_ok_animation_time = self.not_drop_ok_animation_time
        copy_of_self.touch_offset_x = self.touch_offset_x
        copy_of_self.touch_offset_y = self.touch_offset_y
        copy_of_self.drop_recipients = self.drop_recipients
        copy_of_self.droppable_zone_objects = self.droppable_zone_objects
        copy_of_self.bound_zone_objects = self.bound_zone_objects
        copy_of_self.drag_opacity = self.drag_opacity
        copy_of_self.drop_func = self.drop_func
        copy_of_self.remove_on_drag = self.remove_on_drag

    def on_drag_start(self):
        if self._drag_started:
            return
        # self._dragged = True
        if not self.remove_on_drag:
            #create copy of object to drag
            copy_of_self = copy.deepcopy(self)
            # We'll handle those variables that are common to ALL d-n-d
            # widgets. The widgets' classes can handle specifics
            # (such as text, etc.)
            self.deepen_the_copy(copy_of_self)

            copy_of_self.set_drag_start_state()
            copy_of_self.root_window = self.parent.get_root_window()
            ## the final child class MUST implement __deepcopy__
            ## IF self.remove_on_drag == False !!! In this case this is
            ## met in draggableArhellModelImage class
            # TODO: MIKE: it used to be that copy_of_self was added to _old_parent
            # self._old_parent.add_widget(copy_of_self, index=self._old_index)
            copy_of_self.root_parent(copy_of_self)
            copy_of_self.pos = self.pos
        else:
            self.set_drag_start_state()
            self.root_window = self.parent.get_root_window()
            self.root_parent(self)


    def on_drag_finish(self):
        # Don't worry, opacity will be properly set in set_drag_finish_state*)
        # after the animation
        self.opacity = 1.0
        del self.drop_recipients[:]
        if self._dragged and self._draggable:
            dropped_ok = False
            for obj in self.droppable_zone_objects:
                if obj.collide_point(self.touch_x, self.touch_y):
                    self.drop_recipients.append(obj)
                    if obj is self._old_parent:
                        dropped_ok = False
                    else:
                        dropped_ok = True
            if dropped_ok:
                self.drop_func(*self.drop_args)
                for obj in self.drop_recipients:
                    if "drop_func" in dir(obj):
                        obj.drop_func(self)
                anim = Animation(opacity=0, duration=self.drop_ok_animation_time, t="in_quad")
                anim.bind(on_complete=self.un_root_parent)
                anim.start(self)
            else:
                self.failed_drop_func(*self.failed_drop_args)
                anim = Animation(pos=self._old_drag_pos, duration=self.not_drop_ok_animation_time,
                                 t="in_quad")
                if self.remove_on_drag:
                    anim.bind(on_complete = self.reborn)
                else:
                    anim.bind(on_complete = self.un_root_parent)
                anim.start(self)
            self._dragged = False
            self.set_drag_finish_state()

    def un_root_parent(self, widget="dumb", anim="dumb2"):
        self.get_root_window().remove_widget(self)

    def on_being_dragged(self):
        pass

    def reborn(self, widget, anim):
        self.un_root_parent()
        # BUG: We don't just add the reborn child to the parent.
        # Adding child in the first position (the highest index) fails due
        # to a bug in Kivy. We remove all remaining children and then re-add
        # the bunch (including the original child which was not dropped in a new
        # area).
        for childs in self._old_parent.children[:]:
            self._old_parent.remove_widget(childs)
        for childs in self._old_parent_children_reversed_list:
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

    def drop_func(self, *args):
        pass
