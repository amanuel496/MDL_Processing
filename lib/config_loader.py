from configparser import ConfigParser
from pyspark import SparkConf

MDL_CONF_PATH = "conf/mdl.conf"
SPARK_CONF_PATH = "conf/spark.conf"


def get_mdl_config(env):
    config = ConfigParser()
    config.read(MDL_CONF_PATH)
    conf = {}
    for (key, val) in config.items(env):
        conf[key] = val
    return conf


def get_spark_conf(env):
    spark_conf = SparkConf()
    config = ConfigParser()
    config.read(SPARK_CONF_PATH)
    for (key, val) in config.items(env):
        spark_conf.set(key, val)
    return spark_conf
