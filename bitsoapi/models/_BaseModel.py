from datetime import datetime


class BaseModel:

    @classmethod
    def _NewFromJsonDict(cls, data, **kwargs):
        if kwargs:
            for key, val in kwargs.items():
                data[key] = val
        return cls(**data)

    def _iso8601(self, t):
        t = ''.join(re.search("^(.*\+\d\d):(\d\d)$", t).groups())
        return datetime.strptime(t, "%Y-%m-%dT%H:%M:%S%z")

    def _repr(self, *attrs):
        v = lambda v: str(getattr(self, v, None))
        return ", ".join(
            map(lambda attr: "{k}={v}".format(k=attr, v=v(attr)), attrs)
        )

