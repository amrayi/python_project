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

# print(df.loc[df['cat1'].str.contains('for')])
print(df.loc[(df['city'] == 'Tehran') & (df['platform'] == 'web')])
