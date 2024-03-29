import pytest
from lib.utils import get_spark_session
from lib.data_loader import get_party_schema
from lib.config_loader import get_mdl_config
from lib import data_loader, transformations
from pyspark.sql.types import StructType, StructField, StringType, NullType, TimestampType, ArrayType, DateType
from datetime import datetime, date
from chispa import assert_df_equality


@pytest.fixture(scope='session')
def spark():
    return get_spark_session("NONPROD")


@pytest.fixture(scope='session')
def parties_list():
    return [
        (date(2022, 8, 2), '6982391060', '9823462810', 'F-N', datetime.fromisoformat('2019-07-29 06:21:32.000+05:30')),
        (date(2022, 8, 2), '6982391061', '9823462811', 'F-N', datetime.fromisoformat('2018-08-31 05:27:22.000+05:30')),
        (date(2022, 8, 2), '6982391062', '9823462812', 'F-N', datetime.fromisoformat('2018-08-25 15:50:29.000+05:30')),
        (date(2022, 8, 2), '6982391063', '9823462813', 'F-N', datetime.fromisoformat('2018-05-11 07:23:28.000+05:30')),
        (date(2022, 8, 2), '6982391064', '9823462814', 'F-N', datetime.fromisoformat('2019-06-06 14:18:12.000+05:30')),
        (date(2022, 8, 2), '6982391065', '9823462815', 'F-N', datetime.fromisoformat('2019-05-04 05:12:37.000+05:30')),
        (date(2022, 8, 2), '6982391066', '9823462816', 'F-N', datetime.fromisoformat('2019-05-15 10:39:29.000+05:30')),
        (date(2022, 8, 2), '6982391067', '9823462817', 'F-N', datetime.fromisoformat('2018-05-16 09:53:04.000+05:30')),
        (date(2022, 8, 2), '6982391068', '9823462818', 'F-N', datetime.fromisoformat('2017-11-27 01:20:12.000+05:30')),
        (date(2022, 8, 2), '6982391067', '9823462820', 'F-S', datetime.fromisoformat('2017-11-20 14:18:05.000+05:30')),
        (date(2022, 8, 2), '6982391067', '9823462821', 'F-S', datetime.fromisoformat('2018-07-19 18:56:57.000+05:30'))]


@pytest.fixture(scope='session')
def expected_contract_df(spark):
    schema = StructType([StructField('account_id', StringType()),
                         StructField('contractIdentifier',
                                     StructType([StructField('operation', StringType()),
                                                 StructField('newValue', StringType()),
                                                 StructField('oldValue', NullType())])),
                         StructField('sourceSystemIdentifier',
                                     StructType([StructField('operation', StringType()),
                                                 StructField('newValue', StringType()),
                                                 StructField('oldValue', NullType())])),
                         StructField('contactStartDateTime',
                                     StructType([StructField('operation', StringType()),
                                                 StructField('newValue', TimestampType()),
                                                 StructField('oldValue', NullType())])),
                         StructField('contractTitle',
                                     StructType([StructField('operation', StringType()),
                                                 StructField('newValue',
                                                             ArrayType(StructType(
                                                                 [StructField('contractTitleLineType', StringType()),
                                                                  StructField('contractTitleLine', StringType())]))),
                                                 StructField('oldValue', NullType())])),
                         StructField('taxIdentifier',
                                     StructType([StructField('operation', StringType()),
                                                 StructField('newValue',
                                                             StructType([StructField('taxIdType', StringType()),
                                                                         StructField('taxId', StringType())])),
                                                 StructField('oldValue', NullType())])),
                         StructField('contractBranchCode',
                                     StructType([StructField('operation', StringType()),
                                                 StructField('newValue', StringType()),
                                                 StructField('oldValue', NullType())])),
                         StructField('contractCountry',
                                     StructType([StructField('operation', StringType()),
                                                 StructField('newValue', StringType()),
                                                 StructField('oldValue', NullType())]))])

    return spark.read.format("json").schema(schema).load("test_data/results/contract_df.json")


@pytest.fixture(scope='session')
def expected_final_df(spark):
    schema = StructType(
        [StructField('keys',
                     ArrayType(StructType([StructField('keyField', StringType()),
                                           StructField('keyValue', StringType())]))),
         StructField('payload',
                     StructType([
                         StructField('contractIdentifier',
                                     StructType([StructField('operation', StringType()),
                                                 StructField('newValue', StringType()),
                                                 StructField('oldValue', NullType())])),
                         StructField('sourceSystemIdentifier',
                                     StructType([StructField('operation', StringType()),
                                                 StructField('newValue', StringType()),
                                                 StructField('oldValue', NullType())])),
                         StructField('contactStartDateTime',
                                     StructType([StructField('operation', StringType()),
                                                 StructField('newValue', TimestampType()),
                                                 StructField('oldValue', NullType())])),
                         StructField('contractTitle',
                                     StructType([StructField('operation', StringType()),
                                                 StructField('newValue', ArrayType(
                                                     StructType([StructField('contractTitleLineType', StringType()),
                                                                 StructField('contractTitleLine', StringType())]))),
                                                 StructField('oldValue', NullType())])),
                         StructField('taxIdentifier',
                                     StructType([StructField('operation', StringType()),
                                                 StructField('newValue',
                                                             StructType([StructField('taxIdType', StringType()),
                                                                         StructField('taxId', StringType())])),
                                                 StructField('oldValue', NullType())])),
                         StructField('contractBranchCode',
                                     StructType([StructField('operation', StringType()),
                                                 StructField('newValue', StringType()),
                                                 StructField('oldValue', NullType())])),
                         StructField('contractCountry',
                                     StructType([StructField('operation', StringType()),
                                                 StructField('newValue', StringType()),
                                                 StructField('oldValue', NullType())])),
                         StructField('partyRelations',
                                     ArrayType(StructType([
                                         StructField('partyIdentifier',
                                                     StructType([
                                                         StructField('operation', StringType()),
                                                         StructField('newValue', StringType()),
                                                         StructField('oldValue', NullType())])),
                                         StructField('partyRelationshipType',
                                                     StructType([
                                                         StructField('operation', StringType()),
                                                         StructField('newValue', StringType()),
                                                         StructField('oldValue', NullType())])),
                                         StructField('partyRelationStartDateTime',
                                                     StructType([
                                                         StructField('operation', StringType()),
                                                         StructField('newValue', TimestampType()),
                                                         StructField('oldValue', NullType())])),
                                         StructField('partyAddress',
                                                     StructType([StructField('operation', StringType()),
                                                                 StructField(
                                                                     'newValue',
                                                                     StructType(
                                                                         [StructField('addressLine1', StringType()),
                                                                          StructField('addressLine2', StringType()),
                                                                          StructField('addressCity', StringType()),
                                                                          StructField('addressPostalCode',
                                                                                      StringType()),
                                                                          StructField('addressCountry', StringType()),
                                                                          StructField('addressStartDate', DateType())
                                                                          ])),
                                                                 StructField('oldValue', NullType())]))])))]))])
    return spark.read.format("json").schema(schema).load("test_data/results/final_df.json") \
        .select("keys", "payload")


def test_blank_test(spark):
    print(spark.version)
    assert spark.version == "3.5.0"


def test_get_config():
    conf_NONPROD = get_mdl_config("NONPROD")
    assert conf_NONPROD["kafka.topic"] == "mdl_kafka_cloud"


def test_read_accounts(spark):
    accounts_df = data_loader.read_accounts(spark, "NONPROD", "2022-08-02")
    assert accounts_df.count() == 9


def test_read_parties(spark, parties_list):
    expected_df = spark.createDataFrame(parties_list, schema=["load_date", "account_id", "party_id", "relation_type", "relation_start_date"])
    actual_df = data_loader.read_parties(spark, "NONPROD", "2022-08-02")
    assert_df_equality(expected_df, actual_df)


def test_get_contract(spark, expected_contract_df):
    accounts_df = data_loader.read_accounts(spark, "NONPROD", "2022-08-02")
    actual_contract_df = transformations.get_contract(accounts_df)
    assert_df_equality(expected_contract_df, actual_contract_df)


def test_kafka_kv_df(spark, expected_final_df):
    accounts_df = data_loader.read_accounts(spark, "NONPROD", "2022-08-02")
    contract_df = transformations.get_contract(accounts_df)
    parties_df = data_loader.read_parties(spark, "NONPROD", "2022-08-02")
    relations_df = transformations.get_relations(parties_df)
    address_df = data_loader.read_address(spark, "NONPROD", "2022-08-02")
    relation_address_df = transformations.get_address(address_df)
    party_address_df = transformations.join_party_address(relations_df, relation_address_df)
    data_df = transformations.join_contract_party(contract_df, party_address_df)
    actual_final_df = transformations.apply_header(spark, data_df).select("keys", "payload")
    assert_df_equality(actual_final_df, expected_final_df)
