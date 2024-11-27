from pathlib import Path

from app.config import config
from app.model.dataset_builder import DatasetBuilder
from app.utils import SQLiteDatabase

if __name__ == "__main__":
    builder = DatasetBuilder(SQLiteDatabase(Path(config.db_path)))
    builder.run()
