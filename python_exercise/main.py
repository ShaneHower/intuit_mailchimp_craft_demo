# Python imports
import argparse
import logging

# Internal imports
from core.helper_functions import init_logging
from core.customer_dimension import CustomerDimension

log = logging.getLogger(__name__)


def validate_rows(orig_row_cnt: int, new_row_cnt: int):
    assert orig_row_cnt == new_row_cnt, 'Row validation failed.'


def validate_columns(orig_col_cnt, new_col_cnt):
    assert orig_col_cnt + 1 == new_col_cnt, 'Column validation failed.'


def main(args: dict):
    log.info('Begin.')

    # Read the CSV and add a new column that abbreviates the country name.
    customer_dim = CustomerDimension(args)
    orig_row_cnt = customer_dim.get_record_count()
    orig_col_cnt = customer_dim.get_column_count()

    # Add the new column
    customer_dim.add_country_abbr_col()
    new_row_cnt = customer_dim.get_record_count()
    new_col_cnt = customer_dim.get_column_count()

    # Validate data
    log.info('Validate results.')
    validate_rows(orig_row_cnt=orig_row_cnt, new_row_cnt=new_row_cnt)
    validate_columns(orig_col_cnt=orig_col_cnt, new_col_cnt=new_col_cnt)
    log.info('Success.')

    # Write the results
    customer_dim.write_csv()

    log.info('Finished.')


if __name__ == '__main__':
    init_logging()

    # Initialize CLI args
    parser = argparse.ArgumentParser()
    parser.add_argument('--input-csv', required=True, help='The path of the input csv file.')
    parser.add_argument('--output-csv', help='Define a path for the csv output.')
    args = parser.parse_args()

    main(vars(args))
