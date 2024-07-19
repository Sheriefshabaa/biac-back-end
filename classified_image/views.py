
import os
import uuid
from rest_framework.views import APIView
from rest_framework.response import Response
from image.models import Image
from ultralytics import YOLO
from PIL import Image as pil_image
from .models import Classified_image
from rest_framework import status
from .serializers import ClassifiedImageHistoryDataSerializer, ClassifiedImageSerializer



def process_image(image) :
    """ -this function is doing n things :
    1- get the image psth and open it 
    2- reshape the image size to fit into classification model 
    3- load the model and send the image and receives the prediction dictionary
    4- make the predictied image path by removing the extension .jpeg -> get the path together
    5- prediction[0].save(output_image_path) -> this line saves the predicted image into its folder/path
    6- prepare & create the classified_image object in databse
    7- finally make the serializer and return it with response  """

    #1
    image_path = f"media/{image.provided_image}"
    input_image = pil_image.open(image_path)
    #2
    image_resized = input_image.resize([300, 300]) 
    #3
    model_file_path = 'model/burn/best.pt'
    model = YOLO(model_file_path)
    prediction = model.predict(image_resized,conf=0.5)
    #4
    my_uuid = uuid.uuid4()
    image_name = os.path.basename(image_path)
    image_name_without_jpg = image_name[:len(image_name)-5]
    output_image_path = os.path.join("media/", f"output_images/{image_name_without_jpg}_{my_uuid}.jpg")
    #5
    prediction[0].save(output_image_path)

    #6
    box_xywh=prediction[0].boxes.xywh
    box_conf=prediction[0].boxes.conf
    confidence = box_conf[0].item()
    confidence_score_rounded = round(confidence, 2)
    output_image_path = f"output_images/{image_name_without_jpg}_{my_uuid}.jpg"
    #6.1 get the burn_degree field 
    class_counts = {}
    for box in prediction[0].boxes:
        cls = int(box.cls)  # Get class ID
        class_counts[cls] = class_counts.get(cls, 0) + 1

    # Get the class name and count as variables
    class_name = None
    if class_counts:
        sorted_counts = sorted(class_counts.items(), key=lambda x: x[1], reverse=True)
        top_class_id, top_class_count = sorted_counts[0]
        class_name = model.names[top_class_id]
    print(f"bla bla {box_xywh[0][0]}")
    classified_image_object = Classified_image.objects.create(
        image_with_model_classification=output_image_path,
        image_id=image,
        image_width=box_xywh[0][0],
        image_height=box_xywh[0][1],
        image_cordinate_x=box_xywh[0][2],
        image_cordinate_y=box_xywh[0][3],
        confidence_score=(confidence_score_rounded*100),
        burn_degree=class_name,
    )
    #7
    classified_image_serializer = ClassifiedImageHistoryDataSerializer(classified_image_object)
    classified_image_serializer = ClassifiedImageHistoryDataSerializer(classified_image_object)
    return classified_image_serializer.data
    


class classifiy_image(APIView):
    def post(self, request, id,format=None):
        image_id = id
        try:
            image = Image.objects.get(id=image_id)
            processed_image_data = process_image(image)
            return Response({'processed_image_data': processed_image_data}, status=status.HTTP_200_OK)
        except Image.DoesNotExist:
            return Response({'error': 'Image not found'}, status=status.HTTP_404_NOT_FOUND)
        


    