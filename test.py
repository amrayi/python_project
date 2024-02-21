import re
import uuid 
# import face_recognition

# Meta Character   . _ ^ _ $ _ {} _ |
# Sequenses        \d _ \D _ \s _ \S _ \w _ \W
# Sets             [a-z] _ [^] _ [0-9]
# Method           search() _ sub() _ split() _ findall()

# email = r'amirmohammadamrayi@gmail.com'
# pattern1 = '.+\@.+\..+'

# result1 = re.findall(pattern1, email)

# if result1:
#     print("Your email is valid")

# phone = '09365674142'
# pattern2 = '^(0936|0937|0938|0939)(\d{7}$)'

# result2 = re.findall(pattern2, phone)
# if result2:
#     print("Iransell")

# img1 = face_recognition.load_image_df('./1/ih;ohn')
# img1_encod = face_recognition.face_encoding(img1)

# img2 = face_recognition.load_image_df('./2/khch')
# img2_encod = face_recognition.face_encoding(img2)

# img1.save('%s.jpg' %(uuid.uuid1()))