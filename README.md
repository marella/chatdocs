# [ChatDocs](https://github.com/marella/chatdocs) [![PyPI](https://img.shields.io/pypi/v/chatdocs)](https://pypi.org/project/chatdocs/) [![tests](https://github.com/marella/chatdocs/actions/workflows/tests.yml/badge.svg)](https://github.com/marella/chatdocs/actions/workflows/tests.yml)

Chat with your documents offline using AI. No data leaves your system. Internet connection is only required to install the tool and download the AI models. It is based on [PrivateGPT](https://github.com/imartinez/privateGPT) and has more features.

![Demo](https://github.com/marella/chatdocs/raw/main/docs/demo.png)

- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Configuration](#configuration)
- [GPU](#gpu)

## Features

- Supports many GGML models via [C Transformers](https://github.com/marella/ctransformers)
- Supports [🤗 Transformers](https://github.com/huggingface/transformers)
- GPU support
- Highly configurable via `chatdocs.yml`

## Installation

Install the tool using:

```sh
pip install chatdocs
```

Download the AI models using:

```sh
chatdocs download
```

Now it can be run offline without internet connection.

## Usage

Add a directory containing documents to chat with using:

```sh
chatdocs add /path/to/documents
```

> The processed documents will be stored in `db` directory by default.

Chat with your documents using:

```sh
chatdocs chat
```

## Configuration

All the configuration options can be changed using the `chatdocs.yml` config file. Create a `chatdocs.yml` file in some directory and run all commands from that directory. For reference, see the default [`chatdocs.yml`](https://github.com/marella/chatdocs/blob/main/chatdocs/data/chatdocs.yml) file.

You don't have to copy the entire file, just add the config options you want to change as it will be merged with the default config. For example, see [`tests/fixtures/chatdocs.yml`](https://github.com/marella/chatdocs/blob/main/tests/fixtures/chatdocs.yml) which changes only some of the config options.

### Embeddings

To change the embeddings model, add and change the following in your `chatdocs.yml`:

```yml
embeddings:
  model: hkunlp/instructor-large
```

> **Note:** When you change the embeddings model, delete the `db` directory and add documents again.

### C Transformers

To change the C Transformers model, add and change the following in your `chatdocs.yml`:

```yml
ctransformers:
  model: TheBloke/Wizard-Vicuna-7B-Uncensored-GGML
  model_type: llama
```

> **Note:** When you add a new model for the first time, run `chatdocs download` to download the model before using it.

You can also use an existing local model file:

```yml
ctransformers:
  model: /path/to/ggml-model.bin
  model_type: llama
```

### 🤗 Transformers

To use 🤗 Transformers, add the following to your `chatdocs.yml`:

```yml
llm: huggingface
```

To change the 🤗 Transformers model, add and change the following in your `chatdocs.yml`:

```yml
huggingface:
  model: TheBloke/Wizard-Vicuna-7B-Uncensored-HF
```

> **Note:** When you add a new model for the first time, run `chatdocs download` to download the model before using it.

## GPU

### Embeddings

To enable GPU (CUDA) support for the embeddings model, add the following to your `chatdocs.yml`:

```yml
embeddings:
  model_kwargs:
    device: cuda
```

You may have to reinstall PyTorch with CUDA enabled by following the instructions [here](https://pytorch.org/get-started/locally/).

### C Transformers

> **Note:** Currently only LLaMA GGML models have GPU support.

To enable GPU (CUDA) support for the C Transformers model, add the following to your `chatdocs.yml`:

```yml
ctransformers:
  config:
    gpu_layers: 50
```

You should also reinstall the `ctransformers` package with CUDA enabled:

```sh
pip uninstall ctransformers --yes
CT_CUBLAS=1 pip install ctransformers --no-binary ctransformers
```

<details>
<summary><strong>Show commands for Windows</strong></summary><br>

On Windows PowerShell run:

```sh
$env:CT_CUBLAS=1
pip uninstall ctransformers --yes
pip install ctransformers --no-binary ctransformers
```

On Windows Command Prompt run:

```sh
set CT_CUBLAS=1
pip uninstall ctransformers --yes
pip install ctransformers --no-binary ctransformers
```

</details>

### 🤗 Transformers

To enable GPU (CUDA) support for the 🤗 Transformers model, add the following to your `chatdocs.yml`:

```yml
huggingface:
  device: 0
```

You may have to reinstall PyTorch with CUDA enabled by following the instructions [here](https://pytorch.org/get-started/locally/).

## UI

Coming Soon

## License

[MIT](https://github.com/marella/chatdocs/blob/main/LICENSE)
