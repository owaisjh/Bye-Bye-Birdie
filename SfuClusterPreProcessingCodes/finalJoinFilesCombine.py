from pyspark.sql import SparkSession, functions, types
from pyspark.sql.functions import col,isnan,when,count, radians, asin, sin, sqrt, cos,min,year,max
from pyspark.sql import Window as W
import uuid

spark = SparkSession.builder.appName('weather_ebird_etl').getOrCreate()
spark.sparkContext.setLogLevel('WARN')
sc = spark.sparkContext

inputs = "joined-data-final"


schema = types.StructType([
            types.StructField("speciesCode",types.StringType()),
            types.StructField("comName",types.StringType()),
            types.StructField("sciName",types.StringType()),
            types.StructField("locId",types.StringType()),
            types.StructField("locName",types.StringType()),
            types.StructField("obsDt",types.DateType()),
            types.StructField("howMany",types.StringType()),
            types.StructField("lat",types.FloatType()),
            types.StructField("lng",types.FloatType()),
            types.StructField("ebird_id",types.StringType()),

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
            types.StructField("min_dist", types.FloatType()),

     
           
        ])




finalsaver = spark.read.format('csv').option("recursiveFileLookup","true").schema(schema).load(inputs)


finalsaver = finalsaver.filter( finalsaver['lat'].isNotNull() )

filename.write.save("joined-data-final-final", format='csv',header=True)

print(finalsaver.show(3))
print(finalsaver.count())
