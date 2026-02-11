#!/usr/bin/env python3
import argparse
import datetime as dt
import random
from pathlib import Path

from simpleyaml import load


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--taskbank', default='tasks/taskbank.yml')
    p.add_argument('--template', default='tasks/exams/exam_template.md')
    p.add_argument('--output', default='tasks/exams/current_exam.md')
    p.add_argument('--duration', type=int, default=180)
    p.add_argument('--seed', type=int, default=42)
    p.add_argument('--max-points', type=int, default=300)
    p.add_argument('--pass-threshold', type=int, default=210)
    args = p.parse_args()

    tasks = load(args.taskbank)
    if not isinstance(tasks, list):
        raise SystemExit('Taskbank must parse into a YAML list')

    random.Random(args.seed).shuffle(tasks)

    lines = []
    for i, t in enumerate(tasks, start=1):
        lines.append(f"### {i}. [{t['id']}] {t['title']} ({t['points']} points)")
        lines.append(f"**Domain:** {t['objective_domain']}")
        lines.append(str(t['instructions']).rstrip())
        lines.append("")

    body = Path(args.template).read_text()
    body = body.replace('{{ duration_minutes }}', str(args.duration))
    body = body.replace('{{ generated_at }}', dt.datetime.now().isoformat(timespec='seconds'))
    body = body.replace('{{ seed }}', str(args.seed))
    body = body.replace('{{ tasks_markdown }}', '\n'.join(lines))
    body = body.replace('{{ max_points }}', str(args.max_points))
    body = body.replace('{{ pass_threshold }}', str(args.pass_threshold))

    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(body)
    print(f"Generated exam brief: {out}")


if __name__ == '__main__':
    main()
