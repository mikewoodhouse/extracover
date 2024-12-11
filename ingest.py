import fire

from app.ingest.extract_match_data import extract_all_zips
from app.ingest.import_matches import import_everything
from app.ingest.partition_matches import partition_matches
from app.ingest.player_json_to_csv import write_player_csvs
from app.ingest.spider_player_data import spider as spider_player_data
from app.ingest.update_player_info import update_player_info


def unzip():
    extract_all_zips()


def import_data():
    import_everything()


def partition():
    partition_matches()


def spider():
    spider_player_data()


def update():
    "Update player info from spidered data files"
    write_player_csvs()
    update_player_info()


if __name__ == "__main__":
    fire.Fire(
        {
            "extract": unzip,
            "unzip": unzip,
            "partition": partition,
            "import": import_data,
            "spider": spider,
            "update": update_player_info,
        }
    )
