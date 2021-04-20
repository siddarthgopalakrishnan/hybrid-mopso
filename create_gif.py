from PIL import Image
import glob
import os

# Create the frames
frames = []
imgs = glob.glob("./imgs/*.png")
imgs = sorted(imgs, key=lambda x: int(os.path.basename(x).split(".")[0]))
for i in imgs:
    new_frame = Image.open(i)
    frames.append(new_frame)

# Save into a GIF file that loops forever
frames[0].save('visualization.gif', format='GIF',
               append_images=frames[1:],
               save_all=True,
               duration=200)
