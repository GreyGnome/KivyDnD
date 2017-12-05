# KivyDnD
NOTE: Version 0.3 brought some file rearrangement. Check the examples for the new
directory name and usage.

Python library for the Kivy framework that enables drag-n-drop of widgets. Source code is here:
https://github.com/GreyGnome/KivyDnD .

This work is an update of Pavel Kostelnik's master thesis code found on:
http://kostasprogramming.blogspot.com/2012/10/kivy-framework-drag-n-drop-widget.html
He did a great job and created a solid foundation. I needed a drag-and-drop
framework and decided to build on his work. While doing this, I found Pavel and he
agreed to release the library under the Apache 2.0 license.

Additional coding by Edvardas Dlugauskas: Significant restructuring of the project,
added setup.py functionality, general code cleanup. It's nice to have another pair
of eyes on the project. Thanks, Edvardas!
# Description
## DragNDropWidget
A widget subclassed from this class will be able to be picked up and moved
around in the main window, then dropped onto other chosen widgets. Then,
defined functions can be run in response.
## DropDestination
Using DropDestination is optional. It adds two features to the library: drop groups, and 
the ability to fire events when the pointer enters and leaves the boundaries of these
Widgets. Drop groups allow control over which widget(s) can receive a drop from particular
DragNDropWdidget(s). Though the DragNDropWidget can define who
its recipients will be (see `droppable_zone_objects` in the example below),
a draggable widget in a drop group can only be dropped into widgets
in its same drop group. You can have multiple drop groups, any DragNDropWidget can be a
member of multiple drop groups, and any DropDestination can be a member of multiple drop
groups. Another feature is that a DropDestination can fire an event when the pointer enters
its boundaries, and when it leaves. See the code for more information. 

# Usage
Extract the package, and cd into the dragndropwidget diretory. Then run:
`sudo python setup.py`

Or (the old-fashioned way):

Create a subdirectory somewhere alongside your executable. Put all the files in this repo
into that subdirectory. Import the dragndropwidget.py file, then your widget must subclass
`DragNDropWidget`. Example: assume
* that I have a subdirectory "kivydnd" wherein
* I have the file "dragndropwidget.py",
then place in your python file:
```PythonStub
from kivydnd.dragndropwidget import DragNDropWidget

class DraggableButton(Button, DragNDropWidget):
    def __init__(self, **kw):
        super(DraggableButton, self).__init__(**kw)
```
Alternatively, you could simply import the dragndropwidget file, in which case you'd need to be
specific about your subclassing. That is:

```Python
# Here's the directory and module
import kivydnd.dragndropwidget

class DraggableButton(Button, kivydnd.dragndropwidget.DragNDropWidget):
    def __init__(self, **kw):
        super(DraggableButton, self).__init__(**kw)
```
In your .kv file (or Kivy language code section), include a declaration of
your DragNDropWidget which defines the `drop_func` and `failed_drop_func`
(if you want). Objects that are able to be dropped onto must have an id
defined. The id will match one of the id's listed in `droppable_zone_objects`.
```
    DraggableButton:
        text: 'Button 1'
        droppable_zone_objects: [id_of_a_widget]
        drop_func: app.greet
        failed_drop_func: app.oops
        size_hint: None, None
        size: 100, 100 
```

You can define a directory in your `sys.path` and put the library file there:

```PythonStub
sys.path.append("/path/to/directory/containing/dragndropwidget.py")

from dragndropwidget import DragNDropWidget
```

You can find the already-defined directories in your `sys.path` and put the library file there:

*(run python on your command line, then...)*
```PythonStub
from __future__ import print_function
import sys
print ('\n'.join(sys.path))
```
...choose one of the directories that are printed, probably something like
`/usr/lib/python3.5/site-packages` or `/usr/lib/python2.7/site-packages` or the like.
Copy the `dragndropwidget.py` file there.

## Member Summary
### DragNDropWidget
|Member Name |  Type(default value) | Description |
--- | --- |---
| **Properties** |  |  |
| droppable_zone_objects | ListProperty([]) | List of widgets that accept a drop of this widget. |
| bound_zone_objects | ListProperty([]) | List of widgets; this widget cannot be dragged outside of the limits given by the outside boundaries of all the widgets in this list. See "dndapp2.py" for an example. |
| drag_opacity | NumericProperty(1.0) | Opacity of this widget during a drag. |
| drop_args  | ListProperty([]) | List of additional arguments given to drop_func. Note that this widget is always given as the first argument to drop_func (after `self`). |
| failed_drop_args | ListProperty([]) | List of additional arguments given to drop_func. Note that this widget is always given as the first argument to failed_drop_func (after `self`). |
| remove_on_drag | BooleanProperty(True) | Whether this widget should be removed upon a drag. Else a copy will be made. |
| drop_ok_do_animation | BooleanProperty(True) | Whether a fade animation should be performed at the end of a successful drag-n-drop. |
| drop_ok_animation_time | NumericProperty(0.5) | How long the fade should take place. |
| not_drop_ok_do_animation | BooleanProperty(True) | Whether a fade animation should take place after an unsuccessful drag. Note that by default no animation will take place if the widget is dropped back onto parent. |
| not_drop_ok_animation_time | NumericProperty(0.2) | How long the fade should take place. |
| motion_over_widget_args | ListProperty([]) | List of arguments given to motion_over_widget_func (after `self`). |
| motion_flee_widget_args | ListProperty([]) | List of arguments given to motion_over_widget_func (after `self`). |
| motion_outside_widget_args | ListProperty([]) | List of arguments given to motion_outside_widget_func (after `self`). |
| drag_start_args | ListProperty([]) | List of arguments given to drag_start_func (after `self`). |
| can_drop_into_parent | BooleanProperty(False) | Whether a drag-n-drop of the widget back onto its parent counts as a successful drop or not. If a widget's parent is a drop destination for this widget, a drag-n-drop will not be successful there unless this is set. |
| drop_group | StringProperty(None) | A StringProperty that you define, this is a name you assign to a group of widgets that can receive a drop from this widget. Can be used instead of, or in addition to, `droppable_zone_objects`. If used, Widgets in this drop group must subclass `DropDestination`. They must also be added to the 'drop_group' StringProperty in that object. |
| **Methods** | arguments |  |
| drop_func | self, drop_args | The user-defined method or function that will be run at the end of a successful drop. |
| while_draggingn_func | self, MouseMotionEvent | The user defined method or function that will be run as the widget is dragged. |
| failed_drop_func | self, failed_drop_args | The user-defined method or function that will be run at the end of a failed drop. |
| motion_over_widget_func | self, motion_over_widget_args | The user-defined method or function that will be run when the pointer enters the boundaries of this widget. |
| motion_flee_widget_func | self, motion_flee_widget_args | The user-defined method or function that will be run when the pointer leaves this widget, after previously having entered the widget. |
| motion_outside_widget_func | self, motion_outside_widget_args | The user-defined method or function that will be run as long as the pointer is outside this widget. Can be quite chatty. |
| drag_start_func | self, drag_start_args | The user-defined method or function that will be run at the beginning of a drag. If the widget is not removed on drag, then the copied object's drag_start_func is run. |
### DropDestination
| **Properties** | Type(default value) | Description |
--- | --- | ---
| motion_over_widget_args | ListProperty([]) | List of arguments given to motion_over_widget_func (after `self`). |
| motion_flee_widget_args | ListProperty([]) | List of arguments given to motion_flee_widget_func (after `self`). |
| motion_outside_widget_args | ListProperty([]) | List of arguments given to motion_outside_widget_func (after `self`). | |
| motion_inside_widget_args | ListProperty([]) | List of arguments given to motion_inside_widget_func (after `self`). | |
| drop_group | StringProperty(None) | A StringProperty that you define, this is a name you assign to a group of widgets that can receive a drop from DragNDropWidget's in the same drop_group. Can be used instead of, or in addition to, `droppable_zone_objects`, which would be defined in a DragNDropWidget object. |
| **Methods** | arguments |  |
| motion_over_widget_func | self, self.motion_over_widget_args | The user-defined method or function that will be called when your touch point crosses into this DropDestination object.
| motion_flee_widget_func | self, self.motion_flee_widget_args | The user-defined method or function that will be called when your touch point leaves the boundaries of this DropDestination object. |
| motion_outside_widget_func | self, self.motion_outside_widget_args | The user-defined method or function that will be called when your touch point moves outside the boundaries of this DropDestination object. Can be quite chatty; be careful about adding this to too many widgets. |
| motion_inside_widget_func | self, motion_inside_widget_args | The user-defined method or function that will be called when your touch point moves inside the boundaries of this DropDestination object. |

# Example
Here's a complete, working example. For more examples check the distribution's
**examples** folder.
For more information, see **API** below.
```Python
# File: DnDExample1.py
#       Simplest example of the DragNDropWidget Kivy library.
#
from __future__ import print_function
#
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.button import Button
from kivy.uix.label import Label
from dragndropwidget import DragNDropWidget
#
#
kv = '''
FloatLayout:
    BoxLayout:
        id: from_box
        canvas:
            Color:
                rgb: 1, 0.2, 0.2
            Rectangle:
                pos: self.pos
                size: self.size
        size_hint: 0.8, 0.25
        pos_hint: {'x': 0.1, 'y': 0.4}
        # Here's our DragNDropWidget. See below for the class declaration.
        DraggableButton:
            text: 'Button 1'
            droppable_zone_objects: [upper_to_box]
            drop_func: app.greet
            failed_drop_func: app.oops
            size_hint: None, None
            size: 100, 100 
    Label:
        id: upper_to_box
        text: 'drop here'
        canvas.before:
            Color:
                rgb: 0.4, 0.4, 1
            Rectangle:
                pos: self.pos
                size: self.size
        size_hint: 0.8, 0.2
        pos_hint: {'x': 0.1, 'y': 0.8}
'''
#
#
class  DraggableButton(Button, DragNDropWidget):
    def __init__(self, **kw):
        super(DraggableButton, self).__init__(**kw)
#
#
class DnDExample1(App):
    def __init__(self, **kw):
        super(DnDExample1, self).__init__(**kw)

    def build(self):
        return Builder.load_string(kv)

    def greet(self, calling_widget):
        print ("App says: Nicely Dropped!!")

    def oops(self, the_widget=None, parent=None, kv_root=None):
        print("App says: Ooops! Can't drop there!")


if __name__ == '__main__':
    DnDExample1().run()
```
# API
## Classes:
* `DragNDropWidget`
  * Your draggable widget must subclass this class.
* `DropDestination`
  * This is designed to be optional. This is an object that receives a DragNDropWidget. Use this if
  you want to:
    * Have the destination perform actions while an item is being dragged or dropped, or
    * Organize widgets into "drop groups", meaning that certain widgets are restricted to being
    dropped only onto other widgets in a group.

## DragNDropWidget
### Methods
The following are all ObjectProperties (the methods) or ListProperties (the args). Each Method has
a ListProperty that accompanies it, named with an "args" suffix rather than "func", as shown below.
For example, `failed_drop_func` has `failed_drop_args`. The one exception is `while_dragging_func`;
there is no `while_dragging_args`.

Note that the first argument given to each function after `self` is the widget that called it. This is
built in to the library. It's necessary because if you create a widget in
a KV language block, whenever it's dragged `self` is the object you created.
Normally that's fine, unless you're not removing the object upon drag. Then
you want a reference to the copy, not the original.n
* `drop_func`
  * If defined in your DragNDropWidget subclass, this function is called on a successful drop.
  * If defined in the object being dropped onto, a function by this name will be called when a
  droppable object is dropped onto it.
  * Argument ListProperty: `drop_args`. Your function will be called with the following arguments:
  `self`, the calling widget, and then the arguments in the ListProperty.
* `while_dragging_func`
  * If set, this is called continuously as the widget is being dragged.
* `failed_drop_func`
  * If defined in your DragNDropWidget subclass, this function will be called if you drag but fail
  to drop it onto any widget that has been configured to receive a drop from this widget.
  * Argument ListProperty: `failed_drop_args`
* `drag_start_func`
  * If defined in your DragNDropWidget subclass, this function is called when the widget senses that
  a drag has begun.

If you assign any of these `on_motion_...` functions, on_motion events are bound to the
kivy.core.Window (the main Window that encloses your Kivy program). on_motion events are dispatched
with each move of the pointer.

### Event Generation
#### Events
Subsequently, one of three events may then be dispatched by an on_motion event, depending on if you
assign a function to these Properties:
* `on_motion_over` when the pointer crosses from outside the widget to inside the widget
* `on_motion_flee` when the pointer cross out from inside the widget
* `on_motion_outside` if the pointer is moved anywhere outside the bounds of the widget. This can
be quite chatty, as it's called for all DragNDropWidgets that are bound to on_motion events.

### Event Methods Called
* `motion_over_widget_func`
  * If defined in your DragNDropWidget subclass, this function will be called whenever the pointer
  enters into the widget. It is called once, upon entry.
* `motion_flee_widget_func`
  * If defined in your DragNDropWidget subclass, this function will be called whenever the pointer
  leaves the widget. It is called once, upon crossing out of the widget.
* `motion_outside_widget_func`
  * If defined in your DragNDropWidget subclass, this function will be called for all pointer
  motions that are not inside each and every widget that defines this function. Of course, it will
  not be called on the widget you are currently inside, if you are currently inside one.

### Called After a Drop
At the end of a drag and drop, the `on_drag_finish()` method is called. Its job is to find any
possible drag recipients, decide if there was a successful drop and who was dropped onto, and then
call the appropriate user-defined functions. It may then call the ending animation. Finally, it
performs cleanup. The order of methods called from `on_drag_finish()` is as follows:

* If there was at least one successful drop:
 * If the `drop_ok_do_animation` Property is True (the default), we want an end-of-drop Animation.
 Then:
  * Call `on_successful_drop()`. This is called once even if we successfully drop on one or more
  recipients.
   * Call `self.drop_func()`, if defined.
   * Call `found_drop_recipient.drop_func(self)` for each successful drop recipient, if defined.
  * Call `post_successful_animation()` after the widget's animation is finished.
 * If we set the Property to False, we do not want an animation:
  * Call `on_successful_drop()` immediately.
   * Calls `self.drop_func()` and `found_drop_recipient.drop_func(self)` as described above.
  * Call `post_successful_animation()` (which is a misnomer in this case).

`post_successful_animation()` is where you want to put behaviors such as adding a dragged widget
to a new parent. You can override this method in a subclass of DragNDropWidget.

* If there was not any successful drop:
 * If the `not_drop_ok_do_animation` Property is True (the default), we want an Animation.
  * Call `on_unsuccessful_drop()`. This is called once even no matter how many widgets we were
  unsuccessful in dropping onto.
   * Call `self.failed_drop_func()`, if defined.
   * If `self.remove_on_drag` is True (the default),
    * Call `self.reborn()`, which removes the widget from the root Window and re-adds it to the
    original parent.
   * else,
    * Calls `self.un_root_and_close()`, which removes the widget from the root Window and destroys
    it (because it is a copy of the original DragNDropWidget).
  * Call `self.post_unsuccessful_animation()` after the Animation is finished, which simply sets the
  widget's old opacity.
 * If we set the Property to False, we do not want an Animation.
  * Call `on_unsuccessful_drop()` as above.
   * Call its submethods, as above.
  * Call `self.post_unsuccessful_animation()` as above, which simply sets the widget's old opacity.

############## TODO: test app_relative_layout.py ########################################

### Properties:
* `droppable_zone_objects`
  * ListProperty: IDs of objects that you can drop widgets of this class onto (called a "drop
  destination"). You can use this and/or `drop_group` to specify drop destinations.
* `bound_zone_objects`
  * ListProperty: a list of objects that create a boxed-in boundary where the widget cannot be
  dragged past.
* `drag_opacity`
  * NumericProperty a real number between 0.0 and 1.0 that defines the opacity of the widget while
  it is dragged.
* `remove_on_drag`
  * BooleanProperty. If True, the widget is removed from the parent widget (perhaps a layout of
  some sort) and added to the destination widget. It will be re-added to the parent, in its old
  position, if the object is not dragged elsewhere. If False, a copy of the widget is made and
  that copy is added to the destination. If the object is not dragged elsewhere the copy is
  destroyed.
* `drop_ok_animation_time`
  * NumericProperty When it's dropped the object is faded away. This is the duration of that fade.
  Defaults to 0.7s.
* `not_drop_ok_animation_time`
  * NumericProperty If the object is not dragged elsewhere, this is the duration of the fade
  animation. Defaults to 0.7s.
* `can_drop_into_parent`
  * BooleanProperty If the object is allowed to drop back onto its parent, just as if it was
  dropped onto a non-parent widget. Note that the parent must be designated as a drop destination
  or member of a drop_group. If not, the widget will not be droppable onto the parent no matter the
  setting of this property.
* `drop_group`
  * StringProperty This is a string of your choosing. DragNDropWidgets of this drop_group will be
  able to be dropped onto DropDestination widgets that are also members of this drop_group. If you
  use `drop_group` then `droppable_zone_objects` are not recommended.

# Detailed Usage:
TODO: Create examples.

In addition to the simple usage given above, the module has additional capabilities. In the
simplest case you would set `droppable_zone_objects` and those are the objects you can drop into.
However, you can assign DragNDropWidget's to a `drop_group`, which is a Kivy StringProperty.
Accordingly you must subclass a drop destination to the DropDestination class, and then assign
it a drop_group. Your dragged widget, then, will only be droppable onto widgets in `drop_group`

There are a number of Kivy Properties available.
# Additional Capabilities and Notes:

At the end of a drop, the widget is left with no parent. It is up to you to decide what to do with
the widget. So if you want to add the dragged widget onto the place on which it was dropped, you
should do so in drop_func() of the recipient.

---
# Known Issues

You can have a number of widgets stacked on top of each other as drop recipients, but it's
undefined which widget will get chosen first.


# Support
This software is delivered without a warranty, and not even a guarantee that it will work as
advertised. If you encounter a bug, please
* Send me a fix. This is best. If you can't,
* Create a small- wery small- app that demonstrates the anomalous behavior you observe.

I will get to it when I can, but realize that I've got a day job and this class is being used for
an app that I'm building which takes the lion's share of my time.

# Bugs

Besides the ones I don't know about:

* There is a Kivy bug that when removing the leftmost of the children of a widget, if you try to
re-insert the child back into its former place at the beginning of the child list, it is not
actually displayed on the screen. So rather than re-adding a dragged child whose drag was not
completed, I am removing all widgets and re-adding them in order, as a workaround.
  * The bug holds true for any Layout widgets.


# License
Distributed under the Apache 2.0 License. See the LICENSE file for more information.
