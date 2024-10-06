## 1. Change the URL of the AutoRAG api

If you want to change the URL of the AutoRAG API server, you can change it on the settings tab.
With this, you can access to the remote AutoRAG API server easily.

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
