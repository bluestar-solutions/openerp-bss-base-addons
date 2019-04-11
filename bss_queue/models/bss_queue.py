# -*- coding: utf-8 -*-
# Part of Jobs Queue.
# See LICENSE file for full copyright and licensing details.

from datetime import datetime
import logging
from threading import Lock, Thread
import traceback

from odoo import _, api, fields, models, registry, SUPERUSER_ID
from odoo.exceptions import UserError
from odoo.tools.safe_eval import safe_eval


service_lock = Lock()


class Queue(models.Model):
    _name = 'bss.queue'
    _description = "Queue"
    _logger = logging.getLogger(_name)
    _order = "date_from desc, id desc"

    STATES = (
        ('queued', "Queued"),
        ('running', "Running"),
        ('failed', "Failed"),
        ('done', "Done"))

    name = fields.Char("Name")
    state = fields.Selection(STATES, "State", required=True, default='queued')
    model = fields.Char("Model", required=True)
    method = fields.Char("Method", required=True)
    failed_method = fields.Char("Failed Method")
    args = fields.Char("Arguments", required=True, default="[]")
    user_id = fields.Many2one('res.users', "User", default=SUPERUSER_ID)
    date_from = fields.Datetime(
        "Date From", default=lambda self: datetime.now().isoformat(' '))
    error_log = fields.Text("Error Log")
    step_ids = fields.One2many('bss.queue.step', 'queue_id', "Steps")
    flag_stop = fields.Boolean("Stop")

    @api.model
    def new_job(self, name, model, method, failed_method, *args):
        return self.sudo().create({
            'name': name,
            'model': model,
            'method': method,
            'failed_method': failed_method,
            'args': repr(args)})

    @api.model
    def gnome_checking(self):
        queue = self.search(
            [('state', '=', 'queued')], order="date_from desc, id desc",
            limit=1)
        if queue:
            queue.run(queue.id, queue.user_id.id)

    @api.multi
    def manual_run(self):
        self.ensure_one()
        with service_lock:
            if self.state != 'queued':
                raise UserError(_("The job is not in queued state."))
            self.state = 'running'
        Thread(target=self.run, args=(self.id, self.user_id.id, False)).start()

    @api.model
    def run(self, qid, uid, set_state=True):
        Env, reg = api.Environment, registry(self.env.cr.dbname)
        with Env.manage(), reg.cursor() as crc, reg.cursor() as crj:
            control_env = Env(crc, SUPERUSER_ID, {})
            job_env = Env(crj, uid, {})
            # Load queue in a dedicated environment, dedicated to update
            # queue and steps states with explicit commits, outside
            # the job transaction.
            queue = control_env[self._name].browse(qid)
            if set_state:
                queue.state = 'running'
            try:
                getattr(job_env[queue.model], queue.method)(
                    queue, *safe_eval(queue.args))
            except Exception:
                crj.rollback()
                queue.write(
                    {'state': 'failed', 'error_log': traceback.format_exc()})
                if queue.failed_method:
                    getattr(job_env[queue.model], queue.failed_method)(
                        queue, *safe_eval(queue.args))
            else:
                crc.commit()
                crj.commit()
                queue.write({'state': 'done'})
            finally:
                crc.commit()
                crj.commit()

    def stop(self):
        self.ensure_one()
        self.flag_stop = True
        self.env.cr.commit()
        # Force cache clear for all concurrent processes
        self.clear_caches()

    @api.multi
    def define_steps(self, steps):
        """Define steps.
        Dedicated to be called only with the queue loaded in run() method
        (with a dedicated cursor)."""
        self.ensure_one()
        self.write({'step_ids': [
            (0, 0, {'position': s[0], 'name': s[1]}) for s in steps]})
        self.env.cr.commit()
        return {s.position: s for s in self.step_ids}
