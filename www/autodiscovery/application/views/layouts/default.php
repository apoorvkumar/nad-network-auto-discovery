<!DOCTYPE html>
<html>
    <head>
        <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title><?php echo $template['title']; ?></title>
        <?php echo $template['metadata']; ?>
    </head>
    <body>
        <?php echo $template['partials']['header']; ?>
        <?php echo $template['partials']['menu']; ?>
        <h1><?php //echo $template['title'];     ?></h1>
        <?php echo $template['body']; ?>
        <?php echo $template['partials']['footer']; ?>
    </body>
</html>