> WARNING: work in progress

# Current version (`pydantic_v2`)

## Restrictions on task call signatures

### Argument names

Task arguments cannot be named with any of the following reserved names
- `"args"`
- `"kwargs"`
- `"v__args"`
- `"v__kwargs"`
- `"v__duplicate_kwargs"`
- `"v__positional_only"`

### Union types

When top-level task arguments have a union type annotation, we verify that it falls into one of the two supported cases.

> Note that he same check is not currently performed for nested properties of top-level task arguments, but it may be added - ref https://github.com/fractal-analytics-platform/fractal-task-tools/issues/98.

#### Supported case 1: Plain binary unions with `None`

The first supported case is the one of an union of a given type and `None`. If the default is set, it must be `None`. Here are some examples of supported and non-supported type annotations for task arguments:
```python
from pydantic import Field

def task_function_ok(
    arg1: int | None,
    arg2: int | None = None,
    arg3: int | None = Field(default=None),
    arg4: int | None = Field(default_factory=lambda: None),
    arg5: Optional[int],
    arg6: Annotated[int | None, "a comment"],
    arg7: Annotated[int | None, "a comment"] = None,
    arg8: Annotated[int | None, "a comment"] = Field(default=None),
    arg9: int | None = Field(default_factory=lambda _: 7),  # Since the factory requires additional data, it is ignored and the default is not populated.
):
    pass

def task_function_bad(
    arg1: int | str,
    arg2: int | str | None,
    arg3: int | None = 1,
    arg4: int | None = Field(default=1),
    arg5: int | None = Field(default_factory=lambda: 1),
):
    pass
```

#### Supported case 2: Tagged unions

The second supported case is the one of a _tagged_ union, see e.g. https://docs.pydantic.dev/latest/concepts/unions/#discriminated-unions-with-str-discriminators.

Here is a supported example:
```python
from typing import Literal
from typing import Annotated

class Model1(BaseModel):
    label: Literal["label1"] = "label1"
    field1: int = 1


class Model2(BaseModel):
    label: Literal["label2"] = "label2"
    field1: int
    field2: str

MyTaggedUnion = Annotated[Model1 | Model2, Field(discriminator="label")]

def task_function_ok(
    arg1: MyTaggedUnion,
):
    pass

```


## Customizations of generated JSON Schemas

The following customizations apply at all levels, that is, both for top-level task arguments and for nested properties.

1. When the generated schema includes an `anyOf` array, we remove any `{"type": "null"}` element from it.
2. When the generated schema includes a `default` value which is set to `null`, we remove it.
3. The the type annotation is a `Field` with a `default_factory` which is set and which does not require any argument, we compute the `default` value as `default_factory()`.
