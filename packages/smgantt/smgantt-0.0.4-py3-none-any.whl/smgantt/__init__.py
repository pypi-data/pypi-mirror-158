import argparse
import hashlib
import json
from collections import defaultdict
from datetime import datetime
from pathlib import Path

import pandas as pd
import plotly.express as px

__version__ = "0.0.4"


class Runtime:

    def __init__(self, rule: str, stime: datetime, etime: datetime):
        self.rule = rule
        self.stime = stime
        self.etime = etime
        self.cost = (etime - stime).total_seconds()

    def to_dict(self):
        return {"rule": self.rule, "stime": self.stime, "etime": self.etime, "cost": self.cost}


def get_md5sum(file):
    with open(file, "rb") as f:
        return hashlib.md5(f.read()).hexdigest()


def get_runtimes(metadata: str, min_seconds: int = None, sort_by_name: bool = False) -> pd.DataFrame:
    metadata = Path(metadata)
    counter = defaultdict(int)
    dataset = set()
    runtimes = []
    for p in metadata.iterdir():
        md5sum = get_md5sum(p)
        if md5sum not in dataset:
            dataset.add(md5sum)
            with p.open() as f:
                data = json.load(f)
                rule = data["rule"]
                stime = datetime.fromtimestamp(data["starttime"])
                etime = datetime.fromtimestamp(data["endtime"])
                counter[rule] += 1
                runtime = Runtime(rule, stime, etime)
                runtimes.append(runtime)
    buckets = defaultdict(int)
    for runtime in runtimes:
        if counter[runtime.rule] > 1:
            buckets[runtime.rule] += 1
            runtime.rule = runtime.rule + "#" + str(buckets[runtime.rule])
    if sort_by_name:
        runtimes = sorted(runtimes, key=lambda x: x.rule)
    else:
        runtimes = sorted(runtimes, key=lambda x: x.stime)
    runtimes = pd.DataFrame([runtime.to_dict() for runtime in runtimes])
    if min_seconds:
        runtimes = runtimes[runtimes.cost > min_seconds]
    return runtimes


def plot_gantt(runtimes: pd.DataFrame, output: str):
    fig = px.timeline(runtimes, x_start="stime", x_end="etime", y="rule")
    fig.update_yaxes(autorange="reversed")
    height = runtimes.shape[0] * 25
    width = height / 0.618
    fig.write_image(output, engine="kaleido", width=width, height=height)


def main():
    parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter, description="Snakemake Gantt {}".format(__version__))
    parser.add_argument("-V", "--version", action="version", version=__version__)
    parser.add_argument("-m",
                        "--metadata",
                        type=str,
                        default=".snakemake/metadata",
                        help="Snakemake metadata directory, default: .snakemake/metadata")
    parser.add_argument("-o", "--output", type=str, default="gantt.png", help="Output image, default: gantt.png")
    parser.add_argument("-s", "--min-seconds", type=int, default=None, help="Minimum runtime in seconds, default: None, means all")
    parser.add_argument("-n", "--sort-by-name", action="store_true", help="Sort by rule name, default: False")
    args = parser.parse_args()
    runtimes = get_runtimes(args.metadata, args.min_seconds, args.sort_by_name)
    plot_gantt(runtimes, args.output)


if __name__ == "__main__":
    main()
