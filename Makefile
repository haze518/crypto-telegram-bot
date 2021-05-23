all:
	@echo "make devenv_external_resources	- Create & setup development virtual environment for external_resources"
	@echo "make devenv_dashboard						- Create & setup development virtual environment for dashboard"
	@echo "make mongo						- Start mongo container"
	@exit 0

devenv_external_resources:
	cd "${CURDIR}/external_resources" && \
	rm -rf venv && \
	python3 -m venv venv && \
	. venv/bin/activate && \
	pip install -r requirements.txt

devenv_dashboard:
	cd "${CURDIR}/dashboard" && \
	rm -rf env && \
	python3 -m venv venv && \
	. venv/bin/activate && \
	pip install -r requirements.txt

mongo:
	docker stop mongodb-test || true
	docker run --rm --detach --name=mongodb-test \
		--env MONGO_INITDB_ROOT_USERNAME=admin \
		--env MONGO_INITDB_ROOT_PASSWORD=admin \
		--env MONGO_INITDB_DATABASE=crypto_data \
		--publish 27017:27017 mongo:4
