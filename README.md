# SumPAI
Summarization and embedding of Python projects.

Generates information that is useful for helping machines understand your Python code.

The data structure looks like this:

{
    "type": source_type,
    "name": name,
    "path": path,
    "hash": city_hash,
    "summary": summary,
    "embedding": embedding,
}

Each file is broken into Classes, Class Functions,
Functions and global level code.

Each of these are summarized using GPT-3.5-turbo and ada-02 embeddings are generated with the summary and code chunks.

Additionally, each file is summarized by all of the summaries above to give a complete overview of the file.

This project currently consumes about $0.02 for one run to give you an idea of the cost to run this.

If files were not changed it skips the file.

It will also skip classes and functions and globals if they were not changed.

It is intended for the files to be commited to the git repo and not for use by humans, it might make sense to hide these files in the future.

If you're not sure why you might need to run this you probably don't.

If you have a large project be aware that this code will scale models based on token count, for very large projects this might mean you will use gpt-4-32k.

## Installation

```
pip install sum-pai
```

## Usage

Setup your OpenAI API Key as the OPENAI_API_KEY environmental variable.

.env files are supported.

or pass with 

`--openai-api-key=<key>`

```
sum_pai <target>
```

you can also set the logging level with LOG_LEVEL envvar or 

`--log-level=DEBUG`


### Searching

There's a search embedding in the root of the project, will be used for testing.

`search_project.exe --text "perform a knn search" --target src`

Result:

![SS](https://raw.githubusercontent.com/BillSchumacher/SumPAI/main/ss.png)