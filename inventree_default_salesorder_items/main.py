from plugin import InvenTreePlugin
from plugin.mixins import SettingsMixin, EventMixin
from order.models import SalesOrder, SalesOrderLineItem
from part.models import Part


import logging


logger = logging.getLogger('inventree')


class DefaultSalesOrderItemsPlugin(InvenTreePlugin, SettingsMixin, EventMixin):
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

    def log(self, *args):
        logger.debug(f"{self.NAME} {args}")

    @staticmethod
    def wants_process_event(event):
        """In preperation for 0.13.0 https://github.com/inventree/InvenTree/pull/5618"""
        return event == "order_salesorder.created"

    def process_event(self, event, *args, **kwargs):
        if event != "order_salesorder.created":
            return

        self.log(kwargs['id'], "new sales order")

        order = SalesOrder.objects.filter(id=kwargs['id']).first()
        default_part_ids_csv = self.get_setting(
            'DEFAULT_SO_ITEMS_CSV', cache=False)

        if not default_part_ids_csv or default_part_ids_csv == '':
            self.log(
                kwargs['id'],
                "nothing to add, no default items configured"
            )
            return

        default_part_ids = default_part_ids_csv.split(',')

        self.log(kwargs['id'], "add parts", default_part_ids)
        for part_id in default_part_ids:
            self.add_part_id_to_sales_order(order, part_id)

    @staticmethod
    def add_part_id_to_sales_order(order, part_id):
        part = Part.objects.filter(id=part_id).first()

        SalesOrderLineItem.objects.create(
            order=order,
            part=part
        )
