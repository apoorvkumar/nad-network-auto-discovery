-- phpMyAdmin SQL Dump
-- version 3.3.7deb5build0.10.10.1
-- http://www.phpmyadmin.net
--
-- Host: localhost
-- Generation Time: May 15, 2012 at 01:42 PM
-- Server version: 5.1.49
-- PHP Version: 5.3.3-1ubuntu9.10

SET SQL_MODE="NO_AUTO_VALUE_ON_ZERO";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;

--
-- Database: `ad1`
--

-- --------------------------------------------------------

--
-- Table structure for table `config`
--
CREATE DATABASE ad1;
USE ad1;
CREATE TABLE IF NOT EXISTS `config` (
  `oid` text NOT NULL,
  `value` text,
  `neId` int(11) NOT NULL,
  KEY `neId` (`neId`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

--
-- Dumping data for table `config`
--


-- --------------------------------------------------------

--
-- Table structure for table `ip_info`
--

CREATE TABLE IF NOT EXISTS `ip_info` (
  `neid` int(11) NOT NULL,
  `managed` int(11) NOT NULL DEFAULT '0',
  `ip` varchar(15) NOT NULL,
  `name` text NOT NULL,
  PRIMARY KEY (`ip`),
  UNIQUE KEY `ip` (`ip`),
  KEY `neid` (`neid`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

--
-- Dumping data for table `ip_info`
--


-- --------------------------------------------------------

--
-- Table structure for table `link`
--

CREATE TABLE IF NOT EXISTS `link` (
  `srcNodeId` int(11) NOT NULL,
  `destNodeId` varchar(15) NOT NULL,
  PRIMARY KEY (`srcNodeId`,`destNodeId`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

--
-- Dumping data for table `link`
--


-- --------------------------------------------------------

--
-- Table structure for table `ne`
--

CREATE TABLE IF NOT EXISTS `ne` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `type` text NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM  DEFAULT CHARSET=latin1 AUTO_INCREMENT=1217 ;

--
-- Dumping data for table `ne`
--


-- --------------------------------------------------------

--
-- Table structure for table `phyLink`
--

CREATE TABLE IF NOT EXISTS `phyLink` (
  `srcNodeId` int(11) NOT NULL,
  `destNodeId` int(11) NOT NULL,
  PRIMARY KEY (`srcNodeId`,`destNodeId`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

--
-- Dumping data for table `phyLink`
--


-- --------------------------------------------------------

--
-- Table structure for table `sysoid`
--

CREATE TABLE IF NOT EXISTS `sysoid` (
  `oid` text NOT NULL,
  `mib` varchar(50) NOT NULL
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

--
-- Dumping data for table `sysoid`
--

INSERT INTO `sysoid` (`oid`, `mib`) VALUES
('1,3,6,1,2,1,1,1,0', 'System Description'),
('1,3,6,1,2,1,1,2,0', 'System Object Id'),
('1,3,6,1,2,1,1,3,0', 'System Up Time'),
('1,3,6,1,2,1,1,4,0', 'System Contact'),
('1,3,6,1,2,1,1,5,0', 'System Name'),
('1,3,6,1,2,1,1,6,0', 'System Location');
