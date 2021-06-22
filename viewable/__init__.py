import tkinter as tk
import tkutil


# Constants
NEW = "new"
BUILT = "built"
MAPPED = "mapped"
DESTROYED = "destroyed"


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
        self._body = None
        self.__master = None
        self.__state = NEW
        self.__bind_destroy_id = None
        self.__bind_map_id = None

    # ==============================================
    #                 PROPERTIES
    # ==============================================

    @property
    def body(self):
        """
        Get the body of this view.
        """
        return self._body

    @property
    def state(self):
        """ Return the current state of the Viewable instance.
        States are integers, you can use these constants:
            - pyrustic.view.NEW: the state just after instantiation;
            - pyrustic.view.BUILT: the state after the call of _built
            - pyrustic.view.MAPPED: the state after the call of on_map
            - pyrustic.view.DESTROYED: the state after the call of on_destroy
        """
        return self.__state
    # ==============================================
    #               PUBLIC METHODS
    # ==============================================
    def build(self):
        """ Build this view object. It returns the body """
        if self.__state == NEW:
            self.__build()
            self.__binding()
        return self._body

    def build_pack(self, cnf=None, **kwargs):
        """ Build this view then pack it """
        self.build()
        cnf = {} if not cnf else cnf
        self._body.pack(cnf=cnf, **kwargs)

    def build_grid(self, cnf=None, **kwargs):
        """ Build this view then grid it """
        self.build()
        cnf = {} if not cnf else cnf
        self._body.grid(cnf=cnf, **kwargs)

    def build_place(self, cnf=None, **kwargs):
        """ Build this view then place it """
        self.build()
        cnf = {} if not cnf else cnf
        self._body.place(cnf=cnf, **kwargs)

    def build_wait(self):
        """ Build this view then wait till it closes.
         The view should have a tk.Toplevel as body """
        self.build()
        self._body.wait_window(self._body)

    def destroy(self):
        """ Destroy the body of this view """
        if self._body:
            self._body.destroy()


    # ==============================================
    #               METHODS TO IMPLEMENT
    # ==============================================
    def _build(self):
        """
        Build the view here by defining the _body instance
        """
        pass

    def _on_map(self):
        """
        Put here the code that will be executed once
        the body is mapped.
        """
        if isinstance(self._body, tk.Toplevel):
            tkutil.center_dialog_effect(self._body,
                                        within=self.__master.winfo_toplevel())

    def _on_destroy(self):
        """
        Put here the code that will be executed at destroy event
        """
        pass

    # ==============================================
    #                 INTERNAL METHODS
    # ==============================================
    def __build(self):
        self._build()
        if not self._body:
            raise MissingBodyError
        self.__master = self._body.master
        self.__state = BUILT

    def __binding(self):
        self.__bind_map_event()
        self.__bind_destroy_event()

    def __bind_map_event(self):
        # the body is already mapped
        if isinstance(self._body, tk.Toplevel):
            self.__run_on_map()
        else:
            self.__bind_map_id = self._body.bind("<Map>",
                                                 self.__run_on_map,
                                                 "+")

    def __bind_destroy_event(self):
        command = (lambda event,
                          widget=self._body,
                          callback=self.__run_on_destroy:
                   callback(event) if event.widget is widget else None)
        self.__bind_destroy_id = self._body.bind("<Destroy>",
                                                command, "+")

    def __run_on_map(self, event=None):
        self._on_map()
        self.__state = MAPPED
        if self.__bind_map_id is not None:
            self._body.unbind("<Map>", self.__bind_map_id)
            self.__bind_map_id = None

    def __run_on_destroy(self, event=None):
        self._on_destroy()
        self.__state = DESTROYED
        if self.__bind_map_id is not None:
            self._body.unbind("<Destroy>", self.__bind_destroy_id)
            self.__bind_map_id = None
        try:
            if self.__master.focus_get() is None:
                self.__master.winfo_toplevel().focus_lastfor().focus_force()
        except Exception as e:
            pass


class CustomView(Viewable):
    def __init__(self, body=None,
                 builder=None,
                 on_map=None,
                 on_destroy=None):
        super().__init__()
        if body:
            self._body = body
        if builder:
            self._build = builder
        if on_map:
            self._on_map = on_map
        if on_destroy:
            self._on_destroy = on_destroy


class Error(Exception):
    def __init__(self, *args, **kwargs):
        self.message = args[0] if args else ""
        super().__init__(self.message)

    def __str__(self):
        return self.message


class MissingBodyError(Error):
    pass
