from prefect.deployments import Deployment
from prefect.infrastructure.docker import DockerContainer
from parameterized_etl_web_to_gcs import etl_web_to_gcs_parent_flow

docker_block = DockerContainer.load("web-to-gcs")

docker_deploy = Deployment.build_from_flow(
    flow=etl_web_to_gcs_parent_flow,
    name='docker-etl-web-to-gcs-flow',
    infrastructure=docker_block
)

if __name__ == "__main__":
    docker_deploy.apply()
