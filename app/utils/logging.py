"""_summary_
"""

import logging

from app.core.config import settings

logger = logging.getLogger()
logger.setLevel(settings.API_DEBUG_LEVEL)
