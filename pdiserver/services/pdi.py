from pdiserver.config import BASE_DIR
import subprocess
import threading
from pdiserver import providers

KITCHEN = BASE_DIR + "/data-integration/kitchen.sh"
PAN = BASE_DIR + "/data-integration/pan.sh"


def getCommand(job: dict, parameters: dict) -> list[str]:
    jobPath: str = job["path"]
    logLevel: str = job["level"] if job["level"] is not None else 'Basic'
    print(job["level"], logLevel)
    command: list[str] = [KITCHEN, "-file:" + jobPath, "-level:" + logLevel]
    if parameters is not None:
        command = command + getParameterString(parameters)
    print(command)
    return command


def capture_output(process: subprocess.Popen, rowid: int):
    print("enter capture")
    stdout, stderr = process.communicate()
    print("finish capture")
    providers.job.update_execution_result(
        rowid, stdout, stderr, process.returncode)


def executeCommand(job_name: str, command: list[str]) -> str:
    process: subprocess.Popen = subprocess.Popen(command,
                                                 cwd=BASE_DIR + "/jobs",
                                                 stdout=subprocess.PIPE,
                                                 stderr=subprocess.PIPE,
                                                 text=True)
    rowid: int = providers.job.insert_execution(job_name, process.pid)
    thread = threading.Thread(target=capture_output, args=(process, rowid))
    thread.start()
    return str(process.pid) + ":" + str(rowid)


def getParameterString(parameters: dict) -> list[str]:
    paramList: list[str] = []
    for key in parameters:
        paramString = "-param:" + key + "=" + str(parameters[key]) + ""
        paramList.append(paramString)
    return paramList
    return paramList
