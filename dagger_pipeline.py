import dagger
import asyncio

async def deploy():
    async with dagger.Connection() as client:
        # Építés és pusholás GitHub Container Registry-be
        image_ref = await (
            client.container()
            .from_("python:3.9")
            .with_workdir("/app")
            .with_mounted_directory("/app", client.host().directory("."))
            .with_exec(["pip", "install", "-r", "requirements.txt"])
            .with_exec(["python", "main.py"])
            .publish("ghcr.io/myrepo/dagger-demo:latest")
        )

        print(f"Image pushed to: {image_ref}")

        # Kubernetes deployment frissítése
        deploy_result = await (
            client.container()
            .from_("bitnami/kubectl:latest")
            .with_mounted_file("/root/.kube/config", client.host().file("~/.kube/config"))
            .with_exec(["kubectl", "apply", "-f", "k8s/deployment.yaml"])
            .stdout()
        )

        print(deploy_result)

asyncio.run(deploy())