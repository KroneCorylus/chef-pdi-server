from clases.sequence import Sequence
import services
import providers
import json
import threading


def execute(name: str) -> str:
    sequence: Sequence = services.yaml.get_seq(name)
    id_sequence_execution = providers.sequence.insert(name)
    providers.sequence.remove_old()
    thread = threading.Thread(
        target=execute_jobs_in_sequence, args=(sequence, id_sequence_execution))
    thread.start()
    return json.dumps(sequence.toDict())


def execute_jobs_in_sequence(sequence: Sequence, id_sequence_execution: int):
    for job in sequence:
        job_name = job.job
        parameter_overwrites = job.parameter_overwrites
        services.job.execute(
            job_name, parameter_overwrites, id_sequence_execution)
    providers.sequence.update_end_date(id_sequence_execution)


def get_executions(name: str) -> list[dict]:
    return providers.sequence.get_executions(name)
