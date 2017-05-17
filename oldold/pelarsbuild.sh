nvidia-docker run -ti -v ~/pelars/pelars_client:/pelars pelarscompile3 bash
cmake -DCMAKE_PREFIX_PATH=/root/lib/k2 ..



# Buil issues:
# - libfreenect
# - yaml-cpp
# - gst/app include
# - cppnetlib issues with 0.12

# docker-ce
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
sudo apt-add-repository 'deb https://apt.dockerproject.org/repo ubuntu-trusty main'
sudo apt-get update
sudo apt-get install docker-ce

# nvidia-docker
wget -P /tmp https://github.com/NVIDIA/nvidia-docker/releases/download/v1.0.1/nvidia-docker_1.0.1-1_amd64.deb
sudo dpkg -i /tmp/nvidia-docker*.deb && rm /tmp/nvidia-docker*.deb

# Test nvidia-smi
nvidia-docker run --rm nvidia/cuda nvidia-smi
