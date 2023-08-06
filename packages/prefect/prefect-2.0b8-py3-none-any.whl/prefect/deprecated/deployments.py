import abc
import pathlib
import sys
import warnings
from os.path import abspath
from typing import TYPE_CHECKING, Any, Dict, List, Optional, Union
from uuid import UUID

import fsspec
from pydantic import BaseModel, Field, PrivateAttr, validator

from prefect.blocks.core import Block
from prefect.blocks.storage import LocalStorageBlock, StorageBlock, TempStorageBlock
from prefect.client import OrionClient, inject_client
from prefect.context import PrefectObjectRegistry
from prefect.exceptions import (
    DeploymentValidationError,
    MissingFlowError,
    ObjectAlreadyExists,
)
from prefect.flow_runners import SubprocessFlowRunner
from prefect.flow_runners.base import (
    FlowRunner,
    FlowRunnerSettings,
    UniversalFlowRunner,
)
from prefect.flows import Flow, load_flow_from_script
from prefect.orion.schemas.actions import DeploymentCreate
from prefect.orion.schemas.core import raise_on_invalid_name
from prefect.orion.schemas.data import DataDocument
from prefect.orion.schemas.schedules import SCHEDULE_TYPES
from prefect.orion.utilities.schemas import PrefectBaseModel
from prefect.utilities.asyncio import sync_compatible
from prefect.utilities.filesystem import is_local_path

if TYPE_CHECKING:
    from prefect.deployments import DeploymentSpec


class ScriptPackager(BaseModel):
    """
    Pushes the source code for your flow to a remote path.

    This script will be executed again at runtime to retrieve your flow object.

    If a storage block is not provided, the default storage will be retrieved from
    the API. If no default storage is configured, you must provide a storage block to
    use non-local flow runners.

    Args:
        storage: A [prefect.blocks.storage](/api-ref/prefect/blocks/storage/) instance
            providing the [storage](/concepts/storage/) to be used for the flow
            definition and results.
    """

    __dispatch_key__ = "deprecated:script"

    storage: Optional[Union[StorageBlock, UUID]] = None

    @sync_compatible
    @inject_client
    async def check_compat(self, deployment: "DeploymentSpec", client: OrionClient):
        # Determine the storage block

        # TODO: Some of these checks may be retained in the future, but will use block
        # capabilities instead of types to check for compatibility with flow runners

        if self.storage is None:
            default_block_document = await client.get_default_storage_block_document()
            if default_block_document:
                self.storage = Block._from_block_document(default_block_document)
        no_storage_message = "You have not configured default storage on the server or set a storage to use for this deployment"

        if isinstance(self.storage, UUID):
            storage_block_document = await client.read_block_document(self.storage)
            self.storage = Block._from_block_document(storage_block_document)

        if isinstance(deployment.flow_runner, SubprocessFlowRunner):
            local_machine_message = (
                "this deployment will only be usable from the current machine."
            )
            if not self.storage:
                warnings.warn(f"{no_storage_message}, {local_machine_message}")
                self.storage = LocalStorageBlock()
            elif isinstance(self.storage, (LocalStorageBlock, TempStorageBlock)):
                warnings.warn(
                    f"You have configured local storage, {local_machine_message}."
                )
        else:
            # All other flow runners require remote storage, ensure we've been given one
            flow_runner_message = f"this deployment is using a {deployment.flow_runner.typename.capitalize()} flow runner which requires remote storage"
            if not self.storage:
                raise DeploymentValidationError(
                    f"{no_storage_message} but {flow_runner_message}.",
                    deployment,
                )
            elif isinstance(self.storage, (LocalStorageBlock, TempStorageBlock)):
                raise DeploymentValidationError(
                    f"You have configured local storage but {flow_runner_message}.",
                    deployment,
                )

    @inject_client
    async def package(
        self, deployment: "DeploymentSpec", client: OrionClient
    ) -> DeploymentCreate:
        """
        Build the specification.

        Returns a schema that can be used to register the deployment with the API.
        """
        flow_id = await client.create_flow(deployment.flow)

        # Read the flow file
        with fsspec.open(deployment.flow_location, "rb") as flow_file:
            flow_bytes = flow_file.read()

        # Ensure the storage is a registered block for later retrieval

        if not self.storage._block_document_id:
            block_schema = await client.read_block_schema_by_checksum(
                self.storage._calculate_schema_checksum()
            )

            i = 0
            while not self.storage._block_document_id:
                try:
                    block_document = await client.create_block_document(
                        block_document=self.storage._to_block_document(
                            name=f"{deployment.flow_name}-{deployment.name}-{deployment.flow.version}-{i}",
                            block_schema_id=block_schema.id,
                            block_type_id=block_schema.block_type_id,
                        )
                    )
                    self.storage._block_document_id = block_document.id
                except ObjectAlreadyExists:
                    i += 1

        # Write the flow to storage
        storage_token = await self.storage.write(flow_bytes)
        flow_data = DataDocument.encode(
            encoding="blockstorage",
            data={
                "data": storage_token,
                "block_document_id": self.storage._block_document_id,
            },
        )

        return DeploymentCreate(
            flow_id=flow_id,
            name=deployment.name,
            schedule=deployment.schedule,
            flow_data=flow_data,
            parameters=deployment.parameters,
            tags=deployment.tags,
            flow_runner=deployment.flow_runner.to_settings(),
        )


class DeploymentSpec(PrefectBaseModel, abc.ABC):
    """
    A type for specifying a deployment of a flow.

    The flow object or flow location must be provided. If a flow object is not provided,
    `load_flow` must be called to load the flow from the given flow location.

    Args:
        name: The name of the deployment
        flow: The flow object to associate with the deployment
        flow_location: The path to a script containing the flow to associate with the
            deployment. Inferred from `flow` if provided.
        flow_name: The name of the flow to associated with the deployment. Only required
            if loading the flow from a `flow_location` with multiple flows. Inferred
            from `flow` if provided.
        flow_runner: The [flow runner](/api-ref/prefect/flow-runners/) to be used for
            flow runs.
        parameters: An optional dictionary of default parameters to set on flow runs
            from this deployment. If defined in Python, the values should be Pydantic
            compatible objects.
        schedule: An optional schedule instance to use with the deployment.
        tags: An optional set of tags to assign to the deployment.
        flow_storage: A [prefect.blocks.storage](/api-ref/prefect/blocks/storage/) instance
            providing the [storage](/concepts/storage/) to be used for the flow
            definition and results.
    """

    name: str = None
    flow: Flow = None
    flow_name: str = None
    flow_location: str = None
    parameters: Dict[str, Any] = Field(default_factory=dict)
    schedule: SCHEDULE_TYPES = None
    tags: List[str] = Field(default_factory=list)
    flow_runner: Union[FlowRunner, FlowRunnerSettings] = None
    flow_storage: Optional[Union[StorageBlock, UUID]] = None

    # Meta types
    _validated: bool = PrivateAttr(False)
    _source: Dict = PrivateAttr()

    # Hide the `_packager` which is a new interface
    _packager: ScriptPackager = PrivateAttr()

    def __init__(self, **data: Any) -> None:
        warnings.warn(
            "`DeploymentSpec` has been replaced by `Deployment`. Please use the new "
            "`prefect.Deployment` object instead. Note, that the interface for "
            "specifying a flow script and flow storage has changed. `DeploymentSpec` "
            "will be removed in a future release.",
            DeprecationWarning,
            stacklevel=2,
        )
        super().__init__(**data)

        # After initialization; register this deployment specification.

        # Detect the definition location for reporting validation failures
        # Walk up one frame to the user's declaration
        frame = sys._getframe().f_back

        self._source = {
            "file": frame.f_globals["__file__"],
            "line": frame.f_lineno,
        }

        _register_spec(self)

    @validator("name")
    def validate_name_characters(cls, v):
        raise_on_invalid_name(v)
        return v

    @validator("flow_location", pre=True)
    def ensure_paths_are_absolute_strings(cls, value):
        if isinstance(value, pathlib.Path):
            return str(value.absolute())
        elif isinstance(value, str) and is_local_path(value):
            return abspath(value)
        return value

    @sync_compatible
    @inject_client
    async def validate(self, client: OrionClient):
        # Ensure either flow location or flow were provided

        if not self.flow_location and not self.flow:
            raise DeploymentValidationError(
                "Either `flow_location` or `flow` must be provided.", self
            )

        # Load the flow from the flow location

        if self.flow_location and not self.flow:
            try:
                self.flow = load_flow_from_script(self.flow_location, self.flow_name)
            except MissingFlowError as exc:
                raise DeploymentValidationError(str(exc), self) from exc

        # Infer the flow location from the flow

        elif self.flow and not self.flow_location:
            self.flow_location = self.flow.fn.__globals__.get("__file__")

        # Ensure the flow location matches the flow both are given

        elif self.flow and self.flow_location and is_local_path(self.flow_location):
            flow_file = self.flow.fn.__globals__.get("__file__")
            if flow_file:
                abs_given = abspath(str(self.flow_location))
                abs_flow = abspath(str(flow_file))
                if abs_given != abs_flow:
                    raise DeploymentValidationError(
                        f"The given flow location {abs_given!r} does not "
                        f"match the path of the given flow: '{abs_flow}'.",
                        self,
                    )

        # Ensure the flow location is absolute if local

        if self.flow_location and is_local_path(self.flow_location):
            self.flow_location = abspath(str(self.flow_location))

        # Ensure the flow location is set

        if not self.flow_location:
            raise DeploymentValidationError(
                "Failed to determine the location of your flow. "
                "Provide the path to your flow code with `flow_location`.",
                self,
            )

        # Infer flow name from flow

        if self.flow and not self.flow_name:
            self.flow_name = self.flow.name

        # Ensure a given flow name matches the given flow's name

        elif self.flow.name != self.flow_name:
            raise DeploymentValidationError(
                "`flow.name` and `flow_name` must match. "
                f"Got {self.flow.name!r} and {self.flow_name!r}.",
                self,
            )

        # Default the deployment name to the flow name

        if not self.name and self.flow_name:
            self.name = self.flow_name

        # Default the flow runner to the universal flow runner

        self.flow_runner = self.flow_runner or UniversalFlowRunner()

        # Convert flow runner settings to concrete instances

        if isinstance(self.flow_runner, FlowRunnerSettings):
            self.flow_runner = FlowRunner.from_settings(self.flow_runner)

        # Do not allow the abstract flow runner type

        if type(self.flow_runner) is FlowRunner:
            raise DeploymentValidationError(
                "The base `FlowRunner` type cannot be used. Provide a flow runner "
                "implementation or flow runner settings instead.",
                self,
            )

        # Check packaging compatibility

        self._packager = ScriptPackager(storage=self.flow_storage)
        await self._packager.check_compat(self, client=client)

        self._validated = True

    @sync_compatible
    @inject_client
    async def create(self, client: OrionClient) -> UUID:
        """
        Create a deployment from the current specification.

        Deployments with the same name will be replaced.

        Returns the ID of the deployment.
        """
        await self.validate()
        schema = await self._packager.package(self, client=client)
        return await client._create_deployment_from_schema(schema)

    class Config:
        arbitrary_types_allowed = True

    @classmethod
    def __get_validators__(cls):
        # Allow us to use the 'validate' name while retaining pydantic's validator
        for validator in super().__get_validators__():
            if validator == cls.validate:
                yield super().validate
            else:
                yield validator


def deployment_specs_from_script(path: str) -> List[DeploymentSpec]:
    from prefect.context import registry_from_script

    return registry_from_script(path).get_instances(DeploymentSpec)


def deployment_specs_from_yaml(path: str) -> List[DeploymentSpec]:
    from prefect.deployments import load_deployments_from_yaml

    return load_deployments_from_yaml(path).get_instances(DeploymentSpec)


def _register_spec(spec: DeploymentSpec) -> None:
    """
    Collect the `DeploymentSpec` object on the
    PrefectObjectRegistry.deployment_specs dictionary. If multiple specs with
    the same name are created, the last will be used.

    This is convenient for `deployment_specs_from_script` which can collect
    deployment declarations without requiring them to be assigned to a global
    variable.

    """
    registry = PrefectObjectRegistry.get()
    registry.register_instance(spec)
