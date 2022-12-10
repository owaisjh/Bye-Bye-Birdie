<h1> Bye Bye Birdie 🐦 </h1>

The fluctuating weather patterns along with the rise in temperature has brought about adverse changes in the natural terrains of birds present around the globe. This shortfall has particularly affected British Columbia bird sightings as well. It is reported that BC has lost around 20 percent of its habitat over the past three generations which is quite steep. In this project, we mainly aim at finding how weather has affected these sightings and which species have become endangered across British Columbia, Canada.

# Table of Contents:

1. Guide on files in repo
2. Contributors
3. Tasks and Future Scope


## Guide on files in repo 

Ebird Scraping Related -
    Contains python scripts (multi-threaded and single threaded) used for downloading ebird data 
	
    Python script to verify if data for all dates is fetched.
    Python script to combine the date wise ebird data generated to single file per year
    Python script to upload ebird data to google cloud storage
    It has a requirements.txt file which contains python depndencies required to run.
    User will need their own ebird API key which has to be stored in .env file.
    User will need creds.json to connect to GCP cluster.



GcpEtlCodes -
	Contains 5 notebooks pertaining to different aspects of the data cleaning and preprocessing. 
	
	1) Weather-ETL.ipynb: Reads the GHCN dataset by defined schema and filters for null values, British Columbia weather stations, picking year count from 1959 onwards. Pivoting the weather data so that for each date and station, we have one row corresponding to  minimum temperature,maximum temperature, snowfall and precipitation (as columns).

	2) Stations.ipynb: Reads the stations.txt formats it with a regex for the rows value. Filtering the entire dataset for only British Columbia weather stations giving a dataset of all weather stations in BC and their coordinates. 

	3) Weather_and_Stations.ipynb: Joins Stations and Weather (using Stations as Broadcast) based on the Stations ID to get comprehensive details about the latitude, longitude, Station ID, Observation and Value.

	4) Ebird.ipynb: Reads the ebird dataset by defined schema and filters for null values,

	5) CombinedJoin.ipynb: Joins the datasets generated by the weather_and_staions join and ebird dataset. We iterate on the year through both the data sets using pyspark and cross join both the datasets while making sure the date is equal.
	We calculate the haversine distance between the weather station and the ebird data point.
	We aggregate it on this distance to find the station closest to the ebird data point. 
	This allows us to retain only the entry with the closest weather data and get rid of the extra entries created due to cross join. 


SfuEtlCodes-
	
	We have 2 python codes here for some heavy operations which were taking very long processing times on weaker GCP cluster. These codes do the exact same work as their GCP counterpart notebooks.

	1) formatWeather.py: (Weather-ETL.ipynb Counterpart) Reads the GHCN dataset by defined schema and filters for null values, British Columbia weather stations, picking year count from 1959 onwards. Pivoting the weather data so that for each date and station, we have one row corresponding to  minimum temperature,maximum temperature, snowfall and precipitation (as columns).

	2) finalWeatherEbirdJoin.py: (CombinedJoin.ipynb Counterpart)

	3) finalJoinFilesCombine.py: Combines the output generated by finalWeatherEbirdJoin.py for easier upload to GCP.


SfuClusterGcpConnect-

	Contains 2 python scripts which allow file sharing between GCP Cloud storage bucket and SFU cluster

ML - 

    Contains pyspark ml code to predict the bird count 

Analysis -

    1) Identifying species that moved locations.ipynb - identified bird species that moved locations likely due to change in weather conditions 
    
    2) ebird_analysis.ipynb - Visualizations on the basis of purely ebird dataset.

    3) weather_ebird_analysis.ipynb - Visualization on the joined dataset for weather and bird dataset correlating the weather conditions.

## Contributors:

1. [Owais Hetavkar](https://github.com/owaisjh)
2. [Aastha Jha](https://github.com/aastha12)
3. [Roodra Kanwar](https://github.com/roodrakanwar)



## Tasks and Future Scope:

- [x] Gathering the data from API and web scraping
- [x] ETL on weather and ebird data
- [x] Analysis & Visualizations 
- [x] ML model to predict bird count
- [ ] Web app to present our insights