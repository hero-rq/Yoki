from pyspark.sql import SparkSession
from pyspark.sql.types import StringType
from pyspark.sql.functions import col
from pyspark.ml.feature import VectorAssembler
from pyspark.ml import Pipeline
from pyspark.ml.regression import RandomForestRegressor
from pyspark.ml.evaluation import RegressionEvaluator

# Step 1: Initialize Spark Session
spark = SparkSession.builder.appName("SpamDetection").getOrCreate()

# Step 2: Load CSV Data
rawdata = spark.read.csv('./Data/spambase.data', header=False, inferSchema=True)

# Step 3: Cache the DataFrame (for performance optimization)
rawdata.cache()

# Step 4: Read and Process Feature Names
with open('./Data/spambase.data.names', 'r') as f:
    spam_names = [line.rstrip('\n') for line in f]

# Step 5: Extract Feature Names (Remove text after ':')
spam_names = [line.split(':')[0] for line in spam_names]

# Step 6: Ensure Label Column is Named Properly
ncolumns = len(rawdata.columns)
spam_names[ncolumns - 1] = 'labels'  # Ensure last column is 'labels'

# Step 7: Rename Columns to Meaningful Feature Names
schemaNames = rawdata.schema.names
for i in range(ncolumns):
    rawdata = rawdata.withColumnRenamed(schemaNames[i], spam_names[i])

# Step 8: Print Schema (for verification)
rawdata.printSchema()

# Step 9: Convert String Columns to Double (Ensuring Consistent Data Types)
string_columns = [x.name for x in rawdata.schema.fields if x.dataType == StringType()]
for col_name in string_columns:
    rawdata = rawdata.withColumn(col_name, col(col_name).cast("double"))

# Step 10: Show Sample Data (Optional)
rawdata.show(5)

# Step 11: Split Data into Training and Testing Sets
train_data, test_data = rawdata.randomSplit([0.8, 0.2], seed=42)

# Step 12: Prepare Features using VectorAssembler
feature_columns = [col for col in rawdata.columns if col != "labels"]
vectorAssembler = VectorAssembler(inputCols=feature_columns, outputCol="features")

# Step 13: Define RandomForestRegressor Model
rf = RandomForestRegressor(
    labelCol="labels",
    featuresCol="features",
    maxDepth=5,
    numTrees=3,
    featureSubsetStrategy="all",
    seed=123,
    bootstrap=True  # Better for variance reduction
)

# Step 14: Create a Pipeline
pipeline = Pipeline(stages=[vectorAssembler, rf])

# Step 15: Train Model
pipelineModel = pipeline.fit(train_data)

# Step 16: Make Predictions on Test Data
predictions = pipelineModel.transform(test_data)

# Step 17: Evaluate Model using RMSE
evaluator = RegressionEvaluator(labelCol="labels", predictionCol="prediction", metricName="rmse")
rmse = evaluator.evaluate(predictions)
print("RMSE = %g " % rmse)
