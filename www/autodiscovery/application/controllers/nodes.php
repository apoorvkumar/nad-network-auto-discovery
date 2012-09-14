<?php

/*
 * To change this template, choose Tools | Templates
 * and open the template in the editor.
 */

/**
 * Description of nodes
 *
 * @author apoorv
 */
class Nodes extends MY_Controller {

    public function __construct() {
        parent::__construct();
    }
    
    public function index() {
        $this->template->append_metadata('<link href="' . CSS . 'nodes.css" rel="stylesheet" type="text/css" />');
        $this->template->build('nodes/default');
    }

    public function all_nodes() {
        $data['nodes'] = $this->view_all();
        $this->template->build('nodes/all_nodes',$data);
    }
    public function details($id = 0) {
        $data['interfaces'] = $this->view_interfaces($id);
        $data['managed'] = $this->view_managed($id);
        $data['sysinfo'] = $this->view_sysInfo($id);
        $this->template->build('nodes/details',$data);
    }
    
    private function view_managed($id = 0) {
        $this->db->select('managed')
                ->from('ip_info')
                ->where('neid', $id);
        return $this->db->get()->result();
    }
    private function view_interfaces($id = 0) {
        $this->db->select('ip,name')
                ->from('ip_info')
                ->where('neid', $id);
        return $this->db->get()->result();
    }
    private function view_sysInfo($id = 0) {
        $this->db->select('mib,value')
                ->from('config')
                ->join('sysoid','sysoid.oid=config.oid')
                ->where('neid',$id)
                ->limit(6);
        return $this->db->get()->result();
    }

    private function view_all() {
        $this->db->select('ip,name,neid')
                ->from('ip_info');
        return $this->db->get()->result();
    }
}

?>
