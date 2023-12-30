from config import PDI_HOME
import subprocess
import threading
import providers

import sys
KITCHEN = PDI_HOME + "/data-integration/kitchen.sh"
PAN = PDI_HOME + "/data-integration/pan.sh"


def get_command(job: dict, parameters: dict) -> list[str]:
    jobPath: str = job["path"]
    logLevel: str = job.get("level", "Basic")
    command: list[str] = [KITCHEN, "-file:" + jobPath, "-level:" + logLevel]
    if parameters is not None:
        command = command + getParameterString(parameters)
    print(command)
    return command


def execute(job_name: str,
            job: dict,
            parameters: dict,
            id_secuence_execution: int | None = None) -> dict:
    command = get_command(job, parameters)
    return execute_command(job_name, command, id_secuence_execution)


def execute_command(job_name: str, command: list[str], id_secuence_execution: int | None = None) -> dict:
    print(' '.join(command))
    process: subprocess.Popen = subprocess.Popen(command,
                                                 cwd=PDI_HOME + "/jobs",
                                                 stdout=subprocess.PIPE,
                                                 stderr=subprocess.PIPE,
                                                 )
    rowid: int = providers.job.insert_execution(
        job_name, process.pid, id_secuence_execution)

    if id_secuence_execution is None:
        thread = threading.Thread(target=capture_output, args=(process, rowid))
        thread.start()
        providers.job.remove_old()
    else:
        capture_output(process, rowid)
    return {
        "pid": str(process.pid),
        "id": str(rowid)
    }


def capture_output(process: subprocess.Popen, rowid: int):
    stdout_bytes, stderr_bytes = process.communicate()
    stdout = stdout_bytes.decode('utf-8')
    stderr = stderr_bytes.decode('utf-8')
    return_code = process.returncode
    print(f"Return Code: {return_code}")
    # Check the return code
    providers.job.update_execution_result(
        rowid, stdout, stderr, process.returncode)


def getParameterString(parameters: dict) -> list[str]:
    paramList: list[str] = []
    for key in parameters:
        paramString = "-param:" + key + "=" + str(parameters[key]) + ""
        paramList.append(paramString)
    return paramList
