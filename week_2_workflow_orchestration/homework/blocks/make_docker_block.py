from prefect.infrastructure.docker import DockerContainer

# alternative to creating DockerContainer block in the UI
docker_block = DockerContainer(
    image="wathon/prefect:web_to_gcs",
    image_pull_policy="ALWAYS",
    auto_remove=True,
)

docker_block.save("web-to-gcs", overwrite=True)
