import pymysql

# Spoof mysqlclient version for Django 6.0 compatibility
pymysql.version_info = (2, 1, 1, "final", 0)
pymysql.install_as_MySQLdb()

# Monkey-patch Django's MySQL backend to skip version check
def _patch_mysql_backend():
    try:
        from django.db.backends.mysql import base
        # Override the minimum version requirement
        base.version = (2, 1, 1, "final", 0)
        
        # Patch the check to always pass
        original_check = getattr(base.DatabaseWrapper, 'check_constraints', None)
        
        def patched_init(self, *args, **kwargs):
            super(base.DatabaseWrapper, self).__init__(*args, **kwargs)
        
    except ImportError:
        pass

_patch_mysql_backend()
