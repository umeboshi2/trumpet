<!doctype html>
<html>
  <head>
    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="pyramid web application">
    <meta name="author" content="Pylons Project">
    <link rel="shortcut icon" href="/assets/favicon.ico">
    <link rel="stylesheet" type="text/css" href="${csspath}/font-awesome.css"/>
    <link rel="stylesheet" type="text/css" href="${csspath}/bootstrap-${basecolor}.css"/>
    <link href="https://fonts.googleapis.com/css?family=Architects+Daughter" rel="stylesheet" type="text/css">
    <link href="https://fonts.googleapis.com/css?family=Source+Sans+Pro" rel="stylesheet" type="text/css">
    <link href="https://fonts.googleapis.com/css?family=Rambla" rel="stylesheet" type="text/css">
    <link href="https://fonts.googleapis.com/css?family=Play" rel="stylesheet" type="text/css">
  </head>
  <body>
    <div id="root-div" class="container-fluid">
        <div class="row">
            <div class="col-sm-2"></div>
            <div class="col-sm-6 jumbotron">
                <h1>Loading ...<i class="fa fa-spinner fa-spin"></i></h1>
            </div>
            <div class="col-sm-2"></div>
        </div>
    </div>
    <script type="text/javascript" charset="utf-8" src="${req.webpack().get_bundle('vendor')[0]['url']}"></script>
    <script type="text/javascript" charset="utf-8" src="${req.webpack().get_bundle('common')[0]['url']}"></script>
    <script type="text/javascript" charset="utf-8" src="${req.webpack().get_bundle(appname)[0]['url']}"></script>
  </body>
</html>
