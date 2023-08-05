# Bin generator

This repo can now be installed with pip:
```bash
pip install git+https://gitlab.com/six-two/bin_generator
```

## Example usage

You can see some example data in the `example` folder of the source code repository.
To try them out, use the following command:

```bash
src/bin-generator example/bins.yaml --data example/data.yaml
```

## Known issues

- Interrupting the script will delete the remaining files
