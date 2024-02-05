import json


class Job:
    def __init__(self,
                 path: str,
                 level: str,
                 parameter_overwrites: dict[str, str],
                 hidden_parameters: list[str],
                 available_parameters: list[dict[str, str]] = []
                 ):
        self.path: str = path
        self.level: str = level
        self.parameter_overwrites: dict[str, str] = parameter_overwrites
        self.hidden_parameters: list[str] = hidden_parameters
        self.available_parameters: list[dict[str, str]] = available_parameters

    def toJson(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)

    def toDict(self):
        job_dict = {
            'path': self.path,
            'level': self.level,
            'parameter_overwrites': self.parameter_overwrites,
            'hidden_parameters': self.hidden_parameters,
            'available_parameters': self.available_parameters
        }
        return job_dict


class JobManager:
    def __init__(self, jobs: dict[str, Job]):
        self.jobs: dict[str, Job] = jobs

    def get(self, job_name) -> Job:
        seq = self.jobs.get(job_name)
        if seq is not None:
            return seq
        else:
            raise Exception("job not found")

    def toDict(self) -> dict:
        result_dict = {}
        for job_name, job in self.jobs.items():
            result_dict[job_name] = job.toDict()
        return result_dict
