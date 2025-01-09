import cv2
import os

from core.captcha import CaptchaSolver

dirname = os.path.dirname(__file__)
dirname = os.path.join(dirname, 'test-data')

wrong = right = 0
for sample in os.listdir(dirname):
    filename = os.path.join(dirname, sample)

    if not os.path.isfile(filename):
        continue

    img = cv2.imread(filename)
    # crop middle imgage
    img = img[0:200, 200:400]

    captcha = CaptchaSolver()
    captcha.LoadImage(img)
    guessed_code = captcha.GetNumbers(6)
    actual_code = os.path.splitext(sample)[0].split('-')[1]
    if guessed_code == actual_code:
        right+=1
    else:
        wrong+=1

print('right: %d, wrong: %d, ratio %.1f%%' % (right, wrong, ((right / (right + wrong)) * 100)))