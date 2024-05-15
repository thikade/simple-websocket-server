# syntax=docker/dockerfile:1
FROM python:3.11-alpine

ENV USER=python UID=12345 GID=12345
ENV HOME /app/env/python

WORKDIR $HOME

RUN <<EOT
    apk add --update --no-cache curl bash openssh git
    rm -rf /var/cache/apk/*
    addgroup --gid "$GID"  "$USER" 
    adduser  --disabled-password --gecos "python user" \
        --home "$HOME" --no-create-home --uid "$UID" --ingroup "$USER"  "$USER"
    mkdir -p $HOME 
    chown -R $USER:$USER $HOME
EOT

USER $UID

COPY --chown=$USER:$USER requirements.txt server.py server_k8s.py $HOME/

RUN  <<EOT sh
    python3 -m venv $HOME 
    $HOME/bin/pip3 -v install -r $HOME/requirements.txt
    chmod -R a+rw $HOME
    find $HOME -type d -exec chmod a+rwx {} \;      # required for Openshift random user ID
EOT

# activate default env; same as "source env/<ENV>/bin/activate"
ENV PATH $HOME/bin:$PATH

CMD [ "python3", "./server.py" ]

# when running in K8s, override the default CMD with the following in your deployment.yaml "command:
# command: [ "python3", "./server_k8s.py" ]