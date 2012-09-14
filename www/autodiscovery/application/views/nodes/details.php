<div id="view" class="container-fluid">
    <div id="nodes-default" class="row-fluid">
        Interfaces on the Node
        <table id="interface_list" class="row-fluid table-bordered table-striped">
            <thead>
                <tr>
                    <th class="span6">IP</th>
                    <th class="span6">Dns Name</th>
                </tr>
            </thead>
            <tbody>
                <?php foreach ($interfaces as $i) { ?>
                    <tr>
                        <td class="span6"><?php echo $i->ip; ?></td>
                        <td class="span6"><?php echo $i->name; ?></td>
                    </tr>
                <?php } ?>
            </tbody>
        </table>
        <?php foreach ($managed as $m) { ?>
            <?php if ($m->managed != 0) { ?>
                System Information
                <table id="sys_info" class="row-fluid table-bordered table-striped">
                    <tbody>
                        <?php foreach ($sysinfo as $s) { ?>
                            <tr>
                                <td class="span6"><?php echo $s->mib; ?></td>
                                <td class="span6"><?php echo $s->value; ?></td>
                            </tr>
                        <?php } ?>
                    </tbody>
                </table>
            <?php } ?>
        <?php } ?>
    </div>
</div>