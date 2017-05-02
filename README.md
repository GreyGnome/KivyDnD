# KivyDnD
Python library for the Kivy framework that enables drag-n-drop of widgets. Source code is here: https://github.com/GreyGnome/KivyDnD .

This work is an update of Pavel Kostelnik's master thesis code found on:
http://kostasprogramming.blogspot.cz/2012/10/kivy-framework-drag-n-drop-widget.html
He did a great job and created a solid foundation. I needed a drag-and-drop framework and decided to build on his work. While doing this, I found Pavel and he agreed to release the library under the Apache 2.0 license.

Meanwhile, the current maintainer (moi!) made a number of other modifications. They are listed at the end of this README.

# Version

This is version 0.1. This is Beta software, use at your own peril (or delight?). Previous releases were not versioned.

# License

Distributed under the Apache 2.0 License. See the LICENSE file for more information.

# Simple Usage:

Create a subdirectory somewhere alongside your executable. Put all the files in this repo into that subdirectory. Import the dragndropwidget.py file, then your widget must subclass `DragNDropWidget`. Example: assume
* that I have a subdirectory "dragndropwidget" wherein
* I have the file "dragndropwidget.py", then place in your python file:

```Python
from dragndropwidget.dragndropwidget import DragNDropWidget

class DraggableButton(Button, DragNDropWidget):
    <do Button-y stuff>
```
Alternatively, you could simply import the dragndropwidget file, in which case you'd need to be specific about your subclassing. That is:

```Python
# Here's the directory and module
import dragndropwidget.dragndropwidget

class DraggableButton(Button, dragndropwidget.dragndropwidget.DragNDropWidget):
```

See `dndapp2.py` for a fairly complete working example. NOTE: Currently obsolete, this works with the earliest unversioned release, but currently not with 0.1 or higher. Use it as a general guide for now.

For more information, see Detailed Usage below.
# Support
This software is delivered without a warranty, and not even a guarantee that it will work as advertised. If you encounter a bug, please
* Send me a fix. This is best. If you can't,
* Create a small- wery small- app that demonstrates the anomalous behavior you observe.
Finally,
* Realize that I've got a day job and this class is being used for an app that I'm building on my own time. That app takes the lion's share of my attention. Your bug may not be addressed for weeks or months. I'm sorry, but if this dissatisfies you then please do not use this module.

# API

## Classes:
* `DragNDropWidget`
  * Your draggable widget must subclass this class.
* `DropDestination`
  * This is designed to be optional. This is an object that receives a DragNDropWidget. Use this if you want to:
    * Have the destination perform actions while an item is being dragged or dropped, or
    * Organize widgets into "drop groups", meaning that certain widgets are restricted to being dropped only onto other widgets in their group.

## DragNDropWidget
### Methods
These are all ObjectProperties (the methods) or ListProperties (the args). Each Method has a ListProperty that accompanies it, named with an "args" suffix rather than "func". For example, `failed_drop_func` has `failed_drop_args` and so on. The one exception is `while_dragging_func`; there is no `while_dragging_args`.
* `drop_func`
  * If defined in your DragNDropWidget subclass, this function is called on a successful drop.
  * If defined in the object being dropped onto, a function by this name will be called when a droppable object is dropped onto it.
* `while_dragging_func`
  * If set, this is called continuously as the widget is being dragged.
* `failed_drop_func`
  * If defined in your DragNDropWidget subclass, this function will be called if you drop it onto a non-droppable widget. It's also called if you drop the DragNDropWidget onto its old parent and `can_drop_into_parent` is `False`.

If you assign any of these `on_motion_...` functions, on_motion events are bound to the kivy.core.Window (the main Window that encloses your Kivy program). on_motion events are dispatched with each move of the pointer.

Subsequently, one of three events may then be dispatched by an on_motion event, depending on if you assign a function to these Properties:
* `on_motion_over` when the pointer crosses from outside the widget to inside the widget,
* `on_motion_flee` when the pointer cross out frem inside the widget,
* `on_motion_outside` if the pointer is moved anywhere outside the bounds of the widget. This can be quite chatty, as it's called for all DragNDropWidgets that are bound to on_motion events.

* `motion_over_widget_func`
  * If defined in your DragNDropWidget subclass, this function will be called whenever the pointer enters into the widget. It is called once, upon entry.
* `motion_flee_widget_func`
  * If defined in your DragNDropWidget subclass, this function will be called whenever the pointer leaves the widget. It is called once, upon crossing out of the widget.
* `motion_outside_widget_func`
  * If defined in your DragNDropWidget subclass, this function will be called for all pointer motions that are not inside each and every widget that defines this function. Of course, it will not be called on the widget you are currently inside, if you are currently inside one.
* `drag_start_func`
  * If defined in your DragNDropWidget subclass, this function is called when the widget senses that a drag has begun.
* `drop_func`
  * The name of a function that will be called upon a successful drop.
* `failed_drop_func`
  * The name of a function that will be called upon an unsuccessful drop.

### Properties:
* `droppable_zone_objects`
  * ListProperty: IDs of objects that you can drop widgets of this class onto (called a "drop destination"). You can use this and/or `drop_group` to specify drop destinations.
* `bound_zone_objects`
  * ListProperty: a list of objects that create a boxed-in boundary where the widget cannot be dragged past.
* `drag_opacity`
  * NumericProperty a real number between 0.0 and 1.0 that defines the opacity of the widget while it is dragged.
* `remove_on_drag`
  * BooleanProperty. If True, the widget is removed from the parent widget (perhaps a layout of some sort) and added to the destination widget. It will be re-added to the parent, in its old position, if the object is not dragged elsewhere. If False, a copy of the widget is made and that copy is added to the destination. If the object is not dragged elsewhere the copy is destroyed.
* `drop_ok_animation_time`
  * NumericProperty When it's dropped the object is faded away. This is the duration of that fade. Defaults to 0.7s.
* `not_drop_ok_animation_time`
  * NumericProperty If the object is not dragged elsewhere, this is the duration of the fade animation. Defaults to 0.7s.
* `can_drop_into_parent`
  * BooleanProperty If the object is allowed to drop back onto its parent, just as if it was dropped onto a non-parent widget. Note that the parent must be designated as a drop destination or member of a drop_group. If not, the widget will not be droppable onto the parent no matter the setting of this property.
* `drop_group`
  * StringProperty This is a string of your choosing. DragNDropWidgets of this drop_group will be able to be dropped onto DropDestination widgets that are also members of this drop_group. If you use `drop_group` then `droppable_zone_objects` are not recommended.

# Detailed Usage:
TODO: Create examples.

In addition to the simple usage given above, the module has additional capabilities. In the simplest case you would set `droppable_zone_objects` and those are the objects you can drop into. However, you can assign DragNDropWidget's to a `drop_group`, which is a Kivy StringProperty. Accordingly you must subclass a drop destination to the DropDestination class, and then assign it a drop_group. Your dragged widget, then, will only be droppable onto widgets in `drop_group`

There are a number of Kivy Properties available.
# Additional Capabilities and Notes:

You can have a number of widgets stacked on top of each other as drop recipients.

If you cover a drop destination widget with another widget that is not a
drop destination, that widget will prevent the underlying drop
destination from receiving a drop anywhere in the rectangle coordinates
of the covering widget.

---
# Bugs

Besides the ones I don't know about:

* There is a Kivy bug that when removing the leftmost of the children of a widget, if you try to re-insert the child back into its former place at the beginning of the child list, it is not actually displayed on the screen. So rather than re-adding a dragged child whose drag was not completed, I am removing all widgets and re-adding them in order, as a workaround.
  * The bug holds true for any Layout widgets.
