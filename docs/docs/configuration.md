# Configuration

Netts can be configured using a [TOML](https://toml.io/en/) configuration file. This allows you to alter the ports used by netts's two servers, and  alter defaults used to preprocess transcripts.

The easiest way to configure netts is to create config file using the netts CLI which contains all the defaults:

```bash
netts config > config.toml
```

## Validate your configuration

When you make changes to your configuration file it is a good idea to check its still valid, has the correct syntax and has all the required fields. You can do this with:

```bash
netts config-verify config.toml
```

Netts expects `config.toml` to be in the current working directory. If it is somewhere else you can pass the path to the `netts run` command

```bash
netts run transcript.txt OUTPUT_DIR --config PATH_TO_CONFIG
```
