<!-- Image -->
<div align="center">
    <img src="https://raw.githubusercontent.com/pyrustic/misc/master/media/cyberpunk-cover.png" alt="Figure" width="970">
    <p align="center">
    <i>  </i>
    </p>
</div>


<!-- Intro Text -->
# Viewable
<b> Implement better Views for your Tkinter Python app </b>

This project is part of the [Pyrustic Open Ecosystem](https://pyrustic.github.io).

<!-- Quick Links -->
[Installation](#installation) | [Reference](https://github.com/pyrustic/viewable/tree/master/docs/reference#readme)

## Overview

Views are the building blocks of your desktop application GUI. `Viewable` allows you to implement Views that are maintainable and easily extensible. Viewable defines a View in terms of its lifecycle. And so, you can split your source code to align with the main states a View goes through: `init`, `build`, `map`, and `destroy`.

Here's how to implement a View with `Viewable`:

```python
import tkinter as tk
from viewable import Viewable


class View(Viewable):
    def __init__(self, master):
        super().__init__()
        self._master = master

    def _build(self):
        """
        This is the only mandatory method to implement.
        You define the body of the view here
        """
        # the body is generally either
        # a tk.Frame instance
        # or a tk.Toplevel instance
        self._body = tk.Frame(self._master)
        label = tk.Label(self._body, text="Hello Friend !")
        label.pack()

    def _on_map(self):
        """ This method is called when the view is mapped for the first time """

    def _on_destroy(self):
        """ This method is called when the view is destroyed """


# root
root = tk.Tk()

# the view
view = View(root)

# the method build_pack() builds then packs the view
# In fact you could do:
#   view.build() then view.pack()
# or:
#   view.build() then view.body.pack()
view.build_pack()  # it accepts arguments like the Tkinter pack() method

# others ways to install a view:
# .build_grid(), .build_place(), .build_wait()

# you can access the body of the view via
# its .body property
view.body  # here, the body is a tk.Frame

# To destroy a view, call the method .destroy()
view.destroy()

# The .state property reveals the state of the view:
# 'new', 'built', 'mapped', 'destroyed'.
print(view.state)

# mainloop
root.mainloop()

```






## Installation
```bash
pip install viewable
```