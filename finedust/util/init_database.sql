DROP SCHEMA IF EXISTS `sep545`;
CREATE SCHEMA `sep545`;
USE `sep545`;

-- MySQL Workbench Synchronization
-- Generated: 2017-07-29 01:22
-- Model: New Model
-- Version: 1.0
-- Project: Name of the project
-- Author: user

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='TRADITIONAL,ALLOW_INVALID_DATES';

CREATE TABLE IF NOT EXISTS `sep545`.`custom_article` (
  `article_id` INT(11) NOT NULL,
  `writer` VARCHAR(45) NOT NULL,
  `date` DATETIME NOT NULL,
  `content` VARCHAR(512) NOT NULL,
  `region` INT(11) NOT NULL,
  `crawler` INT(11) NOT NULL,
  `data` INT(11) NOT NULL,
  PRIMARY KEY (`article_id`),
  INDEX `data_idx` (`data` ASC),
  INDEX `crawling_event_idx` (`crawler` ASC),
  INDEX `region_idx` (`region` ASC),
  UNIQUE INDEX `article_id_UNIQUE` (`article_id` ASC),
  CONSTRAINT `region1`
    FOREIGN KEY (`region`)
    REFERENCES `sep545`.`region` (`region_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `crawling_event1`
    FOREIGN KEY (`crawler`)
    REFERENCES `sep545`.`crawling_event` (`crawling_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `data1`
    FOREIGN KEY (`data`)
    REFERENCES `sep545`.`finedust_data` (`data_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8;

CREATE TABLE IF NOT EXISTS `sep545`.`region_category` (
  `category_id` INT(11) NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`category_id`),
  UNIQUE INDEX `name_UNIQUE` (`name` ASC))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8;

CREATE TABLE IF NOT EXISTS `sep545`.`region` (
  `region_id` INT(11) NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(45) NOT NULL,
  `eng_name` VARCHAR(45) NULL DEFAULT NULL,
  `category` INT(11) NULL DEFAULT NULL,
  PRIMARY KEY (`region_id`),
  INDEX `category_idx` (`category` ASC),
  CONSTRAINT `category`
    FOREIGN KEY (`category`)
    REFERENCES `sep545`.`region_category` (`category_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8;

CREATE TABLE IF NOT EXISTS `sep545`.`source_info` (
  `source_id` INT(11) NOT NULL AUTO_INCREMENT,
  `desc` VARCHAR(512) NULL DEFAULT NULL,
  `url` VARCHAR(512) NULL DEFAULT NULL,
  PRIMARY KEY (`source_id`),
  UNIQUE INDEX `url_UNIQUE` (`url` ASC))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8;

CREATE TABLE IF NOT EXISTS `sep545`.`crawling_event` (
  `crawling_id` INT(11) NOT NULL AUTO_INCREMENT,
  `date` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `source` INT(11) NOT NULL,
  PRIMARY KEY (`crawling_id`),
  INDEX `source_idx` (`source` ASC),
  CONSTRAINT `source1`
    FOREIGN KEY (`source`)
    REFERENCES `sep545`.`source_info` (`source_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8;

CREATE TABLE IF NOT EXISTS `sep545`.`finedust_data` (
  `data_id` INT(11) NOT NULL AUTO_INCREMENT,
  `info` INT(11) NOT NULL,
  `data_min` INT(11) NULL DEFAULT NULL,
  `data_max` INT(11) NULL DEFAULT NULL,
  `data_avg` INT(11) NOT NULL,
  PRIMARY KEY (`data_id`),
  INDEX `info_id_idx` (`info` ASC),
  CONSTRAINT `info_id1`
    FOREIGN KEY (`info`)
    REFERENCES `sep545`.`finedust_info` (`info_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8;

CREATE TABLE IF NOT EXISTS `sep545`.`finedust_info` (
  `info_id` INT(11) NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`info_id`),
  UNIQUE INDEX `name_UNIQUE` (`name` ASC))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8;

CREATE TABLE IF NOT EXISTS `sep545`.`open_api` (
  `open_id` INT(11) NOT NULL AUTO_INCREMENT,
  `time` DATETIME NOT NULL,
  `region` INT(11) NOT NULL,
  `crawler` INT(11) NOT NULL,
  `data` INT(11) NOT NULL,
  PRIMARY KEY (`open_id`),
  INDEX `data_idx` (`data` ASC),
  INDEX `crawling_event_idx` (`crawler` ASC),
  INDEX `region3_idx` (`region` ASC),
  CONSTRAINT `region3`
    FOREIGN KEY (`region`)
    REFERENCES `sep545`.`region` (`region_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `data3`
    FOREIGN KEY (`data`)
    REFERENCES `sep545`.`finedust_data` (`data_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `crawling_event3`
    FOREIGN KEY (`crawler`)
    REFERENCES `sep545`.`crawling_event` (`crawling_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8;

CREATE TABLE IF NOT EXISTS `sep545`.`telegram_user` (
  `chat_id` INT(11) NOT NULL,
  `start_date` DATETIME NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`chat_id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8;

CREATE TABLE IF NOT EXISTS `sep545`.`favorite_region` (
  `favorite_id` INT(11) NOT NULL AUTO_INCREMENT,
  `user` INT(11) NOT NULL,
  `region` INT(11) NOT NULL,
  PRIMARY KEY (`favorite_id`),
  INDEX `region_idx` (`region` ASC),
  INDEX `user_idx` (`user` ASC),
  CONSTRAINT `user14`
    FOREIGN KEY (`user`)
    REFERENCES `sep545`.`telegram_user` (`chat_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `region4`
    FOREIGN KEY (`region`)
    REFERENCES `sep545`.`region_category` (`category_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;



-- crawling source
INSERT INTO `source_info` (`source_id`, `desc`, `url`)
	VALUES ('0', '국내 사용자 미세먼지 정보',  'http://cafe.naver.com/dustout2');

INSERT INTO `source_info` (`source_id`, `desc`, `url`)
	VALUES ('0', '중국 미세먼지 정보',  'https://api.waqi.info/api/feed/@');

INSERT INTO `source_info` (`source_id`, `desc`, `url`)
	VALUES ('0', '국내 미세먼지 정보',  'http://openapi.airkorea.or.kr/openapi/services/rest/ArpltnInforInqireSvc/getMinuDustFrcstDspth?searchDate=');


-- crawling source
INSERT INTO `finedust_info`
	VALUES ('0', 'PM25'), ('0', 'PM10'), ('0', 'O3'), ('0', 'NO2'), ('0', 'SO2'), ('0', 'CO'), ('0', 'TEMP'),('0', 'DEW'),('0', 'PRESSURE'),('0', 'HUMID'),('0', 'WIND');

-- region_category
INSERT INTO `region_category` (`category_id`, `name`) VALUES ('1', '서울시');
INSERT INTO `region_category` (`category_id`, `name`) VALUES ('2', '경기도');
INSERT INTO `region_category` (`category_id`, `name`) VALUES ('3', '강원도');
INSERT INTO `region_category` (`category_id`, `name`) VALUES ('4', '충청도');
INSERT INTO `region_category` (`category_id`, `name`) VALUES ('5', '경상도');
INSERT INTO `region_category` (`category_id`, `name`) VALUES ('6', '전라도');
INSERT INTO `region_category` (`category_id`, `name`) VALUES ('7', '제주도');
INSERT INTO `region_category` (`category_id`, `name`) VALUES ('8', '대한민국');
INSERT INTO `region_category` (`category_id`, `name`) VALUES ('9', '중국');


-- region
INSERT INTO `region` (`region_id`, `name`, `eng_name`, `category`) VALUES ('1', '동작, 관악', '동작, 관악', '1');
INSERT INTO `region` (`region_id`, `name`, `eng_name`, `category`) VALUES ('2', '성북, 강북, 도봉', '성북, 강북, 도봉', '1');
INSERT INTO `region` (`region_id`, `name`, `eng_name`, `category`) VALUES ('3', '광진, 성동, 동대문', '광진, 성동, 동대문', '1');
INSERT INTO `region` (`region_id`, `name`, `eng_name`, `category`) VALUES ('4', '송파, 강동', '송파, 강동', '1');
INSERT INTO `region` (`region_id`, `name`, `eng_name`, `category`) VALUES ('5', '마포, 은평, 서대문', '마포, 은평, 서대문', '1');
INSERT INTO `region` (`region_id`, `name`, `eng_name`, `category`) VALUES ('6', '구로, 금천, 영등포', '구로, 금천, 영등포', '1');
INSERT INTO `region` (`region_id`, `name`, `eng_name`, `category`) VALUES ('7', '강서, 양천', '강서, 양천', '1');
INSERT INTO `region` (`region_id`, `name`, `eng_name`, `category`) VALUES ('8', '강남, 서초', '강남, 서초', '1');
INSERT INTO `region` (`region_id`, `name`, `eng_name`, `category`) VALUES ('9', '노원, 중랑', '노원, 중랑', '1');
INSERT INTO `region` (`region_id`, `name`, `eng_name`, `category`) VALUES ('10', '종로, 중구, 용산', '종로, 중구, 용산', '1');
INSERT INTO `region` (`region_id`, `name`, `eng_name`, `category`) VALUES ('11', '인천광역시', '인천광역시', '2');
INSERT INTO `region` (`region_id`, `name`, `eng_name`, `category`) VALUES ('12', '양평, 가평', '양평, 가평', '2');
INSERT INTO `region` (`region_id`, `name`, `eng_name`, `category`) VALUES ('13', '수원(영통,팔달,장안,권선)', '수원(영통,팔달,장안,권선)', '2');
INSERT INTO `region` (`region_id`, `name`, `eng_name`, `category`) VALUES ('14', '안산, 시흥', '안산, 시흥', '2');
INSERT INTO `region` (`region_id`, `name`, `eng_name`, `category`) VALUES ('15', '광주', '광주', '2');
INSERT INTO `region` (`region_id`, `name`, `eng_name`, `category`) VALUES ('16', '파주, 일산, 덕양', '파주, 일산, 덕양', '2');
INSERT INTO `region` (`region_id`, `name`, `eng_name`, `category`) VALUES ('17', '광명', '광명', '2');
INSERT INTO `region` (`region_id`, `name`, `eng_name`, `category`) VALUES ('18', '성남, 분당, 판교', '성남, 분당, 판교', '2');
INSERT INTO `region` (`region_id`, `name`, `eng_name`, `category`) VALUES ('19', '여주, 이천', '여주, 이천', '2');
INSERT INTO `region` (`region_id`, `name`, `eng_name`, `category`) VALUES ('20', '용인(처인,기흥,수지)', '용인(처인,기흥,수지)', '2');
INSERT INTO `region` (`region_id`, `name`, `eng_name`, `category`) VALUES ('21', '남양주, 구리, 하남', '남양주, 구리, 하남', '2');
INSERT INTO `region` (`region_id`, `name`, `eng_name`, `category`) VALUES ('22', '평택, 안성, 송탄', '평택, 안성, 송탄', '2');
INSERT INTO `region` (`region_id`, `name`, `eng_name`, `category`) VALUES ('23', '부천', '부천', '2');
INSERT INTO `region` (`region_id`, `name`, `eng_name`, `category`) VALUES ('24', '화성, 오산', '화성, 오산', '2');
INSERT INTO `region` (`region_id`, `name`, `eng_name`, `category`) VALUES ('25', '과천,안양,군포,의왕', '과천,안양,군포,의왕', '2');
INSERT INTO `region` (`region_id`, `name`, `eng_name`, `category`) VALUES ('26', '의정부, 양주, 장흥', '의정부, 양주, 장흥', '2');
INSERT INTO `region` (`region_id`, `name`, `eng_name`, `category`) VALUES ('27', '포천, 연천, 동두천', '포천, 연천, 동두천', '2');
INSERT INTO `region` (`region_id`, `name`, `eng_name`, `category`) VALUES ('28', '김포, 강화', '김포, 강화', '2');
INSERT INTO `region` (`region_id`, `name`, `eng_name`, `category`) VALUES ('29', '원주, 문막, 횡성', '원주, 문막, 횡성', '3');
INSERT INTO `region` (`region_id`, `name`, `eng_name`, `category`) VALUES ('30', '춘천, 홍천, 양구', '춘천, 홍천, 양구', '3');
INSERT INTO `region` (`region_id`, `name`, `eng_name`, `category`) VALUES ('31', '평창, 정선, 태백, 영월', '평창, 정선, 태백, 영월', '3');
INSERT INTO `region` (`region_id`, `name`, `eng_name`, `category`) VALUES ('32', '철원, 화천', '철원, 화천', '3');
INSERT INTO `region` (`region_id`, `name`, `eng_name`, `category`) VALUES ('33', '강릉, 동해, 삼척', '강릉, 동해, 삼척', '3');
INSERT INTO `region` (`region_id`, `name`, `eng_name`, `category`) VALUES ('34', '속초, 양양, 고성, 인제', '속초, 양양, 고성, 인제', '3');
INSERT INTO `region` (`region_id`, `name`, `eng_name`, `category`) VALUES ('35', '대전광역시', '대전광역시', '4');
INSERT INTO `region` (`region_id`, `name`, `eng_name`, `category`) VALUES ('36', '보은, 옥천, 영동', '보은, 옥천, 영동', '4');
INSERT INTO `region` (`region_id`, `name`, `eng_name`, `category`) VALUES ('37', '충주, 제천, 단양', '충주, 제천, 단양', '4');
INSERT INTO `region` (`region_id`, `name`, `eng_name`, `category`) VALUES ('38', '음성, 진천, 괴산, 증평', '음성, 진천, 괴산, 증평', '4');
INSERT INTO `region` (`region_id`, `name`, `eng_name`, `category`) VALUES ('39', '청주', '청주', '4');
INSERT INTO `region` (`region_id`, `name`, `eng_name`, `category`) VALUES ('40', '세종시, 공주', '세종시, 공주', '4');
INSERT INTO `region` (`region_id`, `name`, `eng_name`, `category`) VALUES ('41', '천안, 아산', '천안, 아산', '4');
INSERT INTO `region` (`region_id`, `name`, `eng_name`, `category`) VALUES ('42', '청양, 예산', '청양, 예산', '4');
INSERT INTO `region` (`region_id`, `name`, `eng_name`, `category`) VALUES ('43', '서산, 당진, 태안', '서산, 당진, 태안', '4');
INSERT INTO `region` (`region_id`, `name`, `eng_name`, `category`) VALUES ('44', '논산, 계룡, 부여, 금산', '논산, 계룡, 부여, 금산', '4');
INSERT INTO `region` (`region_id`, `name`, `eng_name`, `category`) VALUES ('45', '보령, 홍성, 서천', '보령, 홍성, 서천', '4');
INSERT INTO `region` (`region_id`, `name`, `eng_name`, `category`) VALUES ('46', '대구', '대구', '5');
INSERT INTO `region` (`region_id`, `name`, `eng_name`, `category`) VALUES ('47', '부산', '부산', '5');
INSERT INTO `region` (`region_id`, `name`, `eng_name`, `category`) VALUES ('48', '울산', '울산', '5');
INSERT INTO `region` (`region_id`, `name`, `eng_name`, `category`) VALUES ('49', '창원', '창원', '5');
INSERT INTO `region` (`region_id`, `name`, `eng_name`, `category`) VALUES ('50', '문경, 예천, 영주, 상주', '문경, 예천, 영주, 상주', '5');
INSERT INTO `region` (`region_id`, `name`, `eng_name`, `category`) VALUES ('51', '김천, 구미, 칠곡', '김천, 구미, 칠곡', '5');
INSERT INTO `region` (`region_id`, `name`, `eng_name`, `category`) VALUES ('52', '봉화, 울진, 영양, 양덕', '봉화, 울진, 영양, 양덕', '5');
INSERT INTO `region` (`region_id`, `name`, `eng_name`, `category`) VALUES ('53', '안동, 의성, 청송', '안동, 의성, 청송', '5');
INSERT INTO `region` (`region_id`, `name`, `eng_name`, `category`) VALUES ('54', '성주, 고령', '성주, 고령', '5');
INSERT INTO `region` (`region_id`, `name`, `eng_name`, `category`) VALUES ('55', '포항, 경주', '포항, 경주', '5');
INSERT INTO `region` (`region_id`, `name`, `eng_name`, `category`) VALUES ('56', '영천, 군위, 경산, 청도', '영천, 군위, 경산, 청도', '5');
INSERT INTO `region` (`region_id`, `name`, `eng_name`, `category`) VALUES ('57', '김해, 양산, 밀양', '김해, 양산, 밀양', '5');
INSERT INTO `region` (`region_id`, `name`, `eng_name`, `category`) VALUES ('58', '합천, 창녕, 의령, 함안', '합천, 창녕, 의령, 함안', '5');
INSERT INTO `region` (`region_id`, `name`, `eng_name`, `category`) VALUES ('59', '거창, 함양, 산청', '거창, 함양, 산청', '5');
INSERT INTO `region` (`region_id`, `name`, `eng_name`, `category`) VALUES ('60', '하동, 진주, 사천, 남해', '하동, 진주, 사천, 남해', '5');
INSERT INTO `region` (`region_id`, `name`, `eng_name`, `category`) VALUES ('61', '고성, 통영, 거제', '고성, 통영, 거제', '5');
INSERT INTO `region` (`region_id`, `name`, `eng_name`, `category`) VALUES ('62', '광주', '광주', '6');
INSERT INTO `region` (`region_id`, `name`, `eng_name`, `category`) VALUES ('63', '부안, 정읍, 고창', '부안, 정읍, 고창', '6');
INSERT INTO `region` (`region_id`, `name`, `eng_name`, `category`) VALUES ('64', '임실, 남원, 순창', '임실, 남원, 순창', '6');
INSERT INTO `region` (`region_id`, `name`, `eng_name`, `category`) VALUES ('65', '진안, 무주, 장수', '진안, 무주, 장수', '6');
INSERT INTO `region` (`region_id`, `name`, `eng_name`, `category`) VALUES ('66', '군산, 익산, 김제', '군산, 익산, 김제', '6');
INSERT INTO `region` (`region_id`, `name`, `eng_name`, `category`) VALUES ('67', '전주, 완주', '전주, 완주', '6');
INSERT INTO `region` (`region_id`, `name`, `eng_name`, `category`) VALUES ('68', '영광, 장성, 담양, 함평', '영광, 장성, 담양, 함평', '6');
INSERT INTO `region` (`region_id`, `name`, `eng_name`, `category`) VALUES ('69', '신안, 무안, 목포, 영암', '신안, 무안, 목포, 영암', '6');
INSERT INTO `region` (`region_id`, `name`, `eng_name`, `category`) VALUES ('70', '곡성, 구례, 광양, 순천, 여수', '곡성, 구례, 광양, 순천, 여수', '6');
INSERT INTO `region` (`region_id`, `name`, `eng_name`, `category`) VALUES ('71', '나주, 화순, 보성, 고흥, 장흥', '나주, 화순, 보성, 고흥, 장흥', '6');
INSERT INTO `region` (`region_id`, `name`, `eng_name`, `category`) VALUES ('72', '영암, 강진, 해남, 진도, 완도', '영암, 강진, 해남, 진도, 완도', '6');
INSERT INTO `region` (`region_id`, `name`, `eng_name`, `category`) VALUES ('73', '제주시', '제주시', '7');
INSERT INTO `region` (`region_id`, `name`, `eng_name`, `category`) VALUES ('74', '서귀포시 ', '서귀포시 ', '7');

INSERT INTO `region` (`region_id`, `name`, `eng_name`, `category`) VALUES ('75', '베이징 ', 'BEJING ', '9');
INSERT INTO `region` (`region_id`, `name`, `eng_name`, `category`) VALUES ('76', '상하이 ', 'SANGHAI ', '9');
INSERT INTO `region` (`region_id`, `name`, `eng_name`, `category`) VALUES ('77', '천진 ', 'TIANJIN ', '9');
INSERT INTO `region` (`region_id`, `name`, `eng_name`, `category`) VALUES ('78', '청도 ', 'QINGDAO ', '9');
INSERT INTO `region` (`region_id`, `name`, `eng_name`, `category`) VALUES ('79', '항주 ', 'HANGZHOU ', '9');

INSERT INTO `region` (`region_id`, `name`, `eng_name`, `category`) VALUES ('80', '부산', 'BUSAN', '8');
INSERT INTO `region` (`region_id`, `name`, `eng_name`, `category`) VALUES ('81', '충북', 'CHUNGBUK', '8');
INSERT INTO `region` (`region_id`, `name`, `eng_name`, `category`) VALUES ('82', '충남', 'CHUNGNAM', '8');
INSERT INTO `region` (`region_id`, `name`, `eng_name`, `category`) VALUES ('83', '대구', 'DAEGU', '8');
INSERT INTO `region` (`region_id`, `name`, `eng_name`, `category`) VALUES ('84', '대전', 'DAEJEON', '8');
INSERT INTO `region` (`region_id`, `name`, `eng_name`, `category`) VALUES ('85', '강원', 'GANGWON', '8');
INSERT INTO `region` (`region_id`, `name`, `eng_name`, `category`) VALUES ('86', '광주', 'GWANGJU', '8');
INSERT INTO `region` (`region_id`, `name`, `eng_name`, `category`) VALUES ('87', '경북', 'GYUONGBUK', '8');
INSERT INTO `region` (`region_id`, `name`, `eng_name`, `category`) VALUES ('88', '경남', 'GYEONGNAM', '8');
INSERT INTO `region` (`region_id`, `name`, `eng_name`, `category`) VALUES ('89', '인천', 'INCHEON', '8');
INSERT INTO `region` (`region_id`, `name`, `eng_name`, `category`) VALUES ('90', '제주', 'JEJU', '8');
INSERT INTO `region` (`region_id`, `name`, `eng_name`, `category`) VALUES ('91', '전북', 'JEONBUK', '8');
INSERT INTO `region` (`region_id`, `name`, `eng_name`, `category`) VALUES ('92', '전남', 'JEONNAM', '8');
INSERT INTO `region` (`region_id`, `name`, `eng_name`, `category`) VALUES ('93', '세종', 'SEJONG', '8');
INSERT INTO `region` (`region_id`, `name`, `eng_name`, `category`) VALUES ('94', '서울', 'SEOUL', '8');
INSERT INTO `region` (`region_id`, `name`, `eng_name`, `category`) VALUES ('95', '울산', 'ULSAN', '8');
INSERT INTO `region` (`region_id`, `name`, `eng_name`, `category`) VALUES ('96', '경기', 'GEYONGGI', '8');