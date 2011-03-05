:mod:`{{name}}`
{{ underline }}

{% if functions %}
Functions
----------
{% for item in functions %}
.. autofunction:: {{item}}
{% endfor %}
{% endif %}

{% if classes %}
Classes
--------
{% for item in classes %}
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
{% for item in exceptions %}
.. autoclass:: {{item}}
   :show-inheritance:
   :members:
   :inherited-members:
   :undoc-members:
   
   .. automethod:: __init__
   
{% endfor %}
{% endif %}
