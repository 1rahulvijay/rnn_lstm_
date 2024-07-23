CREATE OR REPLACE FUNCTION convert_blob_to_clob(blob_in BLOB) RETURN CLOB IS
    clob_out CLOB;
BEGIN
    DBMS_LOB.CREATETEMPORARY(clob_out, TRUE);
    DBMS_LOB.CONVERTTOCLOB(clob_out, blob_in, DBMS_LOB.LOBMAXSIZE, 0, 0, DBMS_LOB.DEFAULT_CSID, 1, DBMS_LOB.DEFAULT_LANG_CTX);
    RETURN clob_out;
END;
SELECT DBMS_LOB.SUBSTR(convert_blob_to_clob(blob_column), 16000, 1) AS varchar_column
FROM your_table;
