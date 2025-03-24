from typing import Any
from typing import Literal
from typing import Optional

from pydantic import BaseModel
from pydantic import ConfigDict
from pydantic import Field


class _BaseTask(BaseModel):
    model_config = ConfigDict(extra="forbid", arbitrary_types_allowed=True)

    name: str
    executable: str
    meta: Optional[dict[str, Any]] = None
    input_types: Optional[dict[str, bool]] = None
    output_types: Optional[dict[str, bool]] = None
    category: Optional[str] = None
    modality: Optional[str] = None
    tags: list[str] = Field(default_factory=list)
    docs_info: Optional[str] = None
    type: str

    @property
    def executable_non_parallel(self) -> str:
        raise NotImplementedError()

    @property
    def meta_non_parallel(self) -> Optional[dict[str, Any]]:
        raise NotImplementedError()

    @property
    def executable_parallel(self) -> str:
        raise NotImplementedError()

    @property
    def meta_parallel(self) -> Optional[dict[str, Any]]:
        raise NotImplementedError()


class CompoundTask(_BaseTask):
    """
    A `CompoundTask` object must include both `executable_init` and
    `executable` attributes, and it may include the `meta_init` and `meta`
    attributes.
    """

    executable_init: str
    meta_init: Optional[dict[str, Any]] = None
    type: Literal["compound"] = "compound"

    @property
    def executable_non_parallel(self) -> str:
        return self.executable_init

    @property
    def meta_non_parallel(self) -> Optional[dict[str, Any]]:
        return self.meta_init

    @property
    def executable_parallel(self) -> str:
        return self.executable

    @property
    def meta_parallel(self) -> Optional[dict[str, Any]]:
        return self.meta


class ConverterCompoundTask(_BaseTask):
    """
    A `ConverterCompoundTask` task is the same as a `CompoundTask`, but it
    is executed differently in the Fractal backend.
    """

    executable_init: str
    meta_init: Optional[dict[str, Any]] = None
    type: Literal["converter_compound"] = "converter_compound"

    @property
    def executable_non_parallel(self) -> str:
        return self.executable_init

    @property
    def meta_non_parallel(self) -> Optional[dict[str, Any]]:
        return self.meta_init

    @property
    def executable_parallel(self) -> str:
        return self.executable

    @property
    def meta_parallel(self) -> Optional[dict[str, Any]]:
        return self.meta


class NonParallelTask(_BaseTask):
    """
    A `NonParallelTask` object must include the `executable` attribute, and it
    may include the `meta` attribute.
    """

    type: Literal["non_parallel"] = "non_parallel"

    @property
    def executable_non_parallel(self) -> str:
        return self.executable

    @property
    def meta_non_parallel(self) -> Optional[dict[str, Any]]:
        return self.meta

    @property
    def executable_parallel(self) -> None:
        return None

    @property
    def meta_parallel(self) -> None:
        return None


class ConverterNonParallelTask(_BaseTask):
    """
    A `ConverterNonParallelTask` task is the same as a `NonParallelTask`, but
    it is executed differently in the Fractal backend.
    """

    type: Literal["converter_non_parallel"] = "converter_non_parallel"

    @property
    def executable_non_parallel(self) -> str:
        return self.executable

    @property
    def meta_non_parallel(self) -> Optional[dict[str, Any]]:
        return self.meta

    @property
    def executable_parallel(self) -> None:
        return None

    @property
    def meta_parallel(self) -> None:
        return None


class ParallelTask(_BaseTask):
    """
    A `ParallelTask` object must include the `executable` attribute, and it may
    include the `meta` attribute.
    """

    type: Literal["parallel"] = "parallel"

    @property
    def executable_non_parallel(self) -> None:
        return None

    @property
    def meta_non_parallel(self) -> None:
        return None

    @property
    def executable_parallel(self) -> str:
        return self.executable

    @property
    def meta_parallel(self) -> Optional[dict[str, Any]]:
        return self.meta
