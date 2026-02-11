.PHONY: provision start grade reset stop status lint

provision:
	./scripts/examctl provision

start:
	./scripts/examctl start

grade:
	./scripts/examctl grade

reset:
	./scripts/examctl reset

stop:
	./scripts/examctl stop

status:
	./scripts/examctl status

lint:
	python3 -m py_compile scripts/simpleyaml.py scripts/generate_exam.py scripts/score.py
	bash -n scripts/examctl scripts/netblock.sh
