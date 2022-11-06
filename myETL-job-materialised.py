import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job

args = getResolvedOptions(sys.argv, ["JOB_NAME"])
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args["JOB_NAME"], args)

# Script generated for node S3 bucket
S3bucket_node1 = glueContext.create_dynamic_frame.from_catalog(
    database="db_youtube_cleansed",
    table_name="cleansed_raw_statistics",
    transformation_ctx="S3bucket_node1",
)

# Script generated for node Amazon S3
AmazonS3_node1667739866439 = glueContext.create_dynamic_frame.from_catalog(
    database="db_youtube_cleansed",
    table_name="cleansed_statistics_reference_data",
    transformation_ctx="AmazonS3_node1667739866439",
)

# Script generated for node ApplyMapping
ApplyMapping_node2 = Join.apply(
    frame1=S3bucket_node1,
    frame2=AmazonS3_node1667739866439,
    keys1=["category_id"],
    keys2=["id"],
    transformation_ctx="ApplyMapping_node2",
)

# Script generated for node S3 bucket
S3bucket_node3 = glueContext.getSink(
    path="s3://data-engg-etl-python/reporting/",
    connection_type="s3",
    updateBehavior="UPDATE_IN_DATABASE",
    partitionKeys=["region", "id"],
    compression="snappy",
    enableUpdateCatalog=True,
    transformation_ctx="S3bucket_node3",
)
S3bucket_node3.setCatalogInfo(
    catalogDatabase="db_youtube_analytics", catalogTableName="youtube_stat_catagories"
)
S3bucket_node3.setFormat("glueparquet")
S3bucket_node3.writeFrame(ApplyMapping_node2)
job.commit()
