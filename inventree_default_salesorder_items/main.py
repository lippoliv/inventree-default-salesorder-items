from plugin import InvenTreePlugin
from plugin.mixins import SettingsMixin


class DefaultSalesOrderItemsPlugin(InvenTreePlugin, SettingsMixin):
    NAME = "DefaultSalesOrderItemsPlugin"
    SLUG = "inventree_default_salesorder_items"
    TITLE = "Default sales order items"

    # metadata
    AUTHOR = "Oliver Lippert"
    DESCRIPTION = "Add the configured items to every new sales order"
    VERSION = "0.0.0"
    WEBSITE = "https://github.com/lippoliv/inventree-default-salesorder-items"
    LICENSE = "MIT"

    SETTINGS = {
        'DEFAULT_SO_ITEMS_CSV': {
            'name': 'Default items',
            'description': 'Add this items to every new sales order (put in ID\'s here as a CSV)',
            'default': '',
            'required': True,
        },
    }
