# Spark MLlib with PySpark

from pyspark.sql import SparkSession
from pyspark.ml.classification import LogisticRegression

spark = SparkSession.builder.appName("LargeScaleML").getOrCreate()
df = spark.read.csv("bigdata.csv", header=True, inferSchema=True)

# Feature assembly, vectorization, model training
from pyspark.ml.feature import VectorAssembler

assembler = VectorAssembler(
    inputCols=[col for col in df.columns if col != "target"], outputCol="features"
)
df = assembler.transform(df)

lr = LogisticRegression(featuresCol="features", labelCol="target")
model = lr.fit(df)
