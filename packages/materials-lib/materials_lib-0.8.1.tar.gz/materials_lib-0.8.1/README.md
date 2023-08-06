# Materials_Lib - General Materials Python Library

This repo is intended to store the physical properties of materials used throughout coding projects. In case you want to define a new material, create a new toml file by duplicating the `template.toml` file.

## Documentation

(Under construction)

## Using Units
It is common to need to use physical units. It is recommended to use the [`pint`](https://pypi.org/project/Pint/). You can add a `pint.UnitRegistry()` as an argument when instancing the `Material` class. The class will then use the same units as the rest of the project.