.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :alt: License: AGPL-3

Gantt view for prduction work orders
====================================

This module adds Gantt to the production's work orders' view mode
so you can have an overall view of all the work orders and their start and
finish dates and production order when using routings.

After uninstalling the module if you get the "No default view of type 'ganttview'
could be found !" error when you open 'Production->Work Orders' remove 'ganttview'
from the 'view_mode' field of the ir.action with extrernal ID: 'mrp_workorder_todo'.

Credits
=======

Contributors
------------

* Alicia Rodríguez <arodriguez@binovo.es>
* Bittor Laskurain <blaskurain@binobo.es>
* Guillermo Murcia <guiller.512@gmail.com>

Maintainer
----------

.. image:: /gantt_workorders/static/src/img/binovo_logo_peque.jpg
   :alt: Binovo IT Human Project SL
   :target: http://www.binovo.es

This module is maintained by Binovo IT Human Project SL.
