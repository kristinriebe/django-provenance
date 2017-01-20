-- use:  `cat data/insert_data_simdm.sql | sqlite3 db.sqlite3`
DELETE FROM prov_simdm_party;
DELETE FROM prov_simdm_experiment;
DELETE FROM prov_simdm_protocol;
DELETE FROM prov_simdm_inputparameter;
DELETE FROM prov_simdm_parametersetting;

DELETE FROM prov_simdm_appliedalgorithm;
DELETE FROM prov_simdm_algorithm;


INSERT INTO prov_simdm_protocol (id, name, code, version, description, referenceURL) VALUES
  ("cs:protocol_artsimu", "ART", "[link to ART code]", "--", "Adaptive Refinement Tree code for running cosmological simulatios, Kravtsov et al. 1997, ApJS, 111, 73", "http://adsabs.harvard.edu/abs/1997ApJS..111...73K"),
  ("cs:protocol_fofhf", "FOF", "not public", "--", "Friends-of-Friends cluster finder, applied version is described in Riebe et al. (2013), AN, 334, 691", "http://adsabs.harvard.edu/abs/2013AN....334..691R"),
  ("cs:protocol_fofmtree", "FOF Merger tree", "not public", "--", "Custom code for generating merger tree data from FOF data", "--"),
  ("cs:protocol_rockstartree", "Rockstar tree", "https://bitbucket.org/gfcstanford/rockstar, https://bitbucket.org/pbehroozi/consistent-trees#markdown-header-quick-start-for-rockstar-users", "--", "Code for building Rockstar catalog with consistent merger trees", ""),
  ("cs:protocol_galacticus", "Galacticus", "https://sites.google.com/site/galacticusmodel/", "--", "Galacticus code for semi-analytical galaxies", "")
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

INSERT INTO prov_simdm_inputparameter (id, name, protocol_id, datatype, description) VALUES  -- need multiplicity?
  ("cs:inparam_forceres", "force resolution", "cs:protocol_artsimu", "string", "(Average) force resolution of the code"),
  ("cs:inparam_zini",     "z_ini",            "cs:protocol_artsimu", "float",  "Initial redshift, at which the simulation was started"),
  ("cs:inparam_foflinklen", "linking length", "cs:protocol_fofhf",   "float",  "Relative linking lenth for Friends-of-Friends halo finder")
  ;

INSERT INTO prov_simdm_parametersetting (experiment_id, inputparameter_id, value) VALUES
  ("mdr1:exp_simulation", "cs:inparam_forceres", "7.0 h-1.kpc"),
  ("mdr1:exp_simulation", "cs:inparam_zini", "65.0"),
  ("mdpl2:exp_simulation", "cs:inparam_forceres", "[5.0,13.0]"),
  ("mdpl2:exp_simulation", "cs:inparam_zini", "120.0"),
  ("mdr1:exp_fof", "cs:inparam_foflinklen", "0.17"),
  ("mdr1:exp_fofc", "cs:inparam_foflinklen", "0.2"),
  ("mdpl2:exp_fof", "cs:inparam_foflinklen", "0.17")
  ;

INSERT INTO prov_simdm_algorithm (id, name, protocol_id, description, label) VALUES
  ("cs:algo_art", "Adaptive mesh refinement", "cs:protocol_artsimu", "code uses a grid for calculating potential, forces etc.; grid size is adaptive", ""),
  ("cs:algo_fof", "Friends-of-Friends", "cs:protocol_fofhf", "code uses friends-of-friends algorithm for finding groups of connected particles (clusters)", ""),
  ("cs:algo_phasespace", "Phase-space halo finder", "cs:protocol_rockstartree", "algorithm for finding halos using phase-space information", ""),
  ("cs:algo_sam", "SAM", "cs:protocol_galacticus", "algorithm for finding halos using phase-space information", "")
 ;

INSERT INTO prov_simdm_appliedalgorithm(algorithm_id, experiment_id) VALUES
  ("cs:algo_art", "mdr1:exp_simulation"),
  ("cs:algo_art", "mdpl2:exp_simulation"),
  ("cs:algo_fof", "mdr1:exp_fof"),
  ("cs:algo_fof", "mdr1:exp_fofc"),
  ("cs:algo_fof", "mdpl2:exp_fof"),
  ("cs:algo_phasespace", "mdr1:exp_rockstar"),
  ("cs:algo_phasespace", "mdpl2:exp_rockstar"),
  ("cs:algo_sam", "mdpl2:exp_galacticus")
  ;

