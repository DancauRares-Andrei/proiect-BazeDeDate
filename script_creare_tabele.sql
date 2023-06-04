-- Generated by Oracle SQL Developer Data Modeler 22.2.0.165.1149
--   at:        2022-12-10 17:08:33 EET
--   site:      Oracle Database 11g
--   type:      Oracle Database 11g



-- predefined type, no DDL - MDSYS.SDO_GEOMETRY

-- predefined type, no DDL - XMLTYPE

CREATE TABLE magazie (
    produse_id_p_cr       NUMBER(2) NOT NULL,
    cantitate_disponibila NUMBER(4) NOT NULL,
    pret                  NUMBER(4) NOT NULL
);

ALTER TABLE magazie ADD CONSTRAINT cant_disp_nr_pozitiv CHECK ( cantitate_disponibila > 0 );

ALTER TABLE magazie ADD CONSTRAINT pret_numar_pozitiv CHECK ( pret > 0 );

ALTER TABLE magazie ADD CONSTRAINT magazie_id_p_cr_un UNIQUE ( produse_id_p_cr );

CREATE TABLE nume_producator (
    id_firma   NUMBER(2) NOT NULL,
    nume_firma VARCHAR2(20) NOT NULL
);

ALTER TABLE nume_producator ADD CONSTRAINT nume_producator_pk PRIMARY KEY ( id_firma );

ALTER TABLE nume_producator ADD CONSTRAINT nume_producator_nume_firma_un UNIQUE ( nume_firma );

CREATE TABLE produse (
    id_p_cr                  NUMBER(2) NOT NULL,
    tip_produs_id_produs     NUMBER(2) NOT NULL,
    car_p                    VARCHAR2(20) NOT NULL,
    nume_producator_id_firma NUMBER(2) NOT NULL,
    stare_produs_id_stare    NUMBER(2) NOT NULL
);

ALTER TABLE produse ADD CONSTRAINT produse_pk PRIMARY KEY ( id_p_cr );

CREATE TABLE stare_produs (
    id_stare   NUMBER(2) NOT NULL,
    nume_stare VARCHAR2(20) NOT NULL
);

ALTER TABLE stare_produs
    ADD CONSTRAINT nume_stare_nu_contine_cifre CHECK ( nume_stare NOT LIKE '%0%'
                                                       AND nume_stare NOT LIKE '%1%'
                                                       AND nume_stare NOT LIKE '%2%'
                                                       AND nume_stare NOT LIKE '%3%'
                                                       AND nume_stare NOT LIKE '%4%'
                                                       AND nume_stare NOT LIKE '%5%'
                                                       AND nume_stare NOT LIKE '%6%'
                                                       AND nume_stare NOT LIKE '%7%'
                                                       AND nume_stare NOT LIKE '%8%'
                                                       AND nume_stare NOT LIKE '%9%' );

ALTER TABLE stare_produs ADD CONSTRAINT stare_produs_pk PRIMARY KEY ( id_stare );

ALTER TABLE stare_produs ADD CONSTRAINT stare_produs_nume_stare_un UNIQUE ( nume_stare );

CREATE TABLE tip_produs (
    id_produs       NUMBER(2) NOT NULL,
    nume_tip_produs VARCHAR2(20) NOT NULL
);

ALTER TABLE tip_produs
    ADD CONSTRAINT nume_tip_produs_fara_cifre CHECK ( nume_tip_produs NOT LIKE '%0%'
                                                      AND nume_tip_produs NOT LIKE '%1%'
                                                      AND nume_tip_produs NOT LIKE '%2%'
                                                      AND nume_tip_produs NOT LIKE '%3%'
                                                      AND nume_tip_produs NOT LIKE '%4%'
                                                      AND nume_tip_produs NOT LIKE '%5%'
                                                      AND nume_tip_produs NOT LIKE '%6%'
                                                      AND nume_tip_produs NOT LIKE '%7%'
                                                      AND nume_tip_produs NOT LIKE '%8%'
                                                      AND nume_tip_produs NOT LIKE '%9%' );

ALTER TABLE tip_produs ADD CONSTRAINT tip_produs_pk PRIMARY KEY ( id_produs );

ALTER TABLE tip_produs ADD CONSTRAINT tip_produs_nume_tip_produs_un UNIQUE ( nume_tip_produs );

CREATE TABLE vanzari (
    produse_id_p_cr  NUMBER(2) NOT NULL,
    cantitate_dorita NUMBER(4) NOT NULL,
    data             DATE NOT NULL
);

ALTER TABLE vanzari ADD CONSTRAINT cantitate_dorita_pozitiv CHECK ( cantitate_dorita > 0 );

ALTER TABLE magazie
    ADD CONSTRAINT magazie_produse_fk FOREIGN KEY ( produse_id_p_cr )
        REFERENCES produse ( id_p_cr );

ALTER TABLE produse
    ADD CONSTRAINT produse_nume_producator_fk FOREIGN KEY ( nume_producator_id_firma )
        REFERENCES nume_producator ( id_firma );

ALTER TABLE produse
    ADD CONSTRAINT produse_stare_produs_fk FOREIGN KEY ( stare_produs_id_stare )
        REFERENCES stare_produs ( id_stare );

ALTER TABLE produse
    ADD CONSTRAINT produse_tip_produs_fk FOREIGN KEY ( tip_produs_id_produs )
        REFERENCES tip_produs ( id_produs );

ALTER TABLE vanzari
    ADD CONSTRAINT vanzari_produse_fk FOREIGN KEY ( produse_id_p_cr )
        REFERENCES produse ( id_p_cr );

CREATE SEQUENCE nume_producator_id_firma_seq START WITH 1 NOCACHE ORDER;

CREATE OR REPLACE TRIGGER nume_producator_id_firma_trg BEFORE
    INSERT ON nume_producator
    FOR EACH ROW
    WHEN ( new.id_firma IS NULL )
BEGIN
    :new.id_firma := nume_producator_id_firma_seq.nextval;
END;
/

CREATE SEQUENCE produse_id_p_cr_seq START WITH 1 NOCACHE ORDER;

CREATE OR REPLACE TRIGGER produse_id_p_cr_trg BEFORE
    INSERT ON produse
    FOR EACH ROW
    WHEN ( new.id_p_cr IS NULL )
BEGIN
    :new.id_p_cr := produse_id_p_cr_seq.nextval;
END;
/

CREATE SEQUENCE stare_produs_id_stare_seq START WITH 1 NOCACHE ORDER;

CREATE OR REPLACE TRIGGER stare_produs_id_stare_trg BEFORE
    INSERT ON stare_produs
    FOR EACH ROW
    WHEN ( new.id_stare IS NULL )
BEGIN
    :new.id_stare := stare_produs_id_stare_seq.nextval;
END;
/

CREATE SEQUENCE tip_produs_id_produs_seq START WITH 1 NOCACHE ORDER;

CREATE OR REPLACE TRIGGER tip_produs_id_produs_trg BEFORE
    INSERT ON tip_produs
    FOR EACH ROW
    WHEN ( new.id_produs IS NULL )
BEGIN
    :new.id_produs := tip_produs_id_produs_seq.nextval;
END;
/



-- Oracle SQL Developer Data Modeler Summary Report: 
-- 
-- CREATE TABLE                             6
-- CREATE INDEX                             0
-- ALTER TABLE                             18
-- CREATE VIEW                              0
-- ALTER VIEW                               0
-- CREATE PACKAGE                           0
-- CREATE PACKAGE BODY                      0
-- CREATE PROCEDURE                         0
-- CREATE FUNCTION                          0
-- CREATE TRIGGER                           4
-- ALTER TRIGGER                            0
-- CREATE COLLECTION TYPE                   0
-- CREATE STRUCTURED TYPE                   0
-- CREATE STRUCTURED TYPE BODY              0
-- CREATE CLUSTER                           0
-- CREATE CONTEXT                           0
-- CREATE DATABASE                          0
-- CREATE DIMENSION                         0
-- CREATE DIRECTORY                         0
-- CREATE DISK GROUP                        0
-- CREATE ROLE                              0
-- CREATE ROLLBACK SEGMENT                  0
-- CREATE SEQUENCE                          4
-- CREATE MATERIALIZED VIEW                 0
-- CREATE MATERIALIZED VIEW LOG             0
-- CREATE SYNONYM                           0
-- CREATE TABLESPACE                        0
-- CREATE USER                              0
-- 
-- DROP TABLESPACE                          0
-- DROP DATABASE                            0
-- 
-- REDACTION POLICY                         0
-- 
-- ORDS DROP SCHEMA                         0
-- ORDS ENABLE SCHEMA                       0
-- ORDS ENABLE OBJECT                       0
-- 
-- ERRORS                                   0
-- WARNINGS                                 0