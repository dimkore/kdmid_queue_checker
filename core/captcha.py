import cv2
import decimal
import pytesseract

def frange(x, y, jump):
  while x < y:
    yield float(x)
    x += decimal.Decimal(jump)

class CaptchaSolver:
    def __init__(self):
        self.Image = None

    def GetNumbers(self, numDig=0):
        apperances = {}
        # try all reasonable angles
        for angle in frange(-45, 45, 0.5):
            rimg = self.rotateImage(angle)
            clean = self.cleanImage(rimg)   
            # crop out center of image 
            clean = clean[330:550, 20:780]

            numbers = self.recognizeImage(clean)
            if numDig>0 and len(numbers) != numDig:
                continue

            if numbers in apperances:
                apperances[numbers] += 1
            else:
                apperances[numbers] = 1

        return max(apperances, key=apperances.get)

    def recognizeImage(self, img):
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img_rgb = cv2.resize(img_rgb, None, fx=2, fy=1)
        digits = pytesseract.image_to_string(img_rgb, config='--psm 8 --oem 0 -c tessedit_char_whitelist=0123456789')
        return digits.replace(" ", "").replace("\n", "")

    def rotateImage(self, angle):
        # Get the dimensions of the image
        (height, width) = self.Image.shape[:2]
        # Compute the center of the image
        center = (width // 2, height // 2)
        # Generate the rotation matrix using the angle and the image center
        rotation_matrix = cv2.getRotationMatrix2D(center, angle, 1.0)
        # Perform the rotation
        return cv2.warpAffine(self.Image, rotation_matrix, (width, height))

    def cleanImage(self, img):
        # Convert to grayscale
        c_gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
        # Enlarge image
        c_gray = cv2.resize(c_gray, None, fx=4, fy=4)
        # Median filter
        out = cv2.medianBlur(c_gray, 1)
        # Image thresholding
        out = cv2.threshold(out, 150, 255, cv2.THRESH_BINARY)[1]

        # Filter using contour area and remove small noise (< 1000)
        cnts = cv2.findContours(out, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        cnts = cnts[0] if len(cnts) == 2 else cnts[1]
        for c in cnts:
            area = cv2.contourArea(c)
            if area < 1000:
                cv2.drawContours(out, [c], -1, 255, cv2.FILLED)
            else:
                # thiner contour erea in order to get rid of small lines
                cv2.drawContours(out, [c], -1, 255, 6)

        # Median filter
        out = cv2.medianBlur(out,3)
        return out

    def ReadImage(self, path):
        # Load the image
        self.Image = cv2.imread(path)
        if self.Image is None:
            raise("Error: Image not found.")

    def LoadImage(self, image):
        self.Image = image