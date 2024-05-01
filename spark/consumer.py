from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col
from pyspark.sql.types import StructType, StructField, StringType


kafkaJaasConfig="org.apache.kafka.common.security.plain.PlainLoginModule required username=\"" + kafkaAPIKey + "\" password=\"" + kafkaAPISecret + "\";"

# Variables
kafkaTopic="entries"

# Define the schema of your data
schema = StructType([
    StructField("timestamp", StringType()),
    StructField("team", StringType()),
    StructField("player", StringType()),
    StructField("type", StringType()),
    StructField("pass_body_part", StringType()), 
    StructField("pass_height", StringType()),
    # Add more fields here
])

# Create a SparkSession
spark = SparkSession.builder \
    .appName("KafkaStreamProcessor") \
    .getOrCreate()

# Read the Kafka stream
df = spark \
    .readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "localhost:9092") \
    .option("subscribe", "gcp-confluent-topic-1") \
    .load()

# Convert the binary value column to string
df = df.selectExpr("CAST(value AS STRING)")

# Parse the JSON strings to a dataframe
df = df.select(from_json(col("value"), schema).alias("data")).select("data.*")

# Start the streaming query
query = df \
    .writeStream \
    .outputMode("append") \
    .format("console") \
    .start()

query.awaitTermination()