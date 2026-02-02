import pandas as pd 
import re

#Background on Dataset:
#This dataset is from a prospective cohort study by Da Silva Rocha et al.(2020) which includes 133 pregnant women with a gestational age below 20 weeks.
#These women have visceral adipose tissue (VAT) measured using ultrasound at the periumbilical region.
#An association between higher VAT levels and GDM diagnosis at the end of pregnancy was observed.

#Dataset: https://physionet.org/content/maternal-visceral-adipose/1.0.0/ 

data = pd.read_csv('visceral_fat_study.csv')
data.head()
for col in data.columns:
    print(col)
data_copy = data

#DATA CLEANING
#Changing column names 
#Using regular expression to remove unit measurements at the end of names 
#Using rstrip to add an underscore to replace spaces and to remove trailing underscores
col_names = []
for col in data_copy.columns:
    x = re.findall(r"\([\w]+\)| \([\w]+[/][\w]+\)", col)
    if len(x) ==0:
        col_names.append(col.replace(" ", "_"))
    else:
        col = col.rstrip(str(x)).replace(" ", "_").rstrip("_")
        col_names.append(col)

#Adding the new column names
data_copy.columns = col_names
data_copy


#Checking for Missing Values
data.isnull().sum()
#Missing Values: 1 for ethnicity, 5 for pregnancies, 30 for fasting glucose, 1 for pregestational bmi 

#Handling Missing Values:
#Dataset is already small so I don't want to remove rows.
#For first fasting glucose and pregestational bmi, the null values will be replaced with the mean.
#For ethnicity and number of pregnancies, they will be converted to the mode

replace_na = { "ethnicity":data["ethnicity"].mode(), "pregnancies": data["pregnancies"].mode().iloc[0], "first_fasting_glucose":data["first_fasting_glucose"].mean(),"bmi_pregestational": data["bmi_pregestational"].mean()}
for col, value in replace_na.items():
    data_copy[col].fillna(value, inplace=True)
data_copy.isnull().sum()


#Fix current gestational age  and gestational age at birth columns
#currently the columns are in a weeks,days format - e.g 12,1
#convert it to a decimal and round the value to 1 decimal place


data_copy.head()

def conv_to_decimals(data, variable):
    new_value = []
    for row in data[variable]:
        weeks,days=row.split(",")
        #convert to total days
        new_value.append(round((int(weeks)*7 + int(days))/7,1))
    return new_value

new_current_gest_age = conv_to_decimals(data_copy,"current_gestational_age")
new_ges_age_birth = conv_to_decimals(data_copy,"gestational_age_at_birth")

data_copy["current_gestational_age"] = new_current_gest_age
data_copy["gestational_age_at_birth"] = new_ges_age_birth

#confirmed that it is now in a decimal format:
data_copy[["gestational_age_at_birth", "current_gestational_age"]].head()


#IDENTIFYING INDIVIDUALS WITH DIABETES MELLITUS
dm_cases = data_copy.loc[data_copy["diabetes_mellitus"]==1]

#Removing participant with diabetes mellitus
data_copy = data_copy.drop([119], axis=0)

#There is one case of diabetes mellitus (DM) in the GDM group. 
#I have removed this individual since having pre-existing diabetes could influence the results.
#Study is looking at using visceral fat content to predict GDM
#If an individual already has diabetes, it impact the findings. 

#REMOVING DIABETES_MELLITUS COLUMN
data_copy = data_copy.drop("diabetes_mellitus", axis=1)

#No more DM cases so dropping the column.


#SUMMARY STATISTICS
round(data_copy.describe(),2)

#Save new dataset with clean data
data_copy.to_csv("gdm_vat_data_cleaned.csv", index=False)

