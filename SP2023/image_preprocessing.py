
from PIL import Image, ImageFont, ImageDraw

# generic function for drawing centered text onto a picture
def drawLetter(file, letter, font_size, font_type, font_color):
    image = Image.open(file).convert("RGBA")
    draw = ImageDraw.Draw(image)
    letter = letter
    font_size = font_size
    font_type = font_type
    font_color = font_color
    font = ImageFont.truetype(font_type, font_size)
    draw.text(((image.width)/2, (image.height)/2), text=letter, fill=font_color, font=font, anchor="mm", align="center")
    image.save(f"box-{letter}.png")

drawLetter("box.png", "A", 133, "cour.ttf", "black")
drawLetter("box.png", "C", 133, "cour.ttf", "black")
drawLetter("box.png", "T", 133, "cour.ttf", "black")
drawLetter("box.png", "G", 133, "cour.ttf", "black")