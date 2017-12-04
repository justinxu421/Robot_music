import sys
from math import floor
from PIL import Image, ImageDraw, ImageFont
import util

#CONSTANTS#

cols = 32
rows = 8

topMargin = 60
leftMargin = 90
bottomMargin = 80
rightMargin = 20

squareSize = 40

bgColor = (70, 70, 70)
txtColor = (214, 214, 214)

imageSize = [leftMargin + rightMargin + cols * squareSize // 2, 
	topMargin + bottomMargin + rows * squareSize]

imageBounds = [0, 0] + imageSize 

#FUNCTIONS#

def getCoords(i):
	row = i // cols
	col = i % cols
	coords = [leftMargin + col * squareSize/2, topMargin + row * squareSize, 
		leftMargin + (col+1) * squareSize/2, topMargin + (row+1) * squareSize]
	return coords

def getRefCoords(i):
	row = i // cols
	col = i % cols
	coords = [refLeftMargin + col * squareSize * 7/8, refTopMargin + row * squareSize, 
		refLeftMargin + (col+1) * squareSize * 7/8, refTopMargin + (row+1) * squareSize]
	return coords

def getColors(prob):
	color = (460.8, 204.8, 819.2)
	amp = (1, 1, 1)
	colorR = int(floor(prob * color[0] * amp[0]))
	colorG = int(floor(prob * color[1] * amp[0]))
	colorB = int(floor(prob * color[2] * amp[0]))
	return (colorR, colorG, colorB)

#####

# Initialize the image and draw object
im = Image.new("RGBA", imageSize, (0, 0, 0, 0))
draw = ImageDraw.Draw(im)

# Paste in the icons
icons = Image.open("images/icons.png")
icons.thumbnail((leftMargin, rows * squareSize))
im.paste(icons, (leftMargin - icons.size[0], topMargin))

# Draw in the percentage references
refLeftMargin = leftMargin - icons.size[0] + 5
refTopMargin = topMargin + rows * squareSize + 5
for i in range(0, 20):
	percentage = i * .05
	draw.rectangle(getRefCoords(i), fill = getColors(percentage))

# Draw in the measures explanation
for i in range(0, 8): 
	arcXY = [leftMargin + cols * squareSize / 2 * i / 8, 
			topMargin - 20, 
			leftMargin + cols * squareSize / 2 * (i+1) / 8, 
			topMargin + 20]
	draw.arc(arcXY, 200, 340, fill=txtColor)

# Add text 
fnt = ImageFont.truetype('fonts/open-sans/OpenSans-Bold.ttf', 20)
draw.text((refLeftMargin + 5, imageSize[1] - 35), "p = 0", font=fnt, fill=txtColor)
draw.text((imageSize[0] - 80, imageSize[1] - 35), "p = 1", font=fnt, fill=txtColor)
draw.text((leftMargin - 60, topMargin - 50), "Beat", font=fnt, fill=txtColor)
for i in range(0, 8):
	textCoords = [leftMargin + cols * squareSize / 2 * i / 8, topMargin - 50]
	draw.text(textCoords, str(i+1), font=fnt, fill=txtColor)

# Draw in the data probabilities
dataFile = "new_songs_data(incl. twitter).csv"

# MLE
#dataProbs = util.getMLEProbs(dataFile)
# light
dataProbs = util.getConditionalProbsFromScratch("min")
for i in dataProbs:
	print(str(i) + ", " + str(dataProbs[i]))

for i in range(0, 32 * 8):
	draw.rectangle(getCoords(i), fill = getColors(dataProbs[i]))

del draw

im.save("images/testing.png")
