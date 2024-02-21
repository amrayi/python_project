import face_recognition
from PIL import Image
import uuid
img1 = face_recognition.load_image_file('./known/robert deniro.jpg')
img1_encod = face_recognition.face_encodings(img1)[0]

img2 = face_recognition.load_image_file('./unknown/alpachino.jpg')
img2_encod = face_recognition.face_encodings(img2)

result = face_recognition.compare_faces([img1_encod], img2_encod)



# img = face_recognition.load_image_file('./known/robert deniro.jpg')
# face_locations = face_recognition.face_locations(img)

# for face_location in face_locations:
#     top, right, bottom, left = face_location
#     face = img[top:bottom , left:right] 
#     pill_img = Image.fromarray(face)
#     pill_img.show()
#     pill_img.save('%s.jpg' %(uuid.uuid1()))


# بررسی وجود داشتن چهره در دو عکس دیگر در ترمینال
# face_recognition ./known ./unknown