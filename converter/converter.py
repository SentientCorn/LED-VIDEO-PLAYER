import cv2
import numpy as np

TLarray, TRarray, BLarray, BRarray = [], [], [], []

def light_dark(image):
    average = image.mean()
    if (average < 127):
        return '0'
    else:
        return '1'

def print_list(my_list):
    for item in my_list:
        print(item)

def display_section (_input, _name, _QWidth, _QHeight, _SWidth, _SHeight, _grid):
  display = np.copy(_input)
  if _grid == 1:
    for i in range (1,8):
      cv2.line(display, (0, _SHeight * i), (_QWidth, _SHeight * i), (0, 0, 255), 1)
      cv2.line(display, (_SWidth * i, 0), (_SWidth * i, _QHeight), (0, 0, 255), 1)
  cv2.imshow(f"{_name}", display)

print("Attempting to read video...")
cap = cv2.VideoCapture('converter\Bad Apple.mp4')

if (cap.isOpened() == 0):
    print("Video not read")
else:
    print("Video read successfully")

frame_count = cv2.CAP_PROP_FRAME_COUNT
fps = cap.get(cv2.CAP_PROP_FPS)
width, height = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
centerX, centerY = int((width // 2)), int((height // 2))

while (cap.isOpened()):
    read, fullSection = cap.read()  # Full frame of the video
    if not read:
        break 
    fullGS = cv2.cvtColor(fullSection, cv2.COLOR_BGR2GRAY)
    thresh, fullBW = cv2.threshold(fullGS, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)

    # Split into quarters
    topLeft     = fullBW[0:centerY, 0:centerX]
    topRight    = fullBW[0:centerY, centerX:width]
    bottomLeft  = fullBW[centerY:height, 0:centerX]
    bottomRight = fullBW[centerY:height, centerX:width]

    # 8x8 section size
    Q_SizeX, Q_SizeY        = int(width // 2), int(height // 2)
    S_Width, S_Height       = int(width // 16), int(height // 16)

    # Display sections (Because why not?)
    display_section(topLeft,"Top Left", Q_SizeX, Q_SizeY, S_Width, S_Height, 1)
    display_section(topRight,"Top Right", Q_SizeX, Q_SizeY, S_Width, S_Height, 1)
    display_section(bottomLeft,"Bottom Left", Q_SizeX, Q_SizeY, S_Width, S_Height, 1)
    display_section(bottomRight,"Bottom Right", Q_SizeX, Q_SizeY, S_Width, S_Height, 1) 

    # Convert to 8x8 square
    # Top left



    for i in range(0, 8):
        for j in range(0, 8):
            roi = topLeft[i * S_Height:i * S_Height + S_Height, j * S_Width:j * S_Width + S_Width]
            TLarray.append(light_dark(roi))
            # print(light_dark(roi), "\t", i + 1, "x", j + 1)
    
    if cv2.waitKey(1) & 0xFF == ord('s'):
        break





# print_list(TLarray)

cap.release()
cv2.destroyAllWindows()
