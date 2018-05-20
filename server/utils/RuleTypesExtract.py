from utils import ImageOCR
import numpy as np
import cv2

def boundaryExtract(data, im, charWhitelist):
    x, y, w, h = map(int, [data['x'], data['y'], data['w'], data['h']])# data.split(",")))
    # crop_img = im[y:y+h, x:x+w] use this for cv2 image
    x, y, x2, y2 = min(x, x+w), min(y, y+h), max(x, x+w), max(y, y+h)
    crop_img = im.crop((x, y, x2, y2))  # use this for pil Image

    # crop_img = ImageOCR.preprocess(crop_img)
    # crop_img.show()
    # https://github.com/tesseract-ocr/tesseract/blob/master/doc/tesseract.1.asc
    if charWhitelist:
        text = ImageOCR.pytesseract.image_to_string(crop_img,
                                                    lang='eng',
                                                    config='--oem 0 -c tessedit_char_whitelist='+charWhitelist)
    else:
        text = ImageOCR.pytesseract.image_to_string(crop_img,
                                                    lang='eng',
                                                    config='')
    return text

def tableExtract(linesX, im, charWhitelist):
    height, width = im.size
    minX, maxX = min(linesX), max(linesX)
    crop_img = im.crop((minX, 0, maxX, height)) # todo

    # convert to opencv image
    open_cv_image = np.array(crop_img.convert("RGB"))

    # Convert RGB to BGR
    # print(open_cv_image.shape)
    # open_cv_image = open_cv_image[:, :, ::-1]

    #HoughLines
    # blur = cv2.bilateralFilter(open_cv_image,9,75,75)
    #open_cv_image = cv2.GaussianBlur(open_cv_image,(5,5),0)
    gray = cv2.cvtColor(open_cv_image,cv2.COLOR_RGB2GRAY)
    cv2.imwrite('crop_img.jpg',gray)
    edges = cv2.Canny(gray,100,200) #,255/3,255)
    # cv2.imwrite('houghlines2.jpg',edges)
    minLineLength = maxX-minX-(maxX-minX)*0.1  # add 5%-10% loss
    maxLineGap = 1000
    theta = np.pi/2 # 180 + 10%
    # img, rhi, treash, theta, min line length, max line gap
    lines = cv2.HoughLinesP(edges, 1, theta,180,minLineLength,maxLineGap)
    linesY = []
    oldY=0
    if lines is not None:
        for line in sorted(lines, key=lambda x:x[0][1]):
            for x1,y1,x2,y2 in line:
                # print(y1, oldY, abs(y1-oldY))
                if abs(y1-oldY) > 15:
                    linesY.append(y1)
                oldY = y1
            # print(x1,y1,x2,y2)
            # cv2.line(open_cv_image,(x1,y1),(x2,y2),(0,255,0),2)
    # https://docs.opencv.org/3.4.0/dd/d1a/group__imgproc__feature.html#ga46b4e588934f6c8dfd509cc6e0e4545a
    # cv2.imwrite('houghlines3.jpg',open_cv_image)

    # print(linesY)
    rows=[]
    linesX = list(map(lambda x:x-minX,linesX))
    for r in range(len(linesY)-1):
        cols = []
        for c in range(len(linesX)-1):
            # (linesX[c],linesY[r],linesX[c+1],linesY[r+1])
            crop_img2 = crop_img.crop((linesX[c], linesY[r], linesX[c+1], linesY[r+1]))
            if charWhitelist:
                cols += [ImageOCR.pytesseract.image_to_string(crop_img2,
                                                              lang='eng',
                                                              config='--oem 0 -c tessedit_char_whitelist='+charWhitelist)]
            else:
                cols += [ImageOCR.pytesseract.image_to_string(crop_img2,
                                                              lang='eng',
                                                              config='')]
        rows.append(cols)
    return rows


def extractProcess(rule, im):
    if rule.ruleType == "boundary":
        return boundaryExtract(rule.data, im, rule.charWhitelist)
    elif rule.ruleType == "table":
        return tableExtract(rule.data, im, rule.charWhitelist)
