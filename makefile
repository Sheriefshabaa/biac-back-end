envactive:
	.venv/Scripts/activate
makeenv:
	python -m venv env
clearcache:
	pip cache purge
regeneratefileschema:
	py manage.py spectacular --file schema.yml