# Data exploration

import pandas as pd
import matplotlib.pyplot as plt

df_bookings = pd.read_csv("C:\\Users\\DELL\\PycharmProjects\\CodeBasics\\Data\\Project-1-Hospitality\\fact_bookings.csv")
# print(df_bookings.head())

# Performing basic data exploration:
# 1. Identifying number of rows and columns in the dataset
print("Shape of the dataset:", df_bookings.shape)
print()

# 2. Identifying unique room categories
print("Room categories are:", df_bookings['room_category'].unique())
print()

# 3. Identifying unique booking platforms
print("Booking platforms are:", df_bookings['booking_platform'].unique())
print()

# 4. Identifying no. of bookings per platform
print("Number of bookings per platform:")
print(df_bookings['booking_platform'].value_counts())

# To plot the above as a barchart
df_bookings['booking_platform'].value_counts().plot(kind='bar')
# plt.show()

# 5. Obtaining quick statistics of the numeric columns
print("Summary statistics of the numeric columns")
print(df_bookings.describe())
print()

# if do not want the e value in revenue_generated column
# print("Revenue generated minimum value:", df_bookings["revenue_generated"].min())
# print("Revenue generated maximum value:", df_bookings["revenue_generated"].max())
# print()

# Python's snake case convention: words separated by _ and everything is small case

# Loading all the other datasets:
df_date = pd.read_csv("C:\\Users\\DELL\\PycharmProjects\\CodeBasics\\Data\\Project-1-Hospitality\\dim_date.csv")
df_hotels = pd.read_csv("C:\\Users\\DELL\\PycharmProjects\\CodeBasics\\Data\\Project-1-Hospitality\\dim_hotels.csv")
df_rooms = pd.read_csv("C:\\Users\\DELL\\PycharmProjects\\CodeBasics\\Data\\Project-1-Hospitality\\dim_rooms.csv")
df_agg_bookings = pd.read_csv("C:\\Users\\DELL\\PycharmProjects\\CodeBasics\\Data\\Project-1-Hospitality\\fact_aggregated_bookings.csv")

# --------------------------------------------------------------------------------------------------------------------

# Data cleaning
print("---------- DATA CLEANING ----------")
print()

print("Summary statistics of bookings data")
print(df_bookings.describe())
print()

# 1. no. of guest column has some error values

print("No. of guests having negative values")
print(df_bookings[df_bookings["no_guests"]<0])
print()

# this is how we clean it
df_bookings = df_bookings[df_bookings["no_guests"] > 0]
print("Shape of data with negative guests removed:", df_bookings.shape)
print()

# 2. data cleaning for revenue generated column
print("Revenue generated minimum value:", df_bookings["revenue_generated"].min())
print("Revenue generated maximum value:", df_bookings["revenue_generated"].max())
print()  # maximum values is coming to 28 million which is not possible

# we will remove those values which are more than 3 standard deviations away from mean
# since we can consider values more than 3 std. deviations away as outliers

avg = df_bookings["revenue_generated"].mean()
print("Mean value of revenue generated:", avg)
std = df_bookings["revenue_generated"].std()
print("Standard deviation of revenue generated:", std)
print()

higher_limit = avg + 3*std
lower_limit = avg - 3*std
print("Value of mean + 3 std deviations:", higher_limit)
print("Value of mean - 3 std deviations:", lower_limit)
print()  # thus values that fall beyond more than this can be considered as outlier

# check whether there is revenue generated in negative
print("Values for revenue generated less than 0")
print(df_bookings[df_bookings["revenue_generated"] < 0])
print()

print("Values for revenue generated greater than higher_limit")
print(df_bookings[df_bookings["revenue_generated"] > higher_limit])
print()

# in order to remove them, we will use the reverse condition
df_bookings = df_bookings[df_bookings["revenue_generated"] < higher_limit]

print("Shape of data with values above higher_limit removed:", df_bookings.shape)
print()

# 3. data cleaning for revenue realized column
print("Summary statistics for revenue realised column:")
print(df_bookings["revenue_realized"].describe())
print()
# maximum values is 45k, now how do we know if it is a valid value or not?
# in order to know, we will perform a std. deviation check

high_limit = df_bookings["revenue_realized"].mean() + 3*df_bookings["revenue_realized"].std()
print("Value of mean + 3 std deviations for revenue realized:", high_limit)
print()

print("Checking the data points in revenue realized above high_limit")
print(df_bookings[df_bookings["revenue_realized"] > high_limit])
print()  # we have 1299 such rows, but upon observation we see they are all RT4 rooms

# what is RT4 rooms?
print(df_rooms)  # RT4 is presidential suite which are expensive rooms

# we look at RT4 rooms more closely
print("RT4 rooms summary statistics")
print(df_bookings[df_bookings["room_category"] == "RT4"].revenue_realized.describe())
print()

# so, for RT4, the real outlier would be any room that is having more than
# 50k nightly rent. and the maximum rent is 45k which means we do not have a
# any outliers in revenue_realized column

print("---------- HANDLING NA VALUES ----------")
# for this we call .isnull() function and see what values it gives: true or false
print("Checking for null values")
print(df_bookings.isnull().sum())
print()  # we have ~77k null values in ratings given
# so, it is okay to have NA values in this column and we wil not perform NA handling
# for this column.

'''
Thus, we did data cleaning for:
- no. of guests column: since no. of guests cannot be negative
- revenue generated column: using statistics
'''

# ---------------------------------------------------------------------------------------------------------------------

# Data transformation
print("---------- DATA TRANSFORMATION ----------")
print()

# In hotel business, there is a concept called occupancy percentage which
# is successful bookings / capacity. Example: out of 30 rooms, only 25 room
# were booked. So, OCC% = 25/30= 83%. It is an important metric.

# So now, in our data frame we will create a new column in our dataframe which
# will show occupancy percentage.

df_agg_bookings["occ_pct"] = df_agg_bookings["successful_bookings"] / df_agg_bookings["capacity"]
print(df_agg_bookings.head())
print()

# getting the occ_pct in percentage format using lambda function
df_agg_bookings["occ_pct"] = df_agg_bookings["occ_pct"].apply(lambda x: round(x*100, 2))
print("Post transformation of occ_pct column")
print(df_agg_bookings.head())
print()

'''
Other types of transformation that we can have
1. Creating new type of column:
If we have stock data frame which has two columns price and earning.
We would have to derive new columns called 'ration fields'. One of them
is pe(price to earning) ratio which is price/earning. e can create a new 
column by writing one line of code
df['pe_ratio'] = df.apply(lambda x: x['price']/x['eps'], axis=1)

2. Normalization:
We have Apple stock prices in USD and RIL stock prices in INR. Now, if 
we want to compare these two stocks, the stocks have to be in the same 
currency.
So, what we can do is apply transformation by creating a new column called 
'price_inr'where all the prices will be in INR by using an apply function.

def convert(x):
    if x['currency'] == 'USD':
        return x['price'] * 8-
    return x['price']
df['price_inr'] = df.apply(convert, axis=1)

We can actually call a forex API and get he latest rate

3. Merge: In the movies example, we had a movies dataframe and a financial 
dataframe. We ca merge the two to see movies and its revenue.

df = pd.merge(df_movies, df_financials, on="movies_id)

4. Aggregation: Here, we have some data where we want to aggregate it,
meaning we would to get the mean/std. dev, etc.
For example, if we want to know what is the revenue generated from every
industry we would use Pandas groupby
df.groupby("industry")["revenue"].sum()
'''


# ---------------------------------------------------------------------------------------------------------------------

# Insights generation
print("---------- INSIGHTS GENERATION ----------")
print()


# We want to find out average occupancy rate for each of the room
# categories as well as the cities


# Ad Hoc Analysis/Questions:
# 1. Average occupancy rate in each of the room categories
print("Occupancy percentage for all room categories")
print(df_agg_bookings.groupby("room_category")["occ_pct"].mean().round(2))
print()

# What kind of rooms are RTs? Is it standard or presidential?
# This information is stored in df_rooms., So, we will merge the
# two DataFrames

df = pd.merge(df_agg_bookings, df_rooms, left_on="room_category", right_on="room_id")

print("Occupancy percentage for all room categories, updated")
print(df.groupby("room_class")["occ_pct"].mean().round(2))
print()

# there are two columns containing RT information
df.drop("room_id", axis=1, inplace=True) # axis=1 is column and inplace=True modify that df

# 2. Average occupancy rate per city
df = pd.merge(df, df_hotels, on="property_id")

df.groupby("city")["occ_pct"].mean().plot(kind="bar")
plt.show()

# 3. When was the occupancy better? Weekday or weekend?
df = pd.merge(df, df_date, left_on="check_in_date", right_on="date")

print("Occupancy better on weekday or weekend?")
print(df.groupby("day_type")["occ_pct"].mean().round(2))
print()

# 4. In the month of June, what was the occupancy for different cities?
# Filter the data just for June
df_june_22 = df[df["mmm yy"] == "Jun 22"]

print("Occupancy percentage of different cities in June 2022")
df = df_june_22.groupby("city")["occ_pct"].mean().round(2).sort_values()
print(df)
print()

# 5. We have a new dataset for the month of august. So, we have to append
# August data ino existing dataframe
df_august = pd.read_csv("C:\\Users\\DELL\\PycharmProjects\\CodeBasics\\Data\\Project-1-Hospitality\\new_data_august.csv")

latest_df = pd.concat([df, df_august], ignore_index=True, axis=0)

# 6. Get the revenue realised per city
df_bookings_all = pd.merge(df_bookings, df_hotels, on='property_id')

df = df_bookings_all.groupby("city")["revenue_realized"].sum()
print("Revenue realized of all cities")
print(df)
print()

# 7. Get all the month by month revenue
pd.merge(df_bookings_all, df_date, left_on="check_in_date", right_on="date")

# Upon performing the merge we saw that the data type of the date is object.
# So, we now want to convert it from object to date type.

df_date["date"] = pd.to_datetime(df_date["date"], format="%d-%m-%y")
df_bookings_all["check_in_date"] = pd.to_datetime(df_bookings_all["check_in_date"], format="%d-%m-%y")

df_bookings_all = pd.merge(df_bookings_all, df_date, left_on="check_in_date", right_on="date")

df = df_bookings_all.groupby("mmm yy")["revenue_realized"].sum()

print("Revenue realised for all months")
print(df)
print()