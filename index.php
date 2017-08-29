<?php
    if (!empty($_SERVER['HTTPS']) && ('on' == $_SERVER['HTTPS'])) {
        $uri = 'https://';
    } else {
        $uri = 'http://';
    }
    $uri .= $_SERVER['HTTP_HOST'];

    //CHANGE THIS LINE
    header('Location: '.$uri.'/ProjectSDN/');
    //header('Location: '.$uri.'/yourproject/');

    exit;
?>
