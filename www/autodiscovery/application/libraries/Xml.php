<?php

if (!defined('BASEPATH'))
    exit('No direct script access allowed');

class XML {

    public static function load($file) {
        $document = new DOMDocument();
        $document->load($file);
        $document->xinclude();
        return $document->saveXML();
    }

    public static function parse($file) {
        return simplexml_load_string(self::load($file));
        //return simplexml_load_file(dirname(FCPATH) . $file, 'SimpleXMLElement', LIBXML_XINCLUDE);
    }

}

?>
