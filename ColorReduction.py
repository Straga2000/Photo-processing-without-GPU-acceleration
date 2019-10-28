from PIL import Image

paletteLimit = 0
sampleDistance = 10
# search for colors in a wider range

colorDifference = 9

class tupleObj:

    def __init__(self, obj):

        self.obj = obj

    def setValues(self, r, g, b):

        self.obj = (r, g, b)
        return self

    def setValues(self, col):

        self.obj = col
        return self

    def minus(self, col):

        self.obj = (self.obj[0] - col.obj[0], self.obj[1] - col.obj[1], self.obj[2] - col.obj[2])
        return self

    def multiply(self, val):

        self.obj = (self.obj[0] * val, self.obj[1] * val, self.obj[2] * val)
        return self

    def add(self, col):

        self.obj = (self.obj[0] + col.obj[0], self.obj[1] + col.obj[1], self.obj[2] + col.obj[2])
        return self

    def intTransform(self):

        self.obj = (int(self.obj[0]), int(self.obj[1]), int(self.obj[2]))
        return self

    def getDifference(self, col):

        #for simple tulips
        return abs(self.obj[0] - col[0]) + abs(self.obj[1] - col[1]) + abs(self.obj[2] - col[2])


imInput1 = Image.open('source.jpg')
imInput2 = Image.open('destination.jpg')

ditheringFactor = ((imInput1.width * imInput1.height) // (imInput2.width * imInput2.height)) - 13

if ditheringFactor < 0:
    ditheringFactor = 20

print(ditheringFactor)

normalizationFactor = ditheringFactor / 256
renormalizeFactor = 256 // ditheringFactor

pixelSrc = imInput1.load()
pixelDest = imInput2.load()

pixelDict = {}
colorPalette = []

# dithering second photo
for i in range(imInput2.width):

    print("Line ", i, " of ", imInput2.width)

    for j in range(imInput2.height):

        error = curObj = tupleObj(pixelDest[i, j])

        curObj.multiply(normalizationFactor).intTransform().multiply(renormalizeFactor)
        pixelDest[i, j] = curObj.obj

        # if pixelDest[i, j] not in pixelDict:
        pixelDict[curObj.obj] = None

        error.minus(curObj).multiply(1/16)

        if i + 1 < imInput2.width:

            downObj = tupleObj(pixelDest[i + 1, j])

            er = tupleObj(error.obj)
            er.multiply(7)

            downObj = downObj.add(er).intTransform()
            pixelDest[i + 1, j] = downObj.obj

        if j + 1 < imInput2.height:

            leftObj = tupleObj(pixelDest[i, j + 1])

            er = tupleObj(error.obj)
            er.multiply(7)

            leftObj = leftObj.add(er).intTransform()
            pixelDest[i, j + 1] = leftObj.obj

            if i + 1 < imInput2.width:

                leftDownObj = tupleObj(pixelDest[i + 1, j + 1])

                er = tupleObj(error.obj)

                leftDownObj = leftDownObj.add(er).intTransform()
                pixelDest[i + 1, j + 1] = leftDownObj.obj

            if i - 1 >= 0:

                rightDownObj = tupleObj(pixelDest[i - 1, j + 1])

                er = tupleObj(error.obj)

                rightDownObj = rightDownObj.add(er).intTransform()
                pixelDest[i - 1, j + 1] = rightDownObj.obj
print("Dithering done.")

# paletteLimit = len(pixelDict)

paletteLimit = int(len(pixelDict) * 1.5)

# creating a vector of colors
for i in range(0, imInput1.width, sampleDistance):

    for j in range(0, imInput1.height, sampleDistance):

        curObj = tupleObj(pixelSrc[i, j])
        exist = False

        for colorElem in colorPalette:

            if curObj.getDifference(colorElem) <= colorDifference:
                exist = True
                break

        if exist is False and len(colorPalette) < paletteLimit:
            colorPalette.append(pixelSrc[i, j])

    if len(colorPalette) >= paletteLimit:
        break
print("Choosing source colors done.")

# associate destination colors with source colors
for srcColor in pixelDict:

    elem = tupleObj(srcColor)
    limit = len(colorPalette)
    index = 0
    memoDiff = 800

    for k in range(limit):

        value = elem.getDifference(colorPalette[k])

        if value < memoDiff:
            index = k
            memoDiff = value

    #print(index)
    if limit == 0:
        pixelDict[srcColor] = srcColor
    else:
        pixelDict[srcColor] = colorPalette[index]
        colorPalette.pop(index)
print("Associate colors done.")

# rewrite pixel values with new ones
for i in range(imInput2.width):
    for j in range(imInput2.height):
        pixelDest[i, j] = pixelDict[pixelDest[i, j]]
print("Change colors done.")

"""""
noneCnt = 0
for elem in pixelDict.values():
    if elem is None:
        noneCnt += 1

print(noneCnt)
"""""

# print(pixelDict)

imInput2.save("Result.jpg")
print("Process done.")
