# -*- coding: utf-8 -*-
"""

    walle-web

    :copyright: © 2015-2017 walle-web.io
    :created time: 2017-03-25 11:15:01
    :author: wushuiyong@walle-web.io
"""

from flask import request, abort,current_app
from walle.api.api import SecurityResource
from walle.model.record import RecordModel
from walle.model.task import TaskModel
from walle.service.deployer import Deployer


class DeployAPI(SecurityResource):
    def get(self, task_id=None):
        """
        fetch deploy list or one item
        /deploy/<int:env_id>

        :return:
        """
        super(DeployAPI, self).get()

    def put(self,task_id):
        """
        update deploy
        /deploy/<int:task_id>
        """
        try:
            current_app.logger.info('-----------start a deploy with gitlab runner--------------')
            current_app.logger.info(task_id)
            task_info = TaskModel(id=task_id).item()
            wi = Deployer(task_id=task_id, console=False, api_trigger=True)
            deploy_status = False
            if task_info['is_rollback']:
                deploy_status =  wi.walle_rollback()
            else:
                deploy_status =  wi.walle_deploy()
            current_app.logger.info('-----------end deploy with gitlab runner--------------')

            return self.render_json(data=deploy_status)
        except Exception as e:
            current_app.logger.info(e)
            return self.render_error(code=2001, message='发布失败')
        
       