build:
	docker build -t quay.io/opsee/compute:latest .

push:
	docker push quay.io/opsee/compute:latest

check: build
	./run coreos-production --check

.PHONY: build check push
