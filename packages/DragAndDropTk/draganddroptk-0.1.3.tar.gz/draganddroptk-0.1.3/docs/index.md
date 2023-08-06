# DragAndDropTk

## **Welcome**

DragAndDropTk is a Tkinter widget that implements drag and drop features and can be customized as needed. It was developed as a Tkinter Frame with the callback functions and can be easily improved to build interfaces that need this behavior.

## **How to use**

To install, run the command:

```
pip install DragAndDropTk
```

It's extremely simple to use. Let's see how we can initialize it in a Tk window in the code below.

```{.py3 linenums=1 hl_lines="12" title="default_case.py"}
from tkinter import Tk
from DragAndDropTk import DragAndDropTk


class MainWindow(Tk):
    
    def __init__(self) -> None:
        super().__init__()
        self.title("Teste Drag and Drop Widget")
        self.geometry(f"1280x720")
        
        self.dnd_widget = DragAndDropTk(self, width=100, height=50, bg="#002255")
        self.dnd_widget.pack()
        
        
MainWindow().mainloop()
```

It couldn't be easier. We just only need initialize a DragAndDropTk as another Tkinter widget and it's working. See the result below.

<video autoplay loop muted>
  <source src="./videos/default_case.mp4" type="video/mp4">
</video>

## **Examples**

This example's very simple, it's a basic widget with no utilities. So let's se who we can improve it.

### Adding child widgets

The following example implements a widget with a label and a image. To do this, we can only instantiate the widget and pack them normally, the only new here is the method `bind_child(widget)`. It might be applied to all widgets, otherwise the translation won't work.

```{.py3 linenums=1 hl_lines="8-31 41-45" title="customized_widget.py"}
from PIL import Image, ImageTk

from tkinter import Label, Tk
from tkinter.ttk import Separator

from DragAndDropTk import DragAndDropTk

class Improved_DragAndDropTk(DragAndDropTk):
    
    def __init__(self, text: str, img_path: str, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs, borderwidth=3)
                
        self.lbl = Label(self, text=text, bg="#002255", foreground='#ffee77', padx=10, pady=10)
        self.lbl.pack(fill='x')
        
        self.sep = Separator(self, orient='horizontal', style="TSeparator")
        self.sep.pack()
        
        logo = ImageTk.PhotoImage(
            Image.open(img_path)
            .resize((100, 100))
        )

        self.lbl.config
        self.img = Label(self, image=logo, bg="#002255", width=self.lbl.winfo_reqwidth())
        self.img.image = logo
        self.img.pack()
        
        self.bind_child(self.lbl)
        self.bind_child(self.sep)
        self.bind_child(self.img)
        

class MainWindow(Tk):
    
    def __init__(self) -> None:
        super().__init__()
        self.title("Teste Drag and Drop Widget")
        self.geometry(f"1280x720")
        
        self.dnd_widget = Improved_DragAndDropTk(
            text="It's a DragAndDrop with a label and a image", 
            img_path=f"./tests/resources/python-logo.png",
            master=self, width=100, height=50
        )
        self.dnd_widget.pack()
        
        
MainWindow().mainloop()
```

Here's the result.

<video autoplay loop muted>
  <source src="./videos/customized_widget.mp4" type="video/mp4">
</video>

### Changing the placing behavior

Although the standard behavior is to place the widget in the point it was dropped, we can change this by overriding the `mouse_release_action` function. The input parameters are the coordinates `pos_x` and `pos_y` the widget is dropped in the window and using the `place` function we can define its final position.

```{.py3 linenums=1 hl_lines="11 35-49 69-73" title="customized_widget.py"}
from PIL import Image, ImageTk

from tkinter import Frame, Label, Tk
from tkinter.ttk import Separator

from DragAndDropTk import DragAndDropTk

class Improved_DragAndDropTk(DragAndDropTk):
    
    def __init__(self, text, *args, **kwargs) -> None:
        self.frames = kwargs.pop('frames')
        super().__init__(*args, **kwargs, borderwidth=3)
      
        self.lbl = Label(self, text=text,
                         bg="#002255", foreground='#ffee77', padx=10, pady=10)
        self.lbl.pack(fill='x')
        
        self.sep = Separator(self, orient='horizontal', style="TSeparator")
        self.sep.pack()
        
        logo = ImageTk.PhotoImage(
            Image.open(f"./tests/resources/python-logo.png")
            .resize((100, 100))
        )

        self.lbl.config
        self.img = Label(self, image=logo, bg="#002255", width=self.lbl.winfo_reqwidth())
        self.img.image = logo
        self.img.pack()
                
        self.bind_child(self.lbl)
        self.bind_child(self.sep)
        self.bind_child(self.img)
        
    def mouse_release_action(self, pos_x: int, pos_y: int) -> None:
        for frame in self.frames:
            l = frame.winfo_x()
            t = frame.winfo_y()
            r = frame.winfo_x() + frame.winfo_width()
            b = frame.winfo_y() + frame.winfo_height()
            
            c_x = (l + r) // 2
            c_y = (b + t) // 2            
            
            if l <= pos_x + self.winfo_width()//2 <= r and t <= pos_y + self.winfo_height()//2 <= b:
                self.place(
                    x=c_x - self.winfo_width() // 2,
                    y=c_y - self.winfo_height() // 2
                )
        

class MainWindow(Tk):
    
    def __init__(self) -> None:
        super().__init__()
        self.title("Teste Drag and Drop Widget")
        self.geometry(f"1280x720")
        
        self.main_frame = Frame(self)
        
        self.frm1 = Frame(self.main_frame, bg="#008899")
        self.frm2 = Frame(self.main_frame, bg="#ffee77")
        
        self.frm1.pack(fill='both', expand=1, side='left')
        self.frm2.pack(fill='both', expand=1, side='left')
        
        self.main_frame.pack(fill='both', expand=2)
        
        Improved_DragAndDropTk(
            "I can be dropped inside the frames", master=self,
            frames=[self.frm1, self.frm2] 
        ).place(x=0, y=0)
        
        
        
MainWindow().mainloop()
```

This example shows a window with two frames. The DragAndDropTk was configured to be placed centered in one of the two Tk frames. The `mouse_release_action` function iterates by the frames and calculates what frame contains the widget center and center the widget inside it.

See the demonstration.

<video autoplay loop muted>
  <source src="./videos/drop_to_frame.mp4" type="video/mp4">
</video>