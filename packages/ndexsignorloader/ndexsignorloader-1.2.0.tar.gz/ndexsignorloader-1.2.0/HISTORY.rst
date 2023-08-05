=======
History
=======

1.2.0 (2022-07-06)
-------------------

* Uploaded networks are now public, searchable, showcased, and fully
  indexed by default

* The search for networks to update is done by matching the **labels**
  network attribute first and if no match is found, the name is used

* Fixed bug where some networks were laid out on a single horizontal
  line. This happened when the `location` attribute for all nodes
  in a network were all the same

* Fixed bug where duplicate symbols ended up in `member` attribute of nodes UD-2078

* Uses **labels** network attribute (if found) to find network on NDEx to update instead
  of upload as new. If no **labels** match, then any network matching the **name** of
  network is updated otherwise network is uploaded as a new network. UD-1677

1.1.1 (2020-10-16)
-------------------

* Removed NODE_LABEL_POSITION discrete mapping from style since it is
  not compatible with CX 2.0

1.1.0 (2020-02-19)
-------------------

* Fixed bug where an empty pathway description file would cause loader to fail. Issue #1

* Removed network visual properties: `NETWORK_CENTER_\*, NETWORK_ HEIGHT, NODE_SELECTION, SCALE_FACTOR, SIZE, WIDTH`
  cause they caused problems when displaying the network in Cytoscape

* Fixed bug where URL for DOI in `reference` network attribute was incorrect

* Set minimum version of ndex2 python client to 3.3.1 and maximum to less then 4.0.0

* Set maximum version of ndexutil package to less then 2.0.0

1.0.0 (2019-07-30)
-------------------

* **--edgecollapse** flag added which collapses all edges putting all attributes
  minus **direct** into lists. For **sentence** attribute each entry the
  list is now prepended with href link to citation labeled pubmed:#### In addition,
  if **--edgecollapse** flag is set then a **notes** network attribute is added to
  let user know.

* **--style** can also accept NDEx UUID for network style. Network needs to be on  same
  server set in **--profile**

0.3.0 (2019-07-29)
-------------------

* Added commandline flag **--visibility** that lets user dictate whether NEW networks are public or private (default is public)

* Signor Full Human, Signor Full Rat, and Signor Full Mouse networks have been renamed
  to Signor Complete - Human, Signor Complete - Rat, Signor Complete - Mouse

* On edges, replaced location attribute value of phenotypesList with empty string NSU-75

* Added __iconurl network attribute and renamed type network attribute to networkType

0.2.0 (2019-06-28)
------------------

* Changed prov:wasDerivedFrom network attribute to just signor website URL for full networks

* Removed author network attribute if no value is found

* Removed labels attribute for full networks 

0.1.0 (2019-06-27)
------------------

* First release on PyPI.
