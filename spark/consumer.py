from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col
from pyspark.sql.types import StructType, StructField, StringType
from config import config
import sys



kafkaAPIKey=sys.argv[1]
kafkaAPISecret=sys.argv[2]
kafkaBootsrapServers=sys.argv[3]

print("Arguments:")
print(f"kafkaBrokerAndPortCSV={kafkaBootsrapServers}")
print(f"kafkaAPIKey={kafkaAPIKey}")
print(f"kafkaAPISecret={kafkaAPISecret}")

# Variables
kafkaJaasConfig="org.apache.kafka.common.security.plain.PlainLoginModule required username=\"" + kafkaAPIKey + "\" password=\"" + kafkaAPISecret + "\";"

# Variables
kafkaTopic="gcp-confluent-topic-1"

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
    .appName("entries-consumer") \
    .getOrCreate()

# Read from Kafka topic
df = spark.readStream.format("kafka") \
    .option("kafka.bootstrap.servers", kafkaBootsrapServers) \
    .option("subscribe", kafkaTopic) \
    .option("kafka.security.protocol", "SASL_SSL") \
    .option("kafka.sasl.mechanism", "PLAIN") \
    .option("kafka.sasl.jaas.config", kafkaJaasConfig) \
    .option("startingOffsets", "earliest") \
    .option("failOnDataLoss", "true") \
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