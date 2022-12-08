# Falcon Tags Tool

This is a simple example script written as a python tool to apply CrowdStrike Falcon Sensor Grouping Tags to a host based on its hostname matching multiple regex patterns. This tool can apply multiple tags to a single host.

```
python3 falcon-tags.py -h
usage: falcon-tags.py [-h] [-j TAGSFILEPATH] [-x] [--verbose]

optional arguments:
  -h, --help            show this help message and exit
  -j TAGSFILEPATH, --tagsfilepath TAGSFILEPATH
                        File location for json.tags
  -x, --execute         Execute command (requires sudo)
  --verbose             increase output verbosity
```  

## Running the tool

The tool will match the hostname to the `tags.json` file using regex patterns. In this example the hostname `balbo` will match three different regex patterns with labels: `production`, `special`, and `special`. Since the collection is a `set[]` we will only apply the `special` tag once. 

```json
{
  "balbo": "production",
  "foo?baz": "test",
  "biz?baz": "smoke",
  "bal*": "special",
  "(bal)?bo.?": "special"
}
```

![](https://raw.githubusercontent.com/cs-shadowbq/falcon-tags-tool/gh-pages/images/run-tags.png)

## Applying the tags

![](https://raw.githubusercontent.com/cs-shadowbq/falcon-tags-tool/gh-pages/images/run-output.png)

## Falcon UI - Host Management

In the screen (circa late - 2022) We can see the host in the UI has the applied "Falcon Sensor Grouping Tags"

![](https://raw.githubusercontent.com/cs-shadowbq/falcon-tags-tool/gh-pages/images/Applied.png)

Create a New Dynamic Group, then add the selected tags to this Group.

![](https://raw.githubusercontent.com/cs-shadowbq/falcon-tags-tool/gh-pages/images/dynamic-group.png)

## Profit $$

Apply any Falcon based policies (Protection, FW, USB, Update, etc..) to the host group and now you have dynamic policies based on regex matching of the hostname.

## Going Further

### FalconPY

[FalconPY](https://www.falconpy.io/Service-Collections/Hosts.html?highlight=tags#updatedevicetags) can be used to update the similar tags called 'FalconGroupingTags' used in the API and stored on the SaaS. Either 'FalconGroupingTags' or 'SensorGroupingTags' can be used for filtering and creating dynamic host groups as they are both listed in 'GroupingTags'.

### Matching Other Data Resources

Specific applications and other tools may hold sorting information that may be useful in tagging hosts. Potential use cases include identifing individual hardware with `dmidecode` or applications installed using `rpm` or `apt`. Extending scripts and parsing the output of those tools could be enabled with [jc](https://github.com/kellyjonbrazil/jc) a json oss common unix tool output parser.

### Porting

This tool could be combined with scripts in Ansible, Salt, Chef or Puppet and other distributed execution systems to ensure full fleet deployment. 
