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

import pandas as pd 
df = pd.read_csv('divar_posts_dataset.csv')

# print(df[['cat1', 'cat2']][0:5])
# print(df.head(10))

# for row in df.iterrows():
#     print(row)

# print(df.loc[df['city'] == 'Tehran'])
# print(df.sort_values(['city' , 'platform'] , ascending= [0,1]))


# df = df.loc[df['city'] == 'Tehran']
# df = df.reset_index(drop= True)
# df.to_csv('tehran_posts.csv', index= False)

print(df.loc[(df['city'] == 'Tehran') & (df['platform'] == 'web')])
# print(df.loc[df['cat1'].str.contains('for')])


import class_math as Riazi

my_math = Riazi.Math(20,5)
print(my_math.sub())
