build:
	docker build -t opsee-ansible .

check: build
	./run coreos-production --check

.PHONY: build check
