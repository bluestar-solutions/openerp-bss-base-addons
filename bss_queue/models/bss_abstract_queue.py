# -*- coding: utf-8 -*-
# Part of Jobs Queue.
# See LICENSE file for full copyright and licensing details.

import logging

from odoo import fields, models


class AbstractQueue(models.AbstractModel):
    _name = 'bss.abstract_queue'
    _description = "Abstract Queue"
    _logger = logging.getLogger(_name)

    queue_id = fields.Many2one('bss.queue', "Queue", ondelete="set null")
    queue_state = fields.Selection(
        lambda self: self.env['bss.queue'].STATES,
        "Queue State", related='queue_id.state', readonly=True)
    queue_stop = fields.Boolean(
        "Queue Stop", related='queue_id.flag_stop', readonly=True)
    step_ids = fields.One2many(
        'bss.queue.step', string="Steps", related='queue_id.step_ids',
        readonly=True)

    def reload(self):
        return True
