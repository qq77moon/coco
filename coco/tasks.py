# coding: utf-8
import weakref
import logging

logger = logging.getLogger(__file__)


class TaskHandler:

    def __init__(self, app):
        self._app = weakref.ref(app)

    @property
    def app(self):
        return self._app()

    def handle_kill_session(self, task):
        logger.info("Handle kill session task: {}".format(task.args))
        session_id = task.args
        session = None
        for s in self.app.sessions:
            if s.id == session_id:
                session = s
                break

        if session:
            session.close()
        self.app.service.finish_task(task.id)

    def handle(self, task):
        if task.name == "kill_session":
            self.handle_kill_session(task)
        else:
            logger.error("No handler for this task: {}".format(task.name))
