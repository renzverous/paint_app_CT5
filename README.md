# paint_app_CT5

A desktop Paint Application built with Python, Tkinter, and Pillow

<img width="1365" height="767" alt="Screenshot 2026-11-24 140638" src="https://github.com/user-attachments/assets/4d22a44c-c326-4f86-aca6-9c8bf40c537a" />


1. BIGGER BRUSH RANGE

<img width="281" height="66" alt="Screenshot 2026-11-24 150140" src="https://github.com/user-attachments/assets/f0810745-65aa-497b-9ed7-25ebb6fb7742" />
<img width="261" height="52" alt="Screenshot 2026-11-24 150152" src="https://github.com/user-attachments/assets/f1f0f2d5-3297-4746-9911-d5676bf93b4b" />

So, what I did here, ma'am, was change the brush size slider. 
To change the range, I simply changed the value from from_=1 (thinnest) to to=100 (thickest). I also made the slider longer, from 100 to 160, so it is easier to pick a size now that there are more numbers.

<img width="580" height="133" alt="Screenshot 2026-11-24 150302" src="https://github.com/user-attachments/assets/c9cfab35-97ad-4322-8470-fa4dc996cfad" />

The requirement also says the saved image must match the canvas. When I tested big brush sizes, I noticed that the canvas draws lines with round ends, but Pillow draws them with flat ends, so the saved file looked different. To fix this, I made a function called draw_dot() that draws a round dot on the Pillow image at every point of the stroke. I also made the program refresh the canvas from the Pillow image every time the mouse is released. Now what you see on the screen is exactly what gets saved, and the image is still 900 x 550, the same size as the canvas.

<img width="534" height="89" alt="Screenshot 2026-11-24 150546" src="https://github.com/user-attachments/assets/d0bb0db1-3b97-42af-8f2a-baf0bc4aad07" />


2. UNDO BUTTON
 <img width="890" height="611" alt="Screenshot 2026-11-24 152605" src="https://github.com/user-attachments/assets/c2ed3609-323c-45c9-aa52-07799981d8aa" /> <img width="892" height="462" alt="Screenshot 2026-11-24 152615" src="https://github.com/user-attachments/assets/b8fb86ad-7c93-4345-b8c3-1acdc1a3f958" />

For the Undo button, ma'am, the program needed to remember how the drawing looked before each action. So I made a list called undo_stack. Before every new action, the function save_undo_step() saves a copy of the picture into the list.

When the user clicks Undo, the undo() function takes the last saved copy out of the list and shows it again, so the most recent action disappears. If there is nothing to undo, it shows a message saying "Nothing to undo."

<img width="480" height="285" alt="Screenshot 2026-11-24 152904" src="https://github.com/user-attachments/assets/28813314-ad00-427b-9128-c3ea16199971" />


3. FILLED SHAPES

<img width="410" height="163" alt="Screenshot 2026-11-24 153554" src="https://github.com/user-attachments/assets/f9f12c45-7549-49f1-ade8-0a7df15ae36c" />
<img width="137" height="95" alt="Screenshot 2026-11-24 153601" src="https://github.com/user-attachments/assets/882efc83-4d8c-4da4-a4fa-2e2ce3ed79f6" />

For filled shapes, ma'am, I added a "Fill shapes" checkbox to the toolbar. I used a BooleanVar to remember whether the box is ticked or not. In the original code, rectangles and ovals only had an outline, so they were always empty inside.
So I added a fill value. If the checkbox is ticked, the fill becomes the current color. I added it to both the preview while dragging and the final shape saved in the Pillow image, so the filled shape looks the same on the screen and in the saved file.
<img width="633" height="428" alt="Screenshot 2026-11-24 155013" src="https://github.com/user-attachments/assets/ca701fe2-5113-416d-8645-dba76c7146b7" />

4. EXTRA SHAPE TOOL: TRIANGLE
 <img width="519" height="118" alt="Screenshot 2026-11-24 160914" src="https://github.com/user-attachments/assets/2bbc7aca-95f1-4998-8997-fa9b29b71676" />
<img width="558" height="89" alt="Screenshot 2026-11-24 160901" src="https://github.com/user-attachments/assets/df81195b-43a6-4940-81c2-51033e1f5c8a" />

For my extra shape, ma'am, I chose a triangle. First, I added a Triangle button to the toolbar.
Then I made a function called triangle_points(). It takes the box the user drags and finds the three corners of the triangle: the top point in the middle, and the two bottom points at the bottom left and bottom right.
The requirement says the shape must show a preview while dragging, so in preview_shape_drawing() I used canvas.create_polygon() to draw a temporary triangle that follows the mouse.
When the mouse is released, finish_drawing() draws the triangle on the Pillow image so it gets saved. I used draw.polygon() for the fill and draw.line() around the three corners for the outline.

<img width="440" height="106" alt="Screenshot 2026-11-24 160012" src="https://github.com/user-attachments/assets/f6338a7e-4dfb-4b86-afa2-17a361fa4438" />
<img width="502" height="74" alt="Screenshot 2026-11-24 155943" src="https://github.com/user-attachments/assets/ba5757b4-1693-4b26-a370-dd8834638b91" />

