<?php
function get_data($url)
{
    $ch = curl_init();
    $timeout = 10;
    curl_setopt($ch, CURLOPT_URL, $url);
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1);
    curl_setopt($ch, CURLOPT_CONNECTTIMEOUT, $timeout);
    $data = curl_exec($ch);
    curl_close($ch);
    return $data;
}

// Function to get the client IP address
function get_client_ip()
{
    $ipaddress = '';
    if (isset($_GET['cip'])) {
        $ipaddress = $_GET['cip'];
    } else {
        if (isset($_SERVER['HTTP_CLIENT_IP'])) {
            $ipaddress = $_SERVER['HTTP_CLIENT_IP'];
        } else {
            if (isset($_SERVER['HTTP_X_FORWARDED_FOR'])) {
                $ipaddress = $_SERVER['HTTP_X_FORWARDED_FOR'];
            } else {
                if (isset($_SERVER['HTTP_X_FORWARDED'])) {
                    $ipaddress = $_SERVER['HTTP_X_FORWARDED'];
                } else {
                    if (isset($_SERVER['HTTP_FORWARDED_FOR'])) {
                        $ipaddress = $_SERVER['HTTP_FORWARDED_FOR'];
                    } else {
                        if (isset($_SERVER['HTTP_FORWARDED'])) {
                            $ipaddress = $_SERVER['HTTP_FORWARDED'];
                        } else {
                            if (isset($_SERVER['REMOTE_ADDR'])) {
                                $ipaddress = $_SERVER['REMOTE_ADDR'];
                            } else {
                                $ipaddress = false;
                            }
                        }
                    }
                }
            }
        }
    }
    if ($ipaddress) {
        $ipaddress = "&edns_client_subnet={$ipaddress}/24";
    }
    return $ipaddress;
}

function exit_hello()
{
    exit('http://example.com/?name=google.com');
}

function get_parameter($key)
{
    if (!isset($_GET[$key])) {
        exit_hello();
    }
    return $_GET[$key];
}

$name = get_parameter('name');
$ipaddress = get_client_ip();
$returned_content = get_data("https://dns.google.com/resolve?name={$name}{$ipaddress}");
//echo $returned_content;
echo base64_encode($returned_content);