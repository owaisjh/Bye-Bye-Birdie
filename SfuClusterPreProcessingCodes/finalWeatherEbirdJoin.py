from pyspark.sql import SparkSession, functions, types
from pyspark.sql.functions import col,isnan,when,count, radians, asin, sin, sqrt, cos,min,year,max
from pyspark.sql import Window as W
import uuid

spark = SparkSession.builder.appName('weather_ebird_etl').getOrCreate()
spark.sparkContext.setLogLevel('WARN')
sc = spark.sparkContext



def main(input1, input2):
    weather_schema = types.StructType([
            types.StructField('station_id', types.StringType()),
            types.StructField('date', types.StringType()),
            types.StructField('PRCP', types.FloatType()),
            types.StructField('SNOW', types.FloatType()),
            types.StructField('SNWD', types.FloatType()),
            types.StructField('TMAX', types.FloatType()),
            types.StructField('TMIN', types.FloatType()),
            types.StructField("Latitude", types.FloatType()),
            types.StructField("Longitude", types.FloatType()),
            types.StructField("Elevation", types.FloatType()),
            types.StructField("State", types.StringType()),
            types.StructField("date_final",types.DateType()),
    ])

    ebird_schema = types.StructType([
            types.StructField("speciesCode",types.StringType()),
            types.StructField("comName",types.StringType()),
            types.StructField("sciName",types.StringType()),
            types.StructField("locId",types.StringType()),
            types.StructField("locName",types.StringType()),
            types.StructField("obsDt",types.DateType()),
            types.StructField("howMany",types.StringType()),
            types.StructField("lat",types.FloatType()),
            types.StructField("lng",types.FloatType()),
            types.StructField("obsValid",types.StringType()),
            types.StructField("obsReviewed",types.StringType()),
            types.StructField("locationPrivate",types.StringType()),
            types.StructField("subId",types.StringType()),
            types.StructField("ebird_id",types.StringType()),
           
        ])


    ebird = spark.read.format('csv').schema(ebird_schema).load(input1)
    weather = spark.read.format('csv').schema(weather_schema).load(input2)


    start = 2011
    end = 2021 
    for yr in range(start,end+1):
        print(yr)
        ebird_1959 = ebird.filter(year("ObsDt")==yr)
        weather_1959 = weather.filter(year("date_final")==yr)

        # print(ebird_1959.count())


        join_1959 = ebird_1959.crossJoin(weather_1959).withColumn("dist_longit", radians(weather_1959["Longitude"]) - radians(ebird_1959["lng"])).withColumn("dist_latit", radians(weather_1959["Latitude"]) - radians(ebird_1959["lat"]))

        join_1959 = join_1959.withColumn("haversine_distance_kms", asin(sqrt(
                                                sin(join_1959["dist_latit"] / 2) ** 2 + cos(radians(join_1959["lat"]))
                                                * cos(radians(join_1959["Latitude"])) * sin(join_1959["dist_longit"] / 2) ** 2
                                                )
                                            ) * 2 * 6371).drop("dist_longit","dist_latit",
                                                            "speciesCode","obsValid","obsReviewed",
                                                            "locationPrivate","subId")


        join_1959= join_1959.filter(join_1959['obsDt'] == join_1959['date_final'])



        min_dist_1959 = join_1959.groupBy(['ebird_id']).agg({'haversine_distance_kms':'min'}).withColumnRenamed('min(haversine_distance_kms)','min_dist')




        min_dist_1959 = min_dist_1959.withColumnRenamed('ebird_id','ebird_id_min')

        condition = [min_dist_1959['ebird_id_min'] == join_1959['ebird_id'] , min_dist_1959['min_dist'] ==join_1959['haversine_distance_kms'] ] 

        join_1959 = join_1959.join(min_dist_1959, condition, 'inner')

        # print(join_1959.count())

        join_1959= join_1959.drop('ebird_id_min','haversine_distance_kms' ) 


        join_1959.write.save("joined-data-final/"+str(yr) +"/weather_ebird.csv", format='csv',header=True)



input1 = "ebird.csv"
input2 = "weather.csv"
main(input1, input2)