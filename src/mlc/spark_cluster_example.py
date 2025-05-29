from pyspark.sql import SparkSession
from pyspark.ml.feature import VectorAssembler
from pyspark.ml.classification import LogisticRegression

spark = SparkSession.builder \
    .appName("LargeScaleLogisticRegression") \
    .getOrCreate()

df = spark.read.csv("large_dataset.csv", header=True, inferSchema=True)

assembler = VectorAssembler(
    inputCols=[col for col in df.columns if col != 'target'],
    outputCol='features'
)
data = assembler.transform(df)

lr = LogisticRegression(featuresCol='features', labelCol='target')
model = lr.fit(data)

predictions = model.transform(data)
predictions.select("prediction", "probability", "target").show(5)

