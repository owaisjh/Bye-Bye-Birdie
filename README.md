Bye Bye Birdie 


Ebird Scraping Related -
	Contains python scripts (multi-threaded and single threaded) used for downloading ebird data 
	
	Python script to verify if data for all dates is fetched.
	Python script to combine the date wise ebird data generated to single file per year
	Python script to upload ebird data to google cloud storage
	It has a requirements.txt file which contains python depndencies required to run.
	User will need their own ebird API key which has to be stored in .env file.
	User will need creds.json to connect to GCP cluster.



GCP Pre-Processing Codes -
	Contains 5 notebooks pertaining to different aspects of the data cleaning and preprocessing. 
	
	1) Weather-ETL.ipynb: Reads the GHCN dataset by defined schema and filters for null values, British Columbia weather stations, picking year count from 1959 onwards. Pivoting the weather data so that for each date and station, we have one row corresponding to  minimum temperature,maximum temperature, snowfall and precipitation (as columns).

	2) Stations.ipynb: Reads the stations.txt formats it with a regex for the rows value. Filtering the entire dataset for only British Columbia weather stations giving a dataset of all weather stations in BC and their coordinates. 

	3) Weather_and_Stations.ipynb: Joins Stations and Weather (using Stations as Broadcast) based on the Stations ID to get comprehensive details about the latitude, longitude, Station ID, Observation and Value.

	4) Ebird.ipynb: Reads the ebird dataset by defined schema and filters for null values,

	5) CombinedJoin.ipynb: Joins the datasets generated by the weather_and_staions join and ebird dataset. We iterate on the year through both the data sets and cross join both the datasets while making sure the date is equal.
	We calculate the haversine distance between the weather station and the ebird data point.
	We aggregate it on this distance to find the station closest to the ebird data point. 
	This allows us to retain only the entry with the closest weather data and get rid of the extra entries created due to cross join. 


SFU Cluster Pre-Processing Codes-
	
	We have 2 python codes here for some heavy operations which were taking very long processing times on weaker GCP cluster. These codes do the exact same work as their GCP counterpart notebooks.

	1) formatWeather.py: (Weather-ETL.ipynb Counterpart) Reads the GHCN dataset by defined schema and filters for null values, British Columbia weather stations, picking year count from 1959 onwards. Pivoting the weather data so that for each date and station, we have one row corresponding to  minimum temperature,maximum temperature, snowfall and precipitation (as columns).

	2) finalWeatherEbirdJoin.py: (CombinedJoin.ipynb Counterpart)

	3) finalJoinFilesCombine.py: Combines the output generated by finalWeatherEbirdJoin.py for easier upload to GCP.


SFU Cluster GCP Connect-

	Contains 2 python scripts which allow file sharing between GCP Cloud storage bucket and SFU cluster