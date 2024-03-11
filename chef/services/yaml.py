from clases.sequence import Sequence, SequenceJob, SequenceManager
from config import PDI_HOME, JOBS_FILE, SEQUENCES_FILE
import yaml as __yaml
from clases.job import Job, JobManager


def load_yaml(path: str) -> dict:
    with open(PDI_HOME + path, 'r') as stream:
        return __yaml.safe_load(stream)


def load_jobs(path: str) -> JobManager:
    with open(PDI_HOME + path, 'r') as stream:
        data = __yaml.safe_load(stream)
    jobs_dict: dict[str, Job] = {}
    for job_name, job_data in data.get('jobs', {}).items():
        jobs_dict[job_name] = Job(
            job_data.get('path', ''),
            job_data.get('level', 'basic'),
            job_data.get('default_parameters', {}),
            job_data.get('hidden_parameters', [])
        )
    return JobManager(jobs_dict)


def load_sequences(path: str) -> SequenceManager:
    with open(PDI_HOME + path, 'r') as stream:
        data = __yaml.safe_load(stream)
    sequences: dict[str, Sequence] = {}
    for sequence_name, sequence_data in data.get('sequences', {}).items():
        sequences[sequence_name] = Sequence([])
        for sequence_job in sequence_data or []:
            sequences[sequence_name].append(SequenceJob(
                sequence_job.get('job', ''),
                sequence_job.get('parameter_overwrites', {}),
            ))
    return SequenceManager(sequences)


def get_sequences() -> SequenceManager:
    return load_sequences("/jobs/" + SEQUENCES_FILE)


def get_seq(name: str) -> Sequence:
    return get_sequences().get(name)


def get_jobs() -> JobManager:
    return load_jobs("/jobs/" + JOBS_FILE)


def get_job(name: str) -> Job:
    return get_jobs().get(name)
