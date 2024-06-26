import duckdb
import os

URL = "s3://projet-ape/log_files/dashboard/**/*.parquet"

con = duckdb.connect(database=":memory:")


LIST_VAR = """date, "Response.1.code" """
# Setting up S3 connection
con.execute(f"""
SET s3_endpoint='{os.getenv("AWS_S3_ENDPOINT")}';
SET s3_access_key_id='{os.getenv("AWS_ACCESS_KEY_ID")}';
SET s3_secret_access_key='{os.getenv("AWS_SECRET_ACCESS_KEY")}';
SET s3_session_token='';

CREATE TABLE naf_sections_mapping (
    code VARCHAR(10),
    section CHAR(1)
);

-- Insert mappings into the table
INSERT INTO naf_sections_mapping (code, section) VALUES
('01', 'A'), ('02', 'A'), ('03', 'A'), ('05', 'B'), ('06', 'B'), ('07', 'B'), ('08', 'B'), ('09', 'B'), ('10', 'C'), ('11', 'C'), ('12', 'C'), ('13', 'C'), ('14', 'C'), ('15', 'C'), ('16', 'C'), ('17', 'C'), ('18', 'C'), ('19', 'C'), ('20', 'C'), ('21', 'C'), ('22', 'C'), ('23', 'C'), ('24', 'C'), ('25', 'C'), ('26', 'C'), ('27', 'C'), ('28', 'C'), ('29', 'C'), ('30', 'C'), ('31', 'C'), ('32', 'C'), ('33', 'C'), ('35', 'D'), ('36', 'E'), ('37', 'E'), ('38', 'E'), ('39', 'E'), ('41', 'F'), ('42', 'F'), ('43', 'F'), ('45', 'G'), ('46', 'G'), ('47', 'G'), ('49', 'H'), ('50', 'H'), ('51', 'H'), ('52', 'H'), ('53', 'H'), ('55', 'I'), ('56', 'I'), ('58', 'J'), ('59', 'J'), ('60', 'J'), ('61', 'J'), ('62', 'J'), ('63', 'J'), ('64', 'K'), ('65', 'K'), ('66', 'K'), ('68', 'L'), ('69', 'M'), ('70', 'M'), ('71', 'M'), ('72', 'M'), ('73', 'M'), ('74', 'M'), ('75', 'M'), ('77', 'N'), ('78', 'N'), ('79', 'N'), ('80', 'N'), ('81', 'N'), ('82', 'N'), ('84', 'O'), ('85', 'P'), ('86', 'Q'), ('87', 'Q'), ('88', 'Q'), ('90', 'R'), ('91', 'R'), ('92', 'R'), ('93', 'R'), ('94', 'S'), ('95', 'S'), ('96', 'S'), ('97', 'T'), ('98', 'T'), ('99', 'U');


COPY(
    SELECT
        {LIST_VAR},
        CASE
            WHEN "Response.IC" > 1 THEN 1
            ELSE "Response.IC"
        END AS "Response.IC",
        "Response.1.code" AS "Sous-classe",
        SUBSTRING("Response.1.code", 1, 4) AS Classe,
        SUBSTRING("Response.1.code", 1, 3) AS Groupe,
        response1.Section AS Section,
        response1.code AS Division
    FROM
        read_parquet('{URL}', hive_partitioning=1)
    LEFT JOIN
        naf_sections_mapping response1 ON SUBSTRING("Response.1.code", 1, 2) = response1.code
    ) TO STDOUT (FORMAT 'parquet', COMPRESSION 'gzip');
""")


con.close()
