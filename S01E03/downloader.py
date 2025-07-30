from common.data_fetcher import DataFetcher

def download_input_file(url: str, logger) -> dict:
    logger.info("Downloading input data...")
    fetcher = DataFetcher()
    return fetcher.fetch_json(url)