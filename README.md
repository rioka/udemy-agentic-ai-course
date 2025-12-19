# Code for Agentic AI Engineering Course (Udemy)

This repository my attempt to replicate and extend the code from Udemy course [The Complete Agent & MCP Course](https://comcast.udemy.com/course/the-complete-agentic-ai-engineering-course/), using plain script instead of Jupyter notebooks.

The structure of this repository tries to mimic the original one, but not pedantically... 

The same principle is applied while implementing the code: it's not meant to be a 1-1 transposition of the code in notebooks, rather use that as a starting point to achieve similar results.

> **Disclaimer**
>
> I have little to no experience in Python, and this code has no ambition to demonstrate anything, especially with respect to best practices: in other terms, it is just the tool I'm using in my attempt to become a bit more familiar with LLMs and agentic AI engineering.

## Containers

A [`compose.yml`](./compose.yml) file has been added, to simplify testing the code without active subscriptions; it currently contains two services:

- Ollama
- LocalAI

OOTB, no model is available: models have to be pulled using one of the many possible methods.

## References

- [The Complete Agent & MCP Course](https://comcast.udemy.com/course/the-complete-agentic-ai-engineering-course/)
- [The Complete Agent & MCP Course - GitHub Repo](https://github.com/ed-donner/agents)
- [LocalAI - Docker Installation](https://localai.io/installation/docker/)