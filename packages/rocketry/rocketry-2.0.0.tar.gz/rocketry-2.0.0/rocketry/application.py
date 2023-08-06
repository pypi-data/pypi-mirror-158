


import logging
from pathlib import Path
import tempfile
from typing import Optional

from redbird import BaseRepo
from redbird.logging import RepoHandler
from redbird.repos import MemoryRepo, CSVFileRepo
from rocketry.log.log_record import LogRecord

from rocketry.tasks import FuncTask, CommandTask
from rocketry.conditions import FuncCond
from rocketry.parameters import FuncParam
from rocketry import Session

class _AppMixin:

    def task(self, start_cond=None, name=None, *, command=None, path=None, **kwargs):
        kwargs['session'] = self.session
        kwargs['start_cond'] = start_cond
        kwargs['name'] = name
        if command is not None:
            return CommandTask(command=command, **kwargs)
        elif path is not None:
            # Non-wrapped FuncTask
            return FuncTask(path=path, **kwargs)
        else:
            return FuncTask(name_include_module=False, _name_template='{func_name}', **kwargs)

    def param(self, name=None):
        "Create one param"
        return FuncParam(name, session=self.session)


class RedEngine(_AppMixin):

    def __init__(self, session=None, logger_repo:Optional[BaseRepo]=None, execution=None, **kwargs):

        self.session = session if session is not None else Session(**kwargs)

        logger = logging.getLogger(self.session.config.task_logger_basename)
        logger.setLevel(logging.INFO)

        if execution is not None:
            self.session.config.task_execution = execution

        self._set_logger_with_repo(logger_repo)

    def run(self, debug=False):
        self.session.config.debug = debug
        self.session.set_as_default()
        self.session.start()

    def cond(self, syntax=None):
        "Create condition"
        return FuncCond(syntax=syntax, session=self.session)

    def params(self, **kwargs):
        "Set session parameters"
        self.session.parameters.update(kwargs)

    def set_logger(self):
        def wrapper(func):
            func(self._get_task_logger())
        return wrapper

    def _get_task_logger(self):
        logger_name = self.session.config.task_logger_basename
        return logging.getLogger(logger_name)

    def _set_logger_with_repo(self, repo):
        if isinstance(repo, str):
            self._get_repo(repo)
        elif repo is None:
            repo = MemoryRepo(model=LogRecord)
        logger = self._get_task_logger()
        logger.handlers = [
            RepoHandler(repo=repo)
        ]
    
    def _get_repo(self, repo:str):
        if repo == "memory":
            return MemoryRepo(model=LogRecord)
        elif repo == "csv":
            filepath = Path(tempfile.gettempdir()) / "rocketry.csv"
            return CSVFileRepo(filename=filepath, model=LogRecord)
        else:
            raise NotImplementedError(f"Repo creation for {repo} not implemented")
