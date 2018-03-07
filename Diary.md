Events during a drag:

`self._draggable` is always true but can be set to False by a user's direct action.
`self.am_touched` set True if touch lingers or it's a double tap
`self.remove_on_drag` set by user

set in set_drag_start_state (called from on_drag_start):
`self._move_counter` set to 0
`self._old_opacity` set to self.opacity
`self.opacity` set to self.drag_opacity
`self._old_drag_pos` set to self.pos
`self._old_parent` set to self.parent
`self._old_parent_children_reversed_list` set to self.parent.children[:].reverse()
`DragNDropWidget.widget_entered` set to None
`self._old_index` set to -1 if a copy, otherwise set to self.parent.children.index(self)
`self._dragged` set to True
# `self._drag_started` set to True DEPRECATED! self._dragged has exactly the same purpose!
``

on_touch_down- If collide_point and self._draggable
    - If touch lingers for > 0.2s, or touch.is_double_tap:
        - self.am_touched = True

on_touch_move-
    - If the widget.am_touched:
        - If not widget._dragged:
            widget.dispatch("on_drag_start")
    - If not widget._drag_started, return
    - widget._move_counter++
    - widget._draggable && widget._drag_started:
        - widget._dragged = True
        - Move the widget
        - If it collides and is in the drop_group,
          Call the drag_destination.while_dragging_func

