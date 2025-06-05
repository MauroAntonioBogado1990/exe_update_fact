from odoo import models, fields, api
import logging

_logger = logging.getLogger(__name__)

class ExeUpdateFact(models.Model):
    _inherit = 'sale.order'

    mrp = fields.Char(string='Production Order Asociated', compute='_compute_mrp_associated', store=True)

    @api.depends('name', 'state')
    def _compute_mrp_associated(self):
        for order in self:
            _logger.info("Buscando producción asociada para la orden de venta: %s", order.name)

            # Buscar la producción cuya 'origin' contiene el nombre de la orden de venta
            production = self.env['mrp.production'].search([('origin', 'like', f"%{order.name}%")], limit=1)

            if production:
                order.mrp = production.name
                _logger.info("Producción encontrada: %s | Origin: %s", production.name, production.origin)

                # Si el estado de la orden de venta cambia a 'sale', actualizar producción a 'done'
                if order.state == 'sale' and production.state != 'done':
                    production.write({"state": "done"})
                    _logger.info("Producción ID: %s actualizada a 'done'", production.id)
            else:
                order.mrp = ""
                _logger.warning("No se encontró producción asociada para la orden: %s", order.name)