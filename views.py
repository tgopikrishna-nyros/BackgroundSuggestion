from django.shortcuts import render, redirect
from .forms import *
from django.template import loader
from .apps import BackgroundConfig
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, routers, serializers, viewsets
from .serializers import UserSerializer, PictureSerializer
from django.contrib.auth.models import User
from .models import Picture
import numpy as np # To work with arrays
import cv2
from sklearn.cluster import KMeans # ML clustering algorithm to extract colors
from collections import Counter # To extract the count
import matplotlib.pyplot
from matplotlib.image import imread
import PIL
import operator
import colorsys
#from colour import Color
# Create your views here.
def index(request): 
  
    if request.method == 'POST':

        Picture.objects.all().delete()
        form = ImageForm(request.POST, request.FILES) 
  
        if form.is_valid():
            form.save()
            return redirect('success')
    else: 
        form = ImageForm() 
    return render(request, 'index.html', {'form' : form}) 
  
  
def success(request):
	img = Picture.objects.last()
	img_name = 'background/static/'+str(img.upload_img)
	image = cv2.imread(img_name)
	image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
	response = get_colors(image, 5)
	context = {
		'img': img,
		'most': response[0],
		'first': response[1],
		'second': response[2],
		'analogous1': response[3][0],
		'analogous2': response[3][1]
	}

	template = loader.get_template('success.html')
	return HttpResponse(template.render(context, request))

# To get complementary color
def get_complementary(color):
	color = color[1:] # Strip the # from the beginning
	color = int(color, 16) # Convert the string into hex
	comp_color = 0xFFFFFF ^ color # Substracting each of RGB component by 255(FF)
	comp_color = "#%06X" % comp_color # convert the color back to hex by prefixing a #
	return comp_color

def get_image(image_path):
	image = cv2.imread(image_path,0)
	image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
	return image

DEG30 = 30/360
def analogous_colors(clr, d=DEG30):
	clr = HEX2RGB(clr)
	print(clr)
	c = tuple(map(lambda x: x/255, clr))
	r = c[0]
	g = c[1]
	b = c[2]
	h, l, s = colorsys.rgb_to_hls(r, g, b)
	h = [(h+d) % 1 for d in (-d, d)]
	adjacent = [map(lambda x: int(round(x*255)), colorsys.hls_to_rgb(hi, l, s)) for hi in h]
	adjacent = list(adjacent)
	return adjacent[0], adjacent[1]

# Function to convert RGB color coding to HEX code
def RGB2HEX(color):
	return "#{:02x}{:02x}{:02x}".format(int(color[0]), int(color[1]), int(color[2]))

# Function to convert HEX to RGB
def HEX2RGB(value):
	value = value.lstrip('#')
	lv = len(value)
	return tuple(int(value[i:i + lv // 3], 16) for i in range(0, lv, lv // 3))

# Function to convert into darker colour
def darker(color, percent):
	# Assumes color is rgb between (0, 0, 0) and (255, 255, 255)
	color = np.array(color)
	#white = np.array([255, 255, 255])
	vector = color-color*percent
	return vector

def lighter(color, percent):
	# Assumes color is rgb between (0, 0, 0) and (255, 255, 255)
	color = np.array(color)
	#white = np.array([255, 255, 255])
	vector = color+color*percent
	return vector


first = ''
second = ''
analogous = ''
def get_colors(image, number_of_colors):
	# interpolation=cv2.INTER_AREA because for image shrinking
	modified_image = cv2.resize(image, (600, 400), interpolation = cv2.INTER_AREA)
	modified_image = modified_image.reshape(modified_image.shape[0]*modified_image.shape[1], 3)
	# It indicates pixels(width, height) and RGB color coding(3)
	    
	clf = KMeans(n_clusters = number_of_colors) # To generate number of clusters and centroids
	labels = clf.fit_predict(modified_image)
	    
	counts = Counter(labels)
	count_list = list(counts)
	mini = count_list.index(min(count_list))
	#counts_max = max(counts.iteritems(), key=operator.itemgetter(1))[0]
	#print(counts_max)
	    
	center_colors = clf.cluster_centers_
	# We get ordered colors by iterating through the keys
	ordered_colors = [center_colors[i] for i in counts.keys()]
	hex_colors = [RGB2HEX(ordered_colors[i]) for i in counts.keys()]
	rgb_colors = [ordered_colors[i] for i in counts.keys()]
	    
	# To get majorly occupied colour
	colors = counts.values()
	colors = list(colors)
	count_max = colors.index(max(colors))
	    
	color_hex = hex_colors[mini]
	#print("Major occupied color is {}".format(color_hex))
	    
	# Suggesting colors
	h2r = HEX2RGB(color_hex)
	threshold = h2r[0] + h2r[1] + h2r[2] # If it is <360 then dark color
	    
	global first
	global second
	global analogous
	if(threshold < 382):
	    lighter_color = RGB2HEX(lighter(h2r,0.4))
	    complementary_color = get_complementary(color_hex)
	    first = lighter_color
	    second = complementary_color
	    clr = lighter_color
	    analogous = list(analogous_colors(clr))
	    analogous[0] = RGB2HEX(list(analogous[0]))
	    analogous[1] = RGB2HEX(list(analogous[1]))
	    #print(color_hex, lighter_color, complementary_color, analogous[0], analogous[1])
	else:
	    darker_color = RGB2HEX(darker(h2r,0.6))
	    complementary_color = get_complementary(color_hex)
	    first = darker_color
	    second = complementary_color
	    clr = darker_color
	    analogous = list(analogous_colors(clr))
	    analogous[0] = RGB2HEX(list(analogous[0]))
	    analogous[1] = RGB2HEX(list(analogous[1]))
	    #print(color_hex, darker_color, complementary_color, analogous[0], analogous[1])
	return color_hex, first, second, analogous

def quality():
	return HttpResponse("Quality issue..!! Try with another image")


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

# ViewSets define the view behavior.
class PictureViewSet(viewsets.ModelViewSet):
    queryset = Picture.objects.all()
    serializer_class = PictureSerializer