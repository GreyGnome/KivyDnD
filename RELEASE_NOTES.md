Thu Jan 18 07:52:56 CST 2018 pre-Version 0.5:
Changes regarding `deepcopy` have been made to the code. See the notes for Version 0.4,
below. As of this version, if you are not deleting your widget upon drag (ie, you are
making a copy), your widget that's being dragged will need to implement the
`self.kivydnd_copy()` method, which must return a copy of the widget.

Wed Dec 13 17:42:26 CST 2017 Version 0.4:
Minor changes to dndexample3.py and example_base_classes.py. 
Added functionality to debug_print so that I can control which debug output I need using
a hex number.

This is the last release that will do a deepcopy in the library. The library
currently (pre-version 0.4) has no requirement for the programmer to perform
copy work at the beginning of a drag. But post-version 0.4, if you have been depending on
the library to perform a deepcopy, you'll need to change your code.
Future versions will require you to properly implement the object copy in
your subclass of DragNDropWidget when you are dragging a copy of a widget.
This is because various internal errors from deep within the
bowels of Kivy made me realize that deepcopy is not up to the library to
implement. Specifically, from
https://stackoverflow.com/questions/10618956/copy-deepcopy-raises-typeerror-on-objects-with-self-defined-new-method,
I note in one of the answers: "one problem is that `deepcopy` and `copy` have no way of
knowing which arguments to pass to `__new__`, therefore they only work with classes that
don't require constructor arguments." Naturally, the library cannot know if a widget will
require constructor arguments. Furthermore, while debugging I performing a deepcopy immediately after the
creation of one of my widgets, I received errors like this:
```
Exception KeyError: ('',) in 'kivy.properties.observable_list_dispatch' ignored
Exception KeyError: ('',) in 'kivy.properties.observable_list_dispatch' ignored
...etc...
 ```
And later, I received another error when doing a deepcopy:
```
   File "/usr/lib64/python2.7/copy_reg.py", line 93, in __newobj__
     return cls.__new__(cls, *args)
   File "kivy/core/text/_text_sdl2.pyx", line 32, in kivy.core.text._text_sdl2._SurfaceContainer.__cinit__ (kivy/core/text/_text_sdl2.c:1280)
 TypeError: __cinit__() takes exactly 2 positional arguments (0 given)
```
So there are bits deep inside Kivy that I don't have knowledge of nor can the library 
anticipate, so I think it's best to stay out of it. Should errors like this arise,
the programmer's code can determine what needs to be copied in a copy-and-drag-the-widget
scenario.

Fri Oct 20 16:39:42 CDT 2017
Version 0.3: This is my first release with release notes.
The next version should have better notes.

Thu Nov  2 16:09:08 CDT 2017
Found a significant bug in the DropDestination class: The dropdestination was not sending motion events properly because of a miscalculation in absolute_collide_point.
