# Copyright 2023 Yiğit Budak (https://github.com/yibudak)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)
from odoo import models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    def _get_images(self):
        """
        Override to add base_multi_image images to the list of images.
        """
        self.ensure_one()
        return self.image_ids.filtered(lambda i: i.bind_ids and i.is_published)
