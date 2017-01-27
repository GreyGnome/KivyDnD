# KivyDnD
Python library for the Kivy framework that enables drag-n-drop of widgets.

This work is an update of Pavel Kostelnik's code found on:
http://kostasprogramming.blogspot.cz/2012/10/kivy-framework-drag-n-drop-widget.html
He did a great job, in my opinion, and got us almost all the way there. I needed
a drag-and-drop framework and decided to build on his work. While doing this,
I found Pavel and he agreed to release the library under the Apache 2.0 license.

Meanwhile, I (Mike Schwager) updated his work. I removed a significant bug that
made it unusable, and made a number of other fixes.

My mods are listed at the end of this README.

# Usage:

Create a subdirectory somewhere alongside your executable. Put all the
files in this repo into that subdirectory. Import the DragNDropWidget.py
file. That is, assuming that I have a subdirectory "DragNDropWidget" wherein
I have the file "DragNDropWidget.py", place in your python file:

import DragNDropWidget.DragNDropWidget


# API

Your widget must subclass DragNDropWidget.

```Python
class DraggableButton(Button, DragNDropWidget):
    pass
```

Properties:
* droppable_zone_objects:
  * a list of IDs of objects that you can drop widgets of this class into
* bound_zone_objects:
  * a list of objects that create a boxed-in boundary where the widget cannot be dragged past.
* drag_opacity:
  * a real number between 0.0 and 1.0 that defines the opacity of the widget while it is dragged.
* drop_func:
  * the name of a function that will be called upon a successful drop
* drop_args:
  * a list which are given as the arguments to the function
* failed_drop_func:
  * the name of a function that will be called upon an unsuccessful drop
* failed_drop_args:
  * a list which are given as the arguments to the function
* remove_on_drag:
  * Boolean. If True, the widget is removed from the parent widget (perhaps a layout of some sort) and added to the destination widget. It will be re-added to the parent, in its old position, if the object is not dragged elsewhere. If False, a copy of the widget is made and that copy is added to the destination. If the object is not dragged elsewhere the copy is destroyed.
* drop_ok_animation_time:
  * When it's dropped the object is faded away. This is the duration of that fade. Defaults to 0.7s.
* not_drop_ok_animation_time:
  * If the object is not dragged elsewhere, this is the duration of the fade animation. Defaults to 0.7s.

# Additional Capabilities and Notes:

You can have a number of widgets stacked on top of each other as drop recipients.

Upon a successful drop, if the destination widget has a function
literally called "drop_func", then that function is called with the
dragged object as its argument.

If you cover a drop destination widget with another widget that is not a
drop destination, that widget will prevent the underlying drop
destination from receiving a drop anywhere in the rectangle coordinates
of the covering widget.

========================================================================
Schwager's mods to DragNDropWidget.py

- Added Properties:
  failed_drop_func
  failed_drop_args
  drop_ok_animation_time
  not_drop_ok_animation_time

- changed the spelling of "dragable" to "draggable". Because it's
  "dragged" and not "draged". And "dragging", not "draging".
  Just sayin'.

- Created function set_drag_start_state

- A drag doesn't start until a touch occurs AND it's followed by a move
  (thus, an immediate touch_up will negate the drag). This prevents the
  drag code from running unless the item is really being dragged.
  Could be important when you're trying to understand your event
  propagation.

- A widget is picked up and moved with the mouse at the point at which
  it's touched. It used to be that widgets were positioned so that the
  lower left-hand corner always jumped up to the mouse, which
  was unnatural looking.

- Fixed a bug that crashed the code upon drop.

- When dragging a non-removable widget, the original is left in place and
  a copy is actually dragged around. This is more to one's expectations,
  I believe.

- There is a Kivy bug that when removing the leftmost of the children of
  a widget, if you try to re-insert the child back into its former place
  at the beginning of the child list, it is not actually displayed on
  the screen. So rather than re-adding a dragged child whose drag was not
  completed, I am removing all widgets and re-adding them in order, as a
  workaround.

  The bug holds true for any Layout widgets.

- If the user defines a function in their widget destination called
  drop_func, it will be called by any DnD widget that gets dropped onto
  the widget destination.


