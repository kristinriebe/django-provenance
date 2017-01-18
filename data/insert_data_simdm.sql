-- use:  `cat data/insert_data_simdm.sql | sqlite3 db.sqlite3`
DELETE FROM prov_simdm_party;
DELETE FROM prov_simdm_experiment;
DELETE FROM prov_simdm_protocol;

DELETE FROM prov_simdm_appliedalgorithm;
DELETE FROM prov_simdm_algorithm;


INSERT INTO prov_simdm_protocol (id, name, code, version) VALUES
  ("cs:protocol_artsimu", "ART", "ART link", "--"), -- should be "various" in code, but in fact using only 1 here.
  ("cs:protocol_fofhf", "FOF", "FOF link", "--"),
  ("cs:protocol_fofmtree", "FOF Merger tree", "not public", "--"),
  ("cs:protocol_rockstartree", "Rockstar tree", "https://bitbucket.org/gfcstanford/rockstar, https://bitbucket.org/pbehroozi/consistent-trees#markdown-header-quick-start-for-rockstar-users", "--"),
  ("cs:protocol_galacticus", "Galacticus", "https://sites.google.com/site/galacticusmodel/", "--")
  ;

INSERT INTO prov_simdm_experiment (id, name, protocol_id, executiontime) VALUES
  ("mdr1:exp_simulation", "MDR1 simulation", "cs:protocol_artsimu", "2010"),  --, "Prada et al. (2012), MNRAS, 423, 3018, http://adsabs.harvard.edu/abs/2012MNRAS.423.3018P"),
  ("mdpl2:exp_simulation", "MDPL2 simulation", "cs:protocol_artsimu", "2014"), --"Klypin, Yepes, Gottlöber, Prada, Heß, (2016) MNRAS 457, 4340"),
  ("mdr1:exp_fof", "MDR1 FOF halo finding", "cs:protocol_fofhf", "2010-11-09"),
  ("mdr1:exp_fofc", "MDR1 FOFc halo finding, c-version", "cs:protocol_fofhf", "2010-08-29"),
  ("mdr1:exp_fofmtree", "MDR1 FOFMtree building", "cs:protocol_fofmtree", "2011"),
  ("mdr1:exp_rockstar", "MDR1 Rockstar building", "cs:protocol_rockstartree", "2015-06-20"),
  ("mdpl2:exp_fof", "MDPL2 FOF halo finding", "cs:protocol_fofhf", "-"),
  ("mdpl2:exp_rockstar", "MDPL2 Rockstar building", "cs:protocol_rockstartree", "2015-09-01"),
  ("mdpl2:exp_galacticus", "Running Galacticus on MDPL2", "cs:protocol_galacticus", "2015-10-01")
  ;