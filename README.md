# KivyDnD
Python library for the Kivy framework that enables drag-n-drop of widgets.

This work is an update of Pavel Kostelnik's master thesis code found on:
http://kostasprogramming.blogspot.cz/2012/10/kivy-framework-drag-n-drop-widget.html
He did a great job, in my opinion, and got us almost all the way there. I needed a drag-and-drop framework and decided to build on his work. While doing this, I found Pavel and he agreed to release the library under the Apache 2.0 license.

Meanwhile, I (Mike Schwager) removed a significant bug that made it unusable, and made a number of other modifications. They are listed at the end of this README.

# License

Distributed under the Apache 2.0 License. See the LICENSE file for more information.

# Usage:

Create a subdirectory somewhere alongside your executable. Put all the files in this repo into that subdirectory. Import the DragNDropWidget.py file, then your widget must subclass `DragNDropWidget`. Example: assume
* that I have a subdirectory "DragNDropWidget" wherein
* I have the file "DragNDropWidget.py", then place in your python file:

```Python
from DragNDropWidget.DragNDropWidget import DragNDropWidget

class DraggableButton(Button, DragNDropWidget):
    <do Button-y stuff>
```

See `dndapp2.py` for a fairly complete working example.

Alternatively, you could simply import the DragNDropWidget file, in which case you'd need to be specific about your subclassing. That is:
```Python
# Here's the directory and module
import DragNDropWidget.DragNDropWidget

# The class is inside it. Ew, ugly...
class DraggableButton(Button, DragNDropWidget.DragNDropWidget.DragNDropWidget):
```
...that's a lot of `DragNDropWidget`'ing.

# Support
This software is delivered without a warranty, and not even a guarantee that it will work as advertised. If you encounter a bug, please
* Send me a fix. This is best. If you can't,
* Create a small- wery small- app that demonstrates the anomalous behavior you observe.
Finally,
* Realize that I've got a day job and this class is being used for an app that I'm building on my own time. That app takes the lion's share of my attention. Your bug may not be addressed for weeks or months. I'm sorry, but if this dissatisfies you then please do not use this class.

# API

## Classes:
* `DragNDropWidget`
  * the only class in this library. Your draggable widget must subclass this class.

## Methods:
* `drop_func`
  * this function is called from the object being dropped onto, if it's defined, when a droppable object is dropped onto it.
* `failed_drop_func`
  * this function is called from the droppable object, if you release it onto a non-droppable widget.
* `easy_access_dnd(function_to_do, function_to_do_out, arguments, bind_functions)`
  * UNTESTED. If you use this, please help complete/update/correct this documentation!
  * Therefore, I don't know what the purpose of this is. But I do know,
  * If you call this function, on_motion events are bound to the kivy.core.Window (whatever that is). One of two events may then be dispatched whenever an on_motion event is dispatched: on_motion_over (when the on_motion event takes place inside the widget), or on_motion_out (event is outside the widget).  When assigned functions using this method, the `function_to_do` will be called whenever there is an on_motion_over event. `function_to_do_out` will be called whenever an on_motion_out event occurs. If on_motion_over is utilized, then it is given the arguments `arguments` and `bind_functions`.

## Properties:
* `droppable_zone_objects`
  * a list of IDs of objects that you can drop widgets of this class into
* `bound_zone_objects`
  * a list of objects that create a boxed-in boundary where the widget cannot be dragged past.
* `drag_opacity`
  * a real number between 0.0 and 1.0 that defines the opacity of the widget while it is dragged.
* `drop_func`
  * the name of a function that will be called upon a successful drop
* `drop_args`
  * a list which are given as the arguments to the function
* `failed_drop_func`
  * the name of a function that will be called upon an unsuccessful drop
* `failed_drop_args`
  * a list which are given as the arguments to the function
* `remove_on_drag`
  * Boolean. If True, the widget is removed from the parent widget (perhaps a layout of some sort) and added to the destination widget. It will be re-added to the parent, in its old position, if the object is not dragged elsewhere. If False, a copy of the widget is made and that copy is added to the destination. If the object is not dragged elsewhere the copy is destroyed.
* `drop_ok_animation_time`
  * When it's dropped the object is faded away. This is the duration of that fade. Defaults to 0.7s.
* `not_drop_ok_animation_time`
  * If the object is not dragged elsewhere, this is the duration of the fade animation. Defaults to 0.7s.

# Additional Capabilities and Notes:

You can have a number of widgets stacked on top of each other as drop recipients.

Upon a successful drop, if the destination widget has a function
literally called `drop_func`, then that function is called with the
dragged object as its argument.

If you cover a drop destination widget with another widget that is not a
drop destination, that widget will prevent the underlying drop
destination from receiving a drop anywhere in the rectangle coordinates
of the covering widget.

---
# Schwager's mods to DragNDropWidget.py

* Added Properties:
``` Python
failed_drop_func
failed_drop_args
drop_ok_animation_time
not_drop_ok_animation_time
```

* Changed the spelling of "dragable" to "draggable". Because it's "dragged" and not "draged". And "dragging", not "draging".  Just sayin'.

* Created function `set_drag_start_state`

* A drag doesn't start until a touch occurs AND it's followed by a move (thus, an immediate `touch_up` will negate the drag). This prevents the drag code from running unless the item is really being dragged.  Could be important when you're trying to understand your event propagation.

* A widget is picked up and moved with the mouse at the point at which it's touched. It used to be that widgets were positioned so that the lower left-hand corner always jumped up to the mouse, which was unnatural looking.

* Fixed a bug that crashed the code upon drop.

* When dragging a non-removable widget, the original is left in place and a copy is actually dragged around. This is more to one's expectations, I believe... the widget is non-removable so, well, it's never removed. The copy is truly a copy (a new object), the original retains its identifier; no surprises.

* There is a Kivy bug that when removing the leftmost of the children of a widget, if you try to re-insert the child back into its former place at the beginning of the child list, it is not actually displayed on the screen. So rather than re-adding a dragged child whose drag was not completed, I am removing all widgets and re-adding them in order, as a workaround.
  * The bug holds true for any Layout widgets.

* If the user defines a function in their widget destination called `drop_func`, it will be called by any DnD widget that gets dropped onto the widget destination.

