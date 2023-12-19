from ..config import BASE_DIR
import subprocess
import threading
from .. import providers

KITCHEN = BASE_DIR + "/data-integration/kitchen.sh"
PAN = BASE_DIR + "/data-integration/pan.sh"


def get_command(job: dict, parameters: dict) -> list[str]:
    jobPath: str = job["path"]
    logLevel: str = job["level"] if job["level"] is not None else 'Basic'
    command: list[str] = [KITCHEN, "-file:" + jobPath, "-level:" + logLevel]
    if parameters is not None:
        command = command + getParameterString(parameters)
    print(command)
    return command


def execute(job_name: str,
            job: dict,
            parameters: dict,
            id_secuence_execution: int = None) -> dict:
    command = get_command(job, parameters)
    return execute_command(job_name, command, id_secuence_execution)


def execute_command(job_name: str, command: list[str], id_secuence_execution: int = None) -> dict:
    process: subprocess.Popen = subprocess.Popen(command,
                                                 cwd=BASE_DIR + "/jobs",
                                                 stdout=subprocess.PIPE,
                                                 stderr=subprocess.PIPE,
                                                 text=True)
    rowid: int = providers.job.insert_execution(
        job_name, process.pid, id_secuence_execution)

    if id_secuence_execution is None:
        thread = threading.Thread(target=capture_output, args=(process, rowid))
        thread.start()
    else:
        capture_output(process, rowid)
    return {
        "pid": str(process.pid),
        "id": str(rowid)
    }


def capture_output(process: subprocess.Popen, rowid: int):
    print("enter capture")
    stdout, stderr = process.communicate()
    print("finish capture")
    providers.job.update_execution_result(
        rowid, stdout, stderr, process.returncode)


def getParameterString(parameters: dict) -> list[str]:
    paramList: list[str] = []
    for key in parameters:
        paramString = "-param:" + key + "=" + str(parameters[key]) + ""
        paramList.append(paramString)
    return paramList
    return paramList
