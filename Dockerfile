FROM python:3.9

WORKDIR /plane-notify

# Added needed folder for plane-notify process
RUN mkdir /home/plane-notify

# Set the Chrome repo. apt-key is removed in current Debian releases, so the
# signing key goes into a keyring file referenced via signed-by instead.
RUN apt-get update && apt-get install -y --no-install-recommends gnupg wget \
    && wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | gpg --dearmor -o /usr/share/keyrings/google-chrome.gpg \
    && echo "deb [arch=amd64 signed-by=/usr/share/keyrings/google-chrome.gpg] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list

# Install Chrome.
RUN apt-get update && apt-get -y install --no-install-recommends \
    google-chrome-stable \
    python3-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Add pipenv
RUN pip install pipenv

# Install dependencies
COPY Pipfile* .
RUN pipenv install

COPY . .
CMD pipenv run python /plane-notify/__main__.py
