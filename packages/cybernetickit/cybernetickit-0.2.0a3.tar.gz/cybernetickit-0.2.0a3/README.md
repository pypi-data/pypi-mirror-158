# Cybernetic Kit

The Cybernetic Kit is a set of conventions and techniques useful for making software-driven social impact. This repository holds a collection of software components for multiple fields of study, such as:

- Open Data & Civic Engagement
- Environmental Science
- Library Science
- Software Development
- Sociology
- Neuroscience


## Meet the Cast

### Data Objects

Data Objects are Python classes designed to make it easier to interact with data. Using Data Objects to describe something of interest tells computers how to manipulate, archive, inspect, and exchange data.

#### Built-In Data Objects

- civic data
- research preprints and archives
- air quality sensor readings
- geopolitical shapes (e.g., county, state)


**How to use built-in Data Objects**

Here's an example of how you'd go about storing air quality sensor readings in Elasticsearch.

```python
from datetime import datetime

from elasticsearch_dsl import connections
from cybernetickit.sensor import AirQuality
from cybernetickit import constants

connections.create_connection(hosts=['localhost'], timeout=20)

observation = AirQuality(date=datetime.now(),
                         state='ga',
                         pollutant=constants.OZONE._asdict(),
                         units=constants.OZONE.units,
                         concentration=2.3)

observation.save()
```

You can use the Elasticsearch DSL to search and aggregations against an existing Elasticsearch index:

```python
from elasticsearch_dsl import Q
s = AirQuality.search(Q('match', state='ny') & Q('match', **{'pollutant.parameter': 'OZONE'}))
response = s.execute()

for obs in response:
    ...
```

#### Custom Data Objects

Simply subclass the `CoreModel` and describe something of interest. Use annotations for runtime validation:

```python
from typing from List, Optional
from cybernetickit from CoreModel, Keyword


class UseOfForce(CoreModel):
    force_applied: str = Keyword()
    deadly_force: Optional[str] = Keyword()
    source_ref: str = Keyword()
    target_ref: str = Keyword()

```



## Getting Started

```sh
pip install cybernetickit
```

```python
from cybernetickit import CoreModel
```


## Licensing

    Cybernetic Kit
    Copyright (C) 2021  Civic Hacker, LLC

    This program is free software: you can redistribute it and/or modify
    it under the terms of the Lesser GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    Lesser GNU General Public License for more details.

    You should have received a copy of the Lesser GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
