import cv2
import numpy as np

def light_dark(image):
    average = image.mean()
    if (average < 127):
        return 'Dark'
    else:
        return 'Light'

print("Attempting to read video...")
cap = cv2.VideoCapture('converter\Bad Apple.mp4')
output = cv2.VideoWriter('Threshold.mp4', cv2.VideoWriter_fourcc(*'mp4v'), 30, (1080, 1920))

if (cap.isOpened() == 0):
    print("Video not read")
else:
    print("Video read successfully")

frame_count = cv2.CAP_PROP_FRAME_COUNT
fps = cap.get(cv2.CAP_PROP_FPS)
width, height = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
centerX, centerY = int((width // 2)), int((height // 2))

while (cap.isOpened()):
    ret, fullSection = cap.read()  # Full frame of the video
    fullGS = cv2.cvtColor(fullSection, cv2.COLOR_BGR2GRAY)
    thresh, fullBW = cv2.threshold(fullGS, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)

    # Split into quarters
    topLeft = fullBW[0:centerY, 0:centerX]
    topRight = fullBW[0:centerY, centerX:width]
    bottomLeft = fullBW[centerY:height, 0:centerX]
    bottomRight = fullBW[centerY:height, centerX:width]

    # 8x8 section size
    Q_SizeX, Q_SizeY = int(width // 2), int(height // 2)
    Q_CenterX, Q_CenterY = int(centerX // 4), int(centerY // 4)
    S_Width, S_Height = int(width // 16), int(height // 16)

    # Convert to 8x8 square
    # Top left
    gridImage = np.copy(topLeft)  # Create a copy of topLeft to draw grid lines

    # Horizontal Line
    for i in range(1, 8):
        cv2.line(gridImage, (0, S_Height * i), (Q_SizeX, S_Height * i), (0, 0, 255), 1)

    # Vertical Line
    for j in range(1, 8):
        cv2.line(gridImage, (S_Width * j, 0), (S_Width * j, Q_SizeY), (0, 0, 255), 1)

    for i in range(0, 8):
        for j in range(0, 8):
            roi = topLeft[i * S_Height:i * S_Height + S_Height, j * S_Width:j * S_Width + S_Width]
            print(light_dark(roi), "\t", i + 1, "x", j + 1)
            output.write(gridImage)  # Write gridImage instead of topLeft
            cv2.imshow("Bad Apple", gridImage)
            if cv2.waitKey(1) & 0xFF == ord('s'):
                break

cap.release()
output.release()
cv2.destroyAllWindows()
