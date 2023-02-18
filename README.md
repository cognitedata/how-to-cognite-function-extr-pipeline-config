## Cognite function template


[Using Cognite Functions](https://docs.cognite.com/cdf/functions/)

# Structure of this repository

## Functions

Here you can find two simple functions implemented: `sine_function`.

Generally a function, named `azure_jackupdata_cognitefunction (previously as example function)` in the example below, consists of the following files:
```
📦my_cognite_function (azure_jackupdata_cognitefunction in this code)
 ┣ 📂schedules
 ┃ ┗ 📜main.yaml - (Optional) Schedule if you want to execute the function on a schedule.
 ┣ 📜__init__.py - Empty file (required to make the function into a package)
 ┣ 📜function_config.yaml - (Optional) Configuration for the function
 ┣ 📜handler.py - Module with script inside a handle function
 ┗ 📜requirements.txt - Explicitly states the dependencies needed to run the handler.py script.
```

<details>
<summary><code>schedules/master.yaml</code></summary>

Each function's folder contains a `schedules` folder where you can put your files that define your
schedules. By default, we have added a file here called `main.yaml` which will be used whenever
you merge a PR to `main` This file is ues with GitHub actions and automatic deployment - If you don't need any schedules
for a specific function, just delete it!

Example
```yaml
- name: My daily schedule
  cron: "0 0 * * *"
  data:
    ExtractionPipelineExtId: "sine-function"
```

</details>

<details>
<summary><code>function_config.yaml</code></summary>

Each function's folder contains a `function_config.yaml` file where you can specify most
configuration parameters (per function). These parameters are extracted and used by the Github
Workflow files during deployment (read more in the "build and deployment" section).

Example template, see [function details](https://github.com/cognitedata/function-action-oidc#function-metadata-in-github-workflow) for description of all configuration parameters.

```yaml

description: "Cognite Function that emits a simple Sine curve into a time series in CDF"
owner: your.name@domain.com
cpu: 0.25
memory: 1.00
metadata:
  version: "1.0.0"
```

</details>


<details>
<summary><code>handler.py</code></summary>

This is the code for your function is provided, where the handle object is required.

Example below, for a full description of the arguments that can be passed to this function see
[cognite-sdk - create function](https://cognite-sdk-python.readthedocs-hosted.com/en/latest/cognite.html#create-function).

```python
def handle(data, client):
    print(f"Hello from {__name__}!")
    print("I got the following data:")
    print(data)
    print("Will now return data")
    return data
```

</details>

<details>
<summary><code>requirements.txt</code></summary>

Each function's folder contains `requirements.txt`. You can use that file to add extra dependencies
that your code is depending on. By default, you have a newer version of `cognite-sdk` installed,
but it doesn't hurt to be specific here!

Example ``requirements.txt`` file

```text
cognite-extractor-utils>=2.2.0
cognite-logger>=0.5
numpy>=1.21.6
```
</details>

## Run code locally
To run code locally, you may create a file `.env`. Content of this file should be:

```text
PYTHONPATH=<path to your root folder of this repository>

COGNITE_PROJECT=<Cognite data Fusion project name>
COGNITE_BASE_URL=https://<CDF cluster>.cognitedata.com

# OIDC - Ex: Azure AD connection details
TENANT_ID=<Azure AD tenant ID>
CLIENT_ID=<Azure AD application object ID>
CLIENT_SECRET=<Azure AD application secret ID>
```
With this file you should be able to run the provide test python file that wil trigger the `handle` function in your `handler.py` file

```

