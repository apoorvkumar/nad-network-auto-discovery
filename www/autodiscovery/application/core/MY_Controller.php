<?php

/*
 * To change this template, choose Tools | Templates
 * and open the template in the editor.
 */
if (!defined('BASEPATH'))
    exit('No direct script access allowed');

/**
 * Description of MY_Controller
 *
 * @author apoorv
 */
class MY_Controller extends CI_Controller {

    protected $articles;

    public function __construct() {
        parent::__construct();
        $this->template->set_layout('default')->set_partial('header', 'layouts/header')
                ->set_partial('menu', 'layouts/menu')->set_partial('footer', 'layouts/footer');
        $this->set_metadata();
    }

    private function set_metadata() {
        $this->template->append_metadata('<link href="' . BOOTSTRAP . 'bootstrap.css" rel="stylesheet" type="text/css" />');
        $this->template->append_metadata('<script src="' . JQUERY . 'jquery.js" type="text/javascript"></script>');
        $this->template->append_metadata('<script src="' . JQUERY . 'jquery.ui.js" type="text/javascript"></script>');
        $this->template->append_metadata('<script src="' . JQUERY . 'jquery.easing.js" type="text/javascript"></script>');
        $this->template->append_metadata('<script src="' . BOOTSTRAP . 'bootstrap.js" type="text/javascript"></script>');
        $this->template->append_metadata('<link href="' . CSS . 'main.css" rel="stylesheet" type="text/css" />');
        $this->template->append_metadata('<script src="' . JS . 'main.js" type="text/javascript"></script>');
    }

}

?>
