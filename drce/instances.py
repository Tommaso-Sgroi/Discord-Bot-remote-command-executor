from drce.command_executor import DistroyExecutor
from drce.command_interpreter import DistroyInterpreter

# from drce.distroy_logger import DistroyLogger

command_interpreter: DistroyInterpreter
command_executor: DistroyExecutor


# command_logger: DistroyLogger

def init():
    global command_executor
    global command_interpreter
    # global command_logger

    command_interpreter = DistroyInterpreter()
    command_executor = DistroyExecutor()

    # command_logger = DistroyLogger()
    # command_executor.attach(command_logger)
