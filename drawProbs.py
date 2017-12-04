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
sepColor = (46, 46, 46)

imageSize = [leftMargin + rightMargin + cols * squareSize, 
	topMargin + bottomMargin + rows * squareSize]

imageBounds = [0, 0] + imageSize 

#FUNCTIONS#

# Input offset = [0, 0, 1, 1] to color the whole square
def getCoordsWithOffset(i, offset):
	row = i // cols 
	col = i % cols 
	coords = [int(float(leftMargin + (col+offset[0]) * squareSize)), 
				int(float(topMargin + (row+offset[1]) * squareSize)), 
				int(float(leftMargin + (col+offset[2]) * squareSize)), 
				int(float(topMargin + (row+offset[3]) * squareSize))]
	return coords 

def getRefCoords(i):
	row = i // cols
	col = i % cols
	coords = [refLeftMargin + col * squareSize * 15/9, refTopMargin + row * squareSize, 
		refLeftMargin + (col+1) * squareSize * 15/9, refTopMargin + (row+1) * squareSize]
	return coords

def getColors(prob):
	color = (460.8, 204.8, 819.2)
	amp = (1, 1, 1)
	colorR = int(floor(prob * color[0] * amp[0]))
	colorG = int(floor(prob * color[1] * amp[0]))
	colorB = int(floor(prob * color[2] * amp[0]))
	return (colorR, colorG, colorB)

def drawConditionalProbabilities(i, dataProbs):	
	if i % cols == 0 and i < 32: 
		# Top-leftmost cell
		prob = dataProbs[ tuple([i]) ]
		draw.rectangle(getCoordsWithOffset(i, [0,0,1,1]), fill = getColors(prob))
	elif i % cols == 0: 
		# Leftmost cell (not top row)
		topProb = dataProbs[ tuple([i, '1']) ]
		draw.rectangle(getCoordsWithOffset(i, [0,0,1,.5]), fill = getColors(topProb))
		bottomProb = dataProbs[ tuple([i, '0']) ]
		draw.rectangle(getCoordsWithOffset(i, [0,.5,1,1]), fill = getColors(bottomProb))
	elif i < 32: 
		# Top row cell (not leftmost)
		leftProb = dataProbs[ tuple([i, '1']) ]
		draw.rectangle(getCoordsWithOffset(i, [0,0,.5,1]), fill = getColors(leftProb))
		rightProb = dataProbs[ tuple([i, '0']) ]
		draw.rectangle(getCoordsWithOffset(i, [.5,0,1,1]), fill = getColors(rightProb))
	else: 
		# Other cell (not top row, not leftmost)
		topLeftProb = dataProbs[ tuple([i, '1', '1']) ]
		draw.rectangle(getCoordsWithOffset(i, [0,0,.5,.5]), fill = getColors(topLeftProb))
		bottomLeftProb = dataProbs[ tuple([i, '1', '0']) ]
		draw.rectangle(getCoordsWithOffset(i, [0,.5,.5,1]), fill = getColors(bottomLeftProb))
		topRightProb = dataProbs[ tuple([i, '0', '1']) ]
		draw.rectangle(getCoordsWithOffset(i, [.5,0,1,.5]), fill = getColors(topRightProb))
		bottomRightProb = dataProbs[ tuple([i, '0', '0']) ]
		draw.rectangle(getCoordsWithOffset(i, [.5,.5,1,1]), fill = getColors(bottomRightProb))

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

# Add text 
fnt = ImageFont.truetype('fonts/open-sans/OpenSans-Bold.ttf', 20)
draw.text((refLeftMargin + 5, imageSize[1] - 35), "p = 0", font=fnt, fill=txtColor)
draw.text((imageSize[0] - 80, imageSize[1] - 35), "p = 1", font=fnt, fill=txtColor)
draw.text((leftMargin - 60, topMargin - 30), "Beat", font=fnt, fill=txtColor)
for i in range(0, 8):
	textCoords = [leftMargin + cols * squareSize * i / 8, topMargin - 30]
	draw.text(textCoords, str(i+1), font=fnt, fill=txtColor)

# Draw in the data probabilities
dataFile = "new_songs_data(incl. twitter).csv"

# MLE
#dataProbs = util.getMLEProbs(dataFile)
#for i in range(0, 32 * 8):
#	draw.rectangle(getCoordsWithOffset(i, [0,0,1,1]), fill = getColors(dataProbs[i]))

# Factor graph
dataProbs = util.getConditionalProbsFromScratch("min")
for i in range(0, cols * rows):
	drawConditionalProbabilities(i, dataProbs)

# Draw separaters 
sepSize = 1
for i in range(1, cols):
	if i % 4 == 0: 
		sepSize = 2
	sepCoords = [leftMargin + i * squareSize - sepSize, 
				topMargin, 
				leftMargin + i * squareSize + sepSize, 
				topMargin + rows * squareSize]
	sepSize = 1
	draw.rectangle(sepCoords, sepColor)
for i in range(1, rows):
	sepCoords = [leftMargin, 
				topMargin + i * squareSize - sepSize, 
				leftMargin + cols * squareSize, 
				topMargin + i * squareSize + sepSize]
	draw.rectangle(sepCoords, sepColor)

del draw

im.save("images/testing.png")
