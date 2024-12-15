# Python imports
import csv
import datetime
import logging
import os
from pathlib import Path
from typing import Union

# Internal imports
from core.helper_functions import get_country_abbr

log = logging.getLogger(__name__)


class CustomerDimension:
    def __init__(self, args: dict):
        log.info('Initializing CustomerDimension object.')

        # CSV metadata
        self.source_csv = Path(args['input_csv'])
        self.output_csv = self._read_output_csv_arg(args.get('output_csv'))

        # Table metadata
        self.rows = self._read_source(source_csv=self.source_csv)
        self.field_names = self.rows[0].keys()

        log.info('Initialization complete.')

    def _read_output_csv_arg(self, output_csv: Union[str, None]) -> Path:
        if output_csv:
            # Use the user-defined output csv path if provided.
            return Path(output_csv)
        else:
            # If the output_csv arg is not defined, we write to the default location.
            source_csv_file_name = str(self.source_csv).split(os.sep)[-1]
            run_date = datetime.datetime.now()
            output_csv = f"{run_date.strftime('%Y%m%d')}_{source_csv_file_name}"
            return Path('csv_files') / output_csv

    def get_record_count(self):
        return len(self.rows)

    def get_column_count(self):
        return len(self.field_names)

    def _read_source(self, source_csv: Path):
        log.info('Reading the source CSV.')
        with open(source_csv, mode='r') as f:
            csv_reader = csv.DictReader(f)
            rows = [row for row in csv_reader]

        log.info('Success.')
        return rows

    def add_country_abbr_col(self):
        log.info('Adding the country abbreviation column.')
        rows = []
        for row in self.rows:
            row['country_abbreviation'] = get_country_abbr(row['country'])
            rows.append(row)

        self.rows = rows
        self.field_names = rows[0].keys()
        log.info('Success.')

    def write_csv(self):
        log.info('Writing to CSV.')
        with open(self.output_csv, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=self.field_names)
            writer.writeheader()
            writer.writerows(self.rows)

        log.info('Success.')
