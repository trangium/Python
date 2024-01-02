''' Test cases:
6 https://cf.geekdo-images.com/imagepage/img/5lvEWGGTqWDFmJq_MaZvVD3sPuM=/fit-in/900x600/filters:no_upscale()/pic260745.jpg
10 cute_dog.jpg
6 turtle.jpg
'''
import PIL
from PIL import Image
import urllib.request
import io, sys, os, random, time
import tkinter as tk
from PIL import Image, ImageTk  # Place this at the end (to avoid any conflicts/errors)

def choose_random_means(k, img, pix, colSet): # done
   return random.choices(list(colSet), k=k)

# goal test: no hopping
def check_move_count(mc):
   return False

# calculate distance with the current color with each mean
# return the index of means
def dist(col, means):
   minIndex, dist_sum = 0, 255**2+255**2+255**2
   for idx, val in enumerate(means):
      dist = (val[0]-col[0])**2 + (val[1]-col[1])**2 + (val[2]-col[2])**2
      if dist < dist_sum:
         dist_sum = dist
         minIndex = idx
   return minIndex

def getMean(tuples):
   return tuple(sum(i[j] for i in tuples)/len(tuples) for j in range(3))

def clustering(img, pix, prevCounts, prevHops, means, count): # return: count for each bucket, move_count, means
   buckets = [[] for x in means]
   for i in range(img.size[0]):
      for j in range(img.size[1]):
         color = pix[i, j]
         idx = dist(color, means)
         buckets[idx].append(color)
   bucketCounts = [len(i) for i in buckets]
   return bucketCounts, 69420, [getMean(b) for b in buckets]

def update_picture(img, pix, means):
   for i in range(img.size[0]):
      for j in range(img.size[1]):
         pix[i, j] = tuple(map(int, means[dist(pix[i, j], means)]))
   region_dict = {}
   return pix, region_dict
   
def distinct_pix_count(img, pix): # done
   cols = {}
   for i in range(img.size[0]):
      for j in range(img.size[1]):
         color = pix[i, j]
         if color not in cols: cols[color] = 1
         else: cols[color] += 1
   max_col, max_count = pix[0, 0], 0
   for col in cols:
      if cols[col] > max_count:
         max_col = col
         max_count = cols[col]
   return len(cols.keys()), max_col, max_count, cols

def main():
   k = int(sys.argv[1])
   file = sys.argv[2]
   if not os.path.isfile(file):
      file = io.BytesIO(urllib.request.urlopen(file).read())
   
   window = tk.Tk() #create an window object
   
   img = Image.open(file)
   
   img_tk = ImageTk.PhotoImage(img)
   lbl = tk.Label(window, image = img_tk).pack()  # display the image at window
   
   pix = img.load()   # pix[0, 0] : (r, g, b) 
   print ('Size:', img.size[0], 'x', img.size[1])
   print ('Pixels:', img.size[0]*img.size[1])
   d_count, m_col, m_count, colSet = distinct_pix_count(img, pix)
   print ('Distinct pixel count:', d_count)
   print ('Most common pixel:', m_col, '=>', m_count)

   count_buckets = [0 for x in range(k)]
   move_count = [10 for x in range(k)]
   means = choose_random_means(k, img, pix, colSet)
   print ('Random means:', means)
   count = 1
   while not check_move_count(move_count):
      count += 1
      count_buckets, move_count, means = clustering(img, pix, count_buckets, move_count, means, count)
      if count == 2:
         print ('first means:', means)
         print ('starting sizes:', count_buckets)
      else:
         diffs = [c-o for c, o in zip(count_buckets, oldCounts)]
         print('diff', count, diffs)
         if all(d==0 for d in diffs): break
      oldCounts = count_buckets
   pix, region_dict = update_picture(img, pix, means)  # region_dict can be an empty dictionary
   print ('Final sizes:', count_buckets)
   print ('Final means:')
   for i in range(len(means)):
      print (i+1, ':', means[i], '=>', count_buckets[i])
      
   img_tk = ImageTk.PhotoImage(img)
   lbl = tk.Label(window, image = img_tk).pack()  # display the image at window

   img.save("kmeans/2023vtrang.png", 'PNG')  # change to your own filename
   window.mainloop()
   #img.show()
   
if __name__ == '__main__': 
   main()
