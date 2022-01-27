# Usually you do not have to specify amd64
# but on a M1 you do if you want to use packages
# that are not optimized for arm64
FROM --platform=amd64 python:3.9.10-slim-bullseye

SHELL ["/bin/bash", "--login", "-c"]

ENV DEBIAN_FRONTEND noninteractive
ENV LANG C.UTF-8

RUN useradd -m veracodesca

RUN apt-get update && apt-get install -y --no-install-recommends \
		ca-certificates \
		netbase \
        curl \
        git \
        bash-completion \
	&& rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir --quiet --upgrade pip && \
    pip install --no-cache-dir --quiet --upgrade setuptools && \
    pip install --no-cache-dir --quiet pytest && \
    pip install --no-cache-dir --quiet black && \
    pip install --no-cache-dir --quiet flake8

USER veracodesca
WORKDIR /home/veracodesca
ENV NODE_VERSION 16.13.0

RUN curl --silent -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.1/install.sh | bash

# nvm
RUN echo 'export NVM_DIR="$HOME/.nvm"'                                       >> "$HOME/.bashrc"
RUN echo '[ -s "$NVM_DIR/nvm.sh" ] && . "$NVM_DIR/nvm.sh"  # This loads nvm' >> "$HOME/.bashrc"
RUN echo '[ -s "$NVM_DIR/bash_completion" ] && . "$NVM_DIR/bash_completion" # This loads nvm bash_completion' >> "$HOME/.bashrc"

RUN nvm install $NODE_VERSION

ENV NODE_PATH $NVM_DIR/versions/node/v$NODE_VERSION/lib/node_modules
ENV PATH $NVM_DIR/versions/node/v$NODE_VERSION/bin:$PATH

# Install VeracodeSCA Packages
COPY --chown=veracodesca:veracodesca . /home/veracodesca/VeracodeCommunitySCA/
RUN cd VeracodeCommunitySCA/buildAndReleaseTask && npm install
RUN cd VeracodeCommunitySCA && pip install --no-cache-dir --quiet -r requirements.txt

CMD [ "bash" ]