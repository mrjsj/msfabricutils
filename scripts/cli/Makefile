

gen:
	cd ../../ && python scripts/cli/generate_cli.py
	cd ../../ && ruff check --fix cli/commands
	cd ../../ && ruff format cli/commands
	cd ../../ && python cli/main.py --help
	cd ../../ && python scripts/cli/validate_fabric_client_call.py


# gen:
# 	python scripts/cli/generate_commands.py
# 	ruff check --fix --exclude src/msfabricutils/etl
# 	ruff format

# gen-all:
# 	python scripts/cli/generate_commands.py
# 	ruff check --fix --exclude src/msfabricutils/etl
# 	ruff format
# 	mkdocs build