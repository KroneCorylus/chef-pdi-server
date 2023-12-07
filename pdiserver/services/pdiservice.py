from pdiserver.config import BASE_DIR
import subprocess
import json
KITCHEN = BASE_DIR + "/data-integration/kitchen.sh"
PAN = BASE_DIR + "/data-integration/pan.sh"


def getCommand(file: str, parameters: dict) -> list[str]:
    # command = KITCHEN + " -file:'" + file + "'"
    command: list[str] = [KITCHEN, "-file:" + file + ""]
    if parameters is not None:
        command = command + getParameterString(parameters)
    return command


def executeCommand(command: list[str]) -> str:
    proc = subprocess.Popen(command,  cwd=BASE_DIR + "/jobs")
    return str(proc.pid)
    # return json.dumps(command)


# def getCommand(file: str) -> str:
#     return KITCHEN + " -file:'" + file + "'"


def getParameterString(parameters: dict) -> list[str]:
    paramList: list[str] = []
    for key in parameters:
        paramString = "-param:" + key + "=" + parameters[key] + ""
        paramList.append(paramString)
    return paramList
