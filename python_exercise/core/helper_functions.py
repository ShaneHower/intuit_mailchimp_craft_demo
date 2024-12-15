import logging

def get_country_abbr(country_name: str) -> str:
    words = country_name.split(' ')
    if len(words) == 1:
        # For single word countries, abbreviate by taking the first two letters + the last letter of the word.
        word = words[0]
        return word[0:2].upper() + word[-1].upper()
    else:
        # For multi-word countries, abbreviate by taking the first letter of each word.
        return ''.join(word[0].upper() for word in words)


def init_logging():
    # Initialize log
    logging.basicConfig(
        filename='log.log',
        filemode='w',
        level=logging.INFO,
        format="%(asctime)s %(levelname)-8s %(name)-50s %(message)s"
    )
