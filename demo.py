# -*- coding: utf-8 -*-
"""UserInterface.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1SoFL9hM12G1dqx7HfNySdlI1rk35rih2
"""

# pip install gradio

import os
import numpy

import tensorflow as tf
import torch
from model import EfficientNetB0
import gradio as gr
import tensorflow_hub as hub

import torchvision
from torchvision import transforms

from torchvision.transforms.functional import to_tensor, to_pil_image


from PIL import Image
from PIL import ImageColor
from PIL import ImageDraw
from PIL import ImageFont
from PIL import ImageOps


model = EfficientNetB0()
checkpoint=torch.load("lastest.pt", map_location='cpu')

model.load_state_dict(checkpoint['my_classifier'])
model.eval()

def load_img(path):
  img = tf.io.read_file(path)
  img = tf.image.decode_jpeg(img, channels=3)
  return img

def run_detector(detector, downloaded_image_list):
  img_list = downloaded_image_list
  result_list=[]
  for imgpath in img_list:
    img = load_img(imgpath)
    converted_img  = tf.image.convert_image_dtype(img, tf.float32)[tf.newaxis, ...]
    result = detector(converted_img)

    result = {key:value.numpy() for key,value in result.items()}
    result_list.append(result)

  return result_list

def save_crop_images(downloaded_result_list, image_path):
  for i in range(len(downloaded_result_list)):
    res = downloaded_result_list[i]
    boxes = res["detection_boxes"]
    class_names = res["detection_class_entities"]
    scores = res["detection_scores"]
    max_area = 0
    img = Image.open(image_path[i])
    im_width, im_height = img.size
    for j in range(min(boxes.shape[0], 10)):
      if scores[j] >= 0.1:
        if (class_names[j]==b'Man' or class_names[j]==b'Woman'):
          ymin, xmin, ymax, xmax = tuple(boxes[j])
          ymin, xmin, ymax, xmax = ymin*im_height, xmin*im_width, ymax*im_height, xmax*im_width
          area = (ymax-ymin) * (xmax-xmin)
          if (area > max_area):
            ymin_r, xmin_r, ymax_r, xmax_r = ymin, xmin, ymax, xmax
            max_area = area
    #display_image(img)
    cropped_img = img.crop((xmin_r, ymin_r, xmax_r, ymax_r))
    resized = ImageOps.fit(cropped_img, (128, 384), Image.ANTIALIAS)
    # newfp = downloaded_image_list[i].replace('jpeg_files', 'cropped_files') #####
    # fplist = newfp.split('/')
    # fplist = fplist[:-1]
    # foldername = '/'.join(fplist)
    # if not os.path.exists(foldername):
      # os.makedirs(foldername)
    resized.save(image_path[i], format="JPEG")
    #display_image(resized)

module_handle = "https://tfhub.dev/google/faster_rcnn/openimages_v4/inception_resnet_v2/1" #@param ["https://tfhub.dev/google/openimages_v4/ssd/mobilenet_v2/1", "https://tfhub.dev/google/faster_rcnn/openimages_v4/inception_resnet_v2/1", "https://tfhub.dev/tensorflow/mask_rcnn/inception_resnet_v2_1024x1024/1"]

detector = hub.load(module_handle).signatures['default']

inputs = [
  gr.inputs.Image(type='file', label="Image1"),
  gr.inputs.Image(type='file', label="Image2"),
  gr.inputs.Image(type='file', label="Image3"),
  gr.inputs.Image(type='file', label="Image4")
  #gr.inputs.CheckBox(lines=1, label="optional catego")
]

def imagesave(image):
  act=Image.open(image.name)
  act.save(image.name, format="JPEG", quality=90)
  act.close()
  return image.name

brands = ('Burberry', 'Prada', 'Thom Browne', 'A.P.C', 'Alexander Mcqueen', 'Balenciaga', 'Chanel', 
           'Louis Vuitton', 'Miu Miu', 'Hermes', 'Saint Laurent', 'Lemaire', 'Comme Des Garcons', 'Off White', 'Dior', 'Gucci')
introductions = ('Your brand identity is "Burberry"!\nYou have a warm, brownish feeling as if in autumn of nice weather.\nOf a style that can look simple, luxurious check adds elegance.',
'Your brand identity is "Prada"!\nYou give a neat feeling with a neat fit.\nEven with not bland color, your neat luxury gives credibility!',
'Your brand identity is "Thom Browne"!\nI guess you prefer gray achromatic colors and its suits!\nYour very neat style gives the feeling of an office worker who does work very well.',
'Your brand identity is “A.P.C."!\nNormality sometimes looks the prettiest and the coolest.\nYour casual style may give a friendly feeling to anybody!',
'Your brand identity is "Alexander Mcqueen"!\nYou give a neat feeling yet with strong individuality.\nYou would have been an aristocrat if you lived in the past.\nA suit may look quite stiff, but with unique individuality, you look cool!',
'Your brand identity is "Balenciaga"!\nYou look so snatched. Snatched and sophisticated feelings dominate you.\nYou seem like a fashion leader of the current generation!',
'Your brand identity is "Chanel"!\nYou are the representative of the luxurious.\nYour neat, but never simple style with splendid colors makes you even more gorgeous!',
'Your brand identity is "Louis Vuitton"!\nSometimes casual, sometimes neatly, you adjust your style to mood!\nWith casual style, you give the friendly feeling, and with your neat style, you give the trust feeling.',
'Your brand identity is "Miu Miu"!\nYou have a very girlish sensibility!\nInferring from your bubbly and lively style, you will be the representative of cuteness wherever you go.',
'Your brand identity is "Hermes"!\nYou look warm and elegant as if in the season of spring or autumn.\nIt may look quite simple, but simplicity gives a rather luxurious feeling.',
'Your brand identity is "Saint Laurent"!\nYou look chic and arrogant as a cold city.\nYour all-black fashion looks neat while giving a strong impression of confidence.',
'Your brand identity is "Lemaire"!\nYou have a casual and neat feeling.\nYour warm beige mood reminds of taking a picnic in warm weather.',
'Your brand identity is "Comme Des Garcons"!\nYou like to stand out everywhere, right?\nYou’re bursting with energy, and that energy you emit is strongly revealed in your fashion!',
'Your brand identity is "Off-White"!\nYou look snatched as if walking around the noisy streets.\nYour street fashion gives the feeling of swag!',
'Your brand identity is "Dior"!\nYou have a refined luxury that no one can easily follow.\nFully elegant, but with unique individuality points, you look luxurious!',
'Your brand identity is "Gucci"!\nYou strongly show your personality with splendor.\nBut with luxurious patterns, your personality looks more elegant.\nYou, the owner of unique fashion, are a true fashionista!')

img=('brand_images/Burberry.jpg', 'brand_images/Prada.jpg', 'brand_images/ThomBrowne.jpg','brand_images/APC.jpg',
     'brand_images/AlexanderMcqueen.jpg','brand_images/Balenciaga.jpg','brand_images/Chanel.jpg','brand_images/LouisVuitton.jpg',
     'brand_images/MiuMiu.jpg','brand_images/Hermes.jpg','brand_images/SaintLaurent.jpg','brand_images/LeMaire.jpg', 'brand_images/CommeDesGarcons.jpg',
     'brand_images/OffWhite.jpg''brand_images/Dior.jpg','brand_images/Gucci.jpg')

def processing(image1, image2, image3, image4):
  image_list=[]
  image_list.append(imagesave(image1))
  image_list.append(imagesave(image2))
  image_list.append(imagesave(image3))
  image_list.append(imagesave(image4))

  result_list=run_detector(detector, image_list)
  save_crop_images(result_list, image_list)
  cropped_images=[]
  test_transforms = transforms.Compose([transforms.ToTensor(),
     transforms.Normalize((0.480, 0.437, 0.425), (0.257, 0.247, 0.245))])
  
  for image in image_list:
    cropped_images.append(to_pil_image(load_img(image)))
    

  for cropped_image in cropped_images:
    image_tensor = test_transforms(cropped_image).float() 
    image_tensor = image_tensor.unsqueeze(0)
    input = Variable(image_tensor)
    input = input.to('cpu')
    output = model(input)
    index += output.data.cpu().numpy()

  idx=(index.argmax(dim=1)).int()
  for image in image_list:
    os.remove(image)
  
  return to_pil_image(load_image(img[idx])), brands[idx], introductions[idx]

outputs = [gr.outputs.Image(), gr.outputs.Textbox(), gr.outputs.Textbox()]

title = "Find my style, find my brand"
description = "Nowadays, fashion represents one's identity. Which brand has the same fashion identity with you?\nFind your brand by simply uploading your daily fashion styles!"

examples = [
    ["example_images/examplepicture1.jpg"],
    ["example_images/examplepicture2.jpg"]
]

gr.Interface(processing, inputs, outputs, title=title, description=description, examples=examples).launch(debug=True)
