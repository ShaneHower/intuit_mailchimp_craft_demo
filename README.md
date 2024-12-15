# Table of Contents
- [Overview](#overview)
- [Python Exercise](#python-exercise)
	- [How to Run](#how-to-run)
	- [Unit Test](#unit-test)
- [SQL Exercise](#sql-exercise)

# Overview
This is my submission for the Experimentation team's craft exercise.

# Python Exercise
Since the prompt was straightforward, I tried to make the structure of this project more "productionized". In particular, I included classes, functions, args parsing, logging, unit testing, and validations.

It's important to note that this script would struggle to handle very large volumes of data and would not be a great solution for anything larger than a few thousand records. Ideally we would want to move to some kind of distributed system like Spark, Athena, Snowflake, or BigQuery.

### How to Run

Use the following call in the project directory to quickly run the script:

```bash
python main.py --input-csv "csv_files/customer_dimension.csv"
```

This will read the `customer_dimension.csv` file in the directory `csv_files`, transform it according to the exercise prompt, and write the results to the same directory.

#### Arguments

- input-csv (str: required): The path to the input csv file.
- output-csv (str: optional): The custom name and path that the generated csv file will use. If this arg is not defined, the script will write to the default `csv_files` folder and use a timestamp to generate the csv file name.

#### Example Calls

##### Standard Call

```bash
python main.py --input-csv "csv_files/customer_dimension.csv"
```

##### Custom Path Call

```bash
python  main.py  \
--input-csv "~/some/special/path/customer_dimension.csv" \
--output-csv "~/some/special/path/results.csv"
```

### Unit Test

I decided to build a unit test for the [get_country_abbr](python_exercise/core/helper_functions.py) function since it holds the bulk of the logic that you requested. You can run this test by executing the following command.

```bash
python -m unittest "tests/test_helper_functions.py"
```

# SQL Exercise

As suggested, I used [SQLite](https://sqliteonline.com/) to complete this exercise.

I first validated that there was uniqueness for both `customer_dimension.customer_id` and `date_dimension.date_id` before joining to the `emails_sent_fact` table.

For the aggregated columns that you requested:

1.  **Maximum number of emails opened** - This was just a simple max function.

2.  **Running total of email opens for each country** - I wasn't sure if I was interpreting this correctly. At first I took the sum at the requested grain. I ended up changing this logic so that it instead shows the total at the country level which I think is what you were looking for.

3.  **Number of customers that sent at least 1 email** - This was a distinct client id count at the requested grain. I first made sure that there were no null or 0 count values in `email_sent_fact.email_opens_cnt`. If there were null or 0 values, I would have had to filter them out of the final count.

I validated the results by making sure the total sum of `email_sent_fact.email_opens_cnt` matched request (2). I did this by comparing the total sum of `email_sent_fact.email_opens_cnt` to the distinct sum at the `country`/`total_emails_sent_per_country` level in my results table `customer_email_metrics`.
