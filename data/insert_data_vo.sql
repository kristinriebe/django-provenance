-- use:  `cat data/insert_data_w3c.sql | sqlite3 db.sqlite3`
DELETE FROM prov_vo_activity;
DELETE FROM prov_vo_entity;
DELETE FROM prov_vo_used;
DELETE FROM prov_vo_wasGeneratedBy;
DELETE FROM prov_vo_agent;
DELETE FROM prov_vo_agent;
DELETE FROM prov_vo_wasassociatedwith;
DELETE FROM prov_vo_wasattributedto;

INSERT INTO prov_vo_activity (id, label, type, subtype, code, parameter, description, startTime, endTime, docuLink) VALUES 
  ("mdr1:act_simulation", "MDR1 simulation", "cs:simulation", "", "ART", "{force resolution: , starting redshift: ...}", "The simulation MultiDark Run 1","2012", "2012", "Prada et al. (2012), MNRAS, 423, 3018, http://adsabs.harvard.edu/abs/2012MNRAS.423.3018P"),
  ("mdr1:act_fof", "MDR1 FOF halo finding", "cs:post-processing", "cs:halofinder", "FOF", "{rel. linking length: 0.17}", "Running the FOF halo finder, basic linking length 0.17", "-", "-", "Riebe et al. (2013), AN, 334, 691, http://adsabs.harvard.edu/abs/2013AN....334..691R"),
  ("mdr1:act_fofc", "MDR1 FOFc halo finding, c-version", "cs:post-processing", "cs:halofinder", "FOF", "{rel. linking length: 0.2}", "Running the FOF halo finder, basic linking length 0.2", "-", "-", "Riebe et al. (2013), AN, 334, 691, http://adsabs.harvard.edu/abs/2013AN....334..691R"),
  ("mdr1:act_fofmtree", "MDR1 FOFMtree building", "cs:post-processing", "cs:mergertreebuilding", "FOF tree builder", "{}", "Building the merger tree for a FOF halo finder", "-", "-", "-"),
  ("mdr1:act_rockstar", "MDR1 Rockstar building", "cs:post-processing", "cs:mergertreebuilding", "Rockstar", "{}", "Building the Rockstar catalog + merger tree", "-", "-", "-"),
  ("mdpl2:act_simulation", "MDPL2 simulation", "cs:simulation", "", "ART", "{}", "The MDPL2 simulation","2014", "2014", "Klypin, Yepes, Gottlöber, Prada, Heß, (2016) MNRAS 457, 4340, http://adsabs.harvard.edu/abs/2012MNRAS.423.3018P"),
  ("mdpl2:act_fof", "MDPL2 FOF halo finding", "cs:post-processing", "cs:halofinder", "FOF", "{}", "Running the FOF halo finder, basic linking length 0.17", "-", "-", "Riebe et al. (2013), AN, 334, 691, http://adsabs.harvard.edu/abs/2013AN....334..691R"),
  ("mdpl2:act_rockstar", "MDPL2 Rockstar building", "cs:post-processing", "cs:mergertreebuilding", "Rockstar", "{}", "Building the Rockstar catalog + merger tree", "-", "-", "-"),
  ("mdpl2:act_galacticus", "Running Galacticus on MDPL2", "cs:post-processing", "cs:galaxybuilding", "Galacticus", "{}", "Building the Galacticus galaxy catalog", "2015-07-01", "2015-09-01", "Behroozi, Wechsler and Wu, 2013, APJ 762, 109")
  ;
-- version?
-- where should I store the code?

INSERT INTO prov_vo_entity (id, label, type, location, access, size, format, description, docuLink, dataproduct_type, dataproduct_subtype, level) VALUES
  ("mdr1:snapshots", "MDR1 simulation snapshots", "voprov:catalog", "erebos.aip.de", 
    "internal", "some GB", "binary-files", "The raw files in original format, partially also uploaded to the database",
    "", "catalog", "", "0"),
  ("mdr1:fof", "MDR1 FOF catalog", "voprov:catalog", "https://www.cosmosim.org/", 
    "public", "some GB", "database-table", "FOF tables (FOF, FOF1, ... FOF4) with object properties for different times and linking lengths",
    "", "catalog", "", "1"),
  ("mdr1:fofc", "MDR1 FOFc catalog", "voprov:catalog", "https://www.cosmosim.org/", 
    "public", "some GB", "database-table", "FOFc table with object properties for different times",
    "", "catalog", "", "1"),
  ("mdr1:fofmtree", "MDR1 FOF mtree", "voprov:catalog", "https://www.cosmosim.org/", 
    "public", "some GB", "database-table", "FOF merger tree",
    "", "catalog", "", "1"),
  ("mdr1:rockstar", "MDR1 Rockstar catalog+trees", "voprov:catalog", "https://www.cosmosim.org/", 
    "public", "some GB", "database-table", "Rockstar table including merger trees",
    "", "catalog", "", "1"),
  ("mdpl2:snapshots", "MDPL2 simulation snapshots", "voprov:catalog", "erebos.aip.de", 
    "internal", "some GB", "binary-files", "The raw files in original format, partially also uploaded to the database",
    "", "catalog", "", "0"),
  ("mdpl2:fof", "MDPL2 FOF catalog", "voprov:catalog", "https://www.cosmosim.org/", 
    "public", "some GB", "database-table", "FOF tables (FOF, FOF1, ... FOF5) with object properties for different times and linking lengths",
    "", "catalog", "", "1"),
  ("mdpl2:rockstar", "MDPL2 Rockstar catalog+trees", "voprov:catalog", "https://www.cosmosim.org/", 
    "public", "some GB", "database-table", "Rockstar table including merger trees",
    "", "catalog", "", "1"),
  ("mdpl2:galacticus", "MDPL2 Galacticus catalog", "voprov:catalog", "https://www.cosmosim.org/", 
    "public", "some GB", "database-table", "Galacticus galaxy catalog, SAM",
    "", "catalog", "", "1")
  ;

-- what if:
-- * an entitity consists of multiple datasets? (e.g. "FOF" entity, but tables FOF, FOF1 to FOF5 belong to this)
-- * an entitity is a combination of different types of datasets (e.g. Rockstar =catalog+consistent merger trees!)

INSERT INTO prov_vo_used(activity_id, entity_id, role) VALUES
  ("mdr1:act_fof", "mdr1:snapshots", "simulation raw data"),
  ("mdr1:act_fofc", "mdr1:snapshots", "simulation raw data"),
  ("mdr1:act_rockstar", "mdr1:snapshots", "simulation raw data"),
  ("mdr1:act_fofmtree", "mdr1:fof", "halo catalogue"),
  ("mdpl2:act_fof", "mdpl2:snapshots", "simulation raw data"),
  ("mdpl2:act_rockstar", "mdpl2:snapshots", "simulation raw data"),
  ("mdpl2:act_galacticus", "mdpl2:rockstar", "halo catalogue")
  ;

INSERT INTO prov_vo_wasgeneratedby(entity_id, activity_id, role) VALUES
  ("mdr1:snapshots", "mdr1:act_simulation", "simulation raw data"),
  ("mdr1:fof", "mdr1:act_fof", "halo catalogue"),
  ("mdr1:fofc", "mdr1:act_fofc", "halo catalogue"),
  ("mdr1:rockstar", "mdr1:act_rockstar", "halo catalogue"),
  ("mdr1:fofmtree", "mdr1:act_fofmtree", "merger tree"),
  ("mdpl2:snapshots", "mdpl2:act_simulation", "simulation raw data"),
  ("mdpl2:fof", "mdpl2:act_fof", "halo catalogue"),
  ("mdpl2:rockstar", "mdpl2:act_rockstar", "halo catalogue"),
  ("mdpl2:galacticus", "mdpl2:act_galacticus", "halo catalogue")
  ;

INSERT INTO prov_vo_agent(id, label, type, description, affiliation) VALUES
  ("cs:Stefan_Gottloeber", "Stefan Gottlöber", "prov:Person", "", "AIP, Potsdam, Germany"),
  ("cs:Jaime_Forero_Romero", "Jaime Forero-Romero", "prov:Person", "", "AIP, Potsdam, Germany"),
  ("cs:Gustavo_Yepes", "Gustavo Yepes", "prov:Person", "", "UAM, Madrid, Spain"),
  ("cs:Peter_Behroozi", "Peter Behroozi", "prov:Person", "", "UC Berkeley, Berkeley, USA"),
  ("cs:Christoph_Behrens", "Christoph Behrens", "prov:Person", "", "Georg-August-Universität Göttingen, Göttingen, Germany"),
  ("cs:MultiDark", "MultiDark project", "prov:organization", "", "Spain+Germany+USA")
  ;

INSERT INTO prov_vo_wasassociatedwith(activity_id, agent_id, role) VALUES
  ("mdr1:act_simulation", "cs:Gustavo_Yepes", "operator"),
  ("mdpl2:act_simulation", "cs:Gustavo_Yepes", "operator"),
  ("mdr1:act_fof", "cs:Stefan_Gottloeber", "operator"),
  ("mdr1:act_fofc", "cs:Stefan_Gottloeber", "operator"),
  ("mdr1:act_fofmtree", "cs:Jaime_Forero_Romero", "operator"),
  ("mdr1:act_rockstar", "cs:Peter_Behroozi", "operator"),
  ("mdpl2:act_fof", "cs:Stefan_Gottloeber", "operator"),
  ("mdpl2:act_rockstar", "cs:Peter_Behroozi", "operator"),
  ("mdpl2:act_galacticus", "cs:Christoph_Behrens", "operator")
  ;
--  ("mdpl2:act_galacticus", "cs:Andrew_Benson", "creator"),

INSERT INTO prov_vo_wasattributedto(entity_id, agent_id, role) VALUES
  ("mdr1:snapshots", "cs:MultiDark", "publisher"),
  ("mdr1:fof", "cs:MultiDark", "publisher"),
  ("mdr1:fofc", "cs:MultiDark", "publisher"),
  ("mdr1:rockstar", "cs:MultiDark", "publisher"),
  ("mdr1:fofmtree", "cs:MultiDark", "publisher"),
  ("mdpl2:snapshots", "cs:MultiDark", "publisher"),
  ("mdpl2:fof", "cs:MultiDark", "publisher"),
  ("mdpl2:rockstar", "cs:MultiDark", "publisher"),
  ("mdpl2:galacticus", "cs:MultiDark", "publisher")
  ;


