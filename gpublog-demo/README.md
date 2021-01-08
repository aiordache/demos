### DEMO GPU support in Docker Compose

`model_generator.py` contains sample code from the Tensorflow docs at https://www.tensorflow.org/tutorials/text/nmt_with_attention

When deploying on a host without an Nvidia GPU device, remove the `deploy` section from the Compose file, otherwise `docker-compose` will request the allocation of a GPU which will fail if the host does not have one.

If no GPU is detected, the tensorflow framework will default to CPU. Training may take very long in this case.
