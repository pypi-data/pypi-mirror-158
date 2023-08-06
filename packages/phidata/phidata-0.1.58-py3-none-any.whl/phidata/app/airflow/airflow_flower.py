from pathlib import Path
from typing import Optional, Dict, Any, List, Union
from typing_extensions import Literal

from phidata.app.db import DbApp
from phidata.infra.k8s.create.core.v1.service import ServiceType
from phidata.infra.k8s.enums.image_pull_policy import ImagePullPolicy
from phidata.infra.k8s.enums.restart_policy import RestartPolicy
from phidata.app.airflow.airflow_base import AirflowBase, AirflowBaseArgs
from phidata.utils.log import logger


class AirflowFlower(AirflowBase):
    def __init__(
        self,
        name: str = "airflow-flower",
        version: str = "1",
        enabled: bool = True,
        # Image args,
        image_name: str = "phidata/airflow",
        image_tag: str = "2.3.2",
        entrypoint: Optional[Union[str, List]] = None,
        command: Optional[str] = "flower",
        # Mount the workspace directory on the container,
        mount_workspace: bool = True,
        workspace_volume_name: str = "airflow-flower-ws-volume",
        # Path to mount the workspace volume under,
        # This is the parent directory for the workspace on the container,
        # i.e. the ws is mounted as a subdir in this dir,
        # eg: if ws name is: idata, workspace_dir would be: /usr/local/workspaces/idata,
        workspace_parent_container_path: str = "/usr/local/workspaces",
        # NOTE: On DockerContainers the workspace_root_path is mounted to workspace_dir,
        # because we assume that DockerContainers are running locally on the user's machine,
        # On K8sContainers, we load the workspace_dir from git using a git-sync sidecar container,
        create_git_sync_sidecar: bool = True,
        git_sync_repo: Optional[str] = None,
        git_sync_branch: Optional[str] = None,
        git_sync_wait: int = 1,
        # But when running k8s locally, we can mount the workspace using
        # host path as well.
        k8s_mount_local_workspace=False,
        # Install python dependencies using a requirements.txt file,
        install_requirements: bool = False,
        # Path to the requirements.txt file relative to the workspace_root
        requirements_file_path: str = "requirements.txt",
        # Mount aws config on the container,
        # Only on DockerContainers, for K8sContainers use IamRole,
        mount_aws_config: bool = False,
        # Aws config dir on the host,
        aws_config_path: Path = Path.home().resolve().joinpath(".aws"),
        # Aws config dir on the container,
        aws_config_container_path: str = "/root/.aws",
        # Configure airflow,
        # The AIRFLOW_ENV defines the current airflow runtime and can be used by DAGs to separate dev vs prd code
        airflow_env: Literal["dev", "stg", "prd"] = "dev",
        # If use_products_as_airflow_dags = True,
        # set the AIRFLOW__CORE__DAGS_FOLDER to the products_dir,
        use_products_as_airflow_dags: bool = True,
        # If use_products_as_airflow_dags = False,
        # set the AIRFLOW__CORE__DAGS_FOLDER to the airflow_dags_path,
        # airflow_dags_path is the directory in the container containing the airflow dags,
        airflow_dags_path: Optional[str] = None,
        # Creates an airflow admin with username: admin, pass: admin,
        create_airflow_admin_user: bool = False,
        executor: Literal[
            "DebugExecutor",
            "LocalExecutor",
            "SequentialExecutor",
            "CeleryExecutor",
            "CeleryKubernetesExecutor",
            "DaskExecutor",
            "KubernetesExecutor",
        ] = "SequentialExecutor",
        # Configure airflow db,
        # If init_airflow_db = True, initialize the airflow_db,
        init_airflow_db: bool = False,
        wait_for_db: bool = True,
        # delay start by 60 seconds for the db to be initialized
        wait_for_db_init: bool = False,
        # Connect to database using a DbApp
        db_app: Optional[DbApp] = None,
        # Connect to database manually
        # db_user can be provided here or as the
        # DATABASE_USER env var in the secrets_file
        db_user: Optional[str] = None,
        # db_password can be provided here or as the
        # DATABASE_USER env var in the secrets_file
        db_password: Optional[str] = None,
        # db_schema can be provided here or as the
        # DATABASE_DB env var in the secrets_file
        db_schema: Optional[str] = None,
        # db_host can be provided here or as the
        # DATABASE_HOST env var in the secrets_file
        db_host: Optional[str] = None,
        # db_port can be provided here or as the
        # DATABASE_PORT env var in the secrets_file
        db_port: Optional[int] = None,
        # db_driver can be provided here or as the
        # DATABASE_DRIVER env var in the secrets_file
        db_driver: str = "postgresql+psycopg2",
        db_result_backend_driver: str = "db+postgresql",
        # Airflow db connections in the format { conn_id: conn_url },
        # converted to env var: AIRFLOW_CONN__conn_id = conn_url,
        db_connections: Optional[Dict] = None,
        # Configure airflow redis,
        wait_for_redis: bool = False,
        # Connect to redis using a PhidataApp
        redis_app: Optional[Any] = None,
        # Connect to redis manually
        # redis_password can be provided here or as the
        # REDIS_PASSWORD env var in the secrets_file
        redis_password: Optional[str] = None,
        # redis_schema can be provided here or as the
        # REDIS_SCHEMA env var in the secrets_file
        redis_schema: Optional[str] = None,
        # redis_host can be provided here or as the
        # REDIS_HOST env var in the secrets_file
        redis_host: Optional[str] = None,
        # redis_port can be provided here, or as the
        # REDIS_PORT env var in the secrets_file
        redis_port: Optional[int] = None,
        # redis_driver can be provided here or as the
        # REDIS_DRIVER env var in the secrets_file
        redis_driver: str = "rediss",
        # Configure the container,
        container_name: Optional[str] = None,
        image_pull_policy: ImagePullPolicy = ImagePullPolicy.IF_NOT_PRESENT,
        container_detach: bool = True,
        container_auto_remove: bool = True,
        container_remove: bool = True,
        # Overwrite the PYTHONPATH env var, which is usually set to the workspace_root_container_path
        python_path: Optional[str] = None,
        # Add container labels
        container_labels: Optional[Dict[str, Any]] = None,
        # NOTE: Available only for Docker
        # container_volumes is a dictionary which adds the volumes to mount
        # inside the container. The key is either the host path or a volume name,
        # and the value is a dictionary with 2 keys:
        #   bind - The path to mount the volume inside the container
        #   mode - Either rw to mount the volume read/write, or ro to mount it read-only.
        # For example:
        # {
        #   '/home/user1/': {'bind': '/mnt/vol2', 'mode': 'rw'},
        #   '/var/www': {'bind': '/mnt/vol1', 'mode': 'ro'}
        # }
        container_volumes: Optional[Dict[str, dict]] = None,
        # Open the flower port if open_flower_port=True
        open_flower_port: bool = True,
        # Flower port number on the container
        flower_port: int = 5555,
        # Only used by the K8sContainer
        flower_port_name: str = "flower",
        # Only used by the DockerContainer
        flower_host_port: int = 5555,
        # Add env variables to container env,
        env: Optional[Dict[str, str]] = None,
        # Read env variables from a file in yaml format,
        env_file: Optional[Path] = None,
        # Configure the ConfigMap used for env variables that are not Secret,
        config_map_name: Optional[str] = None,
        # Configure the Secret used for env variables that are Secret,
        secret_name: Optional[str] = None,
        # Read secrets from a file in yaml format,
        secrets_file: Optional[Path] = None,
        # Configure the deployment,
        deploy_name: Optional[str] = None,
        pod_name: Optional[str] = None,
        replicas: int = 1,
        pod_node_selector: Optional[Dict[str, str]] = None,
        restart_policy: RestartPolicy = RestartPolicy.ALWAYS,
        termination_grace_period_seconds: Optional[int] = None,
        # Add deployment labels
        deploy_labels: Optional[Dict[str, Any]] = None,
        # Determine how to spread the deployment across a topology
        # Key to spread the pods across
        topology_spread_key: Optional[str] = None,
        # The degree to which pods may be unevenly distributed
        topology_spread_max_skew: Optional[int] = None,
        # How to deal with a pod if it doesn't satisfy the spread constraint.
        topology_spread_when_unsatisfiable: Optional[
            Literal["DoNotSchedule", "ScheduleAnyway"]
        ] = None,
        # Configure the flower service
        create_flower_service: bool = True,
        flower_service_name: Optional[str] = None,
        flower_service_type: Optional[ServiceType] = None,
        # The port that will be exposed by the service.
        flower_service_port: int = 5555,
        # The flower_target_port is the port to access on the pods targeted by the service.
        # It can be the port number or port name on the pod.
        flower_target_port: Optional[Union[str, int]] = None,
        # Add labels to flower service
        flower_service_labels: Optional[Dict[str, Any]] = None,
        # Configure rbac
        sa_name: Optional[str] = None,
        cr_name: Optional[str] = None,
        crb_name: Optional[str] = None,
        # Other args
        load_examples: bool = False,
        print_env_on_load: bool = True,
        # Additional args
        # If True, use cached resources
        # i.e. skip resource creation/deletion if active resources with the same name exist.
        use_cache: bool = True,
    ):
        super().__init__(
            name=name,
            version=version,
            enabled=enabled,
            image_name=image_name,
            image_tag=image_tag,
            entrypoint=entrypoint,
            command=command,
            mount_workspace=mount_workspace,
            workspace_volume_name=workspace_volume_name,
            workspace_parent_container_path=workspace_parent_container_path,
            create_git_sync_sidecar=create_git_sync_sidecar,
            git_sync_repo=git_sync_repo,
            git_sync_branch=git_sync_branch,
            git_sync_wait=git_sync_wait,
            k8s_mount_local_workspace=k8s_mount_local_workspace,
            install_requirements=install_requirements,
            requirements_file_path=requirements_file_path,
            mount_aws_config=mount_aws_config,
            aws_config_path=aws_config_path,
            aws_config_container_path=aws_config_container_path,
            airflow_env=airflow_env,
            use_products_as_airflow_dags=use_products_as_airflow_dags,
            airflow_dags_path=airflow_dags_path,
            create_airflow_admin_user=create_airflow_admin_user,
            executor=executor,
            init_airflow_db=init_airflow_db,
            wait_for_db=wait_for_db,
            wait_for_db_init=wait_for_db_init,
            db_app=db_app,
            db_user=db_user,
            db_password=db_password,
            db_schema=db_schema,
            db_host=db_host,
            db_port=db_port,
            db_driver=db_driver,
            db_result_backend_driver=db_result_backend_driver,
            db_connections=db_connections,
            wait_for_redis=wait_for_redis,
            redis_app=redis_app,
            redis_password=redis_password,
            redis_schema=redis_schema,
            redis_host=redis_host,
            redis_port=redis_port,
            redis_driver=redis_driver,
            container_name=container_name,
            image_pull_policy=image_pull_policy,
            container_detach=container_detach,
            container_auto_remove=container_auto_remove,
            container_remove=container_remove,
            python_path=python_path,
            container_labels=container_labels,
            container_volumes=container_volumes,
            open_flower_port=open_flower_port,
            flower_port=flower_port,
            flower_port_name=flower_port_name,
            flower_host_port=flower_host_port,
            env=env,
            env_file=env_file,
            config_map_name=config_map_name,
            secret_name=secret_name,
            secrets_file=secrets_file,
            deploy_name=deploy_name,
            pod_name=pod_name,
            replicas=replicas,
            pod_node_selector=pod_node_selector,
            restart_policy=restart_policy,
            termination_grace_period_seconds=termination_grace_period_seconds,
            deploy_labels=deploy_labels,
            topology_spread_key=topology_spread_key,
            topology_spread_max_skew=topology_spread_max_skew,
            topology_spread_when_unsatisfiable=topology_spread_when_unsatisfiable,
            create_flower_service=create_flower_service,
            flower_service_name=flower_service_name,
            flower_service_type=flower_service_type,
            flower_service_port=flower_service_port,
            flower_target_port=flower_target_port,
            flower_service_labels=flower_service_labels,
            sa_name=sa_name,
            cr_name=cr_name,
            crb_name=crb_name,
            load_examples=load_examples,
            print_env_on_load=print_env_on_load,
            use_cache=use_cache,
        )
