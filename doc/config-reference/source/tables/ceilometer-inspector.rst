..
    Warning: Do not edit this file. It is automatically generated from the
    software project's code and your changes will be overwritten.

    The tool to generate this file lives in openstack-doc-tools repository.

    Please make any changes needed in the code, then run the
    autogenerate-config-doc tool from the openstack-doc-tools repository, or
    ask for help on the documentation mailing list, IRC channel or meeting.

.. _ceilometer-inspector:

.. list-table:: Description of inspector configuration options
   :header-rows: 1
   :class: config-ref-table

   * - Configuration option = Default value
     - Description
   * - **[DEFAULT]**
     -
   * - ``hypervisor_inspector`` = ``libvirt``
     - (String) Inspector to use for inspecting the hypervisor layer. Known inspectors are libvirt, hyperv, vmware, xenapi and powervm.
   * - ``libvirt_type`` = ``kvm``
     - (String) Libvirt domain type.
   * - ``libvirt_uri`` =
     - (String) Override the default libvirt URI (which is dependent on libvirt_type).
