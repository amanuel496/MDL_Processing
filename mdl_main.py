import sys
from lib import utils, config_loader, data_loader, transformations
from lib.logger import Log4j
import uuid
from pyspark.sql.functions import struct, col, to_json

if __name__ == '__main__':

    if len(sys.argv) < 3:
        print("Usage: mdl {local, qa, prod} {load_date} : Arguments are missing")
        sys.exit(-1)

    job_run_env = sys.argv[1].upper()
    if job_run_env == "NONPROD":
        load_date = "2022-08-02"
    else:
        load_date = sys.argv[2]
    job_run_id = "mdl-" + str(uuid.uuid4())

    print("Initializing MDL Job in " + job_run_env + " Job ID: " + job_run_id)
    conf = config_loader.get_mdl_config(job_run_env)

    print("Creating Spark Session")
    spark = utils.get_spark_session(job_run_env)

    logger = Log4j(spark)

    logger.info("Reading MDL Account DF")
    accounts_df = data_loader.read_accounts(spark, job_run_env, load_date)
    contract_df = transformations.get_contract(accounts_df)

    logger.info("Reading MDL party DF")
    parties_df = data_loader.read_parties(spark, job_run_env, load_date)
    relations_df = transformations.get_relations(parties_df)

    logger.info("Reading MDL Address DF")
    address_df = data_loader.read_address(spark, job_run_env, load_date)
    relation_address_df = transformations.get_address(address_df)

    logger.info("Join Party Relations and Address")
    party_address_df = transformations.join_party_address(relations_df, relation_address_df)

    logger.info("Join Account and Parties")
    data_df = transformations.join_contract_party(contract_df, party_address_df)

    logger.info("Apply Header and create Event")
    final_df = transformations.apply_header(spark, data_df)
    logger.info("Preparing to send data to Kafka")
    kafka_kv_df = final_df.select(col("payload.contractIdentifier.newValue").alias("key"),
                                  to_json(struct("*")).alias("value"))

    # input("Press Any Key")
    api_key = conf["kafka.api_key"]
    api_secret = conf["kafka.api_secret"]
    kafka_kv_df.write \
        .format("kafka") \
        .option("kafka.bootstrap.servers", conf["kafka.bootstrap.servers"]) \
        .option("topic", conf["kafka.topic"]) \
        .option("kafka.security.protocol", conf["kafka.security.protocol"]) \
        .option("kafka.sasl.jaas.config", conf["kafka.sasl.jaas.config"].format(api_key, api_secret)) \
        .option("kafka.sasl.mechanism", conf["kafka.sasl.mechanism"]) \
        .option("kafka.client.dns.lookup", conf["kafka.client.dns.lookup"]) \
        .save()

    logger.info("Finished sending data to Kafka")

    spark.stop()
