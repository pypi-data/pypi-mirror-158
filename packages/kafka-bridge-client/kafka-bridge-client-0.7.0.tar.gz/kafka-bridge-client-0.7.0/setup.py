# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['kafka_bridge_client']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp>=3.7.4,<4.0.0',
 'mypy-extensions>=0.4.3,<0.5.0',
 'requests>=2.27.1,<3.0.0']

setup_kwargs = {
    'name': 'kafka-bridge-client',
    'version': '0.7.0',
    'description': 'Python client for Strimzi Kafka Bridge',
    'long_description': "# kafka-bridge-client\nPython async client for [Strimzi Kafka Bridge](https://github.com/strimzi/strimzi-kafka-bridge) and [Confluent REST Proxy](https://docs.confluent.io/platform/current/kafka-rest/index.html) Package include consumer only.\n\n[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)\n[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-green.svg)](https://github.com/shafa-dev/kafka-bridge-client/issues)\n[![PyPI version](https://badge.fury.io/py/kafka-bridge-client.svg)](https://badge.fury.io/py/kafka-bridge-client)\n\n## Install\n```\npip install kafka-bridge-client\n```\n\n## Usage\nBy default client use [Strimzi Kafka Bridge](https://github.com/strimzi/strimzi-kafka-bridge) API\n\n`Consumer (async)`\n\n```python\nfrom kafka_bridge_client import KafkaBridgeConsumer\n\n# Strimzi Kafka Bridge\n\nconsumer1 = KafkaBridgeConsumer(\n    'topic1',\n    'topic2',\n    group_id='my-group,\n    auto_offset_reset='earliest',\n    enable_auto_commit=False,\n    bootstrap_server='your-kafka-bridge-url',\n    consumer_name='consumer-name',\n)\n\n# Confluent REST Proxy\nconsumer2 = KafkaBridgeConsumer(\n    'topic1',\n    'topic2',\n    group_id='my-group,\n    auto_offset_reset='earliest',\n    enable_auto_commit=False,\n    bootstrap_server='your-kafka-bridge-url',\n    consumer_name='consumer-name',\n    proxy='confluent'\n)\n\nasync for rec in consumer1.get_records():\n    print(rec['value'])\n    await consumer.commit()\n\n# or\n\nrecords = await consumer1.poll_records()\nprint(records)\nawait consumer.commit()\n```\n\n\n`Producer (sync)`\n\n```python\nfrom kafka_bridge_client import KafkaBridgeProducer\n\nproducer = KafkaBridgeProducer('http://bridge.url' timeout=5)\nproducer.send(Message(key='1', value='value'))\n```\n\n\n## Deploy\n\nYou need to change version in `pyproject.toml` and run it\n\n```\npoetry publish --build\n```",
    'author': 'Bogdan Zaseka',
    'author_email': 'zaseka.bogdan@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/shafa-dev/kafka-bridge-client',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
