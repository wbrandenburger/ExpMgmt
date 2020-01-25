import logging

logger = logging.getLogger("plugin")

def stevedore_error_handler(manager, entrypoint, exception):
    logger.error("Error while loading entrypoint [{0}]".format(entrypoint))
    logger.error(exception)
