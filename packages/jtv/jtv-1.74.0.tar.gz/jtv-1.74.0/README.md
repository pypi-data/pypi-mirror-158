# jtv

jtv is a command line utility which allows you to visualise JSON and YAML schemas as text trees. It may be used as a complement to `jq`, to facilitate the interpretation of a JSON schema, prior to defining filters.

## Installation

```
$ pip install --upgrade pip
$ pip install jtv
```

## Usage

To show the help use `jtv -h`

![new_help](https://user-images.githubusercontent.com/80931870/178190588-d5b857ad-3f31-4352-b5f1-d40e33259a22.png)

## Inconsistency handling

Arrays may contain objects with different schemas. By default, or using the option `--mode distinct` will wrap all objects in a new object with the node key specifying a schema version. The appended `◎-schema-0` node does not exist in the JSON and is strictly used to differentiate between different object schemas. 

```
$ echo '[{"0": {"00": [{"000": "", "001": true, "002": []}, {"NEW": {"A": 2}}]}, "1": {"10": []}}, {"A": {"r": []}}]' | jtv -j --mode distinct
```

![new_distinct](https://user-images.githubusercontent.com/80931870/178190578-bf58a29a-8b2c-4085-97eb-a223dad08fa3.png)

To display all the nodes from each distinct object under a single object, use `--mode union`. 

```
$ echo '[{"0": {"00": [{"000": "", "001": true, "002": []}, {"NEW": {"A": 2}}]}, "1": {"10": []}}, {"A": {"r": []}}]' | jtv -j --mode union
```

![new_union](https://user-images.githubusercontent.com/80931870/178190593-7f2c1b90-30e8-4859-b2b0-211afa0dd726.png)

To display only the schema of the first object use `--mode first`. 

```
$ echo '[{"0": {"00": [{"000": "", "001": true, "002": []}, {"NEW": {"A": 2}}]}, "1": {"10": []}}, {"A": {"r": []}}]' | jtv -j --mode first
```

![new_first](https://user-images.githubusercontent.com/80931870/178190586-80143e81-3352-4322-b6e5-91596b0a940e.png)

To visualise JSON schemas, as above, use the `-j` flag. To visualise YAML schema use the `-y` flag.

```
$ cat .yml | jtv -y
```

![new_yaml](https://user-images.githubusercontent.com/80931870/178190597-3ed79d53-5405-4c7c-8648-d2c78b057b19.png)


## Tests
Run `tox` in the root project directory.

## Development

Increment version:
```
bumpver update --minor
```
