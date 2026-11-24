import tkinter as tk
from tkinter import colorchooser, filedialog, messagebox
from PIL import Image, ImageDraw, ImageTk

BLUE_BG = "#E3F2FD"        
BLUE_PANEL = "#BBDEFB"     
BLUE_BUTTON = "#90CAF9"    
BLUE_HOVER = "#64B5F6"     
TEXT_COLOR = "#0D3B66"     
FONT_MAIN = ("Arial", 10, "bold")

QUICK_COLORS = [("Black", "#000000"), ("Red", "#FF0000"), ("Blue", "#0000FF"),
                ("Green", "#008000"), ("Yellow", "#FFFF00"), ("Purple", "#800080")]

MAX_UNDO = 30

CANVAS_WIDTH = 900
CANVAS_HEIGHT = 550

root = tk.Tk()
root.title("My Paint Application")
root.geometry("1000x780")
root.configure(bg=BLUE_BG)

image = Image.new("RGB", (CANVAS_WIDTH, CANVAS_HEIGHT), "white")
draw = ImageDraw.Draw(image)
canvas_image = None

current_color = "#000000"
brush_size = 5
tool = "brush"
start_x = start_y = None
last_x = last_y = None
preview_shape = None
undo_stack = []                 
fill_shapes = tk.BooleanVar(value=False)   


def set_color(color):
    global current_color, tool
    current_color = color
    if tool == "eraser":
        set_tool("brush")
    color_button.config(bg=current_color,
                        fg="white" if is_dark(current_color) else TEXT_COLOR)


def is_dark(hex_color):
    r = int(hex_color[1:3], 16)
    g = int(hex_color[3:5], 16)
    b = int(hex_color[5:7], 16)
    return (r * 0.299 + g * 0.587 + b * 0.114) < 140


def choose_color():
    selected = colorchooser.askcolor(title="Choose a color", color=current_color)
    if selected[1] is not None:
        set_color(selected[1])


def set_tool(selected_tool):
    global tool
    tool = selected_tool
    tool_label.config(text=f"Tool: {tool.capitalize()}")


def change_brush_size(value):
    global brush_size
    brush_size = int(float(value))


def save_undo_step():
    undo_stack.append(image.copy())
    if len(undo_stack) > MAX_UNDO:
        undo_stack.pop(0)          


def undo():
    global image, draw
    if not undo_stack:
        messagebox.showinfo("Undo", "Nothing to undo.")
        return
    image = undo_stack.pop()
    draw = ImageDraw.Draw(image)
    refresh_canvas()


def draw_dot(x, y, color):
    r = brush_size / 2
    draw.ellipse((x - r, y - r, x + r, y + r), fill=color)


def start_drawing(event):
    global last_x, last_y, start_x, start_y, preview_shape
    save_undo_step()
    preview_shape = None
    last_x, last_y = event.x, event.y
    start_x, start_y = event.x, event.y
    if tool in ("brush", "eraser"):
        color = "white" if tool == "eraser" else current_color
        r = brush_size / 2
        canvas.create_oval(event.x - r, event.y - r, event.x + r, event.y + r,
                           fill=color, outline="")
        draw_dot(event.x, event.y, color)


def draw_motion(event):
    global last_x, last_y
    if start_x is None:     
        return
    color = "white" if tool == "eraser" else current_color
    if tool in ("brush", "eraser"):
        canvas.create_line(last_x, last_y, event.x, event.y,
                           fill=color, width=brush_size,
                           capstyle=tk.ROUND, joinstyle=tk.ROUND)
        draw.line((last_x, last_y, event.x, event.y),
                  fill=color, width=brush_size)
        draw_dot(event.x, event.y, color)
        last_x, last_y = event.x, event.y
    else:
        preview_shape_drawing(event)


def box(x1, y1, x2, y2):
    return min(x1, x2), min(y1, y2), max(x1, x2), max(y1, y2)


def triangle_points(x1, y1, x2, y2):
    left, top, right, bottom = box(x1, y1, x2, y2)
    return [((left + right) / 2, top), (right, bottom), (left, bottom)]


def preview_shape_drawing(event):
    global preview_shape
    if preview_shape is not None:
        canvas.delete(preview_shape)
    fill = current_color if fill_shapes.get() else ""
    if tool == "line":
        preview_shape = canvas.create_line(
            start_x, start_y, event.x, event.y,
            fill=current_color, width=brush_size, capstyle=tk.ROUND)
    elif tool == "rectangle":
        preview_shape = canvas.create_rectangle(
            start_x, start_y, event.x, event.y,
            outline=current_color, fill=fill, width=brush_size)
    elif tool == "oval":
        preview_shape = canvas.create_oval(
            start_x, start_y, event.x, event.y,
            outline=current_color, fill=fill, width=brush_size)
    elif tool == "triangle":
        points = triangle_points(start_x, start_y, event.x, event.y)
        preview_shape = canvas.create_polygon(
            points, outline=current_color, fill=fill,
            width=brush_size, joinstyle=tk.ROUND)


def finish_drawing(event):
    global preview_shape, start_x, start_y
    if start_x is None:     # safety: the press did not start on the canvas
        return
    fill = current_color if fill_shapes.get() else None
    if tool == "line":
        draw.line((start_x, start_y, event.x, event.y),
                  fill=current_color, width=brush_size)
        draw_dot(start_x, start_y, current_color)
        draw_dot(event.x, event.y, current_color)
    elif tool == "rectangle":
        draw.rectangle(box(start_x, start_y, event.x, event.y),
                       outline=current_color, fill=fill, width=brush_size)
    elif tool == "oval":
        draw.ellipse(box(start_x, start_y, event.x, event.y),
                     outline=current_color, fill=fill, width=brush_size)
    elif tool == "triangle":
        points = triangle_points(start_x, start_y, event.x, event.y)
        if fill:
            draw.polygon(points, fill=fill)
        draw.line(points + [points[0]], fill=current_color,
                  width=brush_size, joint="curve")
        for x, y in points:
            draw_dot(x, y, current_color)
    preview_shape = None
    start_x = start_y = None
    refresh_canvas()


def refresh_canvas():
    global canvas_image
    canvas.delete("all")
    canvas_image = ImageTk.PhotoImage(image)
    canvas.create_image(0, 0, anchor="nw", image=canvas_image)


def clear_canvas():
    global image, draw, preview_shape
    answer = messagebox.askyesno("Clear Canvas",
                                 "Are you sure you want to clear the canvas?")
    if not answer:          
        return
    save_undo_step()        
    image = Image.new("RGB", (CANVAS_WIDTH, CANVAS_HEIGHT), "white")
    draw = ImageDraw.Draw(image)
    preview_shape = None
    refresh_canvas()


def open_image():
    global image, draw
    file_path = filedialog.askopenfilename(
        filetypes=[("Image files", "*.png *.jpg *.jpeg *.bmp")])
    if file_path:
        try:
            opened_image = Image.open(file_path).convert("RGB")
            opened_image = opened_image.resize((CANVAS_WIDTH, CANVAS_HEIGHT))
            save_undo_step()
            image = opened_image
            draw = ImageDraw.Draw(image)
            refresh_canvas()
        except Exception as error:
            messagebox.showerror("Error", f"Could not open image:\n{error}")


def save_image():
    file_path = filedialog.asksaveasfilename(
        defaultextension=".png",
        filetypes=[("PNG Image", "*.png"),
                   ("JPEG Image", "*.jpg"),
                   ("Bitmap Image", "*.bmp")])
    if file_path:
        try:
            image.save(file_path)
            messagebox.showinfo("Saved", "Your drawing has been saved!")
        except Exception as error:
            messagebox.showerror("Error", f"Could not save image:\n{error}")


def make_button(parent, text, command):
    return tk.Button(parent, text=text, command=command,
                     bg=BLUE_BUTTON, fg=TEXT_COLOR,
                     activebackground=BLUE_HOVER, activeforeground=TEXT_COLOR,
                     font=FONT_MAIN, relief="flat", padx=10, pady=4,
                     cursor="hand2")


toolbar = tk.Frame(root, bg=BLUE_PANEL, padx=10, pady=8)
toolbar.pack(pady=(10, 0))

make_button(toolbar, "Brush",
            lambda: set_tool("brush")).pack(side="left", padx=4)
make_button(toolbar, "Eraser",
            lambda: set_tool("eraser")).pack(side="left", padx=4)
make_button(toolbar, "Line",
            lambda: set_tool("line")).pack(side="left", padx=4)
make_button(toolbar, "Rectangle",
            lambda: set_tool("rectangle")).pack(side="left", padx=4)
make_button(toolbar, "Oval",
            lambda: set_tool("oval")).pack(side="left", padx=4)
make_button(toolbar, "Triangle",
            lambda: set_tool("triangle")).pack(side="left", padx=4)

tk.Checkbutton(toolbar, text="Fill shapes", variable=fill_shapes,
               bg=BLUE_PANEL, fg=TEXT_COLOR, activebackground=BLUE_PANEL,
               selectcolor="white", font=FONT_MAIN,
               cursor="hand2").pack(side="left", padx=(10, 4))

tk.Label(toolbar, text="Brush Size:", bg=BLUE_PANEL,
         fg=TEXT_COLOR, font=FONT_MAIN).pack(side="left", padx=(10, 3))

size_slider = tk.Scale(toolbar, from_=1, to=100, orient="horizontal",
                       command=change_brush_size, length=160,
                       bg=BLUE_PANEL, fg=TEXT_COLOR,
                       troughcolor=BLUE_BUTTON, highlightthickness=0)
size_slider.set(5)
size_slider.pack(side="left", padx=3)

colorbar = tk.Frame(root, bg=BLUE_PANEL, padx=10, pady=8)
colorbar.pack(pady=(6, 0))

color_button = make_button(colorbar, "Choose Color", choose_color)
color_button.config(bg=current_color, fg="white")
color_button.pack(side="left", padx=4)

tk.Label(colorbar, text="Quick Colors:", bg=BLUE_PANEL,
         fg=TEXT_COLOR, font=FONT_MAIN).pack(side="left", padx=(10, 3))

for name, code in QUICK_COLORS:
    tk.Button(colorbar, bg=code, activebackground=code, width=2,
              relief="flat", cursor="hand2",
              command=lambda c=code: set_color(c)).pack(side="left", padx=3)

make_button(colorbar, "Undo", undo).pack(side="left", padx=(16, 4))
make_button(colorbar, "Clear", clear_canvas).pack(side="left", padx=4)
make_button(colorbar, "Open", open_image).pack(side="left", padx=4)
make_button(colorbar, "Save", save_image).pack(side="left", padx=4)

tool_label = tk.Label(root, text="Tool: Brush", bg=BLUE_BG,
                      fg=TEXT_COLOR, font=FONT_MAIN)
tool_label.pack(pady=(6, 0))

canvas_frame = tk.Frame(root, bg=BLUE_BUTTON, padx=4, pady=4)
canvas_frame.pack(padx=20, pady=(6, 15))

canvas = tk.Canvas(canvas_frame, width=CANVAS_WIDTH, height=CANVAS_HEIGHT,
                   bg="white", cursor="cross", highlightthickness=0)
canvas.pack()

canvas.bind("<Button-1>", start_drawing)
canvas.bind("<B1-Motion>", draw_motion)
canvas.bind("<ButtonRelease-1>", finish_drawing)
root.bind("<Control-z>", lambda event: undo())
root.bind("<Control-Z>", lambda event: undo())   

if __name__ == "__main__":
    root.mainloop()
