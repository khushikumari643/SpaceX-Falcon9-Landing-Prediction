#==================================================================================================================================================================
#                               DATA WRANGLING
#==================================================================================================================================================================

print(df.isnull().sum()) #calculate the missing values count
df.drop(df.columns[1], axis=1, inplace=True)
df1=pd.read_csv("https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/datasets/dataset_part_1.csv")

#create a set of outcomes where the second stage did not land successfully:
landing_outcomes = df1['Outcome'].value_counts()

for i,outcome in enumerate(landing_outcomes.keys()):
    print(i,outcome)

bad_outcomes=set(landing_outcomes.keys()[[1,3,5,6,7]])
print('The set of bad outcomes')
print(bad_outcomes)

# landing_class = 0 if bad_outcome
# landing_class = 1 otherwise
landing_class=df1['Outcome'].apply(lambda x: 0 if x in bad_outcomes else 1)
#Assigning another column 'Class' to df1
df['Class']=landing_class

#Determine the success rate using mean()
df['Class'].mean()*100
#It is 66.6% of the time a safer launch

