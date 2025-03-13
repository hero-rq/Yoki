from pyspark.sql import SparkSession
from pyspark.sql.types import StringType
from pyspark.sql.functions import col
from pyspark.ml.feature import VectorAssembler
from pyspark.ml import Pipeline
from pyspark.ml.classification import LogisticRegression
from pyspark.ml.evaluation import BinaryClassificationEvaluator
from pyspark.ml.tuning import CrossValidator, ParamGridBuilder

# Step 1: Initialize Spark Session
spark = SparkSession.builder.appName("SpamDetection").getOrCreate()

# Step 2: Load CSV Data
rawdata = spark.read.csv("./Data/spambase.data", header=False, inferSchema=True).cache()

# Step 3: Read and Process Feature Names
with open("./Data/spambase.data.names", "r") as f:
    spam_names = [line.split(":")[0].strip() for line in f]

# Step 4: Ensure Label Column is Named Properly
spam_names[-1] = "labels"  # Rename last column to 'labels'

# Step 5: Rename Columns
for old_name, new_name in zip(rawdata.columns, spam_names):
    rawdata = rawdata.withColumnRenamed(old_name, new_name)

# Step 6: Convert String Columns to Double (if any exist)
for column in rawdata.schema.fields:
    if isinstance(column.dataType, StringType):
        rawdata = rawdata.withColumn(column.name, col(column.name).cast("double"))

# Step 7: Split Data into Training and Test Sets
train_data, test_data = rawdata.randomSplit([0.8, 0.2], seed=42)

# Step 8: Prepare Feature Vector
feature_columns = [col for col in rawdata.columns if col != "labels"]
vectorAssembler = VectorAssembler(inputCols=feature_columns, outputCol="features")

# Step 9: Define Logistic Regression Model
lr = LogisticRegression(featuresCol="features", labelCol="labels", maxIter=10)

# Step 10: Create a Pipeline
pipeline = Pipeline(stages=[vectorAssembler, lr])

# Step 11: Define Hyperparameter Grid for Cross Validation
paramGrid = ParamGridBuilder() \
    .addGrid(lr.regParam, [0.1, 0.01]) \
    .addGrid(lr.elasticNetParam, [0.0, 0.5, 1.0]) \
    .build()

# Step 12: Define Cross Validator
crossval = CrossValidator(
    estimator=pipeline,
    estimatorParamMaps=paramGrid,
    evaluator=BinaryClassificationEvaluator(labelCol="labels"),
    numFolds=3
)

# Step 13: Train Model using Cross Validation
cvModel = crossval.fit(train_data)

# Step 14: Make Predictions on Test Data
predictions = cvModel.transform(test_data)

# Step 15: Show Sample Predictions
predictions.select("labels", "probability", "prediction").show(10)

# Step 16: Evaluate Model Performance
evaluator = BinaryClassificationEvaluator(labelCol="labels")
accuracy = evaluator.evaluate(predictions)
print(f"Test Accuracy: {accuracy:.4f}")
