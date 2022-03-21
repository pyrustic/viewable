import tkinter as tk
from viewable import Viewable


class View(Viewable):
    def __init__(self, master):
        super().__init__()
        self._master = master

    def _build(self):
        self._body = tk.Frame()
        button = tk.Button(self._body, text="Exit",
                           command=self._master.destroy)
        button.pack()

    def _on_map(self):
        print("On Map")

    def _on_destroy(self):
        print("On Destroy")


def main():
    print("https://github.com/pyrustic/viewable")
    root = tk.Tk()
    view = View(root)
    view.build_pack()
    root.mainloop()


if __name__ == "__main__":
    main()
