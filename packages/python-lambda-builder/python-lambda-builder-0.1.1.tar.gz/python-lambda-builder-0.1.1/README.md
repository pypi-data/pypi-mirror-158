# Python Lambda Builder
This library is a CLI tool to solve the problem of 
building together a python project and its dependencies for lambda 
deployment. This command with could be integrated into pipeline 
for deployment.

## Usage
For poetry (pyproject.toml):
```shell
python_lambda_builder --func-src src/ --build_dest dist/
```

For pip (requirements.txt):
```shell
python_lambda_builder --func-src src/ --build_dest dist/ --manager pip
```

Other arguments you can pass include:
- `pyproject_path`: (defaults to `./pyproject.toml`) This can be the relative or absolute 
path to the pyproject.toml file.
- `requirements_path`: (defaults to `./requirements.txt`) This can be the relative or absolute 
path to the requirements.txt file.