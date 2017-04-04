-- use:  `cat data/delete_data_vo.sql | sqlite3 db.sqlite3`
DELETE FROM prov_vo_activity;
DELETE FROM prov_vo_activitydescription;
DELETE FROM prov_vo_parameter;
DELETE FROM prov_vo_parameterdescription;
DELETE FROM prov_vo_entity;
DELETE FROM prov_vo_entitydescription;
DELETE FROM prov_vo_used;
DELETE FROM prov_vo_useddescription;
DELETE FROM prov_vo_wasgeneratedby;
DELETE FROM prov_vo_wasgeneratedbydescription;
DELETE FROM prov_vo_agent;
DELETE FROM prov_vo_wasassociatedwith;
DELETE FROM prov_vo_wasattributedto;
DELETE FROM prov_vo_wasderivedfrom;
DELETE FROM prov_vo_activityflow;
DELETE FROM prov_vo_hadstep;
