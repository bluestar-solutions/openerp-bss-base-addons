# -*- coding: utf-8 -*-
# Part of Jobs Queue.
# See LICENSE file for full copyright and licensing details.

import logging
import time

from odoo import api, fields, models


class QueueStep(models.Model):
    _name = 'bss.queue.step'
    _description = "Queue Step"
    _logger = logging.getLogger(_name)
    _order = "queue_id, position, name"
    _log_access = False

    STATES = (
        ('queued', "Queued"),
        ('running', "Running"),
        ('failed', "Failed"),
        ('done', "Done"))

    queue_id = fields.Many2one('bss.queue', "Queue")
    position = fields.Integer("Position", required=True, default=1)
    name = fields.Char("Name")
    total = fields.Integer("Total")
    current = fields.Integer("Progression", default=0)
    start_time = fields.Float("Start Time")
    total_time = fields.Float("Total Time")
    elapsed_time = fields.Float("Elapsed Time")
    remaining_time = fields.Float("Remaining Time")

    @api.multi
    def set_total(self, total):
        """Update progression.
        Dedicated to be called only with the queue loaded in run() method
        (with a dedicated cursor)."""
        self.ensure_one()
        if total:
            self.total = total
        else:
            self.progression = 1.
        self.start_time = time.time()
        self.env.cr.commit()

    @api.multi
    def set_current(self, current):
        self.ensure_one()
        """Update progression.
        Dedicated to be called only with the queue loaded in run() method
        (with a dedicated cursor)."""
        elapsed = (time.time() - self.start_time) / 3600
        # Write every 10 seconds or if on last element
        if (elapsed - self.elapsed_time) * 3600 > 10 or current == self.total:
            elapsed = (time.time() - self.start_time) / 3600
            total = self.total * elapsed / current if current > 0 else 0
            self.write({
                'current': current,
                'total_time': total,
                'elapsed_time': elapsed,
                'remaining_time': total - elapsed})
            self.env.cr.commit()
