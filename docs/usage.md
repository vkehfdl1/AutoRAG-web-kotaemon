## 1. Change the URL of the AutoRAG api

If you want to change the URL of the AutoRAG API server, you can change it on the settings tab.
With this, you can access to the remote AutoRAG API server easily.

If you want to deploy kotaemon server to remote, but want to use AutoRAG on your own server,
it is great to use the pyNgrok to access to the AutoRAG API server.
It automatically creates an ngrok tunnel to your local server.

After you start your API server, you can see the NGrok URL on the log like below:

```bash
INFO     [api.py:199] >> Public API URL:          api.py:199
         https://8a31-14-52-132-205.ngrok-free.app
```

Then, go to the `settings` Tab and click `Reasoning Settings`. There, you can edit AutoRAG URL.
Put your NGrok URL to the `AutoRAG URL` field and click `Save`.
The input should be like "https://8a31-14-52-132-205.ngrok-free.app".

Or you can put your own AutoRAG server URL to the field.

## 2. Chat History

The chat history will be stored on to your local.
We will add more features when we launch the cloud version of AutoRAG in the future.

## 3. Change the AutoRAG pipeline

You can change the AutoRAG config at the AutoRAG API server setting that you have done.

Go to the directory where you installed AutoRAG and start a new API server with the following command:

```python
from autorag.deploy import ApiRunner
import nest_asyncio

nest_asyncio.apply()

runner = ApiRunner.from_yaml('your/path/to/pipeline.yaml', project_dir='your/project/directory')
runner.run_api_server()
```

or

```python
from autorag.deploy import ApiRunner
import nest_asyncio

nest_asyncio.apply()

runner = ApiRunner.from_trial_folder('/your/path/to/trial_dir')
runner.run_api_server()
```

```bash
autorag run_api --trial_dir /trial/dir/0 --host 0.0.0.0 --port 8000
```
