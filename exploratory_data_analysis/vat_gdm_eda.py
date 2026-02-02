#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan  3 21:09:22 2024

@author: tiffanyng
"""
import pandas as pd 
import numpy as np 
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import norm, f, ttest_ind, chi2_contingency

#Load dataset
data_copy = pd.read_csv("gdm_vat_data_cleaned.csv")


#VISUALIZATIONS

#USING FACETGRID TO COMPARE NUMBER OF PARTICIPANTS BY DISEASE STATUS
#Plot comparing total number of participants with GDM and without GDM
g = sns.FacetGrid(data_copy, col="gestational_dm")
g.map_dataframe(sns.histplot, x="gestational_dm")
g.set_axis_labels("GDM Status", "Count")
plt.show()

#GDM/non-GDM ratio in cohort:
#Filtering for rows based off GDM status
non_gdm = data_copy.loc[data_copy["gestational_dm"] == 0]
gdm = data_copy.loc[data_copy["gestational_dm"] == 1]

#proportion of GDM to non-GDM is around 0.15:
len(gdm)/len(non_gdm)

#Summary
#There are many more individuals without GDM than with GDM in this study.
#This is expected since it is a cohort study where a group of individuals are recruited at random.
#GDM occurs in around 5-15% of pregnancies so the ratio seen in the participants was expected.  

#Visualizations of variables will be stratified by GDM status since the study is comparing GDM vs non-GDM individuals


#BARPLOTS FOR CATEGORICAL VARIABLES
#Barplots to look at averages of categorical variables between GDM and non-GDM
#The demographic variables are categorical variables.

#Categorical variables
cat_var = ["ethnicity", "pregnancies", "type_of_delivery"]

#BARPLOTS
ncols = 2
nrows = int(np.ceil(len(cat_var)/ncols))
fig,axes = plt.subplots(nrows=nrows, ncols=ncols)

for i, var in enumerate(cat_var):
    row = int(np.floor(i/ncols))
    col = i%ncols
    
    #barplot
    sns.set_style("dark")
    a = sns.barplot(data_copy, x=data_copy["gestational_dm"], y=data_copy[var], ax= axes[row,col], color="lightblue")
    
    #axis properties
    a.tick_params(labelsize=8)

plt.suptitle("Barplots of Categorical Variables (non-GDM = 0, GDM = 1)", fontsize=12)
plt.tight_layout()
plt.show() 


#Note about measurements:
#Those with GDM= 1 and non_GDM=0
#Ethnicity (white=0, non-white=1): the results are showing the average value(range from 0 to 1)
#Type of Delivery (vaginal=0, c-section=1): the results are showing the average value(range from 0 to 1)

#Summary:
#It appears that the women with GDM on average are higher age, had more pregnancies, and more c-sections.
#Ethnicity (white vs non-white) seems to be distributed equally.
#I want to take a closer look at the overall distribution of values for these variables with violinplots.



#VIOLINPLOTS FOR CATEGORICAL VARIABLES

#Violin plots can show the distribution and proportion of values for categorical variables.

ncols = 2
nrows = int(np.ceil(len(cat_var)/ncols))
fig,axes = plt.subplots(nrows=nrows, ncols=ncols)

for i,var in enumerate(cat_var):
    row = int(np.floor(i/ncols))
    col = i%ncols
    
    sns.set_style("dark")
    sns.violinplot(ax=axes[row,col], data=data_copy, x=data_copy["gestational_dm"], y=data_copy[var], 
                   palette = "deep", hue= data_copy["gestational_dm"])
    axes[row,col].legend([], [], frameon=False)
 

#add main title
plt.suptitle("Violinplots for Categorical Variables", fontsize=12)
plt.tight_layout()
plt.show()

#Summary:
#This plot makes it more evident that those with GDM tend to be of a higher age, have more pregnancies, and have more c-sections.
#This is expected as these are all risk factors for GDM.




#BOXPLOTS FOR CONTINUOUS VARIABLES
#Boxplots to see distribution of data and to identify potential outliers

#Boxplot variables (continuous variables)
bp_var = ["mean_diastolic_bp", "mean_systolic_bp", "central_armellini_fat",
"first_fasting_glucose","bmi_pregestational", "child_birth_weight", "gestational_age_at_birth", "current_gestational_age", "age"]

#NON-GDM
ncol = 3
nrow = int(np.ceil(len(bp_var)/ncol))
fig,axes = plt.subplots(nrow, ncol)
for i, var in enumerate(bp_var):
    row = int(np.floor(i/ncol))
    col = i%ncol
    
    #boxplots
    axes[row,col].boxplot(non_gdm[var], patch_artist=True,
            boxprops=dict(facecolor="royalblue", color="black", linewidth=1),
            whiskerprops=dict(color="black", linewidth=1), 
            medianprops=dict(color="black", linewidth=1), 
            capprops=dict(color="black", linewidth=1),
            flierprops=dict(markerfacecolor="royalblue", marker="o", markersize=5))
    #axes properties
    axes[row,col].set_title(var, fontsize=10)
    
plt.suptitle("Boxplots for Non-GDM Individuals")
plt.tight_layout()
plt.show()

#GDM
ncol = 3
nrow = int(np.ceil(len(bp_var)/ncol))
fig,axes = plt.subplots(nrow, ncol)
for i, var in enumerate(bp_var):
    row = int(np.floor(i/ncol))
    col = i%ncol
    
    #boxplots
    axes[row,col].boxplot(gdm[var], patch_artist=True,
            boxprops=dict(facecolor="pink", color="black", linewidth=1),
            whiskerprops=dict(color="black", linewidth=1), 
            medianprops=dict(color="black", linewidth=1), 
            capprops=dict(color="black", linewidth=1),
            flierprops=dict(markerfacecolor="pink", marker="o", markersize=5))
    axes[row,col].set_title(var, fontsize=10)

plt.suptitle("Boxplots for GDM Individuals")
plt.tight_layout()
plt.show()


#Summary:
#It appears that there are more outliers in the non-GDM group than GDM group.



#Z-SCORE
#Checking z-score for every continuous variable for GDM and non-GDM groups
#I will check the z-score for every variable and see if any have a standard deviation above 3.
def check_z_score(data,var_list):
    scores = {}
    for var in var_list:
        #rename variable data to data
        new_data = data[var]
        #find mean and standard deviation for the variable
        mu = new_data.mean()
        sd = new_data.std()
        for x in new_data:
            z_score = round((x - mu)/sd,2)
        if abs(z_score) >= 2:
            scores[var] = z_score
    return scores

#Non-GDM z-score
non_gdm_z_scores = check_z_score(non_gdm, bp_var)

#GDM z-score
gdm_z_score = check_z_score(gdm, bp_var)

#Summary:
#A few z-scores are above 2 and are close to 3, but none of them are as high as 3.
#This means that all values are within 3 standard deviations of the mean.



#HISTOGRAMS FOR CONTINUOUS VARIABLES
#Histograms to check for normal distribution of continuous variables


#NON-GDM INDIVIDUALS
ncols = 3
nrows = int(np.ceil(len(bp_var)/ncol))
fig,axes = plt.subplots(nrows=nrows, ncols=ncols,figsize=(10,7))
    
for i,var in enumerate(bp_var):
    row = int(np.floor(i/ncols))
    col = i%ncols
    
    #Histogram
    sns.set_style(style="dark")
    a=sns.histplot(data=non_gdm, x=non_gdm[var], ax=axes[row,col], bins=15, stat="density", color="lightblue")
    
    #PDF
    #fit normal distribution specifically to each variable
    mean, sd = norm.fit(non_gdm[var])
    #fit the min and max x values specifically to each variable
    x = np.linspace(non_gdm[var].min(), non_gdm[var].max(), 100)
    p = norm.pdf(x, mean, sd)
    #overlay the plot on top of the histogram
    a.plot(x, p, "k", linewidth = 1, color = "black", alpha=0.6)
    
    #axis labels
    a.set_xlabel(var, fontsize=10)
    a.set_ylabel("Density", fontsize=10)
    a.tick_params(labelsize=8)

plt.suptitle("Histograms and Density Curve for Non-GDM Individuals", fontsize=12)
plt.tight_layout()
plt.show()

#GDM INDIVIDUALS
ncols = 3
nrows = int(np.ceil(len(bp_var)/ncol))
fig,axes = plt.subplots(nrows=nrows, ncols=ncols, figsize=(10,7))
    
for i,var in enumerate(bp_var):
    row = int(np.floor(i/ncols))
    col = i%ncols
    
    #Histogram
    sns.set_style(style="dark")
    a=sns.histplot(data=non_gdm, x=non_gdm[var], ax=axes[row,col], bins=8, stat="density", color="lightpink")
    
    #PDF
    #fit normal distribution specifically to each variable
    mean, sd = norm.fit(gdm[var])
    #fit the min and max x values specifically to each variable
    x = np.linspace(gdm[var].min(), gdm[var].max(), 100)
    p = norm.pdf(x, mean, sd)
    #overlay the plot on top of the histogram
    a.plot(x, p, "k", linewidth = 1, color = "black", alpha=0.6)
    
    #axis labels
    a.set_xlabel(var, fontsize=10)
    a.set_ylabel("Density", fontsize=10)
    a.tick_params(labelsize=8)

plt.suptitle("Histograms and Density Curve for GDM Individuals", fontsize=12)
plt.tight_layout()
plt.show()

#Summary
#Gestational age at birth does not follow a normal distribution.
#All other values show a normal distribution.


#SCATTERPLOTS
#BMI is highly linked with GDM. 
#I want to look at the impact of both BMI and GDM on other variables. 

ncols = 3
nrows = int(np.ceil(len(bp_var)/ncol))
fig,axes = plt.subplots(nrows=nrows, ncols=ncols, figsize=(10,7))
    
for i,var in enumerate(bp_var):
    row = int(np.floor(i/ncols))
    col = i%ncols
    
    sns.set_style("dark")
    sns.scatterplot(ax= axes[row,col], data = data_copy, x= "bmi_pregestational", y=var, 
                    hue="gestational_dm", palette="pastel")
    axes[row,col].legend([], [], frameon=False)
  
plt.legend()
plt.suptitle("Scatterplot Comparing Pregestational BMI vs. Continuous Variables", fontsize=12)
plt.tight_layout()
plt.show()

#Summary:
#These scatterplots depict the relationship between pregestational BMI and various continous variables.
#I used hue to stratify the points by GDM status (0=non=GDM, 1=GDM).
#The scatterplot is a good way to get general insights on data. 
#Based on these scatterplots, it appears that those with GDM have higher BMI. 
#Those with GDM also have higher fasting glucose, and central fat (visceral fat).  



#TESTS TO COMPARE VARIABLES BETWEEN NON-GDM AND GDM GROUPS

#Non-GDM summary statistics
non_gdm_stats = non_gdm.describe()

#GDM summary statistics
gdm_stats = gdm.describe()

#F-test to compare variances of variables between GDM and non-gdm groups
#Formula: F value = variance_1/variance_2

def f_test(x_gdm, x_non_gdm):
    #converting variables to numpy arrays
    x_gdm = np.array(x_gdm)
    x_non_gdm = np.array(x_non_gdm)
    
    #calculating F test statistic
    f_stat = np.var(x_gdm, ddof=1)/np.var(x_non_gdm, ddof=1) 
    
    #Finding P value of F test stat
    dfn = x_gdm.size-1 #degrees of freedom numerator 
    dfd = x_non_gdm.size-1 #degrees of freedom denominator 
    p = 1-f.cdf(f_stat, dfn, dfd) #finds p-value
    return f, p


for var in bp_var:
    result = f_test(gdm[var], non_gdm[var])
    print(f"{var}:{result}\n")

#The variance of first fasting glucose is significantly different between GDM and non-GDM groups (p = 0.01).
#Will need to adjust t-test for first fasting glucose statistic.
#The variances of all other continous variables are similar since p is greater than 0.05.



#T-TEST
#I will perform t-tests to compare the means of continuous variables between GDM and non-GDM groups. 
#This was done in the study as well.

#T test assumes variables have a normal distribution and similar variances.
#Fasting glucose variances were shown to be different between groups, will adjust t test to account for this.

#Parameters:
# Level of significance: p < 0.05 with 95% confidence interval

#Two sample t-test for all continuous variables 
for var in bp_var:
    #converting all lists of variables to a np array
    gdm_var = np.array(gdm[var])
    non_gdm_var = np.array(non_gdm[var])
    
    #t-test for variables except glucose
    if var != "first_fasting_glucose":        
        #t test
        t_statistic, p_value = ttest_ind(gdm_var, non_gdm_var)
        print(f"{var}: t-statistic of {t_statistic}, p-value of {p_value}\n")
    else:
        #adjust equal_var to be False to perform Welch's t-test which doesn't assume equal variances
        t_statistic, p_value = ttest_ind(gdm_var, non_gdm_var, equal_var=False)
        print(f"{var}: t-statistic of {t_statistic}, p-value of {p_value}\n")
        

#Summary:
#The mean diastolic blood pressure (p = 0.03), central fat (p = 0.0004), first fasting glucose (p = 0.003), age (p =0.03), and BMI (p = 0.003) were significantly different between groups.
#Other continuous variables are not significantly different between groups.


#comparing non-gdm and gdm stats
non_gdm_stats
gdm_stats

#The GDM group has signficantly higher mean diastolic bp, central fat, first fasting glucose, and BMI.


#TESTS FOR CATEGORICAL VARIABLES

#The chi-square test is used to look at the distribution of data between groups

for var in cat_var:
    #fishers test to compare ethnicity and type of delivery 
    if var == "ethnicity" or var == "type_of_delivery":
        gdm_var_0 = gdm.loc[gdm[var]== 0][var]
        gdm_var_1 = gdm.loc[gdm[var]== 1][var]
        
        non_gdm_var_0 = non_gdm.loc[non_gdm[var]== 0][var]
        non_gdm_var_1 = non_gdm.loc[non_gdm[var]== 1][var]
        
        #contingency table
        table = np.array([[non_gdm_var_0.count(),gdm_var_0.count()], [non_gdm_var_1.count(), gdm_var_1.count()]])
        
        #chi square test
        stat, pvalue, dof, expected_freq = chi2_contingency(table)
        
        print(f"{var}: chi-square stat {stat}, p-value {pvalue}\n")
    else:
        #split pregnancies into two groups: less than/equal 3 and greater than 3 
        gdm_var_0 = gdm.loc[gdm[var] <= 3][var]
        gdm_var_1 = gdm.loc[gdm[var] > 3][var]
        
        non_gdm_var_0 = non_gdm.loc[non_gdm[var] <= 3][var]
        non_gdm_var_1 = non_gdm.loc[non_gdm[var] > 3][var]
        
        table = np.array([[non_gdm_var_0.count(),gdm_var_0.count()], [non_gdm_var_1.count(), gdm_var_1.count()]])
        
        stat, pvalue, dof, expected_freq = chi2_contingency(table)

        print(f"{var}: chi-square stat {stat}, p-value {pvalue}\n")


        
        print(f"{var}: chi-square stat {stat}, p-value {pvalue}\n")
        

#Results:
#Type of delivery is significantly different between gdm and non-gdm groups (p=0.04).
#Other categorical variables (age, ethnicity, pregnancies) are not significantly different between groups.
    
    
#ASSESSING CORRELATION OF CONTNIUOUS VARIABLES
#assessing correlation of variables to find highly correlated variables.

#Pearson Correlation coefficient

#creating dataframe with continuous variables and discrete numerical variables
data_corr_coef = data_copy.drop(["number", "gestational_dm", "ethnicity", "type_of_delivery"], axis=1)

#Cannot use ethnicity or type of delivery in Pearson's correlation test since the numbers 
# are assigned to represent labels, and don't represent quantities.

#correlation matrix
corr_matrix = data_corr_coef.corr(method = "pearson")

#correlation heatmap
plt.figure(figsize=(8,6))
a = sns.heatmap(data=corr_matrix, cmap=sns.cubehelix_palette(as_cmap=True), annot=True)
a.set_title("Correlation Heatmap", fontsize = 12)

plt.tight_layout()
plt.show()

#Summary:
#It appears that mean diastolic blood pressure and mean systolic blood pressure has a high correlation (0.77).
#I will remove mean systolic blood pressure as a variable to prevent multicollinearity for prediction models.
#This is because from the t-test mean diastolic blood pressure is significantly different between groups.











    

