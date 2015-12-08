# vim: set ts=8 sts=8 sw=8 noexpandtab:

DIRS := environments library playbooks plugins roles secrets services
USER ?= $(shell whoami)

dependencies: $(DIRS) .env .vault_password

.env:
	@./setup.bash
	@echo
	@echo "Execute: source .env/bin/activate"
	@echo

.vault_password: vault_password/$(USER).gpg
	keybase pgp decrypt -i vault_password/$(USER).gpg > .vault_password

vault_password/*.gpg:

compute.zip: dependencies $(DIRS)
	zip -r compute.zip $(DIRS)
	cd .env && zip -r ../compute.zip lib/python2.7/site-packages

clean:
	rm -rf .env

.PHONY: clean
