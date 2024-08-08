envactive:
	.venv/Scripts/activate
makeenv:
	python -m venv env
clearcache:
	pip cache purge