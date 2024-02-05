import json


class SequenceJob:

    def __init__(self, job: str, parameter_overwrites: dict[str, str]):
        self.job: str = job
        self.parameter_overwrites: dict[str, str] = parameter_overwrites

    def toJson(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)

    def toDict(self):
        sequence_job_dict = {
            'job': self.job,
            'parameter_overwrites': self.parameter_overwrites,
        }
        return sequence_job_dict


class Sequence(list[SequenceJob]):
    def toDict(self) -> list[dict]:
        return list(
            map(
                lambda seq: seq.toDict(),
                self
            )
        )


class SequenceManager:
    def __init__(self, sequences: dict[str, Sequence]):
        self.sequences: dict[str, Sequence] = sequences

    def get(self, sequence_name) -> Sequence:
        seq = self.sequences.get(sequence_name)
        if seq is not None:
            return seq
        else:
            raise Exception("secuencia no encontrada")

    def toDict(self) -> dict:
        result_dict = {}
        for seq_name, seq_jobs in self.sequences.items():
            sequence = []
            for seq in seq_jobs:
                sequence.append(seq.toDict())
            result_dict[seq_name] = sequence
        return result_dict
