# Deployment instructions
To run the repository in a devcontainer, open in VsCode, CTRL+ALT+P > Dev Containers -> Reopen in Container.

The container will build and launch. The code is run as if it was actually running on a linux machine (emulating the Raspberry Pi), so the repositories are installed directly on the machine.
Any edits to the repository inside the container happen in the actual repository, so git etc works as normally.

Note - the current image is running an AMD64 processer instead of an ARM64 (or ARM v8) which is what the Raspberry PI OS 64 bit is running, so we should find another base image to more accurately represent the runtime of the gateway.

Note2: Running the dev container with MQTT requires that it is deployed in the same docker network as the RabbitMQ container. This is configured with the runArgs parameter in the devcontainer.json file.