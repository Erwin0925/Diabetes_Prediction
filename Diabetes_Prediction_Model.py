import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import matplotlib.pyplot as plt #to plot charts
import seaborn as sns #used for data visualization
from scipy import stats #used to determine skewness
from pandas.plotting import scatter_matrix

## Import Dataset
from google.colab import drive
drive.mount('/content/drive')

#df=pd.read_csv('/content/drive/MyDrive/diabetes.csv') #tracy's
#df=pd.read_csv('/content/drive/MyDrive/Y3S1-cloud/FAI(G7)/diabetes.csv') #erwin's
df=pd.read_csv('/content/drive/MyDrive/diabetes.csv') #angeline's
df

# ## Data Understanding
# ☑ perform data exploration using techniques like data visualization and data profiling
# 1.   Head of the dataset
# 2.   Shape of the data set
# 3.   Types of columns
# 4.   Information about data set
# 5.   Summary of the data set
# ☑ data profiling enables us to calculate basic statistics like means, medians, and standard deviations
# ☑ data visualization offers a visual comprehension of data distributions and facilitates the detection of potential outliers or anomalies.
# histograms, scatter plots, and box plots

# view top 5 rows of the dataframe
print("First 5 Rows:")
df.head()

# last 5 rows
print("Last 5 Rows:")
df.tail()

# inspect the number of rows and columns in this dataframe
df.shape

# Accessing the columns attribute
column_names = df.columns
print("Column names:", column_names)

# display the data type of each column
df.dtypes

# Display the information about the data types, non-null values, and memory usage
df.info()

# Display summary statistics for numerical columns
  # count (number of non-null values)
  # mean: average value of the data in the column
  # standard deviation: amount of variation or dispersion of a set of values
  # minimum: smallest value in the column
  # 25th percentile (Q1): measure of the data's spread in the lower direction
  # median (50th percentile or Q2): represents the center of the data distribution
  # 75th percentile (Q3): measure of the data's spread in the upper direction
  # maximum: largest value in the column
df.describe()

# Note:
# *Typically, the normal range of **glucose** is around 70 to 100 mg/dL, with postprandial levels ideally below 140 mg/dL;*
# *normal **blood pressure** is around 120/80 mm Hg;*
# *normal **skin thickness** varies across the body, whcih means that will more than 0.1 millimeters*
# *normal **insulin levels** are generally between 5 and 15 uIU/mL;*
# *The **BMI** categories include underweight (BMI less than 18.5), normal weight (BMI 18.5 to 24.9), overweight (BMI 25 to 29.9), and obesity (BMI 30 or greater).*

# ▶**Data Understanding Conclusion:** <br>
# According to the above results, we can be observed that this dataframe has a total of 768 rows and 9 columns, and except BMI and DiabetesPedigreeFunction are float64, other attributes are int64.
# Although all data are no null value, but we found that its "min" value have 0.
# Logically, all glucose, blood pressure, skin thickness, insulin and BMI cannot have 0 value. So we will perform data cleaning and replacing the 0 value using interpolation.
# In addition, we can see that the "max" value of insulin shown in 846, it should not exist that high, so we will perform outlier detection in a later step.

# Set the style of seaborn for better aesthetics
sns.set(style="whitegrid")

# view the "outcome" is balanced or not
sns.countplot(x="Outcome", data=df, palette={0: '#507B58', 1: '#AB3131'})
plt.title("Distribution of Outcome")
plt.show()

# Selecting columns for histograms (excluding "Outcome")
columns_to_plot = df.drop("Outcome", axis=1).columns

# Histograms for each columns except outcome column
df[columns_to_plot].hist(figsize=(12, 10), color='#98BF64', edgecolor='white')
plt.suptitle("Histograms of Each Columns")
plt.show()

# Note:
# Only glucose and blood pressure are found to be regularly distributed; others are skewed and have outliers.

# Scatter plot for two Glucose and BloodPressure columns
sns.scatterplot(x='Glucose', y='BloodPressure', data=df, hue='Outcome', palette='Set1')
plt.title("Scatter Plot of Glucose vs. Blood Pressure")
plt.show()

sns.set(style="whitegrid")

# Create a pair plot for all columns, color-coded by "Outcome"
sns.pairplot(df, hue='Outcome', palette='Set1')
plt.suptitle("Pair Plot of All Columns", y = 1.02)
plt.show()

scatter_matrix(df, figsize=(20, 20))
plt.tight_layout(pad=1.0)
plt.suptitle("Multivariate Scatter Matrix", y = 1.02)
plt.show()

# Box plot for each columns
plt.figure(figsize=(16,12))
sns.boxplot(data=df, palette='Set2')
plt.title("Box Plots of Each Columns")
plt.show()


# Note:<br>
# According to the Box plot above, we observe that some columns have outliers, such as Blood Presure, Skin Thickness, BMI, especially Insulin.

# ## Data Preparation
# ❗missing values -> all attributes cannot logically have **zero** values.
# ☑ Data cleaning : handling of missing values and transformations of variables as needed
# 1. Dropping duplicate values
# 2. Checking NULL values
# ☑ performed interpolation to fill the missing data with average values for these specific attributes.
# 1. Checking for 0 value and replacing it (interpolation)
# ☑ perform outlier detection to identify and handle the outliers to improve the model quality and performance by using interquartile range (IQR).Check result using:
# 1. Box plots
# 2. Using Z score

duplicates_exist = df.duplicated().any()

if duplicates_exist:
    print("Yes, duplicates found. Proceeding to clean.")
    df = df.drop_duplicates()
else:
    print("No duplicates found. No cleaning required.")


null_counts = df.isnull().sum()

if null_counts.sum() > 0:
    print("Yes, null values found. Here are the counts:")
    print(null_counts)
else:
    print("No null values found.")


columns_to_check = ['BloodPressure', 'Glucose', 'SkinThickness', 'Insulin', 'BMI']

for column in columns_to_check:
    count_zeros = (df[column] == 0).sum()
    if count_zeros > 0:
        print(f"Yes, there are 0 values in column {column}, there are total of {count_zeros} 0 values.")
    else:
        print(f"No, there are no 0 values in column {column}")



# Check skewness for 0 values replacement

for column in columns_to_check:
    skewness = df[column].skew()
    print(f"Skewness for {column}: {skewness}")


# Note:
# Replace 0 values with Median (Skewed Distributions):
# 1. BloodPressure: Highly negatively skewed. (-1.8436079833551302)
# 2. Insulin: Highly positively skewed. (2.272250858431574)
# 3. BMI: Moderately negatively skewed. (-0.42898158845356543)
# Replace 0 values with Mean (Approximately Normal Distributions):
# 1. Glucose: Slightly positively skewed, but relatively close to normal. (0.17375350179188992)
# 2. SkinThickness: Slightly positively skewed, but relatively close to normal. (0.10937249648187608)

#replace 0 values with Median:
df['BloodPressure']=df['BloodPressure'].replace(0,df['BloodPressure'].median())
df['Insulin']=df['Insulin'].replace(0,df['Insulin'].median())
df['BMI']=df['BMI'].replace(0,df['BMI'].median())

#replace 0 values with Mean:
df['Glucose']=df['Glucose'].replace(0,df['Glucose'].mean())
df['SkinThickness']=df['SkinThickness'].replace(0,df['SkinThickness'].mean())

df2 = df.drop("Outcome", axis = "columns")

for column in df.iloc[:, :-1].columns:
    skewness = df[column].skew()
    print(f"Skewness for {column}: {skewness}")

# Note:
# Remove outliers and replace with median:
# 1. Pregnancies
# 2. SkinThickness
# 3. Insulin
# 4. DiabetesPedigreeFunction
# 5. Age
# Remove outliers and replace with mean:
# 1. Glucose
# 2. BloodPressure
# 3. BMI

# List of columns to remove outliers and replace with median
replace_with_median = ['Pregnancies', 'SkinThickness', 'Insulin', 'DiabetesPedigreeFunction', 'Age']

for column in replace_with_median:
    # Calculate Q1 (25th percentile) and Q3 (75th percentile)
    Q1 = df[column].quantile(0.25)
    Q3 = df[column].quantile(0.75)

    # Calculate the IQR (Interquartile range)
    IQR = Q3 - Q1

    # Determine the lower and upper bounds for outliers
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR

    # Find outliers and replace them with the median
    outliers = (df[column] < lower_bound) | (df[column] > upper_bound)
    df.loc[outliers, column] = df[column].median()


# List of columns to remove outliers and replace with mean
replace_with_mean = ['Glucose', 'BloodPressure', 'BMI']

for column in replace_with_mean:
    # Calculate Q1 (25th percentile) and Q3 (75th percentile)
    Q1 = df[column].quantile(0.25)
    Q3 = df[column].quantile(0.75)

    # Calculate the IQR (Interquartile range)
    IQR = Q3 - Q1

    # Determine the lower and upper bounds for outliers
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR

    # Find outliers and replace them with the mean
    outliers = (df[column] < lower_bound) | (df[column] > upper_bound)
    mean_value = df[column].mean()
    df.loc[outliers, column] = mean_value


fig, axes = plt.subplots(3, 3, figsize=(12, 8))

# Flatten the axes array for easy iteration
axes = axes.flatten()

# Plot each column in its subplot
for i, column in enumerate(df.columns):
    sns.boxplot(x=df[column], ax=axes[i])

axes[-1].set_visible(False)

# Adjust layout for better display
plt.suptitle("Box Plots of Each Column")
plt.tight_layout()
plt.show()



from scipy.stats import zscore

fig, axes = plt.subplots(3, 3, figsize=(12, 8))

df_zscores = df.apply(zscore)

# Flatten the axes array for easy iteration
axes = axes.flatten()

# Plot Z-scores of each column in its subplot
for i, column in enumerate(df_zscores.columns):
    sns.boxplot(x=df_zscores[column], ax=axes[i])

axes[-1].set_visible(False)

# Adjust layout for better display
plt.suptitle("Z-Score Box Plots of Each Column")
plt.tight_layout()
plt.show()


from sklearn.preprocessing import QuantileTransformer

# Create a QuantileTransformer object
quantile_transformer = QuantileTransformer(n_quantiles=len(df), output_distribution='normal', random_state=0)

# List of columns to be transformed
columns_to_transform = ['Insulin', 'BMI', 'DiabetesPedigreeFunction', 'Age']

# Apply the QuantileTransformer to the specified columns
df[columns_to_transform] = quantile_transformer.fit_transform(df[columns_to_transform])


column_with_outliers = ['Insulin', 'BMI', 'DiabetesPedigreeFunction', 'Age']
for column in df[column_with_outliers]:
    skewness = df[column].skew()
    print(f"Skewness for {column}: {skewness}")


# List of columns to remove outliers from
replace_with_median = ['Age']

for column in replace_with_median:
    # Calculate Q1 (25th percentile) and Q3 (75th percentile)
    Q1 = df[column].quantile(0.25)
    Q3 = df[column].quantile(0.75)

    # Calculate the IQR (Interquartile range)
    IQR = Q3 - Q1

    # Determine the lower and upper bounds for outliers
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR

    # Find outliers and replace them with the median
    outliers = (df[column] < lower_bound) | (df[column] > upper_bound)
    df.loc[outliers, column] = df[column].median()


# List of columns to remove outliers from and replace with mean
replace_with_mean = [ 'BMI', 'Insulin', 'DiabetesPedigreeFunction']

for column in replace_with_mean:
    # Calculate Q1 (25th percentile) and Q3 (75th percentile)
    Q1 = df[column].quantile(0.25)
    Q3 = df[column].quantile(0.75)

    # Calculate the IQR (Interquartile range)
    IQR = Q3 - Q1

    # Determine the lower and upper bounds for outliers
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR

    # Find outliers and replace them with the mean
    outliers = (df[column] < lower_bound) | (df[column] > upper_bound)
    mean_value = df[column].mean()
    df.loc[outliers, column] = mean_value


df_outliers = df[['Insulin', 'BMI', 'DiabetesPedigreeFunction', 'Age']]

fig, axes = plt.subplots(2, 2, figsize=(8, 4))

# Flatten the axes array for easy iteration
axes = axes.flatten()

# Plot each column in its subplot
for i, column in enumerate(df_outliers.columns):
    sns.boxplot(x=df_outliers[column], ax=axes[i])

# Adjust layout for better display
plt.suptitle("Box Plots of Columns after continues removing outliers")
plt.tight_layout()
plt.show()


fig, axes = plt.subplots(2, 2, figsize=(8, 4))

zscores = df_outliers.apply(zscore)

# Flatten the axes array for easy iteration
axes = axes.flatten()

# Plot Z-scores of each column in its subplot
for i, column in enumerate(zscores.columns):
    sns.boxplot(x=zscores[column], ax=axes[i])

# Adjust layout for better display
plt.suptitle("Z-Score Box Plots of Columns after continues removing outliers")
plt.tight_layout()
plt.show()

# ## Modelling

#Pearson's Correlation Coefficient to find relationship between 2 quantities

corrmat = df.corr()
sns.heatmap(corrmat, annot = True)



df_selected = df.drop(['BloodPressure', 'Insulin', 'DiabetesPedigreeFunction'], axis = 'columns')

# Display the original DataFrame
print("Original DataFrame:")
print(df)

# Drop the 'Outcome' column to create the feature matrix X
X = df.drop('Outcome', axis=1)

# Display the DataFrame after dropping 'Outcome'
print("\nDataFrame after dropping 'Outcome':")
print(X)

# Specify the target variable
target_name = 'Outcome'

# Extract the target variable
y = df[target_name]

from sklearn.model_selection import train_test_split

#Splitting data in 80% training data and 20% testing data
X_train, X_test, y_train, y_test= train_test_split(X,y,test_size=0.2,random_state=0)


X_train.shape,y_train.shape



X_test.shape,y_test.shape


# ## Evaluation

# **Logistic Regression Model**

from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report,confusion_matrix
from sklearn.metrics import f1_score, precision_score, recall_score,accuracy_score


reg = LogisticRegression(penalty='l2', C=0.5, solver='liblinear', max_iter=200)
reg.fit(X_train,y_train)


lr_pred=reg.predict(X_test)


print("Classification Report is:\n",classification_report(y_test,lr_pred))
print("\n F1:\n",f1_score(y_test,lr_pred))
print("\n Precision score is:\n",precision_score(y_test,lr_pred))
print("\n Recall score is:\n",recall_score(y_test,lr_pred))
print("\n Confusion Matrix:\n")
sns.heatmap(confusion_matrix(y_test,lr_pred))


# **Random Forest Model**

from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report,confusion_matrix
from sklearn.metrics import f1_score, precision_score, recall_score
from sklearn.model_selection import RepeatedStratifiedKFold
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
import seaborn as sns


# define models and parameters
model = RandomForestClassifier()
n_estimators = [1800]
max_features = ['sqrt', 'log2']


# define grid search
grid = dict(n_estimators=n_estimators,max_features=max_features)
cv = RepeatedStratifiedKFold(n_splits=10, n_repeats=3, random_state=1)
grid_search = GridSearchCV(estimator=model, param_grid=grid, n_jobs=-1, cv=cv, scoring='accuracy',error_score=0)


best_model = grid_search.fit(X_train, y_train)


rf_pred=best_model.predict(X_test)


print("Random Forest Classifier Metrics:")
print("Classification Report is:\n", classification_report(y_test, rf_pred))
print("Confusion Matrix:\n")
sns.heatmap(confusion_matrix(y_test, rf_pred))

# Train K-Nearest Neighbors Classifier
knn = KNeighborsClassifier()
knn.fit(X_train, y_train)
knn_pred = knn.predict(X_test)

# Print K-Nearest Neighbors Classifier metrics
print("\nK-Nearest Neighbors Classifier Metrics:")
print("F1 Score:\n", f1_score(y_test, knn_pred))
print("Precision Score:\n", precision_score(y_test, knn_pred))
print("Recall Score:\n", recall_score(y_test, knn_pred))

# ☑ drop the “Outcome” attribute before training the model
# ☑ perform feature selection to find out the most relevant and informative features by removing the redundant features.
# Pearson's Correlation Coefficient to help us identify the relationship between pairs of features among the eight attributes
#  -> drop the lower correlation coefficient value of attributes
# ☑ perform data splitting, 80% is for training and 20% is for testing
# ☑ Logistic Regression, Random Forest, and Naive Bayes.

# **Naive Bayes Model**


from sklearn.naive_bayes import GaussianNB
from sklearn.model_selection import GridSearchCV

param_grid_nb = {
    'var_smoothing': np.logspace(0,-2, num=100)
}
nbModel_grid = GridSearchCV(estimator=GaussianNB(), param_grid=param_grid_nb, verbose=1, cv=10, n_jobs=-1)


best_model= nbModel_grid.fit(X_train, y_train)


nb_pred=best_model.predict(X_test)

print("Classification Report is:\n",classification_report(y_test,nb_pred))
print("\n F1:\n",f1_score(y_test,nb_pred))
print("\n Precision score is:\n",precision_score(y_test,nb_pred))
print("\n Recall score is:\n",recall_score(y_test,nb_pred))
print("\n Confusion Matrix:\n")
sns.heatmap(confusion_matrix(y_test,nb_pred))
