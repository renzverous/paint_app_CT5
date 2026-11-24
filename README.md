# paint_app_CT5

A desktop Paint Application built with Python, Tkinter, and Pillow

<img width="1365" height="767" alt="Screenshot 2026-11-24 140638" src="https://github.com/user-attachments/assets/4d22a44c-c326-4f86-aca6-9c8bf40c537a" />


1. Bigger brush range
<img width="281" height="66" alt="Screenshot 2026-11-24 150140" src="https://github.com/user-attachments/assets/f0810745-65aa-497b-9ed7-25ebb6fb7742" />
<img width="261" height="52" alt="Screenshot 2026-11-24 150152" src="https://github.com/user-attachments/assets/f1f0f2d5-3297-4746-9911-d5676bf93b4b" />
So, what I did here, ma'am, was change the brush size slider. 
To change the range, I simply changed the value from from_=1 (thinnest) to to=100 (thickest). I also made the slider longer, from 100 to 160, so it is easier to pick a size now that there are more numbers.
<img width="580" height="133" alt="Screenshot 2026-11-24 150302" src="https://github.com/user-attachments/assets/c9cfab35-97ad-4322-8470-fa4dc996cfad" />

The requirement also says the saved image must match the canvas. When I tested big brush sizes, I noticed that the canvas draws lines with round ends, but Pillow draws them with flat ends, so the saved file looked different. To fix this, I made a function called draw_dot() that draws a round dot on the Pillow image at every point of the stroke. I also made the program refresh the canvas from the Pillow image every time the mouse is released. Now what you see on the screen is exactly what gets saved, and the image is still 900 x 550, the same size as the canvas.<img width="534" height="89" alt="Screenshot 2026-11-24 150546" src="https://github.com/user-attachments/assets/d0bb0db1-3b97-42af-8f2a-baf0bc4aad07" />
