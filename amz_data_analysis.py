# import libraries
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.graph_objects as go
import os

#set charts/tables background to darkgrid
sns.set_theme(style="darkgrid", font='Calibri', font_scale=1.2)

# load dataset
path = os.getcwd()
file_path = os.path.join(path, 'amazon.csv')
archive = pd.read_csv(file_path)

#print main informations

def incial_infos(): #print inicial informations
    print ("inicial infos: ")
    return archive.info()

def statistical_info(): #print statistical infos
    return archive.describe()

def null_values(): # print null value
    print(archive.isnull().sum())

# print line difference before and after basic cleaning

def after_basic_cleaning_len_dif():
    x = initial_len - len_after
    return x

# register initial archive len
initial_len = len(archive)

# removing duplicate

archive.drop_duplicates(inplace=True)

# register len of archieve after basic cleaning
len_after = len(archive)

# drop irrelevant columns to analysis

archive.drop(columns=['product_name', 'user_id', 'about_product', 'review_id', 'review_content', 'img_link', 'product_link'], inplace = True)

# data cleaning



archive['actual_price'] = archive['actual_price'].str.replace(r'[^\d.]', '', regex=True).astype(float) # remove irregular data

archive['discounted_price'] = archive['discounted_price'].str.replace(r'[^\d.]', '', regex=True).astype(float)

archive['rating_count'] = archive['rating_count'].str.replace(r'[^\d.]', '', regex=True).astype(float)

archive['rating'] = archive['rating'].str.replace(r' ', '', regex=True)

archive['rating'] = pd.to_numeric(archive['rating'], errors='coerce') #convert numerical data miss-classifies

archive['discount_percentage'] = pd.to_numeric(archive['discount_percentage'].str.rstrip('%'), errors='coerce')  # do both of the obove




# category creation for faciitating/enabeling data analysis
archive['category_short'] = archive['category'].str[:8] + "..." # create main categories

category_counts = archive['category_short'].value_counts() # count how many products are being selled per category

# create a data frame to enable creation of charts/tables with grouped data

category_apx_qnt = archive.groupby('category_short')['rating_count'].sum().to_dict()  #groups data
category_apx = pd.DataFrame(list(category_apx_qnt.items()), columns=['cat', 'quant']) #creates data frame
category_offer = category_apx.sort_values(by='quant', ascending=False) #sort values

rating_vs_discPD = archive.groupby('discount_percentage')['rating'].sum()
rating_vs_disc = pd.DataFrame(list(rating_vs_discPD.items()), columns=['discount', 'rating'])

category_vs_percPD = archive.groupby('category_short')['discount_percentage'].mean()
category_vs_percentage = pd.DataFrame(list(category_vs_percPD.items()), columns=['category', 'discount'])

category_vs_ratingdef = archive.groupby('category_short')['rating'].mean()
category_vs_rating = pd.DataFrame(list(category_vs_ratingdef.items()), columns=['category', 'rating'])

category_vs_pricePD= archive.groupby('category_short')['actual_price'].mean().sort_values(ascending=False)
category_vs_price = pd.DataFrame(list(category_vs_pricePD.items()), columns=['category', 'price'])

# create bin column

archive['discount_bin'] = pd.cut(
    archive['discount_percentage'], 
    bins=[0, 10, 20, 30, 40, 50, 60, 70, 80, 100],  # Define intervals
    labels=['0-10%', '10-20%', '20-30%', '30-40%', '40-50%', '50-60%', '60-70%', '70-80%', '80-100%']  # labels
)
# filter rating count for better analysis

df_filtered = archive[archive['rating_count'] < 200000]

print(archive['discounted_price'].mean())
print(archive['discount_percentage'].mean())
# - - - analysis - - - #

# Plots


category_counts.plot(kind='bar', 
                     color= ['#ffcad4', '#ffcad4', '#f4acb7']
                     )  

plt.title("Offer by Category")  
plt.xlabel("Category")  
plt.ylabel("Total of products offered")  
plt.xticks(rotation=45)   
plt.show()  


sns.regplot(
    data = archive,
    x = 'rating',
    y = 'rating_count',
    line_kws={"color": '#f4acb7'},
    scatter_kws={"color": "#ffcad4"}
)

plt.xlabel('Ratings')
plt.ylabel('rating_count')
plt.xticks(rotation=45)

plt.show()


sns.barplot(
    data=category_vs_rating,
    x='category',
    y='rating',
    color = '#f4acb7'
)
plt.xticks(rotation = 45)
plt.show()

sns.regplot(data=archive, 
            x="discount_percentage", 
            y="rating_count",
            line_kws={'color': '#f4acb7'},
            scatter_kws={'color': '#ffcad4'}
            )

plt.xlabel('discount')
plt.ylabel('rating_count')
plt.yscale('log')

plt.show()

# proves lack of correlation between discount and sellings
correlation = df_filtered['discount_percentage'].corr(df_filtered['rating_count'])
print(f'Correlação: {correlation:.2f}')

###
sns.barplot(
    data=category_vs_price,
    x='category',
    y='price',
    color = '#f4acb7'
)
plt.xticks(rotation = 45)
plt.show()

###
sns.regplot(data=archive, 
            x='discounted_price',
            y='rating_count',
            line_kws={'color': '#f4acb7'},
            scatter_kws={'color': '#ffcad4'}
            )

plt.xlabel('price')

plt.show()