# validate-generated-files

A GitHub Action to validate generated files stored in a repository.

This is typically useful in contexts where, for one reason or another, generated
files are stored in a version control repository alongside their inputs.

This Action is implemented in Python 3, which must be available within the
runner environment.

## Usage

```yaml
steps:
  - uses: PeterJCLaw/validate-generated-files
    with:
      command: pip-compile
      files: requirements.txt
```
