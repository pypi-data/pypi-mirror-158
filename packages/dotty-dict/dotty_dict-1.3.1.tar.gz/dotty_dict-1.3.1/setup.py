# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dotty_dict']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'dotty-dict',
    'version': '1.3.1',
    'description': 'Dictionary wrapper for quick access to deeply nested keys.',
    'long_description': "**********\nDotty-Dict\n**********\n\n:Info: Dictionary wrapper for quick access to deeply nested keys.\n:Author: Pawel Zadrozny @pawelzny <pawel.zny@gmail.com>\n\n.. image:: https://circleci.com/gh/pawelzny/dotty_dict/tree/master.svg?style=shield&circle-token=77f51e87481f339d69ca502fdbb0c2b1a76c0369\n   :target: https://circleci.com/gh/pawelzny/dotty_dict/tree/master\n   :alt: CI Status\n\n.. image:: https://readthedocs.org/projects/vo/badge/?version=latest\n   :target: http://dotty-dict.readthedocs.io/en/latest/?badge=latest\n   :alt: Documentation Status\n\n.. image:: https://img.shields.io/pypi/v/dotty_dict.svg\n   :target: https://pypi.org/project/dotty_dict/\n   :alt: PyPI Repository Status\n\n.. image:: https://img.shields.io/github/release/pawelzny/dotty_dict.svg\n   :target: https://github.com/pawelzny/dotty_dict\n   :alt: Release Status\n\n.. image:: https://img.shields.io/pypi/status/dotty_dict.svg\n   :target: https://pypi.org/project/dotty_dict/\n   :alt: Project Status\n\n.. image:: https://img.shields.io/pypi/pyversions/dotty_dict.svg\n   :target: https://pypi.org/project/dotty_dict/\n   :alt: Supported python versions\n\n.. image:: https://img.shields.io/pypi/implementation/dotty_dict.svg\n   :target: https://pypi.org/project/dotty_dict/\n   :alt: Supported interpreters\n\n.. image:: https://img.shields.io/pypi/l/dotty_dict.svg\n   :target: https://github.com/pawelzny/dotty_dict/blob/master/LICENSE\n   :alt: License\n\n\nFeatures\n========\n\n* Simple wrapper around python dictionary and dict like objects\n* Two wrappers with the same dict are considered equal\n* Access to deeply nested keys with dot notation: ``dot['deeply.nested.key']``\n* Create, read, update and delete nested keys of any length\n* Expose all dictionary methods like ``.get``, ``.pop``, ``.keys`` and other\n* Access dicts in lists by index ``dot['parents.0.first_name']``\n* key=value caching to speed up lookups and low down memory consumption\n* support for setting value in multidimensional lists\n* support for accessing lists with slices\n\n\nInstallation\n============\n\n.. code:: bash\n\n   pip install dotty-dict\n\n\n* **Package**: https://pypi.org/project/dotty-dict/\n* **Source**: https://github.com/pawelzny/dotty_dict\n\n\nDocumentation\n=============\n\n* Full documentation: http://dotty-dict.readthedocs.io\n* Public API: http://dotty-dict.readthedocs.io/en/latest/api.html\n* Examples and usage ideas: http://dotty-dict.readthedocs.io/en/latest/examples.html\n\n\nTODO\n====\n\nWaiting for your feature requests ;)\n\n\nQuick Example\n=============\n\nCreate new dotty using factory function.\n\n.. code-block:: python\n\n   >>> from dotty_dict import dotty\n   >>> dot = dotty({'plain': {'old': {'python': 'dictionary'}}})\n   >>> dot['plain.old']\n   {'python': 'dictionary'}\n\n\nYou can start with empty dotty\n\n.. code-block:: python\n\n   >>> from dotty_dict import dotty\n   >>> dot = dotty()\n   >>> dot['very.deeply.nested.thing'] = 'spam'\n   >>> dot\n   Dotty(dictionary={'very': {'deeply': {'nested': {'thing': 'spam'}}}}, separator='.', esc_char='\\\\')\n\n   >>> dot['very.deeply.spam'] = 'indeed'\n   >>> dot\n   Dotty(dictionary={'very': {'deeply': {'nested': {'thing': 'spam'}, 'spam': 'indeed'}}}, separator='.', esc_char='\\\\')\n\n   >>> del dot['very.deeply.nested']\n   >>> dot\n   Dotty(dictionary={'very': {'deeply': {'spam': 'indeed'}}}, separator='.', esc_char='\\\\')\n\n   >>> dot.get('very.not_existing.key')\n   None\n\nNOTE: Using integer in dictionary keys will be treated as embedded list index.\n\nInstall for development\n=======================\n\nInstall dev dependencies\n\n.. code-block:: console\n\n    $ make install\n\nTesting\n=======\n\n.. code-block:: console\n\n    $ make test\n\nOr full tests with TOX:\n\n.. code-block:: console\n\n    $ make test-all\n\nLimitations\n===========\n\nIn some very rare cases dotty may not work properly.\n\n* When nested dictionary has two keys of different type, but with the same value.\n  In that case dotty will return dict or list under random key with passed value.\n\n* Keys in dictionary may not contain dots. If you need to use dots, please specify dotty with custom separator.\n\n* Nested keys may not be bool type. Bool type keys are only supported when calling keys with type defined value (e.g. dot[True], dot[False]).\n",
    'author': 'Pawel Zadrozny',
    'author_email': 'pawel.zny@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.5,<4.0',
}


setup(**setup_kwargs)
