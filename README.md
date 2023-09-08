# [ChatDocs](https://github.com/marella/chatdocs) [![PyPI](https://img.shields.io/pypi/v/chatdocs)](https://pypi.org/project/chatdocs/) [![tests](https://github.com/marella/chatdocs/actions/workflows/tests.yml/badge.svg)](https://github.com/marella/chatdocs/actions/workflows/tests.yml)

Chat with your documents offline using AI. No data leaves your system. Internet connection is only required to install the tool and download the AI models. It is based on [PrivateGPT](https://github.com/imartinez/privateGPT) but has more features.

![Web UI](https://github.com/marella/chatdocs/raw/main/docs/demo.png)

**Contents**

- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Configuration](#configuration)
- [GPU](#gpu)

## Features

- Supports GGML/GGUF models via [CTransformers](https://github.com/marella/ctransformers)
- Supports 🤗 Transformers models
- Supports GPTQ models
- Web UI
- GPU support
- Highly configurable via `chatdocs.yml`

<details>
<summary><strong>Show supported document types</strong></summary><br>

| Extension       | Format                         |
| :-------------- | :----------------------------- |
| `.csv`          | CSV                            |
| `.docx`, `.doc` | Word Document                  |
| `.enex`         | EverNote                       |
| `.eml`          | Email                          |
| `.epub`         | EPub                           |
| `.html`         | HTML                           |
| `.md`           | Markdown                       |
| `.msg`          | Outlook Message                |
| `.odt`          | Open Document Text             |
| `.pdf`          | Portable Document Format (PDF) |
| `.pptx`, `.ppt` | PowerPoint Document            |
| `.txt`          | Text file (UTF-8)              |

</details>

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
chatdocs ui
```

Open http://localhost:5000 in your browser to access the web UI.

It also has a nice command-line interface:

```sh
chatdocs chat
```

<details>
<summary><strong>Show preview</strong></summary><br>

![Demo](https://github.com/marella/chatdocs/raw/main/docs/cli.png)

</details>

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

### CTransformers

To change the CTransformers (GGML/GGUF) model, add and change the following in your `chatdocs.yml`:

```yml
ctransformers:
  model: TheBloke/Wizard-Vicuna-7B-Uncensored-GGML
  model_file: Wizard-Vicuna-7B-Uncensored.ggmlv3.q4_0.bin
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

To use 🤗 Transformers models, add the following to your `chatdocs.yml`:

```yml
llm: huggingface
```

To change the 🤗 Transformers model, add and change the following in your `chatdocs.yml`:

```yml
huggingface:
  model: TheBloke/Wizard-Vicuna-7B-Uncensored-HF
```

> **Note:** When you add a new model for the first time, run `chatdocs download` to download the model before using it.

To use GPTQ models with 🤗 Transformers, install the necessary packages using:

```sh
pip install chatdocs[gptq]
```

## GPU

### Embeddings

To enable GPU (CUDA) support for the embeddings model, add the following to your `chatdocs.yml`:

```yml
embeddings:
  model_kwargs:
    device: cuda
```

You may have to reinstall PyTorch with CUDA enabled by following the instructions [here](https://pytorch.org/get-started/locally/).

### CTransformers

To enable GPU (CUDA) support for the CTransformers (GGML/GGUF) model, add the following to your `chatdocs.yml`:

```yml
ctransformers:
  config:
    gpu_layers: 50
```

You may have to install the CUDA libraries using:

```sh
pip install ctransformers[cuda]
```

### 🤗 Transformers

To enable GPU (CUDA) support for the 🤗 Transformers model, add the following to your `chatdocs.yml`:

```yml
huggingface:
  device: 0
```

You may have to reinstall PyTorch with CUDA enabled by following the instructions [here](https://pytorch.org/get-started/locally/).

## License

[MIT](https://github.com/marella/chatdocs/blob/main/LICENSE)
