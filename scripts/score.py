#!/usr/bin/env python3
import argparse
import json
from pathlib import Path


def load_json(path):
    return json.loads(Path(path).read_text())


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--pre', default='artifacts/pre_reboot.json')
    p.add_argument('--post', default='artifacts/post_reboot.json')
    p.add_argument('--out-json', default='artifacts/results.json')
    p.add_argument('--out-md', default='artifacts/results.md')
    p.add_argument('--pass-threshold', type=int, default=210)
    args = p.parse_args()

    pre = load_json(args.pre)['results']
    post = load_json(args.post)['results']

    post_idx = {r['id']: r for r in post}
    merged = []
    score = 0
    max_points = 0

    for r in pre:
        rid = r['id']
        persisted = bool(post_idx.get(rid, {}).get('passed', False))
        initial = bool(r.get('passed', False))
        passed = initial and persisted
        pts = int(r['points'])
        max_points += pts
        if passed:
            score += pts
        merged.append({
            'id': rid,
            'title': r['title'],
            'points': pts,
            'pre_passed': initial,
            'post_passed': persisted,
            'final_passed': passed,
        })

    status = 'PASS' if score >= args.pass_threshold else 'NO PASS'
    result = {
        'score': score,
        'max_points': max_points,
        'pass_threshold': args.pass_threshold,
        'status': status,
        'tasks': merged,
    }

    Path(args.out_json).write_text(json.dumps(result, indent=2))

    md = [
        '# Exam Results',
        f"- Score: **{score}/{max_points}**",
        f"- Threshold: **{args.pass_threshold}**",
        f"- Status: **{status}**",
        '',
        '| ID | Title | Points | Pre | Post | Final |',
        '|---|---|---:|:---:|:---:|:---:|',
    ]
    for t in merged:
        md.append(f"| {t['id']} | {t['title']} | {t['points']} | {'✅' if t['pre_passed'] else '❌'} | {'✅' if t['post_passed'] else '❌'} | {'✅' if t['final_passed'] else '❌'} |")

    Path(args.out_md).write_text('\n'.join(md) + '\n')
    print(f"Final score: {score}/{max_points} => {status}")


if __name__ == '__main__':
    main()
