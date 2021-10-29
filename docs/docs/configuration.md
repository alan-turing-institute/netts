# Configuration

Netspy can be configured using a [TOML](https://toml.io/en/) configuration file. This allows you to alter the ports used by netspy's two servers, and  alter defaults used to preprocess transcripts.

The easiest way to configure netspy is to create config file using the netspy CLI which contains all the defaults:

```bash
netspy config > config.toml
```

## Validate your configuration

When you make changes to your configuration file it is a good idea to check its still valid, has the correct syntax and has all the required fields. You can do this with:

```bash
netspy config-verify config.toml
```

Netspy expects `config.toml` to be in the current working directory. If it is somewhere else you can pass the path to the `netspy run` command

```bash
netspy run transcript.txt OUTPUT_DIR --config PATH_TO_CONFIG
```
