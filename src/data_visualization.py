#====================================================================================================================================================================
#                                      DATA VISUALIZATION
#====================================================================================================================================================================

df1['Class'] = landing_class
sns.catplot(y="PayloadMass", x="FlightNumber", hue="Class", data=df1, aspect = 5)
plt.xlabel("Flight Number",fontsize=20)
plt.ylabel("Pay load Mass (kg)",fontsize=20)
plt.show()

""" From the plot, we can infer a clear trend: as the FlightNumber increases, indicating later missions, there is a noticeable increase in the number of successful
landings (represented by orange dots, where 'Class' is 1). In the earlier flights (lower FlightNumber values), there are more unsuccessful landings (blue dots, where 
'Class' is 0), often associated with lower PayloadMass. As SpaceX gained experience and refined its technology, it was able to successfully land boosters with 
increasingly heavier PayloadMass values."""


sns.scatterplot(x='PayloadMass', y='LaunchSite',data=df1)
plt.xlabel("Payload mass",fontsize=20)
plt.ylabel("LaunchSite",fontsize=20)
plt.show()

""" CCAFS SLC 40 is the most frequently used launch site, handling a wide spectrum of payload masses, including both light and very heavy payloads.

**KSC LC 39A **also serves a substantial number of launches, particularly for heavier payloads, showing a similar versatility to CCAFS SLC 40 in terms of 
the range of masses handled.

VAFB SLC 4E appears to be used for fewer launches, predominantly for payloads in the lower to mid-range of masses, with fewer instances of extremely heavy
payloads compared to the other two sites.

The plot suggests that the CCAFS SLC 40 and KSC LC 39A sites are equipped to handle a broader and heavier range of payloads, indicating their strategic 
importance for diverse mission requirements. """


# To visualize the mean success rate, the plot is as follows
orbit_class_mean = df1.groupby('Orbit')['Class'].mean().reset_index()
print(orbit_class_mean.head())  # snapshot

sns.barplot(x='Orbit', y='Class', data=orbit_class_mean)

plt.xlabel("Orbit", fontsize=15)
plt.ylabel("Mean of Class", fontsize=15)
plt.title("Mean Success Rate by Orbit", fontsize=18)
plt.xticks(rotation=45)
plt.show()


#converting the date to year
year=[]
def Extract_year():
    for i in df1["Date"]:
        year.append(i.split("-")[0])
    return year
Extract_year()
df1['Date'] = year
df1.head()

#Visualizing the success rate
yearly_success = df1.groupby('Date')['Class'].mean().reset_index()
sns.lineplot(x='Date', y='Class', data=yearly_success, marker='*')
plt.xlabel("Date", fontsize=15)
plt.ylabel("Success Rate", fontsize=15)
plt.title("Yearly Success Rate of Launches", fontsize=18)
plt.grid(True)
plt.show()


# It can be observed that the sucess rate since 2013 kept increasing till 2020

#====================================================================================================================================================================
#                          FEATURE ENGINEERING
#====================================================================================================================================================================


features_one_hot = pd.get_dummies(features, columns=['Orbit', 'LaunchSite', 'LandingPad', 'Serial'])
features_one_hot = features_one_hot.astype('float64')
features_one_hot.head()

features_one_hot.to_csv('FeatureEngg_one_hot.csv', index=False)

#imports 

import folium
from folium.plugins import MarkerCluster
from folium.plugins import MousePosition
from folium.features import DivIcon

folium.Map(location=[28.563, -80.576], zoom_start=5)
spacex_df=df1[['LaunchSite', 'Latitude', 'Longitude', 'Class']]
launch_sites_df=spacex_df.groupby(['LaunchSite'], as_index=False).first()
launch_sites_df=launch_sites_df[['LaunchSite', 'Latitude', 'Longitude']]

nasa_coordinate=[29.559684888503615, -95.0830971930759]
site_map=folium.Map(location=nasa_coordinate, zoom_start=5)
marker_cluster=MarkerCluster().add_to(site_map)
for index, row in df1.iterrows():
    # Success = green, Failure = red
    outcome_color = 'green' if row['Class'] == 1 else 'red'

    folium.Marker(
        location=[row['Latitude'], row['Longitude']],   # lat/long columns
        popup=f"Site: {row['LaunchSite']}<br>Outcome: {row['Outcome']}",
        icon=folium.Icon(color=outcome_color, icon='rocket')
    ).add_to(marker_cluster)
site_map

df1['marker_color']=df1['Class'].apply(lambda x: 'green' if x == 1 else 'red')

# Quick check
print(df1[['Class', 'marker_color']].head())

for index, record in spacex_df.iterrows():
    # Determine the color of the marker based on the 'Class' (success or failure)
    color = 'green' if record['Class'] == 1 else 'red'

    # Create a folium.Marker object for each record
    marker = folium.Marker(
        location=[record['Latitude'], record['Longitude']],
        popup=f"Launch Site: {record['LaunchSite']}<br>Class: {record['Class']}", # Popup information
        icon=folium.Icon(color=color, icon='rocket')
    )
    # Add the newly created marker to the marker_cluster
    marker_cluster.add_child(marker)

# Display the map with all the markers
site_map

"""FOLIUM INSIGHTS
Geographical Concentration: The map clearly shows the geographical locations of the three primary launch sites: CCAFS SLC 40, KSC LC 39A (both in Florida,
close to each other), and VAFB SLC 4E (in California).

Success and Failure by Site: By observing the distribution of green (success) and red (failure) rocket icons clustered at each launch site, we can get a 
visual understanding of the success rates. For instance, a site with a higher density of green markers indicates a better success record.

Launch Activity: The number of markers at each location provides a visual representation of the launch frequency from that site."""




