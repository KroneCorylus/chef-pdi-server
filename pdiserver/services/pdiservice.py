from pdiserver.config import BASE_DIR
import subprocess
import threading
from pdiserver.providers.execution import insert_execution, update_execution_result, get_job_executions, get_execution_log
from pdiserver.providers import execution
import os
import xml.etree.ElementTree as ET

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
    update_execution_result(rowid, stdout, stderr, process.returncode)


def executeCommand(job_name: str, command: list[str]) -> str:
    process: subprocess.Popen = subprocess.Popen(command,
                                                 cwd=BASE_DIR + "/jobs",
                                                 stdout=subprocess.PIPE,
                                                 stderr=subprocess.PIPE,
                                                 text=True)
    rowid: int = execution.insert_execution(job_name, process.pid)
    thread = threading.Thread(target=capture_output, args=(process, rowid))
    thread.start()
    return str(process.pid) + ":" + str(rowid)


def get_executions(job_name):
    return get_job_executions(job_name)


def get_job_execution_log(job_name, rowid):
    return get_execution_log(job_name, rowid)


def get_job_parameters(job):
    job_path = os.path.join(BASE_DIR + "/jobs", job["path"])
    tree = ET.parse(job_path)
    params = tree.findall("./parameters/parameter")
    result: list[dict] = []
    for param in params:
        result.append({
            'name': param.findtext("name"),
            'default': param.findtext("default_value"),
            'description': param.findtext("description")
        })
    return result


def getParameterString(parameters: dict) -> list[str]:
    paramList: list[str] = []
    for key in parameters:
        paramString = "-param:" + key + "=" + str(parameters[key]) + ""
        paramList.append(paramString)
    return paramList
    return paramList
