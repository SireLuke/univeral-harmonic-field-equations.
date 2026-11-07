# Branch A reference implementation

A dependency-free Python reference implementation of the ideal fixed-end string model.

## Run tests

From the repository root:

```sh
python -m unittest discover -s tests -v
```

Requires Python 3.10+ (standard library only). No V8, UHFE/UDFE, Fermi, E₈, or external numerical package is required.

The implementation uses SI units for string parameters and keeps the dimensionless barbershop scaling function independent of the physical string calculation.
