
Back to [Reference Overview](https://github.com/pyrustic/viewable/blob/master/docs/reference/README.md#readme)

# viewable.\_\_init\_\_



<br>


```python
BUILT = "built"

DESTROYED = "destroyed"

MAPPED = "mapped"

NEW = "new"

```

<br>

```python

class CustomView:
    """
    Subclass this if you are going to create a view.
    
    Lifecycle of a view:
        1- you instantiate the view
        2- '__init__()' is implicitly called
        3- you call the method '.build()'
        4- '_build()' is implicitly called
        5- '_on_map()' is implicitly called once the widget is mapped
        6- '_on_destroy()' is implicitly called when the widget is destroyed/closed
    
    The rules to create your view is simple:
    - You need to subclass Viewable.
    - You need to implement the methods '_build()', and optionally
        implement '_on_map()' and '_on_destroy()'.
    - You need to set an instance variable '_body' with either a tk.Frame or tk.Toplevel
        in the method '_on_build()'
    That's all ! Of course, when you are ready to use the view, just call the 'build()' method.
    Calling the 'build()' method will return the body of the view. The one that you assigned
    to the instance variable '_body'. The same body can be retrieved with the property 'body'.
    The 'build()' method should be called once. Calling it more than once will still return
    the body object, but the view won't be built again.
    You can't re-build your same view instance after destroying its body.
    You can destroy the body directly, by calling the conventional tkinter destruction method
     on the view's body. But it's recommended to destroy the view by calling the view's method
     'destroy()' inherited from the class Viewable.
    The difference between these two ways of destruction is that when u call the Viewable's
     'destroy()' method, the method '_on_destroy()' will be called BEFORE the effective
     destruction of the body. If u call directly 'destroy' conventionally on the tkinter
     object (the body), the method '_on_destroy()' will be called AFTER the beginning
      of destruction of the body.
    
      By the way, you can use convenience methods "build_pack", "build_grid", "build_place"
      to build and pack/grid/place your widget in the master !!
      Use "build_wait" for toplevels if you want the app to wait till the window closes
    """

    def __init__(self, body=None, builder=None, on_map=None, on_destroy=None):
        """
        Initialize self.  See help(type(self)) for accurate signature.
        """

```

<br>

```python

class Error:
    """
    Common base class for all non-exit exceptions.
    """

    def __init__(self, *args, **kwargs):
        """
        Initialize self.  See help(type(self)) for accurate signature.
        """

```

<br>

```python

class MissingBodyError:
    """
    Common base class for all non-exit exceptions.
    """

```

<br>

```python

class Viewable:
    """
    Subclass this if you are going to create a view.
    
    Lifecycle of a view:
        1- you instantiate the view
        2- '__init__()' is implicitly called
        3- you call the method '.build()'
        4- '_build()' is implicitly called
        5- '_on_map()' is implicitly called once the widget is mapped
        6- '_on_destroy()' is implicitly called when the widget is destroyed/closed
    
    The rules to create your view is simple:
    - You need to subclass Viewable.
    - You need to implement the methods '_build()', and optionally
        implement '_on_map()' and '_on_destroy()'.
    - You need to set an instance variable '_body' with either a tk.Frame or tk.Toplevel
        in the method '_on_build()'
    That's all ! Of course, when you are ready to use the view, just call the 'build()' method.
    Calling the 'build()' method will return the body of the view. The one that you assigned
    to the instance variable '_body'. The same body can be retrieved with the property 'body'.
    The 'build()' method should be called once. Calling it more than once will still return
    the body object, but the view won't be built again.
    You can't re-build your same view instance after destroying its body.
    You can destroy the body directly, by calling the conventional tkinter destruction method
     on the view's body. But it's recommended to destroy the view by calling the view's method
     'destroy()' inherited from the class Viewable.
    The difference between these two ways of destruction is that when u call the Viewable's
     'destroy()' method, the method '_on_destroy()' will be called BEFORE the effective
     destruction of the body. If u call directly 'destroy' conventionally on the tkinter
     object (the body), the method '_on_destroy()' will be called AFTER the beginning
      of destruction of the body.
    
      By the way, you can use convenience methods "build_pack", "build_grid", "build_place"
      to build and pack/grid/place your widget in the master !!
      Use "build_wait" for toplevels if you want the app to wait till the window closes
    """

    def __init__(self):
        """
        Initialize self.  See help(type(self)) for accurate signature.
        """

    @property
    def body(self):
        """
        Get the body of this view.
        """

    @property
    def state(self):
        """
        Return the current state of the Viewable instance.
        States are integers, you can use these constants:
            - pyrustic.view.NEW: the state just after instantiation;
            - pyrustic.view.BUILT: the state after the call of _built
            - pyrustic.view.MAPPED: the state after the call of on_map
            - pyrustic.view.DESTROYED: the state after the call of on_destroy
        """

    def build(self):
        """
        Build this view object. It returns the body 
        """

    def build_grid(self, cnf=None, **kwargs):
        """
        Build this view then grid it 
        """

    def build_pack(self, cnf=None, **kwargs):
        """
        Build this view then pack it 
        """

    def build_place(self, cnf=None, **kwargs):
        """
        Build this view then place it 
        """

    def build_wait(self):
        """
        Build this view then wait till it closes.
        The view should have a tk.Toplevel as body 
        """

    def destroy(self):
        """
        Destroy the body of this view 
        """

```

