# -*- coding: utf-8 -*-
"""eda-on-netflix.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/123F7jPphsTj4etQJddSAVbMxnG4bfRCY

## Exploratory Data Analytics on Netflix Data
![](https://media.giphy.com/media/oenruB2DKC7p6/giphy.gif)

### 2. Load the Packages and Data <a id=section102></a>
####  Import libraries or modules
"""

# Commented out IPython magic to ensure Python compatibility.
# %%time
# import numpy as np                 # for numerical computing
# import pandas as pd                # for dataframe and manipulation
# import seaborn as sns              #for graphs and data visualization
# from matplotlib import pyplot as plt
# sns.set()
# %matplotlib inline

"""#### Load the dataset"""

netflix = pd.read_csv("/content/sample_data/netflix_titles_2021.csv")

"""## 3.Data Profiling (Data Exploration)
<a id=section3></a>

### 3.1 Understanding the Dataset(Basic information about dataset)
<a id=section301></a>
"""

netflix.head() # for shows top 5 rows

netflix.tail() # For bottom 5 rows

netflix.shape         # to show the total no. of columns and rows

"""- This dataset contains 8807 rows and 12 columns."""

netflix.size       # to show the total no. of volume(elements)

netflix.columns       # to shows each column name

netflix.dtypes      # to shows data types each column name

netflix.info()        # to shows indexes,data types each column name

netflix.describe() # for shows statistical information

netflix.describe(include='all')

#Finding how many unique values are in the dataset
netflix.nunique()

"""### Data Preperation(Data Cleaning)
- Check missing values
- Fill null values
"""

netflix.isnull()           # to shows where the null values is present

miss=netflix.isnull().sum()            # to shows the count of null values
miss

miss1 = (netflix.isnull().sum()/len(netflix))* 100
miss1

#missing values with %
m = pd.concat([miss,miss1],axis=1,keys=['Total','Missing%'])
m

sns.heatmap(netflix.isnull())         # using heatmap to shows the null value count

"""- From the above output we can see that __director__ , __cast__ ,**country** columns contains __maximum null values__. We will see how to deal with them.

- So, We Delete director and cast columns because they are not going to use those features right now.
"""

# making copy of dataset for changes
netflix_copy = netflix.copy()
netflix_copy.head()

netflix_copy =netflix_copy.dropna(how='any',subset=['director','cast'])
netflix_copy.head(2)

netflix_copy.fillna({'country':'missing','rating':'missing','duration':'missing'},inplace=True)

netflix_copy.isnull().sum()

"""### 3.2 Pre-Profiling
<a id=section302></a>
"""

pip install -U pandas_profiling

import pandas_profiling as prf

"""#### Now performing __pandas profiling__ to understand data better."""

netflix_profile = prf.ProfileReport(netflix)
netflix_profile

netflix_profile.to_file(output_file="netflix21_before_preprocessing.html")

"""### 3.3 Preprocessing

- Dealing with duplicate rows<br/>
    - Find number of duplicate rows in the dataset.
    - Print the duplicate entries and analyze.
    - Drop the duplicate entries from the dataset.
<a id=section303></a>
"""

netflix[netflix.duplicated()]   # to shows the dupbicate rows

netflix.duplicated().sum()       # to shows the count of dupbicate rows

"""* No duplicate rows are present in this dataset."""

#check size after cleaning
netflix_copy.shape

# save netflix_copy into csv
netflix_copy.to_csv('netflix_clean.csv')

"""## 4.EDA Questions
<a id=section4></a>

### 4.1. What different types of show or movie are uploaded on Netflix?  or
###  How many TV shows & Movies are in the dataset? Show with Bar Gragh?

<a id=section401></a>
"""

netflix_copy.head(2)

# method-1:
netflix_copy.groupby('type')['title'].count().sort_values(ascending = False)

# method-2:
netflix_copy.type.value_counts().to_frame('Value_count')

#sns.countplot(netflix_copy['type'])# to show the count of all uniqu item of a any column in the form of bargragp

"""**Obeservation**: There are **5522-types** of movies and  **178-types** of tv shows are uploaded on Netflix.

### 4.2 What is the Correlation between the features?
<a id=section402></a>
"""

netflix_copy.dtypes

"""- Converting object into datetime formate of "date_added"

"""

netflix_copy["date_added"]=pd.to_datetime(netflix_copy['date_added'])
netflix_copy.head(2)

"""- Now ,we create two features year_added and month_added from date_added column."""

netflix_copy['year_added'] = netflix_copy["date_added"].dt.year
netflix_copy['month_added'] = netflix_copy["date_added"].dt.month
netflix_copy.head(2)

netflix_copy.dtypes

netflix_copy.corr()

plt.subplots(figsize=(5,5))
sns.heatmap(netflix_copy.corr(),annot=True)
plt.show()

"""**Obeservation** : Above Heatmap shows correlation between release_year,year_added  & month_added.

### 4.3 Most watched shows on the Netflix?
<a id=section403></a>
"""

netflix_copy.type.value_counts().to_frame('Value_count')

sns.countplot(x=netflix_copy['type'],orient='v')
plt.xticks(rotation=90)

# by using Pie chart
type_show = ['Movie','TV Show']
Value_count = [5522,178]
plt.pie(Value_count,labels=type_show,autopct="%2.2f%%")
plt.legend(title='Most watched shows on the Netflix')

"""**Obeservation**: Audience likes to watched mostly **movies(96.88% )** over **TV shows(3.12%)**.

### 4.4 Distribution of Ratings? &
### What are the different rating defined by Netflix?
<a id=section404></a>
"""

netflix_copy.head(2)

#countplot for distrubution

sns.countplot(x=netflix_copy['rating'],orient='v')
plt.xticks(rotation=90)

netflix['rating'].nunique()

"""**Obeservation** : 
- Audience prefers mostly TV-MA & TV-14  and less prefers NC-17 as rating. 
- There are 17 types of ratings in the netflix.

### 4.5 Which has the highest rating Tv show or Movies?
<a id=section405></a>
"""

netflix_copy.head(2)

netflix.groupby("type")["rating"].agg(pd.Series.mode)

"""#### Adding new feature
new_genre (Genre 1,Genre 2,Genre 3)
"""

new_genre = netflix_copy['listed_in'].str.split(",",2)
new_genre

netflix_copy['Genre 1'] = new_genre.str.get(0)
netflix_copy['Genre 2'] = new_genre.str.get(1)
netflix_copy['Genre 3'] = new_genre.str.get(2)
netflix_copy.head(2)

netflix_copy['Genre 1'].describe(include=all)

netflix_copy['Genre 2'].describe(include=all)

netflix_copy['Genre 3'].describe(include=all)

"""- drop listed_in column because not need"""

netflix_copy.drop('listed_in',axis = 1,inplace = True)
netflix_copy.head(2)

netflix_copy.duplicated().sum()

netflix_copy.groupby(['Genre 1'])['release_year'].count().sort_values(ascending = False)

netflix_copy.groupby(['Genre 2'])['release_year'].count().sort_values(ascending = False)

netflix_copy.groupby(['Genre 3'])['release_year'].count().sort_values(ascending = False)

"""###  4.6 Finding the best Month for releasing content?
<a id=section406></a>
"""

netflix_copy.head(2)

# converting month number to month name
netflix_copy['month_final'] = netflix_copy['month_added'].replace({1:'Jan', 2:'Feb', 3:'Mar', 4:'Apr', 5:'May', 6:'June', 7:'July', 8:'Aug', 9:'Sep', 10:'Oct', 11:'Nov', 12:'Dec'})
netflix_copy.head(2)

netflix_copy.month_final.value_counts().to_frame('Value_count')

sns.countplot(x=netflix_copy['month_final'],orient='v')
plt.xticks(rotation=90)

"""**Obeservation:** Its clearly shows that **july** month has maximum number of movies released.july is the best Month for releasing content.

###  4.7 Highest watched genres on Netflix?
<a id=section407></a>
"""

netflix_copy.head(2)

netflix_copy['Genre 1'].describe(include=all)

netflix_copy['Genre 2'].describe(include=all)

netflix_copy['Genre 3'].describe(include=all)

# by using Pie chart
genre_types = ['genre 1','genre 2','genre 3']

Value_count = [5700,4485,2434]
plt.pie(Value_count, labels = genre_types, autopct="%2.2f%%")
plt.legend(title='Most watchedgenre on the Netflix')
plt.show()

"""**Obeservation:** Above Pi-chart  Shows that Genre1 has watched maximum times.

### 4.8 Released movie over the years?
<a id=section408></a>
"""

netflix_copy.head(2)

# no. of movies released by every year

netflix_copy.groupby(['release_year'])['release_year'].count().sort_values(ascending = False)

netflix_copy.release_year.value_counts().to_frame('Value_count')

sns.countplot(x='release_year', data=netflix).set_title('Count plot for Movies with passing Years.')
sns.set(rc={'figure.figsize':(20,20)})
plt.show()

"""**Observation:**

From the above we can see that with passing years more movies are being made year by year

The above data shows that there is a sudden increase in the creation of movies in year 2016 as compared to year 2015

### 4.9 movies made on year basis? or 
### In which year highest number of the TV shows & Movies were released? show with Bar Graph.
<a id=section409></a>
"""

netflix_copy.head(2)

netflix_copy.year_added.value_counts().to_frame('Value_count')

netflix_copy.dtypes

netflix_copy["date_added"].dt.year.value_counts()

netflix_copy["date_added"].dt.year.value_counts().plot(kind='bar')

"""**Obeservation**:
    Its clearly shows that maximum movie made on yr 2019.

### 4.10 What is the show id and director for 'House of cards'?
<a id=section410></a>
"""

netflix.head(2)

# method 1:
netflix[netflix['title'].isin(["House of Cards"])]  # to shows all records of a particular item in any column

# method 2:

netflix[netflix['title'].str.contains("House of Cards")]

"""**Obeservation**: For **"House of cards"** the show id is **s1059** and No director.

### 4.11 Show all the movies that were released in year 2000.
<a id=section411></a>
"""

netflix.head(2)

netflix[(netflix['type'] == 'Movie' ) & (netflix['release_year'] == 2000)]

netflix[(netflix['type'] == 'Movie' ) & (netflix['release_year'] == 2000)].shape

"""**Obeservation**: There are 33 movies released in year 2000.

### 4.12 Show only the title of all TV shows that were released in India only.
<a id=section412></a>
"""

netflix.head(2)

netflix[(netflix['type'] == 'TV Show') & (netflix['country'] == 'India')]["title"]

netflix[(netflix['type'] == 'TV Show') & (netflix['country'] == 'India')]["title"].shape

"""**Obeservation**:There are **79 tv shows**  that were released in India only.

### 4.13 Show top 10 director, who gave the highest number of TV shows & Movies to Netflix?
<a id=section413></a>
"""

netflix.head(2)

netflix["director"].value_counts().head(10)

# shown in bar graph 
netflix["director"].value_counts().head(10).plot(kind='bar')

"""**Observation** : Top 10 director list is shown .Rajiv Chilaka he released maximum no. of Tv shows in india

### 4.14 In how many movies/ tv shows, 'tom Cruise' was cast?
<a id=section414></a>
"""

netflix.head(2)

#method1:
netflix[netflix['cast'] == 'Tom Cruise']

#method2:

#netflix[netflix['cast'].str.contains('Tom Cruise')]

"""#### Nan values are present ,first FIll null values

* create new dataframe
"""

netflix_copy = netflix.dropna()
netflix_copy.head(2)

netflix_copy[netflix_copy['cast'].str.contains('Tom Cruise')]

"""**Obeservation**: There are two movies casted Mr.Tom Cruise -"Magnolia" & "Rain Man" .

### 4.15 How many movies got the "TV-14" rating in the caneda?
<a id=section415></a>
"""

netflix.head(2)

netflix[(netflix['type'] == 'Movie') & (netflix['rating'] == 'TV-14')].shape

netflix[(netflix['type'] == 'Movie') & (netflix['rating'] == 'TV-14') & (netflix['country'] == 'Canada')]

netflix[(netflix['type'] == 'Movie') & (netflix['rating'] == 'TV-14') & (netflix['country'] == 'Canada')].shape

"""**Insights**: There are 13  movies got the "TV-14" rating in the caneda.

### Post profiling
"""

netflix_cleaned = prf.ProfileReport(netflix_copy)
netflix_cleaned.to_file(output_file="netflix21_post_preprocessing.html")

netflix_cleaned.to_file(output_file="netflix21_post_preprocessing.html")

"""## 5. Conclusions:
- We explore the Netflix dataset and saw how to clean the data and then jump into how to visualize the data with **Exploratory Data Analysis**. We saw some basic and advanced level charts of seaborn and matplotlib like Heatmap,Pie-chart, Bar chart, Countplot.
- We see highest rating Tv show or Movies in dataset
- Which month is best for movies realising and so on.

- And also visualize a data with **Pandas_Profiling :Preprofiling & Post_profiling**.
<a id=section5></a>

### Thank You! Happy to get any suggestions or feedbacks.
"""