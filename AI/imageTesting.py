import sys; args = sys.argv[1:]

#print (PIL.PILLOW_VERSION)
# URL = 'http://www.w3schools.com/css/trolltunga.jpg'
# #URL = sys.argv[1]
# f = io.BytesIO(urllib.request.urlopen(URL).read())

from PIL import Image, ImageTk # Place this at the end (to avoid any conflicts/errors)

#window.geometry("500x500") # (optional)
imagefile = "image.png"
img = Image.open(imagefile)

pix = img.load()

def chrome(color):
   if color < (255 // 3): return 0
   elif color > (255 // 3 * 2): return 255
   else: return 127
   
for x in range(img.size[0]):
   for y in range(img.size[1]):
      r, g, b, a = pix[x, y]
      bright = int(r*0.2 + g*0.5 + b*0.1)
      pix[x, y] = (bright//3, bright//2, bright//10, 255)

img.show()

img.save("kmeans/{}.png".format("2023vtrang"), "PNG")
