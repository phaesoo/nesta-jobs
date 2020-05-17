CREATE TABLE `snp500_companies` (
    `pit_date` DATE,
    `symbol` VARCHAR(5),
    `security` VARCHAR(100),
    `gics_sector` VARCHAR(100),
    `gics_sub_industry` VARCHAR(100),
    `cik` VARCHAR(10),
    PRIMARY KEY (`pit_date`, `symbol`)
);
