#https://github.com/luxonis/depthai-ros
sudo docker run -it --network host --gpus all --ipc=host --privileged \
    -e DISPLAY=$DISPLAY -v $(pwd):/ws/src -v /tmp/.X11-unix:/tmp/.X11-unix \
    --name oakd_check ros:humble-ros-base

