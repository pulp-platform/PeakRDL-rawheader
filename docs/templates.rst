Custom Templates
================

The built-in formats are rendered from `Mako <https://www.makotemplates.org/>`_
templates that ship with the plugin. When none of them fit your needs, you can
supply your own template with the :option:`--template` option:

.. code-block:: bash

    peakrdl raw-header top.rdl -o top.txt --template my_template.mako

When a template is given, the :option:`--format` option is ignored.

The easiest way to write a custom template is to copy one of the bundled
templates (``c.mako``, ``svh.mako``, ``svpkg.mako``, ``ldh.mako``) from the
``peakrdl_rawheader/templates`` directory and adapt it. They show the variables
available in the template namespace — chiefly ``top_name``, ``blocks``,
``registers``, ``memories``, and ``enums`` — and the formatting helpers in
``peakrdl_rawheader.utils`` (``fmt_hex``, ``fmt_addr_expr``, ``fmt_idx_expr``,
``fmt_license``).
