import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3' 
import tensorflow.keras
from PIL import Image, ImageOps, ImageGrab
import numpy as np
import time
import cv2


def main():
	maindir = os.path.dirname(__file__)
	modelsdir = os.path.join(maindir, "models")

	# Disable scientific notation for clarity
	np.set_printoptions(suppress=True)

	#loading models
	findArrow = tensorflow.keras.models.load_model(os.path.join(modelsdir, 'find_arrow.h5'), compile = False)
	solveArrow = tensorflow.keras.models.load_model(os.path.join(modelsdir, 'solve_arrow.h5'), compile = False)
	
	while(True):
		#get the four arrows
		size = (224, 224)
		x = 675
		counter = 1
		skipFlag = False
		dataFind = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)
		dataSolve = np.ndarray(shape=(4, 224, 224, 3), dtype=np.float32)
		arrowsList = []
		choice = input("run?")
		time.sleep(2)
		
		image = ImageGrab.grab()
		while (x < 1175 and counter < 5):
			y = 150
			while(y < 210):
				im = image.crop((x, y, x + 75, y + 75))
				im1 = ImageOps.fit(im, size, Image.ANTIALIAS)
				image_array = np.asarray(im1)
				normalized_image_array = (image_array.astype(np.float32) / 127.0) - 1
				dataFind[0] = normalized_image_array
				prediction = findArrow.predict(dataFind)
				if (prediction[0][0] > 0.95):
					im1.save("ARROW" + str(counter) + ".png") #UNNECESSARY
					arrowsList.append(image_array)
					counter = counter + 1
					skipFlag = True
					break
				y = y + 20
			if (skipFlag == True):
				x = x + 80
				skipFlag = False
			else:
				x = x + 20

		#check for 4 arrows
		print("THERE ARE " + str(counter - 1) + " ARROWS")

		#preprocess
		for i in range(4):
			img = arrowsList[i]
			img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

		   # gaussian blur
			img = cv2.GaussianBlur(img, (3, 3), 0)

			# color transform
			img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

			coefficients = (0.0445, 0.6568, 0.2987)
			img = cv2.transform(img, np.array(coefficients).reshape((1, 3)))
			
			img = cv2.cvtColor(img, cv2.COLOR_GRAY2RGB)
			cv2.imwrite(("pp" + str(i + 1) +".png"), img) #UNNECESSARY
			dataSolve[i] = (img.astype(np.float32) / 127.0) - 1

		#solve
		order = []

		prediction = solveArrow.predict(dataSolve)
		for i in range (counter - 1):
			#find max
			maxVal = 0
			maxIT = -1
			for j in range(4):
				if(maxVal < prediction[i][j]):
					maxVal = prediction[i][j]
					maxIT = j
			if (maxIT == 0):
				order.append("left")
			elif (maxIT == 1):
				order.append("right")
			elif (maxIT == 2):
				order.append("down")
			elif (maxIT == 3):
				order.append("up")

		print("ORDER IS:") 
		print(order)
		print("Left, Right, Down, Up")
		print(prediction)

	return

main()