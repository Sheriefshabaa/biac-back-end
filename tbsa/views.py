from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.parsers import JSONParser, MultiPartParser, FormParser
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
import torch
from ultralytics import YOLO
from PIL import Image 
from .models import Tbsa_image , Tbsa
import pandas
from tbsa.serializers import TbsaBasicInfoSerializer , TbsaHandImageSerializer , TbsaBurnImagesSerializer , TbsaImageSerializer,ShowTbsaSerializer
# Create your views here.



class TbsaBasicInfoView(APIView):
    serializer_class = TbsaBasicInfoSerializer
    # permission_classes = [IsAuthenticated]
    def post(self, request):
        tbsa_serializer = TbsaBasicInfoSerializer(data=request.data, context={'request': request})
        if tbsa_serializer.is_valid():
            tbsa_serializer.save()
            return Response(tbsa_serializer.data, status=status.HTTP_201_CREATED)
        return Response(tbsa_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TbsaHandImageView(APIView):
    serializer_class = TbsaHandImageSerializer
    parser_classes = [MultiPartParser, FormParser]
    def post(self, request, id, format=None):
        serializer = TbsaHandImageSerializer(data=request.data, context={'tbsa_id': id})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class TbsaBurnImagesView(APIView):
    serializer_class = TbsaBurnImagesSerializer
    parser_classes = [MultiPartParser, FormParser]
    def post(self, request,id):
        serializer = TbsaBurnImagesSerializer(data=request.data,context={'tbsa_id': id})
        if serializer.is_valid():
            tbsa_burn_images_list = serializer.save() 
            burns_images_list_serializer = TbsaImageSerializer(tbsa_burn_images_list, many=True) 
            return Response(burns_images_list_serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


"""function for TBSA models"""


def hand_mask_pixels(hand_model , img):
  #get predictions
  
  results = hand_model(img, conf=0.5)
  #get the mask

  mask = results[0].masks.data
  #calculate the number of pixels
  num_pixels = torch.count_nonzero(mask)
  #save the result
  results[0].save(filename = 'hand_seg.jpg')
  return num_pixels.item()




def burn_mask_pixels(burn_model, imgs):
  #get predictions
  results = burn_model(imgs, conf=0.5)
  #get the masks and calculate the number of pixels
  num_pixels = 0
  for i, result in enumerate(results):
    mask = result.masks.data
    num_pixels = torch.count_nonzero(mask) + num_pixels
    #save the result
    result.save(filename = f'burn{i}.jpg')
  return num_pixels.item()



def resize_images(image_paths, new_width, new_height):
    resized_images = []
    for path in image_paths:
        img = Image.open(path)
        img_resized = img.resize((new_width, new_height))
        resized_images.append(img_resized)
    return resized_images


def calculate_the_tbsa(hand_pixels, burn_pixels):
  #calculate the %TBSA
  tbsa = ((burn_pixels * 3.3) * 0.8) / (hand_pixels)
  return tbsa



#calculate the fluid resuscitation
def calculate_the_fluid_amount(weight, tbsa):
  # (4ml * weight * %TBSA)
  fluid_amount = 4 * weight * tbsa
  return fluid_amount

def calculate_the_survival_probability(age, tbsa, inhalation_injury):
  #calculate the R-Baux score
  r_baux_score = age + tbsa + (17 * inhalation_injury)
  #return the survival probability
  if (r_baux_score >= 100):
    r_baux_score = 100
    return 100
  else:
    return 100 - r_baux_score
  



class TbsaModelView(APIView):
    def get(self, request,tbsa_id,hand_id,burn_last_image_id):
        # try:
            hand_image = Tbsa_image.objects.get(pk=hand_id)
            burn_image_id = hand_id + 1
            burn_images_pathes = []
            for i in range (burn_image_id,burn_last_image_id+1):
                burn_image = Tbsa_image.objects.get(pk=i)
                burn_images_pathes.append('media/'+ str(burn_image.image))
            ##### load hand model #####
            hand_model = YOLO('model/hand/last.pt')
            ##### load burns model #####
            burn_model = YOLO('model/burn/best.pt')
            ##### caculate hands pixels #####
            print("finish loading models")
            image_path = f"media/{hand_image.image}"
            image = Image.open(image_path)
            print(image_path)
            img_resized = image.resize((640, 640))
            print("finish image_resized")
            hand_pixels = hand_mask_pixels(hand_model,img_resized)
            ##### caculate burns images in pixels #####
            imgs_resized = resize_images(burn_images_pathes, 352, 352)
            print(burn_images_pathes)
            burn_pixels = burn_mask_pixels(burn_model, imgs_resized)
            ##### caculate TBSA #####
            tbsa = round(calculate_the_tbsa(hand_pixels, burn_pixels), 2)
            ##### calculate_the_fluid_amount #####
            fluid_amount = calculate_the_fluid_amount(70, tbsa)
            #test of "calculate_the_survival_probability" function
            survival_probability = calculate_the_survival_probability(25, tbsa, 0)
            tbsa_object = Tbsa.objects.get(pk=tbsa_id)
            tbsa_object.survival_probability = round(survival_probability)
            tbsa_object.total_burned_area = burn_pixels
            tbsa_object.first_dose_amount = round((fluid_amount/2))
            tbsa_object.second_dose_amount = round((fluid_amount/4))
            tbsa_object.third_dose_amount = round((fluid_amount/4))
            tbsa_object.tbsa = tbsa
            tbsa_object.save()
            tbsa_serializer = ShowTbsaSerializer(tbsa_object)
            return Response(tbsa_serializer.data,status=status.HTTP_200_OK)
        # except:
        #    return Response('the server is having issue... try later!',status=status.HTTP_400_BAD_REQUEST)
           




        
        






