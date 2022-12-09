import sys
from pyspark.sql import SparkSession, functions, types
from pyspark.sql.functions import when,lit,col,count,year,to_timestamp

def main(inputs):
    observation_schema = types.StructType([
        types.StructField('station_id', types.StringType()),
        types.StructField('date', types.StringType()),
        types.StructField('observation', types.StringType()),
        types.StructField('value', types.IntegerType()),
        types.StructField('mflag', types.StringType()),
        types.StructField('qflag', types.StringType()),
        types.StructField('sflag', types.StringType()),
        types.StructField('obstime', types.StringType()),
    ])

    # weather = spark.read.csv(inputs, schema=observation_schema)
    weather = spark.read.format('csv').schema(observation_schema)\
        .option("recursiveFileLookup", "true").load(inputs)
    # checks for quality assurance test where blank indicates did not fail any quality assurance check
    weather_gflag = weather[weather['qflag'].isNull()]
    weather_station = weather_gflag[weather_gflag['station_id'].startswith('CA')]
    weather_filtered = weather_station.filter(weather_station['observation'].isin(['PRCP',
                                                                              'SNOW',
                                                                              'SNWD',
                                                                              'TMAX',
                                                                              'TMIN']))

    weather_filtered = weather_filtered.filter(weather_filtered['date']>='19580101')
    weather_filtered = weather_filtered.groupBy(['station_id','date'])\
        .pivot('observation') \
        .max('value')
    weather_filtered = weather_filtered.withColumnRenamed('SNOW','SNOW(mm)')\
        .withColumnRenamed('SNWD','SNWD(mm)').withColumnRenamed('PRCP','PRCP(tenths of mm)')\
        .withColumnRenamed('TMAX','TMAX(tenths of degrees C)')\
        .withColumnRenamed('TMIN','TMIN(tenths of degrees C)')

    weather_filtered = weather_filtered.withColumn('TMAX(C)',weather_filtered['TMAX(tenths of degrees C)']/10)\
        .withColumn('TMIN(C)',weather_filtered['TMIN(tenths of degrees C)']/10)\
        .withColumn('PRCP(mm)',weather_filtered['PRCP(tenths of mm)']/10)
    weather_filtered = weather_filtered.select('station_id','date','TMAX(C)','TMIN(C)','PRCP(mm)','SNOW(mm)','SNWD(mm)')

    weather_filtered.write.save("weather_cleaned_1958Onwards.csv",format='csv',header=True)

if __name__ == '__main__':
    spark = SparkSession.builder.appName('weather etl transformation').getOrCreate()
    spark.sparkContext.setLogLevel('WARN')
    sc = spark.sparkContext
    inputs = sys.argv[1]
    main(inputs)
