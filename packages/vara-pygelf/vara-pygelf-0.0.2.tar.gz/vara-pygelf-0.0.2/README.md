# vara pygelf


## Description
Python logging module wrapper for
- GELF format
- syslog level


## Usage
```
from vara_pygelf import logger

logger.debug("test")
```

extra field at log event (note: gelf doesn't allow "id" field)
```
logger.debug("test", {"project_id": 2567})
logger.debug("test", {"name": "abc"})
```


Set log threshold:
```
logger.set_level("INFO")
```

add/remove extra fields for all log msg 
```
logger.add_fields({"b": "122" })
logger.remove_fields(["b"])
```

### Log Levels


| Level name    | Severity value| Logger method  |
| ------------- |---------------| ------|
| EMERGENCY     | 0      | logger.emerg |
| ALERT         | 1      |   logger.alert |
| CRITICAL      | 2      | logger.crit |
| ERROR         | 3      |   logger.err |
| WARNING       | 4      | logger.warning |
| NOTICE        | 5      |   logger.notice |
| INFO          | 6      | logger.info |
| DEBUG         | 7      |   logger.debug |

### TODO
- Unit tests
- Module package?