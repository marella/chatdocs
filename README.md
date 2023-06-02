# [ChatDocs](https://github.com/marella/chatdocs) [![PyPI](https://img.shields.io/pypi/v/chatdocs)](https://pypi.org/project/chatdocs/) [![tests](https://github.com/marella/chatdocs/actions/workflows/tests.yml/badge.svg)](https://github.com/marella/chatdocs/actions/workflows/tests.yml)

Chat with your documents offline using AI. No data leaves your system. Internet connection is only required to install the tool and download the AI models.

![Demo](https://github.com/marella/chatdocs/raw/main/docs/demo.png)

It is based on [PrivateGPT](https://github.com/imartinez/privateGPT) but uses [C Transformers](https://github.com/marella/ctransformers) which supports more GGML models. It also supports [🤗 Transformers](https://github.com/huggingface/transformers).

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

## Basic Usage

Add a directory containing documents to chat with using:

```sh
chatdocs add /path/to/documents
```

Chat with your documents using:

```sh
chatdocs chat
```

## Advanced Usage

To see available options for each command, run:

```sh
chatdocs add --help
chatdocs chat --help
```

### LLM

By default it uses the [Wizard-Vicuna-7B-Uncensored-GGML](https://huggingface.co/TheBloke/Wizard-Vicuna-7B-Uncensored-GGML) model which can be changed using the `--model` option:

```sh
chatdocs chat --model TheBloke/MPT-7B-GGML --download
```

> **Note:** The `--download` option is only required when you use a model for the first time.

It can also be used with an existing local model file:

```sh
chatdocs chat --model /path/to/mpt-7b-ggml.bin --model-type mpt
```

### LLM Provider

By default it uses C Transformers as the LLM provider which can be changed to 🤗 Transformers using the `--hf` option:

```sh
chatdocs chat --hf --model TheBloke/Wizard-Vicuna-7B-Uncensored-HF --download
```

### DB

By default it stores the processed documents in `db` directory which can be changed using the `--db` option:

```sh
chatdocs add documents --db /path/to/some/directory
chatdocs chat --db /path/to/some/directory
```

## UI

Coming Soon

## License

[MIT](https://github.com/marella/chatdocs/blob/main/LICENSE)
