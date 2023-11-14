import cv2
from datetime import datetime

import shownoise
import Noiser
import imgUtils

image_path = "./in/50000.png"
img = image = cv2.imread(image_path)

now = datetime.now()
date_time_string = now.strftime("%Y_%m_%d_%H%M%S")

noisyImg = Noiser.add_poisson_noise(img, 50)

#noise = shownoise.extract_noise(img, noisyImg, 0, 1)

fourier = shownoise.rgb_to_fourier_cv2(noisyImg)

# cv2.imwrite("out/" + date_time_string + ".png", noise)
#imgUtils.writeHistoRGB(fourier, 0, date_time_string)

imgUtils.showHistoRGB(fourier, 0)