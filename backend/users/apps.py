import logging

from django.apps import AppConfig

logger = logging.getLogger(__name__)

class UsersConfig(AppConfig):
    name = 'users'
    verbose_name = 'Users'

    def ready(self):
        pass
        # Prevent multiple imports
        # if hasattr(self, 'signals_loaded'):
        #     return
        # try:
        #     import users.signals
        #     self.signals_loaded = True
        #     logger.info("Users signals imported successfully (once)")
        # except Exception as e:
        #     logger.error(f"Failed to import users.signals: {e}")
