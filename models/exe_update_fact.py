from odoo import models, fields, api
import logging

_logger = logging.getLogger(__name__)

class ExeUpdateFact(models.Model):
    _inherit = 'sale.order'

    def action_confirm(self):
        """Sobreescribe la acción de confirmación de la orden de venta, asegurando que todas las producciones asociadas cambien de estado."""
        _logger.info("Confirmando orden de venta: %s", self.name)

        # Primero, ejecutamos la lógica original de Odoo
        res = super(ExeUpdateFact, self).action_confirm()

        # Buscar todas las órdenes de producción asociadas a la orden de venta
        for order in self:
            productions = self.env['mrp.production'].search([('origin', 'like', f"%{order.name}%")])

            if productions:
                _logger.info("Producciones asociadas encontradas: %s", productions.mapped("name"))
                
                for production in productions:
                    # Cambiar el estado de todas las producciones a "done" si aún no están completadas
                    if production.state != 'done':
                        production.write({"state": "done"})
                        _logger.info("Producción ID: %s actualizada a 'done'", production.id)
            else:
                _logger.warning("No se encontraron producciones asociadas para la orden: %s", order.name)

        return res
