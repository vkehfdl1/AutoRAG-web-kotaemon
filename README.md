# Deploying AutoRAG with Kotaemon Tutorial

In this tutorial, we’ll guide you on how to deploy AutoRAG using Kotaemon to create a functional chat UI. With this guide, you can utilize an optimized RAG system through [AutoRAG](https://github.com/Marker-Inc-Korea/AutoRAG) and experience it in a seamless chat interface.

[Watch the Result Video](https://youtu.be/skVNh0azjgs)

## Tutorial Outline

1. Optimize RAG using [AutoRAG](https://github.com/Marker-Inc-Korea/AutoRAG).
2. Run the API server from the optimized RAG.
3. Deploy the AutoRAG x Kotaemon web app on [fly.io](fly.io).
4. Connect and use the API server in the web app.

### Prerequisites

- Git installed on your system
- Homebrew (for macOS users)
- fly.io account
- Completion of optimization using [AutoRAG](https://github.com/Marker-Inc-Korea/AutoRAG)

### Step 1: Optimizing RAG with AutoRAG

First, find an optimized RAG pipeline.
Check out this [tutorial](https://docs.auto-rag.com/tutorial.html) for instructions on optimizing with AutoRAG.

### Step 2: Running the AutoRAG API Server

To run the [AutoRAG](https://github.com/Marker-Inc-Korea/AutoRAG) API server locally, use the following command:

```bash
autorag run_api --trial_dir /trial/dir/0 --host 0.0.0.0 --port 8000
```

The trial directory is a subdirectory within your project directory post-optimization, typically named with a “number.” Specify the directory name to be used as the backend for the chat interface.

For public access to the API server, [AutoRAG](https://github.com/Marker-Inc-Korea/AutoRAG) uses NGrok. Upon server startup, you can find the public URL in the logs:

```
INFO     [api.py:199] >> Public API URL:          api.py:199
<https://8a31-14-52-132-205.ngrok-free.app>
```

![NGrok URL](https://velog.velcdn.com/images/autorag/post/947c4f3b-6d49-4bba-924c-75a844bb0499/image.png)

Make sure to remember the URL displayed in the terminal.

### Step 3: Deploying AutoRAG-Kotaemon

First, clone the AutoRAG Kotaemon repository:

```bash
git clone https://github.com/vkehfdl1/AutoRAG-web-kotaemon.git
cd AutoRAG-web-kotaemon
```

Then proceed to [fly.io]:

1. Install the Fly.io CLI tool:

```bash
brew install flyctl
```

This is for macOS users.

For other operating systems, refer to [here](https://fly.io/docs/flyctl/install/).

2. Authenticate with Fly.io:

```bash
fly auth login
```

3. Deploy on Fly.io:

```bash
fly launch
```

![Fly.io deployment](https://velog.velcdn.com/images/autorag/post/e2d53990-9551-4ef3-958b-091812a39a11/image.png)

Set up the deployment as shown above. You can set Region, Name, etc., as desired.

Note: The initial deployment may take around 10-15 minutes.

Also, a minimum of 1GB memory is recommended for smooth operation.

Once deployed, you’ll see the Fly URL. If you don’t see it in the CLI, you can find it in the Fly.io dashboard. Clicking on it will open Kotaemon’s initial setup screen.

### Step 5: Configuring Kotaemon

![Kotaemon initial setup](https://velog.velcdn.com/images/autorag/post/58fef8fe-ac9a-4647-ac08-2cd55e30197a/image.png)

Upon first launch, you’ll see the initial setup screen as shown above. Here, you can set your OpenAI API Key or Cohere API key, or proceed without setting one by pressing the red button.

Without setting an API key, you won’t be able to use the “Automatic Conversation Title” feature. For private data, avoid setting an API key and proceed to the next step by pressing the red button.

![Kotaemon login](https://velog.velcdn.com/images/autorag/post/988560f0-ea88-4110-9d7f-997133142cab/image.png)

Next, you’ll see the login screen. For the first run, set both the ID and password to `admin`. This will allow you to use the service without issues.

After logging in, be sure to enter the Settings tab at the top left and go to the Reasoning settings tab.

![API Endpoint setup](https://velog.velcdn.com/images/autorag/post/7d10f7cb-bc71-4409-92e0-33882bc2a64a/image.png)

In the AutoRAG API Endpoint URL tab, enter the API server URL you noted down earlier. Ensure it ends with `.app` and do not add a `/` at the end.

Finally, press the Save Changes button!

### Step 6: Try It Out

Now you can use the optimized RAG pipeline with Kotaemon as shown below!

![Kotaemon chat interface](https://velog.velcdn.com/images/autorag/post/19f851d1-ed51-46ac-94a2-bc3983c35f88/image.png)

### Stopping Deployment on Fly.io

Since Fly.io is a paid service, it’s best to stop deployment when not in use.

To stop an application on Fly.io, use:

```
fly scale count 0
```
