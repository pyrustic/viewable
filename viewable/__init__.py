import tkinter as tk
from viewable import error


__all__ = ["Viewable"]


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
        self.__body = None
        self.__built = False

    # ======== PROPERTIES ========

    @property
    def body(self):
        """
        Get the body of this view.
        """
        return self.__body

    # ======== PUBLIC METHOD =======

    def build(self, parent):
        """ Build this view """
        if self.__built:
            return self.body
        body = self._create_body(parent)
        self.__body = body
        if body:
            implement_lifecycle(body,
                                on_map=self._on_map,
                                on_remap=self._on_remap,
                                on_unmap=self._on_unmap,
                                on_destroy=self._on_destroy)
        self._build()
        self.__built = True
        return body

    def build_pack(self, parent, cnf=None, **kwargs):
        """ Build this view then pack it """
        self.build(parent)
        cnf = {} if not cnf else cnf
        self.body.pack(cnf=cnf, **kwargs)
        return self.body

    def build_grid(self, parent, cnf=None, **kwargs):
        """ Build this view then grid it """
        self.build(parent)
        cnf = {} if not cnf else cnf
        self.body.grid(cnf=cnf, **kwargs)
        return self.body

    def build_place(self, parent, cnf=None, **kwargs):
        """ Build this view then place it """
        self.build(parent)
        cnf = {} if not cnf else cnf
        self.body.place(cnf=cnf, **kwargs)
        return self.body

    def build_wait(self, parent):
        """ Build this view then wait till it closes.
         The view should have a tk.Toplevel as body """
        self.build(parent)
        if self.body.winfo_exists():
            self.body.wait_window(self.body)
        return self.body

    # ======= METHODS TO IMPLEMENT ========
    def _create_body(self, parent):
        return tk.Frame(parent)

    def _build(self):
        """
        Build the view layout here
        """
        pass

    def _on_map(self):
        """
        Put here the code that will be executed when
        the body is mapped.
        """
        pass

    def _on_remap(self):
        pass

    def _on_unmap(self):
        """
        Put here the code that will be executed when
        the body is unmapped.
        """
        pass

    def _on_destroy(self):
        """
        Put here the code that will be executed at destroy event
        """
        pass


def implement_lifecycle(body, on_map=None, on_remap=None, on_unmap=None,
                        on_destroy=None):
    """
    Use this function to implement lifecyle mechanism

    [parameters]
    - body: the target tk object
    - on_map: callback to be called on map
    - on_unmap: callback to be called on unmap
    - on_destroy: callback to be called on destroy
    """
    lifecycle = Lifecycle(body, on_map=on_map, on_remap=on_remap,
                          on_unmap=on_unmap, on_destroy=on_destroy)
    lifecycle.activate()


class Lifecycle:
    def __init__(self, body, on_map=None, on_remap=None, on_unmap=None,
                 on_destroy=None):
        self._body = body
        self._master = body.master
        self._on_map = on_map
        self._on_remap = on_remap
        self._on_unmap = on_unmap
        self._on_destroy = on_destroy
        self._bind_map_id = None
        self._bind_unmap_id = None
        self._bind_destroy_id = None
        self._previously_mapped = False
        self._active = False

    @property
    def body(self):
        return self._body

    @property
    def on_map(self):
        return self._on_map

    @property
    def on_remap(self):
        return self._on_remap

    @property
    def on_unmap(self):
        return self._on_unmap

    @property
    def on_destroy(self):
        return self._on_destroy

    @property
    def active(self):
        return self._active

    def activate(self):
        if not self._body.winfo_exists():
            return False
        self._bind()
        self._active = True
        return True

    def deactivate(self):
        if not self._body.winfo_exists():
            return False
        self._unbind()
        self._active = False
        return True

    def _bind(self):
        self._bind_map_event()
        self._bind_unmap_event()
        self._bind_destroy_event()

    def _unbind(self):
        bind_ids = {self._bind_map_id: "<Map>",
                    self._bind_unmap_id: "<Unmap>",
                    self._bind_destroy_id: "<Destroy>"}
        for bind_id, item in bind_ids.items():
            self._body.unbind(item, bind_id)
        self._bind_map_id = None
        self._bind_unmap_id = None
        self._bind_destroy_id = None

    def _bind_map_event(self):
        self._bind_map_id = self._body.bind("<Map>", self._handle_map_event, True)

    def _bind_unmap_event(self):
        self._bind_unmap_id = self._body.bind("<Unmap>", self._handle_unmap_event, True)

    def _bind_destroy_event(self):
        command = (lambda event: self._handle_destroy_event(event)
                   if event.widget is self._body else None)
        self._bind_destroy_id = self._body.bind("<Destroy>", command, True)

    def _handle_map_event(self, event):
        if event.widget is not self._body:
            return
        if self._previously_mapped:
            self._on_remap()
        else:
            self._on_map()
            self._previously_mapped = True
        return

    def _handle_unmap_event(self, event):
        if event.widget is not self._body:
            return
        self._on_unmap()

    def _handle_destroy_event(self, event):
        if event.widget is not self._body:
            return
        self._unbind()
        self._on_destroy()
        self._previously_mapped = False
        self._active = False
        try:
            if self._master.focus_get() is None:
                self._master.winfo_toplevel().focus_lastfor().focus_force()
        except Exception as e:
            pass
