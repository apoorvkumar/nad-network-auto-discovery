<div id="view" class="container-fluid">
    <div id="nodes-default" class="row-fluid">
        Discovered Interfaces
        <table id="nodes_list" class="row-fluid table-bordered table-striped">
                <thead>
                <tr>
                <th class="span6">IP</th>
                <th class="span6">Dns Name</th>
                </tr>
            </thead>
            <tbody>
                <?php foreach ($nodes as $n) { ?>
                    <tr>
                        <td class="span6"><?php echo anchor(base_url('nodes/details/' . $n->neid), $n->ip); ?></td>
                        <td class="span6"><?php echo $n->name; ?></td>
                    </tr>
                <?php } ?>
            </tbody>
        </table>
    </div>
</div>
