FROM golang:alpine
MAINTAINER "Mohammad Dabour @mdabour"


ENV PACKER_DEV=1
RUN apk add --update sudo


RUN adduser -G wheel -g "Deployer" -s /bin/ash -D deployer \
&&  echo '%wheel ALL=(ALL) NOPASSWD:ALL' >> /etc/sudoers


USER deployer

RUN sudo apk add --update git bash openssl
RUN go get github.com/mitchellh/gox
RUN go get github.com/hashicorp/packer

WORKDIR $GOPATH/src/github.com/hashicorp/packer

RUN /bin/bash scripts/build.sh

#Ansible part credit goes to https://github.com/William-Yeh/docker-ansible/blob/master/alpine3/Dockerfile
RUN echo "===> Installing sudo to emulate normal OS behavior..."  && \
    #sudo apk --update add sudo                                         && \
    \
    \
    echo "===> Adding Python runtime..."  && \
    sudo apk --update add python py-pip openssl ca-certificates  openssh  ospd-netstat && \
    sudo apk --update add --virtual build-dependencies \
                python-dev libffi-dev openssl-dev build-base  && \
    sudo pip install --upgrade pip cffi                            && \
    \
    \
    echo "===> Installing Ansible..."  && \
    sudo pip install ansible                && \
    \
    \
    echo "===> Installing handy tools (not absolutely required)..."  && \
    sudo pip install --upgrade pywinrm                  && \
    sudo apk --update add sshpass openssh-client rsync  && \
    \
    \
    echo "===> Removing package list..."  && \
    sudo apk del build-dependencies            && \
    sudo rm -rf /var/cache/apk/*               && \
    \
    \
    echo "===> Adding hosts for convenience..."  && \
    sudo mkdir -p /etc/ansible                        && \
    echo 'localhost' |sudo tee  /etc/ansible/hosts
RUN rm -rf /etc/ssh/ssh_host_rsa_key /etc/ssh/ssh_host_dsa_key


ARG CLOUD_SDK_VERSION=226.0.0
ENV CLOUD_SDK_VERSION=$CLOUD_SDK_VERSION

RUN sudo apk --no-cache add curl
RUN curl -sSL https://sdk.cloud.google.com | bash
RUN ls -lths /home/deployer/google-cloud-sdk/bin

ENV PATH $PATH:/home/deployer/google-cloud-sdk/bin 
RUN gcloud config set core/disable_usage_reporting true && \
    gcloud config set component_manager/disable_update_check true && \
    gcloud config set metrics/environment github_docker_image
RUN sudo apk add --update --no-cache netcat-openbsd
#ENV PATH $PATH:/usr/local/gcloud/google-cloud-sdk/bin
VOLUME ["/home/deployer/.config"]

COPY  .  /tmp

WORKDIR /home/deployer

CMD [ "ansible-playbook", "--version" ]
