from lib.config_loader import get_mdl_config

BASE_PATH = "base.path"


def get_account_schema():
    schema = """
        load_date date, active_ind int, account_id string,
        source_sys string, account_start_date timestamp,
        legal_title_1 string, legal_title_2 string,
        tax_id_type string, tax_id string, branch_code string, country string"""
    return schema


def get_party_schema():
    schema = """
        load_date date, account_id string, party_id string,
        relation_type string, relation_start_date timestamp"""
    return schema


def get_address_schema():
    schema = """
        load_date date, party_id string, address_line_1 string,
        address_line_2 string, city string, postal_code string,
        country_of_address string, address_start_date date"""
    return schema


def read_accounts(spark, env, date):
    conf = get_mdl_config(env)
    base_path = conf[BASE_PATH]
    return spark.read \
        .format("csv") \
        .option("header", "true") \
        .schema(get_account_schema()) \
        .load(base_path + "accounts/" + date + "/")


def read_parties(spark, env, date):
    conf = get_mdl_config(env)
    base_path = conf[BASE_PATH]
    return spark.read \
        .format("csv") \
        .option("header", "true") \
        .schema(get_party_schema()) \
        .load(base_path + "parties/" + date + "/")


def read_address(spark, env, date):
    conf = get_mdl_config(env)
    base_path = conf[BASE_PATH]
    return spark.read \
        .format("csv") \
        .option("header", "true") \
        .schema(get_address_schema()) \
        .load(base_path + "party_address/" + date + "/")
