import argparse
from external_ingestor.ExternalIngestor import ExternalIngestor
from external_ingestor.utils.logging import get_logger
from external_ingestor.utils.parse_config import parse_config
import time



def get_args():
    parser = argparse.ArgumentParser(description="specify job")
    parser.add_argument('--jobname', help="Job Name", required=True)
    parser.add_argument('--start_time', help="Date start", required=True)
    parser.add_argument('--end_time', help="Date end")
    return parser.parse_args()


def run_config():
    logger.info("--- Running job {} ---".format(args.jobname))
    configs = parse_config(args.jobname)
    transformer = configs['transformer']
    domain = configs['domain']
    sink = configs['sink']
    client = configs['client']
    path = configs['path']
    method = configs['method']
    client_settings = configs['client_settings']
    sink_settings = configs['sink_settings']
    runner = ExternalIngestor(domain, transformer, sink, client, method, client_settings, sink_settings)
    runner.run(path, args.start_time, args.end_time)


if __name__ == "__main__":
    logger = get_logger(__name__)
    start_time = time.time()
    args = get_args()
    run_config()
    logger.info("--- Job execution finished in %s seconds ---" % (time.time() - start_time))

