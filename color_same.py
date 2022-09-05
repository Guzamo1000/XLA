import cv2
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
import imutils


# Chuyển RGB sang tên
import webcolors
import time
start = time.time()
def closest_colour(requested_colour):
    min_colours = {}
    for key, name in webcolors.CSS3_HEX_TO_NAMES.items():
        r_c, g_c, b_c = webcolors.hex_to_rgb(key)
        rd = (r_c - requested_colour[0]) ** 2
        gd = (g_c - requested_colour[1]) ** 2
        bd = (b_c - requested_colour[2]) ** 2
        min_colours[(rd + gd + bd)] = name
    return min_colours[min(min_colours.keys())]

requested_colour = (141,13,16)
closest_name = closest_colour(requested_colour)

print("closest colour name:", closest_name)
print("Tempo: ", time.time() - start)
def get_colour_name(requested_colour):
    try:
        closest_name = actual_name = webcolors.rgb_to_name(requested_colour)
    except ValueError:
        closest_name = closest_colour(requested_colour)
        actual_name = None
    return actual_name, closest_name
def color_high_kmean(path,clusters):
    """
    Find popular colors
    input: path image
    output: list RGB (image)
    """
    img=cv2.imread(path,1)
    img=imutils.resize(img,height=200)
    flat_img=np.reshape(img,(-1,3))
    kmeans=KMeans(n_clusters=clusters,random_state=0)
    kmeans.fit(flat_img)
    dominant_colors = np.array(kmeans.cluster_centers_,dtype='uint')
    percentages = (np.unique(kmeans.labels_,return_counts=True)[1])/flat_img.shape[0]
    p_and_c = zip(percentages,dominant_colors)
    p_and_c = sorted(p_and_c,reverse=True)
    image=[]
    for i in range(len(p_and_c)):
        image.append(p_and_c[i][1])
        image[i]=(image[i].tolist())
        image[i].reverse()
    return image

def name_main_color(rgb):
    """
    find color near (Euclidean distance)
    input: code RGB
    output: RGB near
    """
    COLORS={
        "RED": ["lighsalmon","salmon","darksalmon","LightCoral","IndianRed","Crimson","Red","FireBrick","DarkRed"],
        "ORANGE": ["Orange","DarkOrange","Coral","Tomato","OrangeRed"],
        "YELLOW": ["Gold","Yellow","LightYellow","LemonChiffon","LightGoldenRodYellow","PapayaWhip","Moccasin","PeachPuff","PaleGoldenRod","Khaki","DarkKhaki"],
        "GREEN": ["GreenYellow","Chartreuse","LawnGreen", "Lime","LimeGreen","PaleGreen","LightGreen","MediumSpringGreen","SpringGreen","MediumSeaGreen","SeaGreen","ForestGreen","Green","DarkGreen","YellowGreen","OliveDrab","DarkOliveGreen","MediumAquaMarine","DarkSeaGreen","LightSeaGreen","DarkCyan","Teal" ]
    }
    vl=None
    for keys,value in COLORS.items():
      for i in value:
        i=i.lower()
        color=get_colour_name(rgb)[1]
        # print(color)
        if i.lower()==color.lower():
          return keys
    return get_colour_name(rgb)[1]
def cl(path,clusters):
  c=color_high_kmean(path,clusters)
  return name_main_color(c[0])
  # return get_colour_name(min(d)[1])