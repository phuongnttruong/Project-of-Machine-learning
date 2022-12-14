import os

DATA_DIR = os.path.dirname(os.path.realpath(__file__)) + "/../data"
DIGITRAFFIC_DATA_DIR = DATA_DIR + "/digitraffic"

BIN_SIZE_MINUTES = 5

LAM_IDS = [
    "11", "101",
    "109", "117", "119", "126", "131", "145", "146", "147", "148", "149", "151",
    "152", "153", "154", "155", "164", "165", "172", "195", "196", "197",
]
YEARS = ["20"]

COLUMN_NAMES = [
    "location_id",
    "year",
    "day_number",
    "hour",
    "minute",
    "second",
    "sub_second",
    "length",
    "lane",
    "direction",
    "vehicle_type",
    "speed",
    "faulty",
    "total_time",
    "time_diff",
    "queue_start"
]

HEADERS = {"Digitraffic-User": "ds-project-app"}
