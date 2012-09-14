<?php

function get_nodes()
{

	$hostname = "localhost";
	$user = "root";
	$passwd = "pass";
	$dbconfig_file = "/home/apoorv/autodiscovery/dbconfig";

	$file = fopen($dbconfig_file,"r") or exit("Cannot read the database configuration file");
	$db = fgets($file);
	$db = trim($db);
	fclose($file);
	
	$db = $db=="ad2" ? "ad1" : "ad2";
	
	// Open a database connection and make a query for all the node and
	// links that are present in the table.
	$mysqli = new mysqli($hostname,$user,$passwd,$db);

	// Get all the unique nodes.
	$result1 = $mysqli->query("select distinct(srcNodeId) from phyLink");
	$result2 = $mysqli->query("select distinct(destNodeId) from phyLink");
	$links_res = $mysqli->query("select * from phyLink");

	
	// Make sure that the queries were successful
	if(!($result1 and $result2 and $links_res))
	{
		echo "There was an error querying the database for the network links";
		exit;
	}
	
	$nodes = array();
	
	while($row = $result1->fetch_object())
	{
		$nodes[$row->srcNodeId] = 1;
	}
	while($row = $result2->fetch_object())
	{
		$nodes[$row->destNodeId] = 1;
	}

	$u_nodes = array_keys($nodes);
	
	// Fetch label info for each of the nodes.
	$unique_nodes = array();
	
	foreach($u_nodes as $u_node)
	{
		$ips = $mysqli->query("select ip,name from ip_info where neid=$u_node");
		if(!$ips)
		{
			$unique_nodes[$u_node] = "graphnode$u_node";
			continue;
		}
		$label = "";
		while($row = $ips->fetch_object())
		{
			$label .= $row->ip."-".$row->name.",";
		}
		$unique_nodes[$u_node] = $label;
	}
/*	
	$unique_nodes = array_keys($nodes);
*/
	// Now eliminate duplicate links.
	$links = array();
	
	while($row = $links_res->fetch_object())
	{
		$src = $row->srcNodeId;
		$dest = $row->destNodeId;
		$lower = $src < $dest ? $src : $dest;
		$higher = $src < $dest ? $dest : $src;
		$links[$lower."-".$higher] = array($lower,$higher);
	}

		
	$unique_links = array();
	foreach($links as $key=>$value)
	{
		if(!array_key_exists($value[0],$unique_links))
		{
			$unique_links[$value[0]] = array();
		}
		$unique_links[$value[0]][] = $value[1];
	}

	
	// Now that we have all the unique nodes and links, construct the 
	// json string to be forwarded
	
	$ret = "[";
	// loop over all the unique nodes in the graph and create an entry for
	// each
	foreach($unique_nodes as $node=>$label)
	{

		$ret .= "{";

		// Insert the adjacencies
		$ret .=  '"adjacencies": [';

		foreach($unique_links[$node] as $link_dest)
		{
			$ret .= '"graphnode'.$link_dest.'",';
		}
        $ret .='],';
		
		$ret .= '        
		"data": {
          "$color": "#83548B",
          "$type": "circle",
          "$dim": 10
        },';
        
        $ret .= '"id": "graphnode'.$node.'",';
        $ret .= '"name": "'.$label.'",';
        //"graphnode'.$node.'",';
        
		$ret .= "},";

	}
	
	$ret .= "]";

	return $ret;

}

?>
<html>
	<head>
		<title>
			Network Topology
		</title>
		<link type="text/css" href="base.css" rel="stylesheet" />
		<link type="text/css" href="ForceDirected.css" rel="stylesheet" />

		<!--[if IE]><script language="javascript" type="text/javascript" src="../../Extras/excanvas.js"></script><![endif]-->

		<!-- JIT Library File -->
		<script language="javascript" type="text/javascript" src="jit.js"></script>

		<!-- Example File -->
		<script language="javascript" type="text/javascript" src="topology.js"></script>
	</head>

<body onload="init();">
	
		<div id="network_graph_data" data-graph='<?php echo get_nodes(); ?>'> </div>
		
		<h1>IIT Mandi Network</h1>

<div id="container">

<div id="left-container">

        <div id="id-list"></div>


</div>

<div id="center-container">
    <div id="infovis"></div>    
</div>

<div id="right-container">

<div id="inner-details"></div>

</div>

<div id="log"></div>
</div>		
	</body>
</html>
