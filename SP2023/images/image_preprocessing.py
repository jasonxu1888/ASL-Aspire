# DO NOT CHANGE ANYTHING IN THIS FILE
# DO NOT CHANGE ANYTHING IN THIS FILE
# DO NOT CHANGE ANYTHING IN THIS FILE
# DO NOT CHANGE ANYTHING IN THIS FILE
# DO NOT CHANGE ANYTHING IN THIS FILE
# DO NOT CHANGE ANYTHING IN THIS FILE
# DO NOT CHANGE ANYTHING IN THIS FILE
# DO NOT CHANGE ANYTHING IN THIS FILE
# DO NOT CHANGE ANYTHING IN THIS FILE
# DO NOT CHANGE ANYTHING IN THIS FILE
# DO NOT CHANGE ANYTHING IN THIS FILE
# DO NOT CHANGE ANYTHING IN THIS FILE
# DO NOT CHANGE ANYTHING IN THIS FILE
# DO NOT CHANGE ANYTHING IN THIS FILE
# DO NOT CHANGE ANYTHING IN THIS FILE
# DO NOT CHANGE ANYTHING IN THIS FILE
# DO NOT CHANGE ANYTHING IN THIS FILE
# DO NOT CHANGE ANYTHING IN THIS FILE
# DO NOT CHANGE ANYTHING IN THIS FILE
# DO NOT CHANGE ANYTHING IN THIS FILE
# DO NOT CHANGE ANYTHING IN THIS FILE
# DO NOT CHANGE ANYTHING IN THIS FILE
# DO NOT CHANGE ANYTHING IN THIS FILE
# DO NOT CHANGE ANYTHING IN THIS FILE
# DO NOT CHANGE ANYTHING IN THIS FILE
# DO NOT CHANGE ANYTHING IN THIS FILE
# DO NOT CHANGE ANYTHING IN THIS FILE
# DO NOT CHANGE ANYTHING IN THIS FILE
# DO NOT CHANGE ANYTHING IN THIS FILE
# DO NOT CHANGE ANYTHING IN THIS FILE
# DO NOT CHANGE ANYTHING IN THIS FILE
# DO NOT CHANGE ANYTHING IN THIS FILE
# DO NOT CHANGE ANYTHING IN THIS FILE
# DO NOT CHANGE ANYTHING IN THIS FILE
# DO NOT CHANGE ANYTHING IN THIS FILE
# DO NOT CHANGE ANYTHING IN THIS FILE

from PIL import Image, ImageFont, ImageDraw

# generic function for drawing centered text onto a picture
def drawLetter(file, letter, font_size, font_type, font_color):
    image = Image.open(file).convert("RGBA")
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype(font_type, font_size)
    draw.text(((image.width)/2, (image.height)/2), text=letter, fill=font_color, font=font, anchor="mm", align="center")
    image.save(f"box-{letter}.png")

drawLetter("box.png", "A", 133, "cour.ttf", "black")
drawLetter("box.png", "C", 133, "cour.ttf", "black")
drawLetter("box.png", "T", 133, "cour.ttf", "black")
drawLetter("box.png", "G", 133, "cour.ttf", "black")

image = Image.open("aslaspire-logo.png").convert("RGBA")
factor = 0.5
resized = image.resize((int(image.width*factor), int(image.height*factor)))
resized.save("logo-resized.png")
print(resized.width)
print(resized.height)

image = Image.open("title-screen.png").convert("RGBA")
factor = 0.4
resized = image.resize((int(image.width*factor), int(image.height*factor)))
resized.save("title-screen-resized.png")

image = Image.open("base-A.png")
print(image.width, image.height)
image = Image.open("base-C.png")
print(image.width, image.height)
image = Image.open("base-G.png")
print(image.width, image.height)
image = Image.open("base-T.png")
print(image.width, image.height)