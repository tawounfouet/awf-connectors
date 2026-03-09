import logging
from pyconnectors.config import ConnectorConfig
from pyconnectors.factory import ConnectorFactory
import pyconnectors.connectors.http.rest  # noqa

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("hooks")


def pre_log(connector, *args, **kwargs):
    logger.info(f"Starting execution for {connector.__class__.__name__}")


def post_log(connector, result, *args, **kwargs):
    logger.info(f"Finished in {result.duration:.3f}s. Success: {result.success}")


def error_log(connector, result, *args, **kwargs):
    logger.error(f"Execution failed: {result.error}")


def main():
    config = ConnectorConfig()
    http = ConnectorFactory.create("http.rest", config=config)

    http.add_hook("pre_execute", pre_log)
    http.add_hook("post_execute", post_log)
    http.add_hook("on_error", error_log)

    print("Executing valid request...")
    http.safe_execute("GET", "https://httpbin.org/get")

    print("\nExecuting invalid request (expecting error)...")
    http.safe_execute("GET", "invalid_url")


if __name__ == "__main__":
    main()
