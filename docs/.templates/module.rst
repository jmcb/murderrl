:mod:`{{name}}`
{{ mod_underline }}

.. automodule:: {{ fullname }}

{% if functions %}
Functions
----------
{% for item, members in functions %}
.. autofunction:: {{item}}
{% endfor %}
{% endif %}

{% if classes %}
Classes
--------
{% for item, members in classes %}
.. autoclass:: {{item}}
    :show-inheritance:
    :members:
    :inherited-members:
    :undoc-members:
    
    .. automethod:: __init__
    
{% endfor %}
{% endif %}

{% if exceptions %}
Exceptions
------------
{% for item, members in exceptions %}
.. autoclass:: {{item}}
    :show-inheritance:
    :members:
    :inherited-members:
    :undoc-members:
    
    .. automethod:: __init__
    
{% endfor %}
{% endif %}
