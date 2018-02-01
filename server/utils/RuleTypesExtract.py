from utils import ImageOCR

def boundaryExtract(data, im):
    x, y, w, h = map(int, map(float, data.split(",")))
    # crop_img = im[y:y+h, x:x+w] use this for cv2 image
    x, y, x2, y2 = min(x, x+w), min(y, y+h), max(x, x+w), max(y, y+h)
    crop_img = im.crop((x, y, x2, y2))  # use this for pil Image
    # crop_img = ImageOCR.preprocess(crop_img)
    # crop_img.show()
    text = ImageOCR.pytesseract.image_to_string(crop_img, lang='eng')
    return text

def extractProcess(rule, im):
    if rule.ruleType == "boundary":
        return boundaryExtract(rule.data, im)
