import numpy as np
import cv2
    

def blue_noise_generator(width, height):
    try:
        # Generate white noise
        noise = np.random.rand(width, height)
        
        # Apply a low-pass filter to the noise
        kernel = np.array([[1, 1, 1], [1, 0, 1], [1, 1, 1]]) / 8
        
        # Ensure that kernel has the same shape as noise
        kernel = np.pad(kernel, ((0, width - 3), (0, height - 3)), 'constant')
        
        # Perform 2D convolution between noise and kernel
        filtered_noise = np.real(np.fft.ifft2(np.fft.fft2(noise) * np.fft.fft2(kernel)))
        
        # Normalize the filtered noise to [0, 1]
        normalized_noise = (filtered_noise - np.min(filtered_noise)) / (np.max(filtered_noise) - np.min(filtered_noise))
        
        # Invert the normalized noise to get blue noise
        blue_noise = 1 - normalized_noise
        
        return blue_noise
    except Exception as e:
        # Log the error
        print(f"Error: {e}")
        return None
    



image = cv2.imread("classroom_512_50000.png", cv2.IMREAD_COLOR)
hauteur, largeur, _ = image.shape

noiseImg = blue_noise_generator(largeur, hauteur)

for y in range(hauteur):
        for x in range(largeur):
             if(noiseImg[y,x] < 1):
                  noiseImg[y,x] = 0

noiseImg = cv2.multiply(noiseImg, 1)

cv2.imwrite("blueNoise.png", noiseImg)