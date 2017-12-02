import sys
from math import floor
from PIL import Image, ImageDraw, ImageFont

#CONSTANTS#

cols = 32
rows = 8

topMargin = 60
leftMargin = 90
bottomMargin = 80
rightMargin = 20

squareSize = 40

bgColor = (35, 35, 40)

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

## Colors
# 1.1, .2, .9
# 1.8, .2, 3.2
# 1.8, .8, 3.2
def getColors(prob):
	color = floor(prob * 256)
	colorR = int(floor(color * 1.8))
	colorG = int(floor(color * .8))
	colorB = int(floor(color * 3.2))
	return (colorR, colorG, colorB)

def getDataProbs(dataFile):
    numDataFeatures = 8 * 32 
    numDataPoints = -1
    dataSum = [0] * numDataFeatures

    fp = open(dataFile,'r')
    for _,line in enumerate(fp):
        numDataPoints += 1
        if numDataPoints == 0: continue
        for i in range(len(line)): 
            if line[i].isdigit():
                dataSum[i // 2] += int(line[i]) # Change to adjust to data
    fp.close()

    dataProbs = [x / (1.0 * numDataPoints) for x in dataSum]
    return dataProbs

#####

imageSize = [leftMargin + rightMargin + cols * squareSize // 2, 
	topMargin + bottomMargin + rows * squareSize]

imageBounds = [0, 0] + imageSize 

im = Image.new("RGB", imageSize, bgColor)
draw = ImageDraw.Draw(im)

# Paste in the icons
icons = Image.open("icons.png")
icons.thumbnail((leftMargin, rows * squareSize))
im.paste(icons, (leftMargin - icons.size[0], topMargin))

# Draw in the percentage references
refLeftMargin = leftMargin - icons.size[0] + 5
refTopMargin = topMargin + rows * squareSize + 5
for i in range(0, 20):
	percentage = i * .05
	draw.rectangle(getRefCoords(i), fill = getColors(percentage))

# Draw in the measure explanation
for i in range(0, 8): 
	arcXY = [leftMargin + cols * squareSize / 2 * i / 8, 
			topMargin - 20, 
			leftMargin + cols * squareSize / 2 * (i+1) / 8, 
			topMargin + 20]
	draw.arc(arcXY, 200, 340, fill=(255, 255, 255))

# Draw in the data probabilities
dataFile = "new_songs_data.csv"
dataProbs = getDataProbs(dataFile)
for i in range(0, 32 * 8):
	draw.rectangle(getCoords(i), fill = getColors(dataProbs[i]))

# Add text 
fnt = ImageFont.truetype('open-sans\OpenSans-Regular.ttf', 20)
draw.text((refLeftMargin + 5, imageSize[1] - 35), "p = 0", font=fnt, fill=(255,255,255))
draw.text((imageSize[0] - 80, imageSize[1] - 35), "p = 1", font=fnt, fill=(255,255,255))
draw.text((leftMargin - 60, topMargin - 50), "Beat", font=fnt, fill=(255,255,255))
for i in range(0, 8):
	textCoords = [leftMargin + cols * squareSize / 2 * i / 8, topMargin - 50]
	draw.text(textCoords, str(i+1), font=fnt, fill=(255,255,255))

del draw

im.save("image.png")
