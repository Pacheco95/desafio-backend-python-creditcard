.PHONY: $(MAKECMDGOALS)

clean:
	@find . -name "*.pyc" | xargs rm -rf
	@find . -name "*.pyo" | xargs rm -rf
	@find . -name "*.log" | xargs rm -rf
	@find . -name "__pycache__" -type d | xargs rm -rf
	@find . -name ".pytest_cache" -type d | xargs rm -rf
	@rm -f .coverage*
	@rm -rf htmlcov/
	@rm -f coverage.xml
	@rm -f *.log

test:
	coverage run -m pytest && coverage report -m

test-quick:
	coverage run -m pytest -v -m "not slow" && coverage report -m

api:
	uvicorn app.main:app --host 0.0.0.0 --port 8000
